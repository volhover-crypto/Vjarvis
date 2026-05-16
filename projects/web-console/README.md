# Jarvis Web Console v2.0

Безопасный веб-интерфейс для взаимодействия с агентом через браузер.

## Безопасность v2.0

- ✅ Пароль через bcrypt + env var (не в коде)
- ✅ CSRF-токены для всех POST-запросов
- ✅ Rate limiting на логин (5 попыток / 5 минут)
- ✅ CORS строго на разрешённый origin
- ✅ Security headers (CSP, HSTS, X-Frame-Options, etc.)
- ✅ HttpOnly + Secure + SameSite cookies
- ✅ Валидация длины сообщений
- ✅ Логирование всех событий

## Установка

```bash
cd /root/.openclaw/workspace/projects/web-console

# Установить зависимости
pip install fastapi uvicorn bcrypt pydantic

# Сгенерировать пароль
python3 -c "
import bcrypt
password = input('Пароль: ')
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(f'WEB_CONSOLE_PASSWORD={hashed.decode()}')
"

# Сгенерировать секрет
python3 -c "import secrets; print(f'WEB_CONSOLE_SECRET={secrets.token_hex(32)}')"
```

## Запуск

```bash
# Установить переменные окружения
export WEB_CONSOLE_PASSWORD='$2b$12$...'  # bcrypt-хеш
export WEB_CONSOLE_SECRET='...'           # 32-байт hex
export WEB_CONSOLE_ORIGIN='https://your-domain.com'
export WEB_CONSOLE_PORT=8080

# Запустить
python3 server.py
```

## Docker (опционально)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python3", "server.py"]
```

## API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/` | Главная (логин или чат) |
| POST | `/api/login` | Аутентификация |
| POST | `/api/logout` | Выход |
| GET | `/api/health` | Проверка статуса |
| POST | `/api/chat` | Отправить сообщение |
| GET | `/api/history` | История чата |
| DELETE | `/api/history` | Очистить историю |

## Переменные окружения

| Переменная | Обязательная | Описание |
|------------|--------------|----------|
| `WEB_CONSOLE_PASSWORD` | ✅ | bcrypt-хеш пароля |
| `WEB_CONSOLE_SECRET` | ✅ | Секрет для подписи сессий |
| `WEB_CONSOLE_ORIGIN` | ✅ | Разрешённый origin для CORS |
| `OPENCLAW_API_URL` | ❌ | URL OpenClaw (по умолчанию http://localhost:18789) |
| `WEB_CONSOLE_PORT` | ❌ | Порт (по умолчанию 8080) |
