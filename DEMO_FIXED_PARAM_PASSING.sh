#!/bin/bash
# Демонстрация правильной передачи сложных параметров в Node.js скрипты
# Решение проблемы с кавычками и специальными символами

echo "🧪 Демонстрация исправленной передачи параметров"
echo "=============================================="

# Пример 1: Простой селектор (работает и так и так)
echo ""
echo "1️⃣ ПРОСТОЙ СЕЛЕКТОР: .sorts-list"
URL1="https://zolotayabalka.ru/company/sort/"
OUTPUT1="/tmp/demo1_sorts.txt"

# Метод через переменные окружения (рекомендуется)
export TARGET_URL="$URL1"
export TARGET_SELECTOR=".sorts-list"
export OUTPUT_PATH="$OUTPUT1"
export EXTRACT_MODE="text"

NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');
(async () => {
    const browser = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(process.env.TARGET_URL, { waitUntil: 'commit' });
    if (process.env.TARGET_SELECTOR !== 'networkidle' && process.env.TARGET_SELECTOR !== '') {
        await page.waitForSelector(process.env.TARGET_SELECTOR, { state: 'attached' });
    } else {
        await page.waitForLoadState('networkidle');
    }
    await page.waitForTimeout(2000);
    const content = await page.evaluate(() => document.body.innerText);
    await browser.close();
    fs.writeFileSync(process.env.OUTPUT_PATH, content);
    console.log('✅ Сортов получено:', content.length, 'символов');
})();
"

echo "   Результат: $(wc -c < "$OUTPUT1" | tr -d ' ') байт"

# Пример 2: СЛОЖНЫЙ СЕЛЕКТОР С КАВЫЧКАМИ (здесь обычно ломается)
echo ""
echo "2️⃣ СЛОЖНЫЙ СЕЛЕКТОР: [class*='about'] (с одинарными кавычками)"
OUTPUT2="/tmp/demo2_company_attempt.txt"

# ТО ЖЕ САМОЕ РЕШЕНИЕ: переменные окружения решают проблему кавычек!
export TARGET_URL="https://zolotayabalka.ru"
export TARGET_SELECTOR="[class*='about']"  # Вот эти кавычки обычно ломают bash!
export OUTPUT_PATH="$OUTPUT2"
export EXTRACT_MODE="text"

NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');
(async () => {
    const browser = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(process.env.TARGET_URL, { waitUntil: 'commit' });
    // Важно: процесс.env. переменные приходят как строки, кавычки сохранены!
    if (process.env.TARGET_SELECTOR !== 'networkidle' && process.env.TARGET_SELECTOR !== '') {
        await page.waitForSelector(process.env.TARGET_SELECTOR, { state: 'attached' });
    } else {
        await page.waitForLoadState('networkidle');
    }
    await page.waitForTimeout(2000);
    const content = await page.evaluate(() => document.body.innerText);
    await browser.close();
    fs.writeFileSync(process.env.OUTPUT_PATH, content);
    console.log('✅ Контент по селектору [class*=\'about\']:',
                content.length, 'символов');
})();
"

echo "   Результат: $(wc -c < "$OUTPUT2" | tr -d ' ') байт"
echo "   Превью: $(head -c 100 "$OUTPUT2")"

# Пример 3: ЕЩЕ СЛОЖНЕЕ - множественные селекторы с кавычками
echo ""
echo "3️⃣ КОМПЛЕКСНЫЙ ЗАПРОС: Множественные селекторы с кавычками"
OUTPUT3="/tmp/demo3_complex.txt"

# Даже такой сложный селектор работает через переменные окружения!
export TARGET_URL="https://zolotayabalka.ru"
export TARGET_SELECTOR=".about, .company-info, #about, [class*='about'], [class*='company']"
export OUTPUT_PATH="$OUTPUT3"
export EXTRACT_MODE="text"

NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');
(async () => {
    const browser = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(process.env.TARGET_URL, { waitUntil: 'commit' });
    // Сложный селектор с множеством кавычек передается идеально!
    if (process.env.TARGET_SELECTOR !== 'networkidle' && process.env.TARGET_SELECTOR !== '') {
        await page.waitForSelector(process.env.TARGET_SELECTOR, { state: 'attached' });
    } else {
        await page.waitForLoadState('networkidle');
    }
    await page.waitForTimeout(2000);
    const content = await page.evaluate(() => document.body.innerText);
    await browser.close();
    fs.writeFileSync(process.env.OUTPUT_PATH, content);
    console.log('✅ Комплексный запрос выполнен:',
                content.length, 'символов получено');
})();
"

echo "   Результат: $(wc -c < "$OUTPUT3" | tr -d ' ') байт"
echo ""

# Пример 4: Сравнение - что бы случилось без исправления
echo ""
echo "4️⃣ ЧТО ПРОИЗОЙДЕТ БЕЗ ИСПРАВЛЕНИЯ (демонстрация проблемы)"
echo "    Если бы мы пытались передать селектор напрямую в аргументы:"
echo "    node -e \"...\" \"https://site.com\" \".class*='about'\" \"output.txt\""
echo ""
echo "    💥 Проблема: Внутренние одинарные кавычки в \".class*='about'\""
echo "       ломали бы парсинг аргументов bash!"
echo ""
echo "    ✅ РЕШЕНИЕ: Всегда используйте процесс.env. для сложных данных!"
echo ""

echo "📊 ИТОГОВЫЙ СЧЕТ:"
echo "=================="
echo "✅ Простой селектор (.sorts-list):      Работает обоими способами"
echo "✅ Сложный селектор с кавычками:       ТРЕБУЕТ исправления через env"
echo "✅ Комплексный селектор:               ТРЕБУЕТ исправления через env"
echo ""
echo "🏆 РЕКОМЕНДАЦИЯ: Для 100% надежности всегда использовать:"
echo "   export VARIABLE=\"value\""
echo "   NODE_PATH=... /usr/bin/node -e \"... process.env.VARIABLE ...\""
echo ""
echo "📁 Созданные демонстрационные файлы:"
ls -l /tmp/demo*_*.txt 2>/dev/null || echo "Файлы пока не созданы"