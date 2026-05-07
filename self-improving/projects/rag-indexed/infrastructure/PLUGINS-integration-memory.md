# 🔌 Интеграция плагинов памяти

**Дата:** 2026-04-05  
**Статус:** ⏳ В процессе

---

## 📦 Установленные плагины

### ✅ **PowerMem (memory-powermem)** — УСТАНОВЛЕН
- **Плагин:** v0.3.0 installed
- **pmem CLI:** v1.1.0
- **Слот:** `memory` (заменил memory-core и memory-lancedb)
- **Режим:** CLI (локальный pmem)

**Что работает:**
- ✅ Плагин загружен OpenClaw
- ✅ pmem CLI доступен
- ✅ SQLite база настроена
- ❌ Embeddings не работают (требуется Ollama или API ключ)

**Что нужно доделать:**
1. Установить Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Запустить модель embeddings: `ollama pull nomic-embed-text`
3. Перезапустить gateway: `openclaw gateway restart`
4. Протестировать: `openclaw ltm add "тест"` и `openclaw ltm search "тест"`

**Конфигурация:**
- Env файл: `~/.openclaw/powermem/powermem.env`
- База: `~/.openclaw/powermem/powermem.db` (SQLite)
- Режим: CLI (без HTTP сервера)

**Команды:**
```bash
# Проверить здоровье
openclaw ltm health

# Добавить память
openclaw ltm add "Я предпочитаю кофе американо по утрам"

# Поиск
openclaw ltm search "кофе"

# Удалить
openclaw ltm forget "ID_ПАМЯТИ"
```

---

### ❌ **Claude-Mem** — НЕ УСТАНОВЛЕН
- Требует worker на порту 37777
- Более сложная архитектура (HTTP worker + SSE stream)
- Не приоритет для текущей задачи

**Если нужен:**
```bash
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

---

### ❓ **ClawdBoost** — НЕ НАЙДЕН
- Возможно, маркетинговое название
- Или внутреннее название другого проекта
- Нет публичного плагина с таким именем

---

## 🎯 Следующие шаги

1. **Доустановить Ollama** (уже запущено, ожидает завершения)
2. **Запустить embeddings модель**
3. **Протестировать PowerMem**
4. **Обновить SESSION_BOOTSTRAP.md** с информацией о новом плагине
5. **Документировать в RAG** процесс интеграции

---

## 🔗 Ссылки
- PowerMem GitHub: https://github.com/oceanbase/powermem
- Плагин: https://github.com/ob-labs/openclaw-extension-powermem
- Claude-Mem Docs: https://docs.claude-mem.ai/openclaw-integration

**Автор:** Джарвис  
**Версия документа:** 0.1
