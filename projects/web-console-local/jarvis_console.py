#!/usr/bin/env python3
"""
Jarvis Web Console — Windows Local Version
Запуск: python jarvis_console.py
Открыть: http://localhost:8080

Первый запуск:
  pip install fastapi uvicorn python-multipart

Затем:
  python jarvis_console.py
"""

import os
import json
import asyncio
import secrets
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ─── НАСТРОЙКИ ──────────────────────────────────────────────────
PORT = 8080
PASSWORD = "jarvis1972"

# Telegram Bot — здесь будет токен и ID чата
# Пришли Bot Token Джарвису, и он заполнит автоматически
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ─── Приложение ─────────────────────────────────────────────────
app = FastAPI(title="Jarvis Console", version="1.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

sessions: dict = {}
histories: dict = {}

def create_session() -> str:
    sid = secrets.token_hex(32)
    sessions[sid] = {"expires": (datetime.utcnow() + timedelta(hours=24)).isoformat()}
    return sid

def validate(request: Request) -> Optional[str]:
    sid = request.cookies.get("session_id")
    if sid and sid in sessions:
        if datetime.utcnow() < datetime.fromisoformat(sessions[sid]["expires"]):
            return sid
        del sessions[sid]
    return None

# ─── API ─────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "ts": datetime.utcnow().isoformat()}

@app.post("/api/login")
async def login(password: str = Form(...)):
    if password.strip() == PASSWORD:
        sid = create_session()
        resp = JSONResponse({"ok": True})
        resp.set_cookie("session_id", sid, httponly=True, max_age=86400, path="/")
        return resp
    raise HTTPException(401, "Неверный пароль")

@app.post("/api/logout")
async def logout(request: Request):
    sid = request.cookies.get("session_id")
    if sid in sessions: del sessions[sid]
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("session_id")
    return resp

@app.post("/api/chat")
async def chat(request: Request):
    sid = validate(request)
    if not sid: raise HTTPException(401, "Не авторизован")

    body = await request.json()
    message = (body.get("message") or "").strip()
    if not message: raise HTTPException(400, "Пустое сообщение")

    if sid not in histories: histories[sid] = []
    histories[sid].append({"role": "user", "content": message, "ts": datetime.utcnow().isoformat()})

    # Отправляем через Telegram Bot API
    reply = await _send_via_telegram(message)

    histories[sid].append({"role": "assistant", "content": reply, "ts": datetime.utcnow().isoformat()})
    if len(histories[sid]) > 200: histories[sid] = histories[sid][-200:]
    return {"reply": reply}

@app.get("/api/history")
async def history(request: Request):
    sid = validate(request)
    if not sid: raise HTTPException(401)
    return {"messages": histories.get(sid, [])}

@app.delete("/api/history")
async def clear_history(request: Request):
    sid = validate(request)
    if not sid: raise HTTPException(401)
    histories[sid] = []
    return {"ok": True}

# ─── Telegram интеграция ───────────────────────────────────────

async def _send_via_telegram(message: str) -> str:
    """Отправляет сообщение в Telegram и ждёт ответа через long polling."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return "[Настройка] Нужен Telegram Bot Token. Пришли его Джарвису в чат — он всё настроит."

    try:
        # Отправляем сообщение в чат
        payload = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🌐 [Web Console] {message}",
            "parse_mode": "HTML",
        }).encode()

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())

        if not result.get("ok"):
            return f"[Telegram error] {result}"

        return "📨 Сообщение отправлено в Telegram. Проверь ответ в чате с Джарвисом."

    except Exception as e:
        return f"[Ошибка Telegram: {str(e)}]"

# ─── HTML — встроенный шаблон ──────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if validate(request):
        return HTMLResponse(_PAGE)
    return HTMLException(_LOGIN)

_HTML_PAGE = None  # rendered below

def _page_html(sid: str = "") -> str:
    return PAGE_HTML_TEMPLATE

def _render_login() -> str:
    return LOGIN_HTML

def _render_chat() -> str:
    return PAGE_HTML

# ─── Инициализация ──────────────────────────────────────────────

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════╗
║   🧠 Jarvis Web Console v1.2        ║
║   http://localhost:{PORT}              ║
║   Password: {PASSWORD}          ║
╠══════════════════════════════════════╣
║   Telegram: {'✅' if TELEGRAM_BOT_TOKEN else '❌ не настроен':<24} ║
╚══════════════════════════════════════╝
    """)

    # Проверяем что токен не пуст
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️  Для полной работы нужен Telegram Bot Token")
        print("    Отправь его Джарвису в Telegram")
        print("    Или задай через переменную окружения:")
        print("    TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=yyy python jarvis_console.py")

    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")


# ════════════════════════════════════════════════════════════════
# HTML Шаблоны (в конце чтобы не мешали коду)
# ════════════════════════════════════════════════════════════════

LOGIN_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jarvis — Web Console</title>
<style>
:root{--bg:#0d1117;--bg2:#161b22;--in:#21262d;--t:#c9d1d9;--t2:#8b949e;--a:#58a6ff;--b:#30363d;--r:12px;--rs:6px;--font:system-ui,-apple-system,sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--t);font-family:var(--font);display:flex;align-items:center;justify-content:center;min-height:100vh}
.card{background:var(--bg2);border:1px solid var(--b);border-radius:var(--r);padding:40px 32px;width:100%;max-width:380px}
.hdr{text-align:center;margin-bottom:32px}
.logo{font-size:48px;display:block;margin-bottom:12px}
h1{font-size:24px;margin-bottom:4px}
.sub{color:var(--t2);font-size:14px}
label{display:block;font-size:14px;margin-bottom:6px;color:var(--t2)}
input[type=password]{width:100%;background:var(--in);border:1px solid var(--b);border-radius:var(--rs);color:var(--t);font-size:16px;padding:10px 14px;outline:none}
input:focus{border-color:var(--a)}
.btn{background:var(--a);color:#000;border:none;border-radius:var(--rs);padding:10px;font-size:16px;font-weight:500;width:100%;cursor:pointer;margin-top:16px}
.btn:hover{background:#388bfd}
.err{color:#f85149;font-size:13px;margin-top:12px;text-align:center;display:none}
</style>
</head>
<body>
<div class="card">
<div class="hdr"><span class="logo">🧠</span><h1>Jarvis</h1><p class="sub">Web Console</p></div>
<form onsubmit="return login()">
<label>Пароль</label>
<input type="password" id="p" placeholder="Введите пароль" autofocus>
<button class="btn" type="submit">Войти</button>
<div id="e" class="err"></div>
</form>
</div>
<script>
async function login(){
const p=document.getElementById('p').value,e=document.getElementById('e');
e.style.display='none';
try{
const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'password='+encodeURIComponent(p)});
if(r.ok)location.reload();
else{e.textContent='Неверный пароль';e.style.display='block';}
}catch(e){e.textContent='Ошибка соединения';e.style.display='block';}
return false;
}
</script>
</body>
</html>"""

PAGE_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jarvis — Chat</title>
<style>
:root{--bg:#0d1117;--bg2:#161b22;--in:#21262d;--t:#c9d1d9;--t2:#8b949e;--a:#58a6ff;--b:#30363d;--g:#3fb950;--r:#f85149;--user:#238636;--asst:#1f6feb22;--R:12px;--Rs:6px;--font:system-ui,-apple-system,sans-serif;--mono:'Consolas','Courier New',monospace}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:var(--bg);color:var(--t);font-family:var(--font);height:100vh;overflow:hidden}
.app{display:flex;flex-direction:column;height:100vh}
.hdr{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:var(--bg2);border-bottom:1px solid var(--b);flex-shrink:0}
.hl{display:flex;align-items:center;gap:10px}.hl .lg{font-size:22px}.hl .tt{font-size:16px;font-weight:600}
.hr{display:flex;align-items:center;gap:4px}
.dot{width:8px;height:8px;border-radius:50%}.dot.on{background:var(--g);box-shadow:0 0 6px var(--g)}.dot.off{background:var(--r)}
.b2{border:none;border-radius:var(--Rs);padding:6px 10px;background:transparent;color:var(--t2);cursor:pointer;font-size:14px}
.b2:hover{background:var(--in);color:var(--t)}
.sb{background:var(--a);color:#000;border-radius:50%;width:40px;height:40px;border:none;cursor:pointer;font-size:18px;flex-shrink:0}
.sb:hover{background:#388bfd}.sb:disabled{opacity:.4;cursor:not-allowed}
main{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:16px}
.msg{display:flex;flex-direction:column;max-width:80%}.msg.u{align-self:flex-end;align-items:flex-end}.msg.a{align-self:flex-start;align-items:flex-start}.msg.s{align-self:center;max-width:100%}
.mh{font-size:11px;color:var(--t2);margin-bottom:4px}
.mb{padding:12px 16px;border-radius:var(--R);font-size:14px;line-height:1.5;word-wrap:break-word;white-space:pre-wrap}
.msg.u .mb{background:var(--user);color:#fff;border-bottom-right-radius:4px}
.msg.a .mb{background:var(--asst);border:1px solid var(--b);border-bottom-left-radius:4px}
.msg.s .mb{background:transparent;color:var(--t2);font-size:13px;padding:8px}
.mb code{font-family:var(--mono);background:rgba(0,0,0,.3);padding:2px 6px;border-radius:4px;font-size:13px}
.mb pre{background:rgba(0,0,0,.4);padding:12px;border-radius:var(--Rs);overflow-x:auto;margin:8px 0;font-size:13px}
.mb pre code{background:none;padding:0}.mb p{margin-bottom:8px}.mb p:last-child{margin-bottom:0}
.mb ul,.mb ol{padding-left:20px;margin:8px 0}.mb li{margin-bottom:4px}.mb strong{color:var(--a)}.mb a{color:var(--a)}
.td span{display:inline-block;width:6px;height:6px;background:var(--t2);border-radius:50%;animation:bl 1.2s infinite}
.td span:nth-child(2){animation-delay:.2s}.td span:nth-child(3){animation-delay:.4s}
@keyframes bl{0%,80%,100%{opacity:.2}40%{opacity:1}}
.ftr{padding:16px 20px;background:var(--bg2);border-top:1px solid var(--b);flex-shrink:0}
.form{display:flex;align-items:flex-end;gap:10px}
textarea{flex:1;background:var(--in);border:1px solid var(--b);border-radius:var(--R);color:var(--t);font-family:var(--font);font-size:14px;padding:10px 14px;resize:none;outline:none;min-height:40px;max-height:120px;line-height:1.4}
textarea:focus{border-color:var(--a)}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--b);border-radius:3px}
@media(max-width:600px){main{padding:12px;gap:12px}.msg{max-width:90%}.hdr{padding:10px 14px}.ftr{padding:10px 14px}}
</style>
</head>
<body>
<div class="app">
<header class="hdr">
<div class="hl"><span class="lg">🧠</span><span class="tt">Jarvis</span><span id="dot" class="dot off"></span></div>
<div class="hr">
<button class="b2" onclick="clearChat()">🗑️</button>
<button class="b2" onclick="logout()">🚪</button>
</div>
</header>
<main id="msgs"></main>
<footer class="ftr">
<form onsubmit="return send()" class="form">
<textarea id="i" placeholder="Сообщение..." rows="1" onkeydown="hk(event)" oninput="resize(this)"></textarea>
<button class="sb" id="sb" type="submit">➤</button>
</form>
</footer>
</div>
<script>
let busy=false;
const msgs=document.getElementById('msgs'),dot=document.getElementById('dot'),input=document.getElementById('i');

fetch('/api/history').then(r=>r.json()).then(d=>{if(d.messages)d.messages.forEach(m=>add(m.role,m.content,m.ts));}).catch(()=>{});
setInterval(()=>{fetch('/api/health').then(r=>r.json()).then(()=>{dot.className='dot on';dot.title='Онлайн';}).catch(()=>{dot.className='dot off';});},15000);

function add(role,content,ts){
const d=document.createElement('div');d.className='msg '+role[0];
const t=ts?new Date(ts).toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit'}):'';
const lb=role==='user'?'Ты':role==='assistant'?'Jarvis':'';
if(role==='system'){d.innerHTML=`<div class="mb">${esc(content)}</div>`;}
else{d.innerHTML=`<div class="mh">${esc(lb)}·${t}</div><div class="mb">${fmt(content)}</div>`;}
msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;
}
function showT(){const d=document.createElement('div');d.id='tp';d.className='msg a';d.innerHTML='<div class="mh">Jarvis</div><div class="mb"><span class="td"><span></span><span></span><span></span></span></div>';msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;}
function hideT(){const e=document.getElementById('tp');if(e)e.remove();}

function send(){
if(busy)return false;
const t=input.value.trim();if(!t)return false;
input.value='';resize(input);add('user',t);busy=true;showT();
fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})})
.then(r=>r.json()).then(d=>{hideT();add('assistant',d.reply||'(пусто)');})
.catch(()=>{hideT();add('system','Ошибка соединения');})
.finally(()=>{busy=false;input.focus();});
return false;
}
function clearChat(){if(!confirm('Очистить историю?'))return;fetch('/api/history',{method:'DELETE'}).then(()=>{msgs.innerHTML='<div class="msg s"><div class="mb">История очищена.</div></div>';});}
function logout(){fetch('/api/logout',{method:'POST'}).then(()=>location.reload());}
function resize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,120)+'px';}
function hk(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}
function esc(t){const d=document.createElement('div');d.textContent=t;return d.innerHTML;}
function fmt(t){let h=esc(t);h=h.replace(/```(\w*)\n([\s\S]*?)```/g,'<pre><code>$2</code></pre>');h=h.replace(/`([^`]+)`/g,'<code>$1</code>');h=h.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');h=h.replace(/\*([^*]+)\*/g,'<em>$1</em>');h=h.replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank">$1</a>');h=h.replace(/^- (.+)$/gm,'<li>$1</li>');h=h.replace(/(<li>.*<\/li>\n?)+/g,m=>'<ul>'+m+'</ul>');h=h.replace(/\n/g,'<br>');h=h.replace(/<br>(<pre>|<ul>)/g,'$1');h=h.replace(/(<\/pre>|<\/ul>)<br>/g,'$1');return h;}
input.focus();
</script>
</body>
</html>"""
