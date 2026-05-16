# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Что настроено

### Vikunja (таск-менеджер)
- URL: http://localhost:3456 (внешний: http://176.12.74.69:3456)
- Логин: volhover / A03g10l31~
- API token: см. /root/vikunja/.token
- Config: /root/vikunja/config.yml
- Docker: /root/vikunja/docker-compose.yml
- DB: /root/vikunja/db/vikunja.db (SQLite)
- ⚠️ Vikunja v2.2.2 использует `database.path` (не `database.file`)!
- ⚠️ Не использовать `docker compose recreate` — теряет env. Всегда `down` → `up`

### Summarize (суммаризация контента)
- Нет Linux-бинарника (только macOS)
- Функциональность: суммаризация URL, PDF, YouTube через LLM напрямую
- API ключи: OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY

### Whisper STT (голос → текст)
- Бесплатный, локальный, без API ключей
- Скрипт: /root/.openclaw/workspace/skills/whisper-stt/scripts/transcribe.py
- Модели: tiny, base, small, medium, large, large-v3-turbo
- Языки: ru, en, zh, ja и др. (auto-detect)
- Форматы вывода: json, txt, srt, vtt
- Зависимости: openai-whisper, torch, ffmpeg

### Syncthing (синхронизация файлов)
- URL: http://176.12.74.69:8384
- Логин: admin
- Пароль: A03g10l31~
- API key: 7p6yxmGzrvs2kKjrg6a7swao3gkHotfX
- Device ID: BFGCD5T-L24YF3U-TPWLJH2-3D62UPJ-IUDURK7-KVCZW5P-22ORS2B-CAX7FA4
- Папка: "Obsidian Vault" → /root/vault
- Порт: 8384 (GUI), 22000 (sync TCP/QUIC), 21027 (discovery UDP)
- Systemd: syncthing.service (autostart enabled)
- Config: /root/syncthing/config.xml

### ProtonMail (email)
- Email: Jarvis1972@proton.me
- Логин: Jarvis92
- Пароль: jNWec6PCfkr7cCB~
- Провайдер: ProtonMail (Швейцария)
- API доступ: python3 + protonmail-api-client
- Учётные данные: /root/vikunja/protonmail_account.json

### Obsidian Vault
- Путь: /root/vault/
- Структура: daily/, projects/, ideas/, archive/, templates/, attachments/
- Подключается через Obsidian как vault из этой папки

---

### Управление знаниями
| Инструмент | Статус | Применie |
|------------|--------|------------|
| gbrain search/query | ✅ АКТИВЕН | Семантический поиск по Vault и проектам |
| gbrain import/sync | ✅ АКТИВЕН | Импорт markdown → PostgreSQL, обновление индекса |
| gbrain embed --stale | ⚠️ ТРЕБУЕТ МОДЕЛЬ | Векторные эмбеддинги (см. Шаг 3 роадмапа) |
| qmd | ✅ АКТИВЕН | Локальный гибридный поиск без внешних API |
| mem0ai | ✅ УСТАНОВЛЕН | Персональная memoria (/root/mem0env) |
| mcp-memory | РЕЗЕРВНЫЙ | Использовать если gbrain недоступen |

## GBRAIN INFRASTRUCTURE
- PostgreSQL 16: localhost:5432
- База данных: gbrain
- Расширение: pgvector (HNSW-индекс)
- Vault: /root/vault (Obsidian, markdown-файлы)
- Цикл синхронизации: gbrain sync --repo /root/vault && gbrain embed --stale

Add whatever helps you do your job. This is your cheat sheet.


### Управление знаниями (обновлено)
| Инструмент | Статус | Применение |
|------------|--------|------------|
| gbrain search/query | ✅ АКТИВЕН | Семантический поиск по Vault и проектам |
| gbrain import/sync | ✅ АКТИВЕН | Импорт markdown → PostgreSQL, обновление индекса |
| gbrain embed --stale | ⚠️ ТРЕБУЕТ МОДЕЛЬ | Векторные эмбеддинги (см. Шаг 3 роадмапа) |
| qmd | ✅ АКТИВЕН | Локальный гибридный поиск без внешних API |
| mem0ai | ✅ УСТАНОВЛЕН | Персональная memoria (/root/mem0env) |
| mcp-memory | РЕЗЕРВНЫЙ | Использовать если gbrain недоступen |

## GBRAIN INFRASTRUCTURE
- PostgreSQL 16: localhost:5432
- База данных: gbrain
- Расширение: pgvector (HNSW-индекс)
- Vault: /root/vault (Obsidian, markdown-файлы)
- Цикл синхронизации: gbrain sync --repo /root/vault && gbrain embed --stale

