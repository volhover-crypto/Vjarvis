---
name: gbrain-integration
version: 1.0.0
description: Управление базой знаний GBrain — поиск, импорт, синхронизация
capabilities:
 - Искать людей и проектов в базе знаний GBrain
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

# GBrain Integration Skill

## BRAIN-AGENT LOOP (выполнять для каждого значимого запроса)

### READ (перед ответом)
```bash
gbrain search "[ключевые слова из запроса]"
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
gbrain sync --repo /root/vault
gbrain embed --stale # только если эмбеддинг-модель доступна
```

## ТИПЫ ПОИСКОВЫХ ЗАПРОСОВ
- По проекту: `gbrain search "Золотая Балка"` → все связанные файлы
- По человеку: `gbrain query "person: Иванов"` → карточка человека
- По концепции: `gbrain search "виноградарство ирригация"` → связанные знания
- Семантический: `gbrain query --semantic "управление поливом"` (требует эмбеддинги)