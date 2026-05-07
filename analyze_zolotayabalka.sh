#!/bin/bash
# Комплексный анализ сайта Золотая Балка
# Извлекает структурированную информацию о предприятии

echo "🔍 Комплексный анализ сайта https://zolotayabalka.ru"
echo "========================================================"

OUTPUT_DIR="/tmp/zolotayabalka_analysis_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# Функция для извлечения конкретных секций
extract_section() {
    local url="$1"
    local output_file="$2"
    local wait_for="$3"
    local description="$4"
    
    echo "📥 Извлечение: $description"
    
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
            await page.goto(process.argv[2], { waitUntil: 'commit' });
            if (process.argv[3] !== 'networkidle') {
                await page.waitForSelector(process.argv[3], { state: 'attached' });
            } else {
                await page.waitForLoadState('networkidle');
            }
            await page.waitForTimeout(2000);
            
            const content = await page.evaluate(() => 
                process.argv[4] === 'html' ? 
                    document.documentElement.outerHTML : 
                    document.body.innerText
            );
            
            await browser.close();
            fs.writeFileSync(process.argv[5], content);
            console.log('✅ ' + process.argv[6] + ' сохранен');
        } catch (error) {
            console.error('❌ Ошибка при извлечении ' + process.argv[6] + ': ' + error.message);
            process.exit(1);
        }
    })();
    " "$url" "$wait_for" "$text_or_html" "$output_file" "$description"
}

# 1. Головная страница - общая информация
echo ""
echo "1️⃣ ГЛАВНАЯ СТРАНИЦА - ОБЩАЯ ИНФОРМАЦИЯ"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/main_page.txt" "networkidle" "text" "Главная страница"

# 2. О компании
echo ""
echo "2️⃣ О КОМПАНИИ"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/about_company.txt" ".about, .company-info, #about" "text" "Информация о компании"

# 3. Наши виноградники (уже частично сделали)
echo ""
echo "3️⃣ НАШИ ВИНОГРАДНИКИ И СОРТА"
extract_section "https://zolotayabalka.ru/company/sort/" "$OUTPUT_DIR/grape_varieties.txt" ".sorts-list, .varieties, #sorts" "text" "Список сортов винограда"

# 4. Наши вина
echo ""
echo "4️⃣ НАШИ ВИНА"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/wines.txt" ".wines, .product-list, #wines" "text" "Информация о винах"

# 5. Туристический комплекс
echo ""
echo "5️⃣ ТУРИСТИЧЕСКИЙ КОМПЛЕКС"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/tourism.txt" ".tourism, .hotel, #tourism" "text" "Информация о туристическом комплексе"

# 6. Ресторан
echo ""
echo "6️⃣ РЕСТОРАН"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/restaurant.txt" ".restaurant, .menu, #restaurant" "text" "Информация о ресторане"

# 7. Новости и события
echo ""
echo "7️⃣ НОВОСТИ И СОБЫТИЯ"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/news.txt" ".news, .events, #news" "text" "Новости и события"

# 8. Контакты
echo ""
echo "8️⃣ КОНТАКТЫ"
extract_section "https://zolotayabalka.ru" "$OUTPUT_DIR/contacts.txt" ".contacts, .address, #contacts" "text" "Контактная информация"

# 9. Также попробуем извлечь структурированные данные через селекторы по умолчанию
echo ""
echo "9️⃣ СТРУКТУРИРОВАННЫЙ АНАЛИЗ ГЛАВНОЙ СТРАНИЦЫ"
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
        await page.goto('https://zolotayabalka.ru', { waitUntil: 'commit' });
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);
        
        const structuredData = await page.evaluate(() => {
            const data = {};
            
            // Пытаемся найти структурированные данные
            const titleElements = document.querySelectorAll('h1, h2, h3, .title, .heading');
            data.titles = Array.from(titleElements).map(el => el.textContent.trim()).filter(t => t.length > 0);
            
            // Находим блоки с информацией
            const infoBlocks = document.querySelectorAll('.info, .description, .text, .content, p, .block');
            data.infoBlocks = Array.from(infoBlocks)
                .map(el => el.textContent.trim().substring(0, 200)) // первые 200 символов
                .filter(text => text.length > 20);
                
            // Ищем номера телефонов
            const phonePattern = /\+?\d[\d\s\-\(\)]{10,}/g;
            const allText = document.body.innerText;
            const phones = [...allText.matchAll(phonePattern)].map(m => m[0]).filter((p, i, arr) => arr.indexOf(p) === i);
            data.phones = phones;
            
            // Ищем email адреса
            const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
            const emails = [...allText.matchAll(emailPattern)].map(m => m[0]).filter((e, i, arr) => arr.indexOf(e) === i);
            data.emails = emails;
            
            // Ищем ссылки на соцсети
            const socialLinks = Array.from(document.querySelectorAll('a[href]'))
                .map(link => link.href)
                .filter(href => 
                    /(facebook|instagram|vk|telegram|youtube)\.(com|ru)/.test(href) ||
                    href.includes('t.me') ||
                    href.includes('instagram.com') ||
                    href.includes('facebook.com')
                );
            data.socialLinks = socialLinks;
            
            return data;
        });
        
        await browser.close();
        fs.writeFileSync('$OUTPUT_DIR/structured_data.json', JSON.stringify(structuredData, null, 2));
        console.log('✅ Структурированные данные сохранены');
    } catch (error) {
        console.error('❌ Ошибка при извлечении структурированных данных: ' + error.message);
        process.exit(1);
    }
})();
"

echo ""
echo "📊 АНАЛИЗ ЗАВЕРШЕН"
echo "=================="
echo "📁 Результаты сохранены в директории: $OUTPUT_DIR"
echo ""
echo "📄 Содержимое директории:"
ls -la "$OUTPUT_DIR"
echo ""
echo "📖 Краткий обзор извлеченной информации:"
echo ""

# Показываем краткое содержимое каждого файла
for file in "$OUTPUT_DIR"/*.txt; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "--- $filename ---"
        head -5 "$file"
        echo "..."
        echo ""
    fi
done

# Показываем структурированные данные если есть
if [ -f "$OUTPUT_DIR/structured_data.json" ]; then
    echo "--- structured_data.json ---"
    cat "$OUTPUT_DIR/structured_data.json"
    echo ""
fi

echo ""
echo "💡 Для полного анализа изучите файлы в директории: $OUTPUT_DIR"