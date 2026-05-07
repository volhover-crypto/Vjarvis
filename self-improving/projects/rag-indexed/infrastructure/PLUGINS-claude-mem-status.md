# 🔌 Статус интеграции: Claude-Mem

**Дата:** 2026-04-05  
**Статус:** ⚠️ УСТАНОВЛЕН, НЕ РАБОТАЕТ (нехватка RAM)

---

## 📦 Что сделано

### ✅ **Установка завершена:**
- Плагин `claude-mem` установлен в `~/.openclaw/extensions/claude-mem/`
- Worker-service скопирован: `plugin/scripts/worker-service.cjs` (1.9 MB)
- Bun runtime установлен: v1.3.11
- Конфигурация: `~/.claude-mem/settings.json`
- Memory slot переключён: `claude-mem` (заменил `memory-powermem`)

### ❌ **Проблема запуска:**
- Worker запущен, но **убит системой (SIGKILL)** через 3 секунды
- **Причина:** Нехватка памяти (2GB RAM недостаточно для Node.js + Bun worker)
- Worker требует ~500-800 MB RAM на старте

---

## 💡 **Рекомендация**

**Для сервера 2GB RAM claude-mem НЕ подходит.**

**Альтернативы:**
1. ✅ **PowerMem** — лёгкий, работает через CLI, SQLite
2. ⚠️ **Claude-Mem** — требует больше RAM, не рекомендуется

---

## 🔄 **Откат на PowerMem (рекомендуется)**

```bash
# 1. Отключить claude-mem
openclaw plugins disable claude-mem

# 2. Включить PowerMem
openclaw plugins enable memory-powermem

# 3. Настроить memory slot
# В ~/.openclaw/openclaw.json:
# "plugins": {
#   "slots": { "memory": "memory-powermem" }
# }

# 4. Перезапустить gateway
openclaw gateway restart
```

---

## 📊 **Сравнение плагинов**

| Параметр | PowerMem | Claude-Mem |
|----------|----------|------------|
| **RAM usage** | ~50 MB | ~500-800 MB |
| **Зависимости** | Python + SQLite | Bun + Node.js |
| **Сложность** | Низкая | Средняя |
| **2GB RAM** | ✅ Работает | ❌ Не работает |
| **Функционал** | Базовая память | Наблюдения + SSE |

---

## 🔗 **Установленные файлы**

- Плагин: `~/.openclaw/extensions/claude-mem/`
- Worker: `~/.openclaw/extensions/claude-mem/plugin/scripts/worker-service.cjs`
- Config: `~/.claude-mem/settings.json`
- Logs: `~/.claude-mem/logs/`

---

**Вывод:** Claude-Mem установлен, но **не работает** на 2GB RAM. Рекомендуется откат на PowerMem.

**Автор:** Джарвис  
**Версия:** 0.1  
**Дата:** 2026-04-05
