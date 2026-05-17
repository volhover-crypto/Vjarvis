# MEMORY.md - Долгосрочная память и контекст общения

**Владелец:** Александр Волховер  
**Агент:** Джарвис (Цифровой фамильяр v2.0)  
**Последнее обновление:** 18.05.2026

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
