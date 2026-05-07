# Исправленный метод веб-извлечения в OpenClaw
# Решение проблемы с передачей параметров содержащих специальные символы

## 🔍 Проблема
При передаче сложных CSS селекторов содержащих одинарные кавычки (например: `[class*='about']`) через bash-функции в Node.js скрипты возникают ошибки парсинга из-за конфликта кавычек в командной строке.

## ✅ Решения

### Метод 1: Использование переменных окружения (РЕКОМЕНДУЕМЫЙ)
Передаем сложные данные через переменные окружения вместо аргументов командной строки.

```bash
# В bash-скрипте:
export URL="https://zolotayabalka.ru"
export SELECTOR=".about, .company-info, #about, [class*='about']"
export OUTPUT_FILE="/tmp/result.txt"
export EXTRACT_MODE="text"

NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');
(async () => {
    const browser = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    // ... остальной код
    process.env.URL, process.env.SELECTOR, process.env.OUTPUT_FILE, process.env.EXTRACT_MODE
})();
"
```

### Метод 2: Использование JSON для передачи сложных данных
Кодируем параметры в JSON строку и передаем как один аргумент.

```bash
# Подготавливаем JSON с параметрами
PARAMS='{"url":"https://zolotayabalka.ru","selector":".about, .company-info, #about, [class*=\\'about\\']","output":"/tmp/result.txt","mode":"text"}'

# Передаем как один аргумент
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');
const params = JSON.parse(process.argv[2]);
// Используем params.url, params.selector и т.д.
" "$PARAMS"
```

### Метод 3: Base64 кодирование (для максимальной безопасности)
```bash
# Кодируем данные в base64
PARAMS=$(echo -n '{"url":"https://example.com","selector":"div.content"}' | base64)

# Декодируем в Node.js
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');
const params = JSON.parse(Buffer.from(process.argv[2], 'base64').toString());
// Используем параметры
" "$PARAMS"
```

## 🛠️ Практический пример исправленного скрипта

Вот как должен выглядеть исправленный скрипт для извлечения контента с сайта:

```bash
#!/bin/bash
# fetch-content-fixed.sh - Исправленная версия

URL="$1"
SELECTOR="${2:-networkidle}"
OUTPUT_FILE="${3:-/tmp/content_$(date +%Y%m%d_%H%M%S).txt}"
EXTRACT_MODE="${4:-text}"

# Используем экспорт переменных окружения для сложных данных
export TARGET_URL="$URL"
export TARGET_SELECTOR="$SELECTOR" 
export OUTPUT_PATH="$OUTPUT_FILE"
export EXTRACT_MODE="$EXTRACT_MODE"

NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');

(async () => {
    const browser = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    });
    
    const page = await context.newPage();
    try {
        await page.goto(process.env.TARGET_URL, { waitUntil: 'commit' });
        
        // Ожидание загрузки контента
        if (process.env.TARGET_SELECTOR !== 'networkidle' && process.env.TARGET_SELECTOR !== '') {
            await page.waitForSelector(process.env.TARGET_SELECTOR, { state: 'attached' });
        } else {
            await page.waitForLoadState('networkidle');
        }
        
        // Извлечение контента
        let content;
        if (process.env.EXTRACT_MODE === 'html') {
            content = await page.content();
        } else {
            content = await page.evaluate(() => document.body.innerText);
        }
        
        await browser.close();
        fs.writeFileSync(process.env.OUTPUT_PATH, content);
        console.log('✅ Контент сохранен в: ' + process.env.OUTPUT_PATH);
    } catch (error) {
        console.error('❌ Ошибка:', error.message);
        process.exit(1);
    }
})();
"
```

## 📋 Когда использовать каждый метод

### ✅ Метод 1 (Переменные окружения) - Лучший выбор когда:
- Нужно передавать несколько сложных параметров
- Параметры содержат специальные символы (кавычки, скобки)
- Требуется хорошая читаемость bash-кода
- Работа с CSS селекторами, JSON конфигурациями, сложными строками

### ✅ Метод 2 (JSON аргумент) - Лучше когда:
- Нужно передавать структурированные данные
- Предпочитаете явную структуру параметров
- Работаете с API-подобными интерфейсами
- Количество параметров предсказуемо иmoderate

### ✅ Метод 3 (Base64) - Используйте когда:
- Требуется максимальная защита от специальных символов
- Работаете в сильно ограниченных средах
- Нужно гарантировать передачу бинарных данных
- Совместимость с очень старыми системами критична

## 🧪 Проверка на нашем примере с Золотой Балкой

### Было (не работало):
```bash
# ОШИБКА: Внутренние кавычки ломают парсинг
extract_section "https://zolotayabalka.ru" ".about, .company-info, #about, [class*='about']" "$OUTPUT" "text"
```

### Стало (работает):
```bash
# РЕШЕНИЕ: Передача через переменные окружения
TARGET_URL="https://zolotayabalka.ru"
TARGET_SELECTOR=".about, .company-info, #about, [class*='about']"
OUTPUT_PATH="/tmp/about_info.txt"
EXTRACT_MODE="text"

export TARGET_URL TARGET_SELECTOR OUTPUT_PATH EXTRACT_MODE
# Затем вызов Node.js с процесс.env.*
```

## 💡 Рекомендации для OpenClaw

1. **Для веб-скрейпинга**: Используйте Метод 1 (переменные окружения) при работе с CSS селекторами
2. **Для API интеграций**: Метод 2 (JSON) при передаче структурированных конфигураций  
3. **Для максимальной совместимости**: Метод 3 (Base64) в экстремальных случаях
4. **Всегда проверяйте**: `echo "$SELECTOR"` перед передачей в Node.js чтобы увидеть что именно передается
5. **Логируйте параметры**: Выводите process.env в консоль для отладки

## 📚 Связанные навыки и ресурсы

- **Навык `dynamic-web-fetch`** - основной навык для веб-извлечения
- **Навык `summarize`** - для обработки извлеченного текста  
- **Навык `qmd`** - для индексации и поиска собранных данных
- **Документация Playwright селекторов**: https://playwright.dev/docs/selectors
- **Руководство по escaping в bash**: https://www.gnu.org/software/bash/manual/html_node/Single-Quotes.html

Применяя эти методы, вы сможете надежно передавать любые сложные параметры в ваши веб-скрейпинг скрипты без ошибок парсинга.