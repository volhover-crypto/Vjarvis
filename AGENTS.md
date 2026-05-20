# AGENTS.md — Навигационная карта агента (Constitutional Layer, NFD)

> Краткий указатель на ключевые разделы рабочего пространства.  
> Не содержит знание — только ссылки на него.  
> Целевой объём: ≤100 строк.  
> Обновляется после значительных изменений в структуре работы.

---

## 📁 Основные директории

- `skills/` — модульные навыки агента  
  → Подробнее: `skills/agent-skills/` (22 инженерных навыка), `skills/agronomy_advisor/`, `skills/iot_monitor/`
- `memory/` — дневные логи, журналы ошибок, кейсы, библиотека принципов  
  → Подробнее: `memory/YYYY-MM-DD.md`, `memory/error_patterns.md`, `memory/principles_lib.md`
- `vault/` — основное хранилище знаний (Obsidian)  
  → Подробнее: `vault/WIKI.md` (schema), `vault/learning-log.md` (лог обучения), `vault/reading/` (конспекты), `vault/knowledge/` (домены)
- `~/self-improving/` — личный журнал уроков и улучшений агента  
  → Подробнее: `~/self-improving/memory.md` (append-only журнал уроков)
- `/root/.openclaw/secrets/` — токены и credentials (chmod 600)  
  → Подробнее: `MEMORY.md` раздел «🔐 Доступы и токены»

---

## 🔗 Быстрые ссылки на ключевые файлы

- **Принципы работы** → `SOUL.md`
- **Профиль пользователя** → `USER.md`
- **Идентичность и стиль** → `IDENTITY.md`
- **Сводка ключевых воспоминаний** → `MEMORY.md`
- **Журнал обучения** → `vault/learning-log.md`
- **Schema wiki** → `vault/WIKI.md`
- **Журнал уроков (append-only)** → `~/self-improving/memory.md`
- **База ошибок** → `memory/error_patterns.md`
- **Библиотека принципов** → `memory/principles_lib.md`
- **Секреты и токены** → `/root/.openclaw/secrets/`
- **Шаблоны фазовой работы** → `templates/CONTEXT.md`, `templates/PLAN.md`, `templates/SUMMARY.md`
- **Deviation Rules** → `SOUL.md` раздел «🔧 Deviation Rules»
- **Adversarial Verification** → `SOUL.md` раздел «🎯 Adversarial Verification»
- **Phase-Based Work** → `HEARTBEAT.md` раздел «📋 PHASE-BASED WORK»
- **Context Monitoring** → `HEARTBEAT.md` раздел «🔍 CONTEXT MONITORING»

---

## 🧭 Как использовать эту карту

- При начале работы: проверьте, в какой домене или задаче вы находитесь
- Используйте ссылки выше, чтобы быстро перейти к нужному разделу
- При обновлении среды: изменяйте файлы в `skills/`, `memory/`, `vault/` — а не этот файл
- Этот файл предназначен только для навигации

---

## 🚨 Восстановление после сбоя

1. **GitHub:** `export GITHUB_TOKEN=$(cat /root/.openclaw/secrets/github_token)`
2. **Google Drive:** `cp /root/.openclaw/secrets/rclone.conf /root/.config/rclone/rclone.conf`
3. **Vault:** `gbrain sync --repo /root/vault`
4. **OpenClaw:** `openclaw gateway restart`

Подробная инструкция в `MEMORY.md` раздел «🚨 Восстановление после сбоя».

---

*Файл AGENTS.md обновлен: 20.05.2026*  
*Соответствует правилу Constitutional Layer из NFD*
