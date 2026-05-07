# Инструкция по работе с RAG-разделом "n8n-orchestration"

**Назначение:** Управление базой знаний по оркестрации данных, n8n, AI-агентам и векторным базам данных.

## 1. Структура базы знаний
Все файлы хранятся в `~/self-improving/projects/rag-indexed/n8n-orchestration/`:
- `core_platform`: Архитектура n8n, воркфлоу, автоматизация.
- `ai_agents`: LLM-агенты, автономные системы, reasoning.
- `rag_theory`: Теория RAG, чанкинг, индексация.
- `mcp_integrations`: Model Context Protocol.
- `vector_databases`: Векторные БД (Chroma, Milvus, pgvector).
- `prompt_engineering`: Промпт-инжиниринг, оптимизация запросов.

## 2. Добавление новых статей
1. **Загрузка:** Добавь PDF-файлы в папку `N 8 N` на Google Drive (ID: `1KUL4QLvRK1oF0zu-hPa-LnaUqsvdEax8`).
2. **Запуск:** Выполни команду:
   ```bash
   python3 /root/.openclaw/workspace/scripts/process_n8n_rag.py
   ```
3. **Автоматика:** Скрипт сам скачает новые файлы, классифицирует их, конвертирует в Markdown и разложит по папкам.

## 3. Метаданные
Каждый чанк содержит:
- `source_block`: Категория (папка).
- `source_file`: Оригинальное имя файла.
- `topic_tags`: Теги для поиска.

## 4. Резервное копирование
Все инструкции и ключевые файлы копируются в папку `rezerv` на Google Drive для сохранности.

---
*Эта инструкция также сохранена в `rezerv` на Google Drive.*