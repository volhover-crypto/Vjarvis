#!/bin/bash
# Извлечение информации о компании Золотая Балка с исправленной передачей параметров

echo "🏢 Извлечение информации о компании Золотая Балка"
echo "Используем исправленный метод передачи параметров через переменные окружения"
echo "========================================================================"

URL="https://zolotayabalka.ru"
OUTPUT_FILE="/tmp/zolotayabalka_company_info_$(date +%Y%m%d_%H%M%S).txt"

# Пробуем разные селекторы для поиска информации о компании
SELECTORS=(
    "networkidle"  # Сначала просто ждем загрузки всей страницы
    ".about"
    ".company-info" 
    "#about"
    "[class*='about']"
    "[class*='company']"
    "section"
    ".content"
)

echo "🎯 Целевой URL: $URL"
echo "💾 Выходной файл: $OUTPUT_FILE"
echo ""

# Пробуем каждый селектор по порядку
for selector in "${SELECTORS[@]}"; do
    echo "🔄 Пробуем селектор: '$selector'"
    
    # ЭКСПЕРТНЫЙ МЕТОД: Передача сложных данных через переменные окружения
    export TARGET_URL="$URL"
    export TARGET_SELECTOR="$selector"
    export OUTPUT_PATH="$OUTPUT_FILE"
    export EXTRACT_MODE="text"
    
    NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
    const playwright = require('playwright-core');
    const fs = require('fs');
    
    (async () => {
        console.log('🚀 Запуск браузера...');
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
            console.log(`🌐 Переход на: ${process.env.TARGET_URL}`);
            await page.goto(process.env.TARGET_URL, { waitUntil: 'commit' });
            
            // Ожидание загрузки контента
            if (process.env.TARGET_SELECTOR !== 'networkidle' && process.env.TARGET_SELECTOR !== '') {
                console.log(`🎯 Ожидание селектора: ${process.env.TARGET_SELECTOR}`);
                await page.waitForSelector(process.env.TARGET_SELECTOR, { state: 'attached' });
            } else {
                console.log('⏳ Ожидание полной загрузки страницы (networkidle)...');
                await page.waitForLoadState('networkidle');
            }
            
            // Небольшая дополнительная задержка для динамического контента
            await page.waitForTimeout(2000);
            
            // Извлечение контента
            console.log('📥 Извлечение контента...');
            let content;
            if (process.env.EXTRACT_MODE === 'html') {
                content = await page.content();
            } else {
                content = await page.evaluate(() => document.body.innerText);
            }
            
            await browser.close();
            
            // Проверяем, что получили осмысленный контент
            if (content && content.length > 50) {
                console.log(`✅ Получено ${content.length} символов контента`);
                fs.writeFileSync(process.env.OUTPUT_PATH, content);
                console.log(`💾 Контент сохранен в: ${process.env.OUTPUT_PATH}`);
                process.exit(0);
            } else {
                console.log('⚠️  Получено слишком мало контента, пробуем следующий селектор...');
                process.exit(1);  // Пытаем следующий селектор
            }
        } catch (error) {
            console.error(`❌ Ошибка с селектором '${process.env.TARGET_SELECTOR}': ${error.message}`);
            process.exit(1);  // Пытаем следующий селектор
        }
    })();
    " || echo "   ❌ Селектор '$selector' не сработал, пробуем следующий..."
    
    # Проверяем, получили ли мы полезный результат
    if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
        CONTENT_LENGTH=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
        if [ "$CONTENT_LENGTH" -gt 100 ]; then  # Если получили достаточно контента
            echo ""
            echo "🎉 УСПЕШНО! Информация о компании извлечена:"
            echo "============================================="
            echo "🔑 Использован селектор: '$selector'"
            echo "📊 Размер полученных данных: $CONTENT_LENGTH байт"
            echo ""
            echo "📖 Первые 500 символов извлеченной информации:"
            echo "----------------------------------------"
            head -c 500 "$OUTPUT_FILE"
            echo ""
            echo "..."
            echo ""
            echo "💡 Полный результат сохранен в: $OUTPUT_FILE"
            break  # Выходим из цикла, так как получили результат
        fi
    fi
done

# Если ничего не сработало, пробуем просто получить всю страницу
if [ ! -f "$OUTPUT_FILE" ] || [ ! -s "$OUTPUT_FILE" ] || [ $(wc -c < "$OUTPUT_FILE" | tr -d ' ') -lt 100 ]; then
    echo ""
    echo "🔄 Пытаемся получить весь контент страницы как последний resort..."
    
    export TARGET_URL="$URL"
    export TARGET_SELECTOR="networkidle"
    export OUTPUT_PATH="$OUTPUT_FILE"
    export EXTRACT_MODE="text"
    
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
            await page.waitForLoadState('networkidle');
            await page.waitForTimeout(3000);
            
            const content = await page.evaluate(() => document.body.innerText);
            await browser.close();
            
            fs.writeFileSync(process.env.OUTPUT_PATH, content);
            console.log(`✅ Получен полный контент страницы: ${content.length} символов`);
            console.log(`💾 Сохранено в: ${process.env.OUTPUT_PATH}`);
        } catch (error) {
            console.error('❌ Критическая ошибка:', error.message);
            process.exit(1);
        }
    })();
fi

echo ""
echo "📊 ИТОГОВЫЙ РЕЗУЛЬТАТ:"
echo "===================="
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    CONTENT_SIZE=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
    LINE_COUNT=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
    echo "✅ Файл создан: $OUTPUT_FILE"
    echo "📏 Размер: $CONTENT_SIZE байт"
    echo "📄 Строк: $LINE_COUNT"
    echo ""
    echo "🖋️  Превью содержимого (первые 20 строк):"
    echo "----------------------------------------"
    head -20 "$OUTPUT_FILE"
    echo ""
else
    echo "❌ Не удалось извлечь информацию о компании"
    echo "💡 Возможные причины:"
    echo "   - Сайт блокирует автоматизированные запросы"
    echo "   - Требуется JavaScript выполнение для отображения контента"
    echo "   - Селекторы не совпадают с фактической структурой сайта"
    echo "   - Нужны дополнительные параметры ожидания или взаимодействия"
fi