# Knowledge Pipeline — Пополнение знаний агента

## Описание
Автоматизированная система пополнения базы знаний агента из различных источников.
Все знания сохраняются в vault, индексируются в GBrain с локальными эмбеддингами.

## Источники знаний

| Источник | Команда | Описание |
|----------|---------|----------|
| Web-страница | `knowledge_pipeline.py url <URL>` | Скачивает и сохраняет содержимое |
| Файл | `knowledge_pipeline.py file <path>` | Копирует и индексирует файл |
| Текст | `knowledge_pipeline.py text <title>` | Сохраняет текст напрямую |
| arXiv | `knowledge_pipeline.py arxiv <id>` | Скачивает научную статью |

## Домены знаний

- **agronomy** — агрономия, точное земледелие, почвы, удобрения
- **viticulture** — виноградарство, сорта, ампелография
- **iot** — IoT, датчики, мониторинг, MQTT
- **ai_ml** — AI/ML, LLM, агенты, RAG
- **agritech** — AgriTech, precision agriculture

## Использование

### Добавить знания из URL
```bash
python3 /root/.openclaw/workspace/projects/knowledge-pipeline/knowledge_pipeline.py \
  url "https://example.com/article" --domain agronomy --tags "полив,почва"
```

### Добавить файл
```bash
python3 /root/.openclaw/workspace/projects/knowledge-pipeline/knowledge_pipeline.py \
  file /path/to/document.pdf --domain viticulture
```

### Добавить текст
```bash
echo "Текст знаний..." | python3 /root/.openclaw/workspace/projects/knowledge-pipeline/knowledge_pipeline.py \
  text "Название" --domain iot --source "книга Чиркова"
```

### Добавить статью с arXiv
```bash
python3 /root/.openclaw/workspace/projects/knowledge-pipeline/knowledge_pipeline.py \
  arxiv "2401.12345" --tags "LLM,RAG"
```

### Синхронизировать с GBrain
```bash
python3 /root/.openclaw/workspace/projects/knowledge-pipeline/knowledge_pipeline.py sync
```

### Семантический поиск
```bash
python3 /root/.openclaw/workspace/projects/gbrain-embed-local/search_local.py "запрос"
```

## Автоматический мониторинг (HEARTBEAT)

В HEARTBEAT.md добавлены задачи:
- Еженедельный поиск новостей по доменам
- Обновление знаний из отслеживаемых источников
- Проверка новых статей на arXiv

## Структура файлов

```
/root/vault/knowledge/
├── agronomy/      # Агрономия
├── viticulture/   # Виноградарство
├── iot/           # IoT и мониторинг
├── ai-ml/         # AI/ML
├── agritech/      # AgriTech
└── misc/          # Прочее
```

## Логи

- Обработанные источники: `/root/.openclaw/workspace/memory/processed_sources.json`
- Статистика: команда `knowledge_pipeline.py stats`
