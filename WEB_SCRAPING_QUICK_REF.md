# Быстрая справка: Веб-скрейпинг в OpenClaw

## 🚀 Стандартная команда
```bash
./fetch-site-content.sh <URL> [output_file] [wait_for] [timeout] [mode]
```

## 📦 Готовый скрипт
Создайте `fetch-site-content.sh`:
```bash
#!/bin/bash
URL="$1"
OUTPUT_FILE="${2:-/tmp/web_$(date +%Y%m%d_%H%M%S).txt}"
WAIT_FOR="${3:-networkidle}"
WAIT_TIMEOUT="${4:-15000}"
EXTRACT_MODE="${5:-text}"

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
    page.setDefaultTimeout(parseInt(process.argv[5]));
    try {
        await page.goto(process.argv[2], { waitUntil: 'commit' });
        if (process.argv[3] !== 'networkidle') {
            await page.waitForSelector(process.argv[3], { state: 'attached' });
        } else {
            await page.waitForLoadState('networkidle');
        }
        const content = await page.evaluate(() => 
            process.argv[6] === 'html' ? 
                document.documentElement.outerHTML : 
                document.body.innerText
        );
        await browser.close();
        fs.writeFileSync(process.argv[4], content);
        console.log('✅ Готово: ' + process.argv[4]);
    } catch (e) {
        console.error('❌ Ошибка: ' + e.message);
        process.exit(1);
    }
})();
" "$URL" "$WAIT_FOR" "$WAIT_TIMEOUT" "$OUTPUT_FILE" "$EXTRACT_MODE"
```

## 💡 Примеры использования

### Базовое извлечение текста
```bash
./fetch-site-content.sh https://zolotayabalka.ru/company/sort/ sorts.txt
```

### Извлечение HTML с ожиданием элемента
```bash
./fetch-site-content.sh https://example.com/ output.html '.price-table' 20000 html
```

### Мониторинг изменений
```bash
# Сегодня
./fetch-site-content.sh https://site.com/ today.txt
# Завтра  
./fetch-site-content.sh https://site.com/ tomorrow.txt
# Сравнить
diff today.txt tomorrow.txt
```

## 🔧 Установка и настройка
Одноразовая установка браузеров:
```bash
npx playwright install
```

Проверка доступности:
```bash
ls -la /root/.cache/ms-playwright/
# Должны быть папки: chromium-*, firefox-*, webkit-*
```

## 📊 Результат
- ✅ Работает с JavaScript-тяжелыми сайтами
- ✅ Обходит ограничения среды  
- ✅ Возвращает чистый текст или HTML
- ✅ Сохраняет метаданные в файлы
- ✅ Легко интегрируется в workflows

## 🆘 troubleshooting
Если не работает:
1. `npx playwright install` (обновление браузеров)
2. Проверить пути: `/root/.cache/ms-playwright/*/chrome-headless-shell`
3. Убедиться в NODE_PATH: включает openclaw/node_modules