---
name: gbrain-integration
version: 2.0.0
description: Управление базой знаний GBrain — поиск, импорт, синхронизация (v0.35.8, RAM-патч)
capabilities:
 - Искать по ключевым словам и семантически в базе знаний GBrain
 - Создавать новые страницы wiki по итогам аналитических сессий
 - Добавлять timeline-события в хронологию проектов
 - Синхронизировать Obsidian Vault с PostgreSQL базой
 - Строить граф связей между концепциями и проектами
permissions:
 - read: /root/vault/
 - write: /root/vault/
 - execute: gbrain
 - database: postgresql://gbrain@localhost:5432/gbrain
inputs:
 - name: query
 description: Поисковый запрос для gbrain search
 required: false
 - name: page_name
 description: Имя страницы для создания/обновления
 required: false
 - name: page_type
 description: Тип страницы (person/project/concept/deal/source)
 required: false
---

# GBrain Integration Skill v2.0

## КРИТИЧЕСКИЕ ОГРАНИЧЕНИЯ (1.8GB RAM)

- **AI Gateway ОТКЛЮЧЁН** — работает только keyword search + hybrid search (tsvector + pgvector)
- **gbrain embed НЕ работает** без OpenAI/Anthropic API ключа
- **gbrain doctor может упасть** по RAM — использовать `gbrain-lite doctor` для диагностики
- **При падении gbrain** — использовать `gbrain-lite` (fallback через psql)
- **НЕ запускать `gbrain embed --stale`** — упадёт по RAM без API ключа

## BRAIN-AGENT LOOP (выполнять для каждого значимого запроса)

### READ (перед ответом)
```bash
# Основной поиск (keyword + hybrid)
gbrain search "[ключевые слова из запроса]" --limit 5

# Если gbrain недоступен — fallback
gbrain-lite search "[ключевые слова]" --limit 5

# Если результаты есть → использовать как контекст
# Если результатов нет → продолжить без них
```

### WRITE (после ответа с новым знанием)
Когда получено существенно новое знание о проекте/человеке/концепции:
1. Найти или создать страницу в /root/vault/
2. Обновить раздел "Compiled truth" или добавить в "Timeline"
3. Добавить ссылки [[project: X]] или [[person: Y]]

Шаблон новой страницы:
```markdown
---
type: [person|project|concept|deal|source]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# [Название]

## Compiled truth
[Текущее лучшее понимание — что это, кто это, как работает]

## Timeline
- YYYY-MM-DD: [Событие]

## Ссылки
- [[project: ...]]
- [[person: ...]]
```

### SYNC (фоново после обновления vault)
```bash
# Основной путь (без embedding)
gbrain sync --repo /root/vault --no-embed

# Fallback если gbrain упал
gbrain-lite sync /root/vault

# Embedding — ТОЛЬКО при наличии API ключа и >2GB RAM
# gbrain embed --stale  # НЕ ЗАПУСКАТЬ без ключа!
```

## ТИПЫ ПОИСКОВЫХ ЗАПРОСОВ
- По проекту: `gbrain search "Золотая Балка"` → все связанные файлы
- По человеку: `gbrain query "Иванов"` → карточка человека
- По концепции: `gbrain search "виноградарство ирригация"` → связанные знания
- Семантический: `gbrain query "управление поливом"` (hybrid search, работает без API ключа)

## ДИАГНОСТИКА
```bash
# Быстрая диагностика (не требует много RAM)
gbrain-lite doctor

# Полная диагностика (может упасть по RAM)
gbrain doctor --json
```

## ВОССТАНОВЛЕНИЕ ПОСЛЕ СБОЯ
1. `curl -fsSL https://bun.sh/install | bash`
2. `git clone https://github.com/garrytan/gbrain.git /tmp/gbrain-src`
3. `cd /tmp/gbrain-src && bun install`
4. Применить RAM-патч (см. SOUL.md)
5. `bun build src/cli.ts --compile --outfile /usr/local/bin/gbrain`
6. Проверить: `gbrain search "test" --limit 1`
