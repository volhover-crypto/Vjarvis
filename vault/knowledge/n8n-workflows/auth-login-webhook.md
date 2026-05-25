# Auth Login — n8n Workflow

**ID:** `rFNcxozuWQI5c0wo`  
**Статус:** ✅ Активен (единственный активный workflow)  
**Создан:** 2026-05-23  
**Версия:** 9 (activeVersionId: `1e16c679-2605-43b5-a2a8-5b46968a4ded`)  
**Владелец:** Admin Jarvis (personal project)  
**Webhook ID:** `b776bc99-be6e-4432-bcfa-c2b76d3043e5`

---

## Назначение

Workflow реализует **API-шлюз авторизации** для Jarvis Hub. Принимает входящие запросы на логин, проксирует их на бэкенд FastAPI (порт 8765) и возвращает результат клиенту.

**Цепочка:** `Вебхук → HTTP-запрос → Ответ`

---

## Архитектура

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Webhook   │────▶│ HTTP Request│────▶│   Respond   │
│  (приём)    │     │ (прокси)    │     │  (ответ)    │
│  POST auth/ │     │ POST :8765/ │     │ JSON ответ  │
│    login    │     │  auth/login │     │  = $json    │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Ноды (3 штуки)

### 1. Webhook — приём запросов

- **Тип:** `n8n-nodes-base.webhook` (v2)
- **HTTP метод:** `POST`
- **Путь:** `auth/login`
- **Режим ответа:** `responseNode` (ответ будет отправлен через ноду Respond)
- **Позиция:** `[250, 300]`

Принимает POST-запросы от внешних клиентов (HTML-форма логина на Hub). Тело запроса должно содержать JSON с полями `username` и `password`.

### 2. HTTP Request — проксирование на бэкенд

- **Тип:** `n8n-nodes-base.httpRequest` (v4.2)
- **HTTP метод:** `POST`
- **URL:** `http://localhost:8765/auth/login`
- **Тело запроса:** JSON (формула n8n):
  ```
  ={{ {"username": $input.first().json.body.username, "password": $input.first().json.body.password} }}
  ```
- **Таймаут:** 10000ms (10 сек)
- **Позиция:** `[450, 300]`

Проксирует учётные данные на FastAPI auth service (порт 8765). Извлекает `username` и `password` из тела входящего webhook-запроса и отправляет как JSON на бэкенд. Auth service проверяет credentials в PostgreSQL и возвращает токен сессии.

### 3. Respond — отправка ответа

- **Тип:** `n8n-nodes-base.respondToWebhook` (v1.1)
- **Формат ответа:** JSON
- **Тело ответа:** `={{ $json }}` (полный JSON от HTTP Request)
- **Позиция:** `[650, 300]`

Возвращает ответ от auth service обратно клиенту, который инициировал webhook-запрос.

---

## Подключения (Connections)

```
Webhook.main[0] → HTTP Request.main[0]
HTTP Request.main[0] → Respond.main[0]
```

---

## Пример входящего запроса

```json
POST https://mdked.hlab.kz/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "A03g10l31~"
}
```

## Пример исходящего запроса (на auth service)

```json
POST http://localhost:8765/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "A03g10l31~"
}
```

## Пример успешного ответа

```json
{
  "token": "eyJhbGciOi...",
  "user": {
    "id": "...",
    "email": "admin@jarvis.local",
    "role": "admin"
  }
}
```

---

## Зависимости от внешних сервисов

| Сервис | Адрес | Назначение |
|--------|-------|------------|
| FastAPI Auth Service | `localhost:8765` | Проверка credentials, выдача токена |
| PostgreSQL | `localhost:5432` | БД `gbrain`, таблица `auth_users` |

**Auth Service endpoints:**
- `POST /auth/login` — авторизация (username + password → token)
- `GET /auth/verify?token=...` — проверка токена
- `POST /auth/logout?token=...` — логаут
- `GET /health` — health check

---

## Путь запроса (end-to-end)

```
Браузер (Hub login form)
  → POST /auth/login (JSON: username + password)
    → n8n Webhook (ловит /auth/login)
      → n8n HTTP Request (POST → localhost:8765/auth/login)
        → FastAPI Auth Service
          → PostgreSQL (bcrypt проверка password_hash)
        ← Токен + user data (JSON)
      ← Проксирует ответ
    ← Respond отправляет JSON обратно
  ← Браузер получает токен
    → localStorage.setItem('token')
    → sessionStorage.setItem('agropilot_authed')
```

---

## Безопасность

- Пароли хранятся в PostgreSQL как bcrypt-хеш
- Auth service слушает только на localhost (127.0.0.1:8765), не доступен извне
- HTTPS через nginx (порт 443)

---

## Связанные файлы

- **Auth Service:** `/root/auth-service/main.py` (FastAPI + asyncpg + bcrypt)
- **n8n Config:** `/root/n8n/docker-compose.yml`
- **Nginx Config:** `/etc/nginx/sites-enabled/coach`
- **HTML Login Form:** `/root/.openclaw/workspace/web/login.html`

---

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| 401 Unauthorized | Неверный username/password | Проверить credentials в БД |
| 500 Internal Server | Auth service упал | `systemctl restart jarvis-auth` |
| Timeout | Auth service не отвечает | Проверить `ss -tlnp \| grep 8765` |
| Workflow не срабатывает | Webhook неактивен | Убедиться что workflow = active |

---

*Документ создан: 25.05.2026*
*Источник: n8n API `/rest/workflows/rFNcxozuWQI5c0wo`*
