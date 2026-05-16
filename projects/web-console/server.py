"""
Web Console — FastAPI сервер для взаимодействия с агентом через браузер.
Запуск: uvicorn server:app --host 0.0.0.0 --port 8080

Требует переменные окружения:
  WEB_CONSOLE_PASSWORD  — bcrypt-хеш пароля (обязательно)
  WEB_CONSOLE_SECRET    — секрет для подписи сессий (обязательно)
  OPENCLAW_API_URL      — URL OpenClaw API (по умолчанию http://localhost:18789)
  WEB_CONSOLE_PORT      — порт (по умолчанию 8080)
  WEB_CONSOLE_ORIGIN    — разрешённый origin для CORS (обязательно)
"""

import os
import json
import asyncio
import logging
import secrets
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps

from fastapi import FastAPI, Request, Response, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, validator
import uvicorn

# ─── Логирование ────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("web-console")

# ─── Конфигурация ───────────────────────────────────────────────

class Config:
    """Конфигурация из переменных окружения. Всё обязательное."""

    WEB_PASSWORD: str = os.environ.get("WEB_CONSOLE_PASSWORD", "")
    WEB_SECRET: str = os.environ.get("WEB_CONSOLE_SECRET", "")
    OPENCLAW_API: str = os.environ.get("OPENCLAW_API_URL", "http://localhost:18789")
    PORT: int = int(os.environ.get("WEB_CONSOLE_PORT", "8080"))
    ORIGIN: str = os.environ.get("WEB_CONSOLE_ORIGIN", "")

    # Rate limiting
    LOGIN_ATTEMPTS_LIMIT: int = 5
    LOGIN_WINDOW_SECONDS: int = 300  # 5 минут

    @classmethod
    def validate(cls):
        """Проверяет что все обязательные переменные заданы."""
        missing = []
        if not cls.WEB_PASSWORD:
            missing.append("WEB_CONSOLE_PASSWORD")
        if not cls.WEB_SECRET:
            missing.append("WEB_CONSOLE_SECRET")
        if not cls.ORIGIN:
            missing.append("WEB_CONSOLE_ORIGIN")
        if missing:
            raise EnvironmentError(
                f"Обязательные переменные окружения не заданы: {', '.join(missing)}\n"
                f"Сгенерируйте пароль: python3 -c \"import bcrypt; print(bcrypt.hashpw(b'your-password', bcrypt.gensalt()).decode())\"\n"
                f"Сгенерируйте секрет: python3 -c \"import secrets; print(secrets.token_hex(32))\""
            )

# Валидация при импорте
Config.validate()

# ─── Приложение ─────────────────────────────────────────────────

app = FastAPI(
    title="Jarvis Web Console",
    version="2.0.0",
    docs_url=None,  # Отключаем Swagger UI
    redoc_url=None,  # Отключаем ReDoc
)

# CORS — строго только разрешённый origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "X-CSRF-Token"],
)

# Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[Config.ORIGIN.replace("https://", "").replace("http://", ""), "localhost", "127.0.0.1"],
)

# ─── Модели ─────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str

    @validator("message")
    def validate_message(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Сообщение не может быть пустым")
        if len(v) > 4000:
            raise ValueError("Сообщение слишком длинное (макс. 4000 символов)")
        return v

# ─── Хранилище сессий ───────────────────────────────────────────

sessions: dict[str, dict] = {}
chat_histories: dict[str, list] = {}

# Rate limiting: {ip: [timestamp, ...]}
login_attempts: dict[str, list] = {}

# ─── CSRF токены ────────────────────────────────────────────────

csrf_tokens: dict[str, str] = {}  # session_id -> csrf_token

# ─── Утилиты ────────────────────────────────────────────────────

def _hash_password(password: str) -> str:
    """Хеширует пароль с использованием WEB_SECRET как salt."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        Config.WEB_SECRET.encode(),
        100_000,
    ).hex()


def _verify_password(password: str) -> bool:
    """Проверяет пароль против хеша из конфигурации."""
    try:
        # Поддержка bcrypt-хеша (начинается с $2b$)
        if Config.WEB_PASSWORD.startswith("$2b$"):
            import bcrypt
            return bcrypt.checkpw(password.encode(), Config.WEB_PASSWORD.encode())
        # Fallback: PBKDF2
        return hmac.compare_digest(_hash_password(password), Config.WEB_PASSWORD)
    except Exception:
        return False


def _check_rate_limit(ip: str) -> bool:
    """Проверяет rate limit для IP. Возвращает True если превышен."""
    now = time.time()
    attempts = login_attempts.get(ip, [])
    # Очищаем старые попытки
    attempts = [t for t in attempts if now - t < Config.LOGIN_WINDOW_SECONDS]
    login_attempts[ip] = attempts
    if len(attempts) >= Config.LOGIN_ATTEMPTS_LIMIT:
        return True  # Превышен
    attempts.append(now)
    return False


def create_session() -> tuple[str, str]:
    """Создаёт сессию и CSRF-токен. Возвращает (session_id, csrf_token)."""
    sid = secrets.token_hex(32)
    csrf = secrets.token_hex(16)
    sessions[sid] = {
        "created": datetime.utcnow().isoformat(),
        "expires": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
    }
    csrf_tokens[sid] = csrf
    return sid, csrf


def validate_session(request: Request) -> Optional[str]:
    """Валидирует сессию из cookie."""
    sid = request.cookies.get("session_id")
    if sid and sid in sessions:
        exp = datetime.fromisoformat(sessions[sid]["expires"])
        if datetime.utcnow() < exp:
            return sid
        else:
            # Сессия истекла — чистим
            del sessions[sid]
            csrf_tokens.pop(sid, None)
    return None


def validate_csrf(request: Request, sid: str) -> bool:
    """Валидирует CSRF-токен из заголовка."""
    token = request.headers.get("X-CSRF-Token", "")
    expected = csrf_tokens.get(sid, "")
    return hmac.compare_digest(token, expected)


# ─── Security Headers Middleware ────────────────────────────────

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# ─── Маршруты: страницы ─────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    sid = validate_session(request)
    if sid:
        return HTMLResponse(content=_render_chat_page(sid, csrf_tokens.get(sid, "")))
    return HTMLResponse(content=_render_login_page())


@app.post("/api/login")
async def login(request: Request, response: Response, password: str = Form(...)):
    client_ip = request.client.host

    # Rate limiting
    if _check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for IP {client_ip}")
        raise HTTPException(status_code=429, detail="Слишком много попыток. Попробуйте позже.")

    if _verify_password(password):
        sid, csrf = create_session()
        logger.info(f"Successful login from {client_ip}")
        resp = JSONResponse({"ok": True, "csrf_token": csrf})
        resp.set_cookie(
            key="session_id",
            value=sid,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=86400,
            path="/",
        )
        return resp

    logger.warning(f"Failed login attempt from {client_ip}")
    raise HTTPException(status_code=401, detail="Неверный пароль")


@app.post("/api/logout")
async def logout(request: Request):
    sid = request.cookies.get("session_id")
    if sid and sid in sessions:
        del sessions[sid]
        csrf_tokens.pop(sid, None)
        logger.info(f"Session {sid[:8]}... logged out")
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("session_id")
    return resp


# ─── Маршруты: API ──────────────────────────────────────────────

@app.get("/api/health")
async def health():
    oc_status = "unknown"
    try:
        import urllib.request
        r = urllib.request.urlopen(f"{Config.OPENCLAW_API}/health", timeout=5)
        oc_status = "online" if r.status == 200 else "offline"
    except Exception:
        oc_status = "offline"

    return {
        "status": "ok",
        "openclaw": oc_status,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/api/chat")
async def chat(request: Request):
    sid = validate_session(request)
    if not sid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    # CSRF проверка
    if not validate_csrf(request, sid):
        raise HTTPException(status_code=403, detail="Неверный CSRF-токен")

    try:
        body = await request.json()
        chat_req = ChatRequest(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Инициализируем историю
    if sid not in chat_histories:
        chat_histories[sid] = []

    chat_histories[sid].append({
        "role": "user",
        "content": chat_req.message,
        "ts": datetime.utcnow().isoformat(),
    })

    reply = await _send_to_openclaw(chat_req.message, sid)

    chat_histories[sid].append({
        "role": "assistant",
        "content": reply,
        "ts": datetime.utcnow().isoformat(),
    })

    # Ограничиваем историю
    if len(chat_histories[sid]) > 200:
        chat_histories[sid] = chat_histories[sid][-200:]

    return {"reply": reply}


@app.get("/api/history")
async def history(request: Request):
    sid = validate_session(request)
    if not sid:
        raise HTTPException(status_code=401, detail="Не авторизован")
    return {"messages": chat_histories.get(sid, [])}


@app.delete("/api/history")
async def clear_history(request: Request):
    sid = validate_session(request)
    if not sid:
        raise HTTPException(status_code=401, detail="Не авторизован")
    if not validate_csrf(request, sid):
        raise HTTPException(status_code=403, detail="Неверный CSRF-токен")
    chat_histories[sid] = []
    return {"ok": True}


# ─── OpenClaw интеграция ────────────────────────────────────────

async def _send_to_openclaw(message: str, session_id: str) -> str:
    """Отправляет сообщение в OpenClaw через CLI."""
    import subprocess

    try:
        proc = await asyncio.create_subprocess_exec(
            "openclaw", "message", "send",
            "--message", message,
            "--source", "web-console",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        if proc.returncode == 0:
            result = stdout.decode().strip()
            return result if result else "Ответ получен"
        err = stderr.decode().strip()
        logger.error(f"OpenClaw CLI error: {err}")
        return f"[Ошибка агента] {err}"
    except asyncio.TimeoutError:
        logger.error("OpenClaw timeout")
        return "[Таймаут] Агент не ответил за 120 секунд"
    except Exception as e:
        logger.error(f"OpenClaw send error: {e}")
        return f"[Ошибка] {str(e)}"


# ─── HTML шаблоны ────────────────────────────────────────────────

def _render_login_page() -> str:
    return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis — Web Console</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-body">
    <div class="login-card">
        <div class="login-header">
            <span class="logo">🧠</span>
            <h1>Jarvis</h1>
            <p>Web Console v2.0</p>
        </div>
        <form id="login-form" onsubmit="return doLogin(event)">
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" id="password" placeholder="Введите пароль" autofocus autocomplete="current-password">
            </div>
            <button type="submit" class="btn btn-primary btn-full">Войти</button>
            <div id="login-error" class="error-msg" style="display:none"></div>
        </form>
    </div>
    <script src="/static/app.js"></script>
    <script>initLogin();</script>
</body>
</html>"""


def _render_chat_page(session_id: str, csrf_token: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis — Chat</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body class="chat-body">
    <div class="chat-app">
        <header class="chat-header">
            <div class="header-left">
                <span class="logo">🧠</span>
                <span class="header-title">Jarvis</span>
                <span id="status-dot" class="status-dot offline" title="Отключён"></span>
            </div>
            <div class="header-right">
                <button class="btn btn-sm btn-ghost" onclick="clearChat()" title="Очистить">🗑️</button>
                <button class="btn btn-sm btn-ghost" onclick="doLogout()" title="Выйти">🚪</button>
            </div>
        </header>
        <main id="chat-messages" class="chat-messages">
            <div class="msg system">
                <div class="msg-bubble">Добро пожаловать в Web Console v2.0. Задайте вопрос агенту.</div>
            </div>
        </main>
        <footer class="chat-input-area">
            <form id="chat-form" onsubmit="return sendMsg(event)" class="chat-form">
                <textarea id="msg-input" placeholder="Сообщение..." rows="1"
                    onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
                <button type="submit" class="btn btn-send" title="Отправить">➤</button>
            </form>
        </footer>
    </div>
    <script src="/static/app.js"></script>
    <script>initChat("{csrf_token}");</script>
</body>
</html>"""


# ─── Статические файлы ──────────────────────────────────────────

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ─── Точка входа ────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"🧠 Jarvis Web Console v2.0 — http://0.0.0.0:{Config.PORT}")
    print(f"   OpenClaw API: {Config.OPENCLAW_API}")
    print(f"   CORS origin: {Config.ORIGIN}")
    print(f"   Rate limit: {Config.LOGIN_ATTEMPTS_LIMIT} attempts per {Config.LOGIN_WINDOW_SECONDS}s")
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT, log_level="info")
