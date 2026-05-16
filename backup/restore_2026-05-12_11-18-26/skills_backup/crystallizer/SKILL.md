# skills/crystallizer/SKILL.md — Навык кристаллизации знаний (NFD Knowledge Crystallization Cycle + EvolveR)

> Навык для периодической обработки накопленного опыта и превращения его в структурированные, проверенные принципы.  
> Реализует:
> - Knowledge Crystallization Cycle (KCC) из Nurture-First Development (NFD):  
>   Conversational Immersion → Experiential Accumulation → Deliberate Crystallization → Grounded Application  
> - EvolveR метрика эффективности для принципов: отслеживание applied_count, success_rate, last_applied  
>  
> Триггеры (три режима по NFD):
> - **Scheduled**: каждые 2 недели (>20 записей в memory/)
> - **Threshold**: при накоплении >5 записей с тегом `[ERROR]` одного типа
> - **Event**: после завершения сезонного агроцикла, крупного IoT-инцидента, нового проекта
>  
> Алгоритм кристаллизации (выполняется в Surgical Workspace — Claude Code / n8n / ручная обработка):
> ```
> 1. Собрать все записи memory/ за период
> 2. Сгруппировать по тегам [DECISION|INSIGHT|ERROR|PATTERN]
> 3. Извлечь повторяющиеся паттерны (≥3 похожих записи)
> 4. Для каждого паттерна:
>    a. Сформулировать обобщённый принцип (de-contextualize)
>    b. Проверить в principles_lib.md на дублирование
>    c. Предложить пользователю валидацию (человек-в-петле)
>    d. После подтверждения → записать в релевантный skill references/
> 5. Устаревшие/опровергнутые принципы → пометить [DEPRECATED]
> 6. Обновить MEMORY.md сводкой новых кристаллизованных знаний
> 7. Записать в plans/ отчёт о кристаллизации с метриками
> ```
>  
> Метрика эффективности (EvolveR): для каждого принципа в `principles_lib.md` отслеживать:
> - `applied_count` — сколько раз применялся
> - `success_rate` — доля задач, где вывод был верным
> - `last_applied` — дата последнего применения
> - Принципы с `success_rate < 0.4` и `applied_count > 5` → предлагать пересмотр
>  
> Входы:
> - Папка `memory/` (дневные логи, error_patterns.md, principles_lib.md, cases/)
> - Папка `skills/*/references/` (для обновления)
> - Папка `plans/` (для записи отчётов)
> - Файл `MEMORY.md` (для обновления сводки)
>  
> Выходы:
> - Обновленные `skills/*/references/` с кристаллизованными принципами
> - Обновленная `memory/principles_lib.md` (метрики принципов)
> - Обновленная `MEMORY.md` (сводка новых знаний)
> - Новые отчёты в `plans/crystallization_report_YYYY-MM-DD.md`
>  
> Зависимости: доступ к файловой системе, стандартные текстовые инструменты (grep, awk, sed, sort, uniq, date)
>  
> Выполняется в Surgical Workspace (внешние инструменты: Claude Code, Cursor, n8n, локальный редактор)  
> как batch-операция по триггеру из навыка или расписанию.
>  
> *Файл создан: 01.05.2026*
> *После создания — добавить скрипт-реализацию в scripts/*