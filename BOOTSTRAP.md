# BOOTSTRAP.md - Initialization and External Access Procedures

## Текущая конфигурация (обновлено 02.05.2026)

### Модели
- **Текущая модель:** openrouter/owl-alpha
- **Модель по умолчанию:** openrouter/nvidia/nemotron-3-super-120b-a12b:free
- Для переключения: session_status с параметром model

### Инфраструктура
- **Хост:** mdked.hlab.kz (AMD EPYC 9655, 1 vCPU, 1.8 ГБ RAM)
- **Диск:** 40 ГБ (следить за заполнением, критично >90%)
- **OS:** Ubuntu 24.04 LTS, kernel 6.8.0-106-generic
- **UFW:** установлен и активен (22, 80, 443, 8384 открыты)

### Ключевые сервисы
- **OpenClaw:** 2026.4.10 — основной агент-шлюз
- **PostgreSQL 16 + pgvector:** localhost:5432, база gbrain
- **GBrain:** v0.5.0 (Bun 1.3.13) — семантический поиск по vault
- **Syncthing:** localhost:8384 — синхронизация /root/vault
- **mem0ai:** v1.0.11 — /root/mem0env
- **qmd:** v0.1.2 — локальный гибридный поск
- **Whisper:** openai-whisper — транскрибация (модели: tiny → large-v3-turbo)
- **Xray:** localhost:10808/10809 — прокси

### Известные ограничения
- **RAM 1.8 ГБ** — полная генерация эмбеддингов GBrain (1546 чанков) не помещается в память. Требуется модель с меньшим потреблением или увеличение RAM.
- **GBrain embed** — падает при нехватке RAM (OOM killer). Решение: обрабатывать порциями или увеличить RAM.
- **Vikunja** — контейнер удалён при очистке Docker. Требуется пересоздание через docker-compose если нужна.

### Доступ к внешним ресурсам
- **Web search:** web_search (DuckDuckGo, без API-ключа)
- **Web fetch:** web_fetch (HTML → markdown)
- **Summarize:** через web_fetch + LLM (нативный бинарник только macOS)
- **Email:** ProtonMail (Jarvis1972@proton.me)
- **Telegram:** основной канал коммуникации

### Управление знаниями
- **Vault:** /root/vault/ (Obsidian, markdown)
- **Memory:** /root/.openclaw/workspace/memory/ (дневные логи)
- **Self-improving:** ~/self-improving/ (журнал уроков)
- **GBrain sync:** `gbrain sync --repo /root/vault`
- **GBrain embed:** `gbrain embed --stale` (⚠️ требует >2GB RAM для полной обработки)

### Навыки (ключевые)
- agritech-viticulture — виноградарство Крыма
- agronomy_advisor — агрономия и точное земледелие
- iot_monitor — мониторинг сенсоров
- report_generator — генерация отчётов
- dynamic-web-fetch — скрейпинг JS-страниц
- whisper-stt — транскрибация аудио
- self-improving — самообучение
- gbrain-integration — управление базой знаний
- arxiv — поиск научных статей
- pdf — обработка PDF
- python — стандарты кодирования
- engineering — инженерная экспертиза
- aider — AI-парное программирование
