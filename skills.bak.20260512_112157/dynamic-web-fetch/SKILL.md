---
name: dynamic-web-fetch
description: Extract content from dynamic web pages using headless browser (Playwright). Accepts URL, loads page, waits for content load (selector or network idle), extracts content (text, tables, HTML), and returns as markdown or text for further analysis. Use when you need to scrape JavaScript-heavy sites, SPAs, or pages requiring interaction.
---
# dynamic-web-fetch

Навык для извлечения содержимого с динамических веб-страниц с использованием headless-браузера Playwright.

## Быстрый старт

Извлечь текст со страницы, ожидая загрузки контента:
[code example]

## Расширенные возможности

- **Ожидание селектора**: См. [WAIT_SELECTOR.md](references/wait-selector.md) для полного руководства
- **Ожидание сетевого бездействия**: См. [NETWORK_IDLE.md](references/network-idle.md)
- **Извлечение таблиц**: См. [TABLE_EXTRACTION.md](references/table-extraction.md)
- **Примеры**: См. [EXAMPLES.md](references/examples.md)

## Как это работает

1. Принимает URL целевой страницы
2. Запускает headless-браузер Playwright
3. Переходит по URL
4. Ждет выполнения условия загрузки (селектор appears или network idle)
5. Извлекает содержимое страницы
6. Преобразует в markdown или plain text
7. Возвращает результат для дальнейшего анализа

## Требования

- Установленный Playwright (установлен глобально в OpenClaw среде)
- Доступ к целевому URL (можно комбинировать с прокси при необходимости)

## Выходные форматы

- **markdown** - для удобного чтения и дальнейшей обработки
- **text** - чистый текст без markdown разметки
- **html** - исходный HTML (опционально, для отладки)

## Обработка ошибок

Навык возвращает структурированные сообщения об ошибках при:
- Недоступности URL
- Таймауте ожидания контента
- Ошибках парсинга/извлечения
- Проблемах с браузером

## Безопасность

- Выполняется в изолированном окружении
- Нет доступа к локальной файловой системе помимо временных файлов
- Автоматическая очистка ресурсов после выполнения**
