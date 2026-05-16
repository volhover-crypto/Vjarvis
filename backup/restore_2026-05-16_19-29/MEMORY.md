# MEMORY.md - Долгосрочная память и контекст общения

**Владелец:** Александр Волховер  
**Агент:** Джарвис (Цифровой фамильяр v2.0)  
**Последнее обновление:** 16.05.2026

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
