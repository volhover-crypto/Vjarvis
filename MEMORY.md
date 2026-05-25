# MEMORY.md - Долгосрочная память и контекст общения

**Владелец:** Александр Волховер  
**Агент:** Джарвис (Цифровой фамильяр v2.0)  
**Последнее обновление:** 20.05.2026

## 🔴 ЖЁСТКОЕ ПРАВИЛО: Самотестирование при каждом старте сессии

**При КАЖДОМ старте новой сессии — ДО любого ответа пользователю — проводить полное самотестирование:**
1. `openclaw gateway status` — gateway работает?
2. `openclaw plugins list` — все плагины загружены и включены? (memory-tencentdb, deltachat, telegram, openrouter, duckduckgo, groq)
3. `pg_isready -h localhost -p 5432` — PostgreSQL доступен?
4. `gbrain search "тест" --limit 1` — GBrain работает?
5. `df -h /` — диск < 90%?
6. `free -h` — RAM > 200MB available?
7. `ls ~/.openclaw/memory-tdai/` — данные TencentDB Agent Memory на месте?
8. Ключевые файлы workspace на месте?

**Любой сбой → немедленный отчёт с тегом `[ERROR]`. Не начинать работу до устранения или подтверждения пользователя.**
Это непреложное правило — без исключений, даже если сессия "срочная".

**Формат отчёта (всегда после самотестирования):**
```
🧪 Session Self-Report:
  [✅/❌] Gateway | Plugins | PG | GBrain | Disk | RAM | memory-tdai | Workspace
  → [✅ All passed / ❌ N failed: details]
```

---

---

## 📁 Структура памяти

- **Лог обучения (положительный опыт)** → `vault/learning-log.md`
- **Инженерные навыки (agent-skills)** → `skills/agent-skills/README.md`
- **Навигация по vault** → `AGENTS.md`
- **Принципы поведения** → `SOUL.md`
- **Ритуалы и проверки** → `HEARTBEAT.md`
- **Schema wiki** → `vault/WIKI.md`
- **Дневные логи** → `memory/YYYY-MM-DD.md`
- **Ошибки и паттерны** → `memory/error_patterns.md`
- **Библиотека принципов** → `memory/principles_lib.md`
- **Секреты и токены** → `/root/.openclaw/secrets/` (chmod 600)

---

## 🔐 Доступы и токены

### GitHub
- **Токен:** `/root/.openclaw/secrets/github_token`
- **User:** volhover-crypto
- **Репозитории:**
  - `jarvis-web-console` — https://github.com/volhover-crypto/jarvis-web-console
  - `Vjarvis` — https://github.com/volhover-crypto/Vjarvis (бэкап рабочей среды)
- **Восстановление:**
  ```bash
  export GITHUB_TOKEN=$(cat /root/.openclaw/secrets/github_token)
  git clone https://volhover-crypto:${GITHUB_TOKEN}@github.com/volhover-crypto/Vjarvis.git
  ```

### Google Drive (OAuth)
- **Credentials:** `/root/.openclaw/secrets/google_oauth.json`
- **rclone config:** `/root/.openclaw/secrets/rclone.conf`
- **Scope:** `drive.readonly` (только чтение)
- **Папки:** Jarvis, YAG, istohniki, RAG_Knowledge_Base_v2
- **Восстановление:**
  ```bash
  # Копируем конфиги
  cp /root/.openclaw/secrets/rclone.conf /root/.config/rclone/rclone.conf
  cp /root/.openclaw/secrets/google_oauth.json /root/.config/mirage/
  
  # Проверяем
  rclone lsd gdrive:
  rclone ls gdrive:Jarvis/
  ```
- **⚠️ Для записи** нужен новый токен с scope `https://www.googleapis.com/auth/drive`

---

## Краткая хронология

* 11.04.2026: Фаза 0 — структура доменов, GBrain, MCP, навыки
* 14.04.2026: Анализ регрессии Claude Code (thinking tokens)
* 19.04.2026: Claude Code vs Aider. Подводная связь (arXiv, 78 статей)
* 29.04.2026: OpenMythos — 3 урока о самосовершенствовании
* 30.04.2026: Harness Engineering. Разработка навыков. Ubuntu Touch. SEMR226
* 03.05.2026: QLoRA (arXiv:2305.14314)
* 07.05.2026: Dreaming, circuit-weaver, book-to-skill. KiCad 7 формат PCB v20221018
* 11.05.2026: Очистка диска. Обновление OpenClaw. Doctor --repair. Data Products. LLM Wiki Карпати. Agent Skills (addyosmani). Web Console v2.0
* 12.05.2026: Google Drive OAuth. GitHub репозитории. Модернизация web-console

---

## ДОМЕНЫ ЗНАНИЙ

### Домен 1: AI/ML и автоматизация
- Ключевые концепции: LLM-агенты, MCP, OpenClaw, n8n, RAG, SCADA, MQTT, Edge computing
- Критические метрики: LLM latency <2s, token cost, IoT data freshness <15 мин
- Источники: arXiv cs.AI/cs.LG, GitHub openclaw/openclaw, Anthropic research

### Домен 2: Агрономия и точное земледелие
- Ключевые концепции: NDVI, ETc, BBCH, SWD, GDD, terroir, ампелография
- Критические метрики: NDVI 0.2–0.6, сбор при >17° Brix, pH 3.0–3.5, урожайность 5–12 т/га
- Источники: PubMed, OIV, ВНИИВиВ, FAO Cropwat

### Домен 3: AgriTech стратегия
- Ключевые концепции: Precision Ag ROI, data sovereignty, CAPEX vs OPEX, ISOBUS
- Источники: Россельхозбанк, АСИ, РБК Тренды, McKinsey Global Institute

### Домен 4: 3D-печать и аддитивное производство
- Ключевые концепции: FDM, SLA, SLS, STL, 3MF, CadQuery, OpenSCAD, Piper TTS
- Русские голоса Piper: Руслан (бархатный), Дмитри, Ирина, Денис

---

## КРОСС-ДОМЕННЫЕ ПАТТЕРНЫ
- Иммунный ответ растений ↔ incident management в IT
- Фенофазы виноградника ↔ product lifecycle
- Управление ирригацией ↔ rate limiting в API
- Ожидание загрузки DOM ↔ управление ирригацией

---

## ТЕКУЩАЯ КОНФИГУРАЦИЯ СИСТЕМЫ
- Навыков: 50 (33 отключены doctor'ом) + 22 agent-skills
- Web Console: v2.0 (security hardening, CSRF, rate limiting)
- GitHub: ✅ подключён (volhover-crypto)
- Google Drive: ✅ подключён (OAuth, readonly)
- TTS: Piper (Руслан/Дмитри) + Edge TTS (Dmitry/Svetlana)
- STT: faster-whisper v1.2.1, модель small, русский язык
- Swap: 2.9Gi | Диск: ~81% | RAM: 1.8G
- Локальный семантический поиск: ✅ sentence-transformers + pgvector (384 dims)
- GBrain embed: ✅ 1579 чанков | GBrain query: ❌ требует OpenAI
- commands.ownerAllowFrom: ✅ telegram:1051427322

---

## DREAMING [2026-05-07]
### Паттерны:
- KiCad 7.0.11 формат PCB v20221018, не v20240108
- numpy 1.x/2.x конфликт с matplotlib → использовать venv
- exec preflight блокирует сложные Python-скрипты → write + прямой запуск

### Инсайты:
- Автогенерация PCB требует точного знания спецификации
- Dreaming запускать и вручную после крупных проектов

### Нерешённые:
- Обоснование сети датчиков (HEARTBEAT с 03.05)
- Полная принципиальная схема ЛВМ-485-СОЛАР-01
- Gerber файлы — ✅ сгенерированы (9 слоёв)

---

## НАВЫКИ ПОИСКА И УСТАНОВКИ
* ClawHub: https://clawhub.ai | Vercel Skills: https://skills.sh
* Команды: npx clawhub search <query>, npx skills find <query>
* Agent Skills: https://github.com/addyosmani/agent-skills → `skills/agent-skills/`

---

## 🚨 Восстановление после сбоя

### Порядок восстановления:
1. **OpenClaw:** `openclaw gateway restart`
2. **GitHub доступ:**
   ```bash
   export GITHUB_TOKEN=$(cat /root/.openclaw/secrets/github_token)
   git clone https://volhover-crypto:${GITHUB_TOKEN}@github.com/volhover-crypto/Vjarvis.git /tmp/vjarvis-restore
   ```
3. **Google Drive доступ:**
   ```bash
   mkdir -p /root/.config/rclone /root/.config/mirage
   cp /root/.openclaw/secrets/rclone.conf /root/.config/rclone/rclone.conf
   cp /root/.openclaw/secrets/google_oauth.json /root/.config/mirage/
   rclone lsd gdrive:  # проверка
   ```
4. **Vault:** `gbrain sync --repo /root/vault`
5. **Навыки:** скопировать из `/tmp/vjarvis-restore/skills/` в `~/.openclaw/workspace/skills/`

## [2026-05-12_10-47-00] Точка восстановления создана
- Описание: /root/.openclaw/workspace/backup/restore_2026-05-12_10-47-00/SUMMARY.md
- Навыки: перечислены в skills.txt
- Доступы: извлечены из MEMORY.md
- Ресурсы: resources.txt
- Полная копия доступна в Google Drive: gdrive:OpenClaw/RestorePoints/restore_2026-05-12_10-47-00

---

## ВИНОГРАДАРСТВО — База знаний (обновлено 15.05.2026)

### Фенологическая шкала E&L/BBCH
- Файл: `knowledge/viticulture/fenologicheskaya_shkala_vinograda.md`
- Шкала Эйшорн & Лоренс (E&L) → BBCH, стадии А–О (01/02 → 47/97)
- Типичные сроки для Крыма: набухание — конец марта, цветение — конец мая, сбор — сентябрь–октябрь
- Источник: vinograd.info (vignevin.com)

### Фитоклимат виноградника
- Файл: `knowledge/viticulture/fitoklimat_vinogradnika.md`
- Сравнение шпалерной и беседочной систем (Дигоми, 1971)
- Ключевые выводы:
  - Беседка: более стабильная влажность (амплитуда 31% vs 45% на шпалере)
  - При одинаковом водопотреблении урожайность на беседке в 2+ раза выше
  - Полив эффективнее на беседке (+7% vs +5% на шпалере)
  - Беседка подвержена грибковым заболеваниям из-за повышенной влажности
- Источник: vinograd.info


---

## [2026-05-16] n8n Workflows Deployed
- n8n 2.20.9 установлен и настроен (Docker, порт 5678)
- Создано и активировано 5 workflows:
  1. **Infrastructure Monitor** — мониторинг сервисов каждые 30 мин → Telegram alert
  2. **Session Context Recovery** — ежедневно 6:00, сбор контекста из memory logs
  3. **Memory Crystallizer** — ежедневно 2:00, git sync + GBrain sync
  4. **Task Tracker** — пн-пт 8:00, поиск открытых задач → Telegram
  5. **Error Pattern Detector** — ежедневно 3:00, сканирование логов → Telegram
- API key сохранён в /root/.openclaw/secrets/n8n_api_key
- Проблема: executeCommand нода не работает в n8n 2.20.9 → используем Code node с child_process
- Проблема: webhook требует активации через сессию (не через API key)

---

## [2026-05-16_19:29] КРИСТАЛЛИЗАЦИЯ — Полная фиксация состояния

### Точка восстановления
- Путь: `/root/.openclaw/workspace/backup/restore_2026-05-16_19-29/`
- GitHub: push в Vjarvis (master) выполнен

### Состояние системы
- **OpenClaw**: 2026.5.7, gateway running (PID 1287040)
- **Плагины**: memory-tencentdb ✅, telegram ✅, deltachat ✅, openrouter ✅, duckduckgo ✅, groq ✅, claude-mem ❌ (отключён)
- **БД**: PostgreSQL 16 ✅, localhost:5432 accepting connections
- **GBrain**: v0.5.0 ✅ search works, sync timeout (RAM 1.8G constraint)
- **n8n**: v2.20.9 ✅ Docker, port 5678, 5 workflows active
- **Syncthing**: ✅ port 8384
- **Disk**: 89% (34G/40G) ⚠️
- **RAM**: 1.8G (1.2G used, 569MB available) ⚠️
- **Swap**: 2.9G (435M used)

### n8n Workflows (все активны)
1. **Infrastructure Monitor** — каждые 30 мин → Telegram alert
2. **Session Context Recovery** — ежедневно 6:00 MSK → memory/context-latest.md
3. **Memory Crystallizer** — ежедневно 2:00 MSK → git sync + GBrain sync
4. **Task Tracker** — пн-пт 8:00 MSK → Telegram сводка задач
5. **Error Pattern Detector** — ежедневно 3:00 MSK → scan logs → Telegram

### Конфигурация memory-tencentdb
```json
{
  "storeBackend": "sqlite",
  "embedding": {"enabled": false, "provider": "none"},
  "recall": {"strategy": "keyword", "maxResults": 5},
  "bm25": {"enabled": true, "language": "zh"},
  "capture": {"enabled": true, "l0l1RetentionDays": 0},
  "pipeline": {"everyNConversations": 5, "enableWarmup": true},
  "offload": {"enabled": false}
}
```

### Навыки
- Всего: 57 директорий локально, 57 в GitHub репозитории
- Agent-skills: 24 поддиректории (API design, TDD, debugging, engineering и др.)
- Ключевые: agritech-viticulture, agronomy_advisor, iot_monitor, gbrain-integration, whisper-stt, arxiv, engineering, self-improving
- SKILL.md: 37 проверенных — все byte-match с GitHub

### Известные проблемы
- **Google Drive**: shared drive 404 (ID 1n9gjvZk5YNQC5_JhgJDifqOp4sUvywac). Требуется проверка в Google Cloud Console
- **GBrain embed**: требуется OpenAI API key. Без него — только keyword поиск
- **RAM 1.8G**: критично мало для GBrain embed. Swap 2.9G помогает избежать OOM
- **tsx**: не установлен глобально (работает через npx)
- **Disk 89%: следить за заполнением

### Доступы (Credentials)
- GitHub: volhover-crypto / token в /root/.openclaw/secrets/github_token
- Google Drive: service account jarvis-drive@jarvis-2026-492009.iam.gserviceaccount.com
- n8n API: key в /root/.openclaw/secrets/n8n_api_key
- ProtonMail: Jarvis1972@proton.me
- Telegram bot: token в openclaw.json

### Жёсткие правила (закреплённые в SOUL.md и HEARTBEAT.md)
1. **Самотестирование при каждом старте**: 8 проверок ДО любого ответа пользователю
2. **Формат отчёта**: 🧪 Session Self-Report с ✅/❌ по каждой проверке
3. **Любой сбой → [ERROR]**, работа не начинается до устранения или подтверждения
4. **MEMORY.md — append-only**, никогда не редактировать прошлые записи
5. **n8n Safety**: не модифицировать third-party workflows без явного разрешения

### Принципы работы (из principles_lib.md)
- Проверять конфликты pip/apt при установке пакетов
- Отправлять файлы только из workspace (не из /tmp)
- Самодиагностика после каждого изменения
- При анализе новых концепций — проверять наличие открытых исходных данных

---

## [2026-05-18] COMPOUND EVENTS — Анализ для виноградарства Крыма и юга России

### Ключевые исследования
- **Li et al., Nature (2026):** TCoRE метрика — compound events растут нелинейно, модели недооценивают на 37–75%. DOI: 10.1038/s41586-026-10544-1
- **Science Advances (2025):** CDHEs (Compound Drought-Heatwave Events) участились с 2000-х
- **Nature Communications (2024):** «Озеленение» от CO₂ парадоксально усиливает compound засухи
- **PNAS (2023):** Record-shattering CDHW события — экспоненциальный рост вероятности
- **NHESS (2025):** Обзор роста compound event research за десятилетие после IPCC SREX

### Фактические данные 2025 года
- **Крым:** потери урожая винограда 30–50%, засуха (самая серьёзная за 30–40 лет), влажность почвы ~50% от 2024, t° почвы >32°C на глубине корней
- **Краснодар:** ущерб $572 млн (46 млрд руб), потери винограда до 25%, 9 районов — зона ЧС, сдвиг сбора на 14–18 дней

### Прогноз 2026–2030
- Дни >35°C: с 15–20 до 25–35 за лето
- Засухи: каждые 2–3 года (вместо 1 раз в 3–5 лет)
- Compound жара+засуха — доминирующий паттерн
- GDD: +150–200 градусо-дней к 2030
- Сроки сбора: сдвиг на 2–4 недели

### Критические пороги для мониторинга виноградников
- **t° почвы >28°C** на глубине корней → запуск полива
- **t° воздуха >35°C** → риск солнечных ожогов ягод
- **Влажность почвы <50%** от нормы → гидростресс, блокировка фенольного вызревания
- **Индекс теплового стресса** — расчёт по t° воздуха + влажности в кроне

### Стратегии адаптации (подтверждённые исследованиями)
- **Беседческая система** предпочтительнее шпалерной (стабильнее влага, меньше перегрев почвы — данные Дигоми 1971)
- **Засухоустойчивые сорта:** Гевюрцтраминер, Сапеави, Марселан (INRAE) + автохтонные крымские (Кеша-1, Ранний Магарача)
- **Мульчирование** приствольной зоны (↓t° почвы на 3–5°C)
- **RDI (Регулируемый дефицитный полив)** — подтверждён MDPI (2025)
- **Обязательный мониторинг:** влажность почвы (30/60/90 см), t° почвы, t° воздуха в кроне, точка росы

### Экономика
- Потери от засухи 2025: $572 млн (все культуры, Краснодар), 30–50% винограда (Крым)
- При текущих тенденциях: каждые 2–3 года повторение потерь уровня 2025
- Адаптация (капельный полив + мониторинг + сортозамена) окупается за 3–5 лет

### Файл в vault
- `knowledge/viticulture/compound_events_viticulture_2026_2030.md` — полный анализ с таблицами, ссылками, прогнозами

---

## [2026-05-18_23:23] КРИСТАЛЛИЗАЦИЯ — Ревизия ресурсов

### Очистка диска
- **Было:** 34G (91%) → **Стало:** 30G (80%)
- **Освобождено:** ~4.5 GB
- Удалено:
  - /tmp аудио файлы (102MB) — транскрибация завершена
  - Whisper base.pt + large-v3-turbo.pt (744MB) — не используются на CPU
  - Playwright browsers (1.2GB) — не используется
  - Copilot SDK (133MB) — не используется
  - Claude-EDA (90MB) — не используется
  - .codex tmp + .copilot logs (52MB)
  - /root/.npm (707MB) — кэш npm
  - /root/.bun (249MB) — кэш bun
  - cern-kicad-libs репозиторий (891MB) — зеркало, доступно на GitHub
  - awesome-electronics репозиторий (468KB) — список ссылок
  - apt cache

### Установлено
- **faster-whisper 1.2.1** — быстрая транскрибация (в 4-8x быстрее whisper)
- **vosk 0.3.45 + vosk-model-small-ru-0.22** — офлайн STT для русского (87MB модель)
- **gitmcp-docs + gitmcp-openclaw** — MCP-серверы для анализа GitHub-репозиториев

### Ключевые проекты
- **soil-sensor-lora** — проект почвенного датчика на STM32WL55 + LoRa (KiCad 7)
  - Схема: 42 компонента, 9 разделов
  - PCB: 60x40mm, 2-layer
  - Gerber + STEP сгенерированы
  - BOM: 42 позиции с LCSC part numbers
- **STM32-LoRa-Node** — клонирован reference design (STM32L072 + SX1276 + BME280)

### Протокол встречи 18.05.2026
- Файл: `ИСТОРИЯ/protocol_2026-05-18_12-23.md`
- Тема: «Агры Элемент 2.0» — интеграция с Золотым банком
- Ключевые решения: подключение к Золотому банку, n8n workflow, AI-менеджер проекта

### Текущие задачи
1. Подключение к Золотому банку — запуск серверов, n8n
2. Прототип «Агры Элемент 2.0» — май-июнь
3. Формулы на дашборде — редактируемые коэффициенты
4. AI-менеджер проекта — координация сроков
5. Ремонт сервера с 16GB RAM

### Ресурсы для изучения
- RAK WisBlock — модульная IoT платформа (RAK12035 — почвенная влажность)
- ChirpStack — LoRaWAN Network Server (Docker)
- LoRaMac-node — эталонный LoRaWAN stack
- RadioLib — универсальная LoRa библиотека
- Vosk — офлайн STT для русского

---

## [2026-05-19_00:42] КРИСТАЛЛИЗАЦИЯ — Принципы работы с GBrain

### Архитектура
- **GBrain** = Obsidian vault (/root/vault/) → PostgreSQL 16 + pgvector → семантический поиск
- **Источник:** github.com/garrytan/gbrain (garrytan/gbrain, v0.35.8.0)
- **Бинарник:** /usr/local/bin/gbrain (собран через bun build src/cli.ts --compile)
- **Исходники:** /tmp/gbrain-src/ (НЕ УДАЛЯТЬ — нужны для пересборки)
- **Конфиг:** /root/.gbrain/config.json
- **БД:** postgresql://gbrain:secure_password_123@localhost:5432/gbrain
- **Пользователь БД:** gbrain (BYPASSRLS привилегия выдана)
- **Схема:** v67 (миграция v23→67, 44 миграции, выполнены 2026-05-19)

### RAM-патч (КРИТИЧЕСКИ ВАЖНО)
Проблема: gbrain v0.35.8 при каждом запуске инициализирует AI gateway (~400MB RAM), что невозможно при 1.8GB общего RAM.
Решение: патч в /tmp/gbrain-src/src/cli.ts — configureGateway() вызывается ТОЛЬКО при наличии OPENAI_API_KEY или ANTHROPIC_API_KEY.
При любом обновлении gbrain — ОБЯЗАТЕЛЬНО пересобирать с патчем:
  cd /tmp/gbrain-src && bun build src/cli.ts --compile --outfile /usr/local/bin/gbrain

### Что работает без API ключа
- gbrain search "запрос" — keyword search (tsvector, русский + английский)
- gbrain query "вопрос" — hybrid search (tsvector + pgvector)
- gbrain sync --repo /root/vault --no-embed — синхронизация vault → PostgreSQL
- gbrain list -n N — список страниц

### Что НЕ работает без API ключа
- gbrain embed — генерация эмбеддингов (требует OpenAI/Anthropic ключ)
- gbrain doctor — работает, но медленно и может упасть по RAM

### GBrain Lite (fallback)
- Путь: /usr/local/bin/gbrain-lite
- Лёгкая обёртка через прямые SQL-запросы к PostgreSQL
- Использовать если gbrain недоступен или падает по памяти
- Команды: search, query, list, sync, doctor

### Статистика БД (на 19.05.2026)
- Страниц: 300
- Чанков: 1840
- С эмбеддингами: 1579
- Модель эмбеддингов: text-embedding-3-large (1536 dims)
- Последняя синхронизация: 2026-05-16T14:53:53Z

### ЖЁСТКИЕ ПРАВИЛА
1. НИКОГДА не запускать gbrain embed --stale без API ключа
2. НИКОГДА не удалять /tmp/gbrain-src/
3. При обновлении gbrain — ВСЕГДА пересобирать с RAM-патчем
4. При падении gbrain по памяти — использовать gbrain-lite
5. При восстановлении после сбоя — см. инструкцию в SOUL.md раздел "GBrain — Принципы работы"

---

## [2026-05-20] GSD Framework Integration

### Источник
- Репозиторий: github.com/gsd-build/get-shit-done
- Автор: TÂCHES (Lex Christopherson)
- Версия на момент анализа: v1.42.1
- Звёзды: 31K+

### Что интегрировано
1. **Deviation Rules** (SOUL.md) — 4 правила отклонений при выполнении задач:
   - Rule 1: Авто-fix багов (без разрешения)
   - Rule 2: Авто-добавление критического (error handling, validation, auth)
   - Rule 3: Авто-fix блокирующего (кроме установки пакетов)
   - Rule 4: Остановка при архитектурных изменениях
2. **Adversarial Verification** (SOUL.md) — goal-backward анализ, stub detection, wiring check
3. **Phase-Based Work** (HEARTBEAT.md) — фазовый подход: discuss → plan → execute → verify → ship
4. **Context Monitoring** (HEARTBEAT.md) — мониторинг context rot, протокол при исчерпании
5. **Шаблоны** (templates/) — CONTEXT.md, PLAN.md, SUMMARY.md

### Ключевые концепции GSD
- Context rot: качество падает непрерывно по мере заполнения контекста (все 18 моделей деградируют)
- Fresh context per agent: каждый сабагент получает чистые 200k токенов
- File-based state: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, CONTEXT.md
- Absent = enabled: если ключ отсутствует в config — он true
- Two-stage routing: 6 namespace-роутеров вместо 86 скиллов (экономия ~2000 токенов)
- Package legitimacy checks: при падении установки пакета — checkpoint, не авто-замена

### Что НЕ интегрировано (и почему)
- `--dangerously-skip-permissions` — рискованно без отдельной ветки
- Многоагентная архитектура — жрёт токены кратно (у нас 1.8GB RAM)
- $GSD токен на Solana — не влияет на функциональность
- Полный GSD CLI (gsd-sdk) — избыточно для нашей архитектуры

### Файлы
- `SOUL.md` — Deviation Rules + Adversarial Verification
- `HEARTBEAT.md` — Phase-Based Work + Context Monitoring
- `templates/CONTEXT.md` — шаблон решений по проекту
- `templates/PLAN.md` — шаблон плана выполнения
- `templates/SUMMARY.md` — шаблон отчёта
- `AGENTS.md` — обновлены ссылки

---

## [2026-05-21] Learning Patterns Integration (Барбара Оакли)

### Источник
- Курс: «Accelerate Your Learning with ChatGPT» (Coursera, Oakley & White)
- Ссылка: https://habr.com/ru/news/841434/
- 30K+ записей, 98% одобрения, ~5 часов

### Что интегрировано (8 паттернов)
1. **Learning is Linking** — новое знание связывать с 2-3 существующими доменами в vault
2. **Context Window ≈ Working Memory** — pre-test: 3 ключевых факта перед длинной сессией
3. **Options, Not Answers** — при альтернативах предлагать варианты, не единственное решение
4. **Metaphor Template** — объяснять через аналогии из доменов пользователя (виноградарство, IoT)
5. **Flipped Interaction** — задать вопросы ДО выполнения, не сразу выполнять
6. **Cognitive Verifier** — пересказать задачу своими словами, подтвердить с пользователем
7. **Pre-test** — сначала попробовать, зафиксировать пробелы, потом изучить
8. **Multimodal Prompts** — использовать скриншоты/фото как входные данные

### Критические вопросы для Adversarial Verification (добавлено)
- «Что здесь может пойти не так?» — 3 вопроса критика
- «Пользователь получит то, что просил, или то, что я решил?»
- «Если бы объяснял через аналогию — было бы понятно?»

### Файлы обновлены
- `SOUL.md` — секция «🧠 Learning Patterns» + критические вопросы в Adversarial Verification
- `HEARTBEAT.md` — Pre-test + Flipped Interaction протоколы
- `docs/agent-onboarding-guide.md` — раздел 7 «Learning Patterns» + обновлённый чеклист
- `vault/reading/agent-onboarding-guide.md` — синхронизировано

---

## [2026-05-23] n8n Auth System — Завершено

### Архитектура
- **Auth Service**: FastAPI + asyncpg + bcrypt, порт 8765, systemd (`jarvis-auth.service`)
- **n8n**: `network_mode: host` (для доступа к localhost:8765), webhook → HTTP Request → Respond
- **PostgreSQL**: `auth_users` + `auth_sessions` в базе `gbrain`
- **Хранение паролей**: bcrypt (hash в поле `password_hash`)

### Ключевые решения
- n8n Code node с `require('pg')` не работает (sandbox) → вынесено в отдельный микросервис
- n8n в bridge network не видит localhost хоста → `network_mode: host`
- Docker контейнер auth service не видит PostgreSQL на хосте → auth service на хосте через systemd
- Hash был в старом формате `$2b$12$...` → перегенерирован через `bcrypt.hashpw()`

### Credentials
- **Admin user**: `admin` / `A03g10l31~` / `admin@jarvis.local`
- **n8n**: admin@jarvis.local / A03g10l31~

### Эндпоинты
- `POST http://176.12.74.69:5678/webhook/auth/login` — авторизация (username + password → token)
- `GET /auth/verify?token=...` — проверка токена
- `POST /auth/logout?token=...` — логаут
- `GET /health` — health check

### Файлы
- `/root/auth-service/main.py` — FastAPI auth service
- `/etc/systemd/system/jarvis-auth.service` — systemd unit
- `/root/n8n/docker-compose.yml` — n8n с `network_mode: host`
- `/root/.openclaw/workspace/web/login.html` — HTML форма логина

### n8n Workflow
- ID: `rFNcxozuWQI5c0wo`
- Webhook (`/auth/login`) → HTTP Request (`POST http://localhost:8765/auth/login`) → Respond

---

## [2026-05-26] Claude-BugHunter — Архитектурная интеграция

### Источник
- Репозиторий: github.com/elementalsouls/Claude-BugHunter
- Автор: Sachin Sharma (Bug Hunting & GenAI Security Research)
- Состав: 51 skills + 15 slash commands + 574+ disclosed HackerOne reports
- Клон: /tmp/Claude-BugHunter/ (4.7MB, 173 файла)

### Что интегрировано
- **7-Question Gate** — обязательная валидация ДО отчёта (Q1-Q7, первый FAIL = KILL)
- **5-Phase Hunting Workflow** — SCOPE → RECON → HUNT → VALIDATE → REPORT
- **Red Team Discipline** — DO NOT STOP directive, 10 self-throttling anti-patterns
- **A→B Bug Chaining** — систематическое наращивание цепочек (IDOR→ATO, SSRF→RCE)
- **OOB-Or-It-Didn't-Happen Gate** — Collaborator confirmation для blind vulns
- **Evidence Hygiene** — cookie redaction, PII black-bar, HAR sanitization
- **Report Writing** — impact-first, title formula, CVSS 3.1, no "could potentially"
- **Enterprise Attack Surface** — VPN, M365, Cloud IAM, VMware matrices

### Связь с существующей системой
- Adversarial Verification (SOUL.md) ↔ 7-Question Gate (расширение)
- Deviation Rules (SOUL.md) ↔ OOB Gate / Engagement type confirmation
- Phase-Based Work (HEARTBEAT.md) ↔ 5-Phase Workflow
- Практическое применение: аудит mdked.hlab.kz, AgroPilot, n8n, auth service

### Отложено до RAM 8GB
- Полный GBrain embed для security findings
- Автоматизированный scanning (nuclei, Burp MCP)
- public-skills-builder (Anthropic API key required)
- cbh CLI (curl-only mode работает сейчас)

### Файлы
- Навык: `skills/claude-bughunter-integration/SKILL.md`
- Quick Ref: `skills/claude-bughunter-integration/QUICKREF.md`
- Vault: `vault/knowledge/skills/claude-bughunter-integration/`

---

## [2026-05-26_01:24] КРИСТАЛЛИЗАЦИЯ — Полная фиксация состояния

### Критические проблемы
1. **NGINX FAILED** — упал ~12:57 25.05, `nginx: command not found`. Hub, Coach, auth, n8n proxy — всё недоступно. Требует восстановления.
2. **GBrain FAILED** — SIGKILL при search. PG работает. Отложено до RAM 8GB.
3. **certbot.service FAILED** — давно, требует проверки сертификата.

### Ресурсы
- RAM: 1.8GB (600MB free), Swap: 2.9GB (1.1GB used — zram 921MB + swapfile 2GB)
- Disk: 76% (9.3G free)
- Docker: 2.52GB images, 1.079GB volumes (99% reclaimable)
- Vault: 164MB | Workspace: 459MB

### Навыки: 57 (включая новый claude-bughunter-integration)
### Git: 5 коммитов, последний 50887e0 (BugHunter integration)
### Апгрейд: RAM 1.8→8GB, диск +500MB — на днях по плану Александра
