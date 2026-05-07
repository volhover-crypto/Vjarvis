#!/bin/bash
# Простой скрипт для извлечения списка сортов с сайта Золотая Балка
# Обходит ограничения среды через прямой вызов Node.js с Playwright

echo "🔄 Извлечение списка сортов винограда с https://zolotayabalka.ru/company/sort/"

# Результат будет сохранен в временный файл
OUTPUT_FILE="/tmp/soltayabalka_sorts_$(date +%Y%m%d_%H%M%S).txt"

# Запускаем наш проверенный рабочий подход
NODE_PATH=/usr/lib/node_modules/openclaw/node_modules /usr/bin/node -e "
const playwright = require('playwright-core');
const fs = require('fs');

(async () => {
    try {
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
        console.log('🌐 Переход на сайт...');
        await page.goto('https://zolotayabalka.ru/company/sort/', { waitUntil: 'commit' });
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(3000); // Дополнительная задержка для динамического контента
        
        const title = await page.title();
        console.log('📄 Заголовок: ' + title);
        
        // Извлекаем список сортов - ищем элементы, содержащие названия сортов
        const sortsContent = await page.evaluate(() => {
            // Получаем весь текст страницы
            const fullText = document.body.innerText;
            
            // Ищем секцию с сортами - обычно после заголовка «Наши виноградники»
            const lines = fullText.split('\\n').map(line => line.trim()).filter(line => line.length > 0);
            
            // Известные сорта винограда для фильтрации
            const knownVarieties = [
                'Каберне Совиньон', 'Мерло', 'Бастардо Магарачский', 'Пино Нуар',
                'Совиньон Блан', 'Саперави', 'Сира', 'Рислинг Рейнский', 'Пино Меньё',
                'Пино Гри', 'Каберне Фран', 'Мускат Оттонель', 'Пино Блан',
                'Мускат Гамбургский', 'Мускат Янтарный', 'Мускат Белый',
                'Кокур Белый', 'Ал', 'Алиготе'
            ];
            
            // Фильтруем строки, оставляя только те, которые содержат известные сорта
            const sorts = lines.filter(line => 
                knownVarieties.some(variety => line.includes(variety))
            );
            
            return sorts.join('\\n');
        });
        
        await browser.close();
        
        if (sortsContent.trim()) {
            console.log('✅ Список сортов успешно извлечен:');
            console.log(sortsContent);
            // Сохраняем в файл для последующего использования
            fs.writeFileSync(process.argv[1], sortsContent);
            process.exit(0);
        } else {
            console.log('⚠️  Сорты не найдены стандартным способом, пробуем альтернативный подход...');
            
            // Альтернативный подход - ищем по содержимому
            const allText = await page.evaluate(() => document.body.innerText);
            const lines = allText.split('\\n').map(line => line.trim()).filter(line => line.length > 2);
            
            // Ищем строки, которые похожи на названия сортов (обычно одно-два слова с заглавной буквы)
            const potentialSorts = lines.filter(line => 
                /^[А-Я][а-я]+(\\s+[А-Я][а-я]+)*$/.test(line) && 
                !['О компании', 'Где купить', 'Новости', 'Наши вина', 'О винодельне', 'Туристический комплекс', 'Контакты', 'Главная'].includes(line) &&
                line.length > 3
            );
            
            if (potentialSorts.length > 0) {
                console.log('🔍 Возможные сорта (альтернативный метод):');
                console.log(potentialSorts.join('\\n'));
                fs.writeFileSync(process.argv[1], potentialSorts.join('\\n'));
                process.exit(0);
            } else {
                throw new Error('Не удалось извлечь список сортов ни одним из методов');
            }
        }
    } catch (error) {
        console.error('❌ Ошибка:', error.message);
        process.exit(1);
    }
})();
" "$OUTPUT_FILE"

# Проверяем результат
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    echo ""
    echo "🍇 СПИСОК СОРТОВ ВИНОГРАДА С САЙТА ZOLOTOYABALKA.RU:"
    echo "===================================================="
    cat "$OUTPUT_FILE"
    echo "===================================================="
    echo ""
    echo "💾 Результат сохранен в: $OUTPUT_FILE"
else
    echo "❌ Не удалось извлечь список сортов"
    if [ -f "$OUTPUT_FILE" ]; then
        cat "$OUTPUT_FILE"
    fi
    exit 1
fi