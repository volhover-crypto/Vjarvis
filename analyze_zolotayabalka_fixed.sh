#!/bin/bash
# Исправленный комплексный анализ сайта Золотая Балка
# Правильно передает параметры в Node.js скрипт

echo "🔍 Исправленный комплексный анализ сайта https://zolotayabalka.ru"
echo "=============================================================="

OUTPUT_DIR="/tmp/zolotayabalka_analysis_fixed_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# Исправленная функция для извлечения конкретных секций
extract_section() {
    local url="$1"
    local selector="$2" 
    local output_file="$3"
    local description="$4"
    local extract_mode="$5"  # text или html
    
    echo "📥 Извлечение: $description"
    echo "   URL: $url"
    echo "   Селектор: '$selector'"
    echo "   Режим: $extract_mode"
    
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
            
            // Правильная обработка ожидания
            const waitForArg = process.argv[3];
            if (waitForArg !== 'networkidle' && waitForArg !== '') {
                await page.waitForSelector(waitForArg, { state: 'attached' });
            } else {
                await page.waitForLoadState('networkidle');
            }
            await page.waitForTimeout(2000);
            
            // Извлечение контента в зависимости от режима
            let content;
            if (process.argv[5] === 'html') {
                content = await page.evaluate(() => document.documentElement.outerHTML);
            } else {
                content = await page.evaluate(() => document.body.innerText);
            }
            
            await browser.close();
            fs.writeFileSync(process.argv[4], content);
            console.log('✅ ' + process.argv[6] + ' сохранен в: ' + process.argv[4]);
        } catch (error) {
            console.error('❌ Ошибка при извлечении ' + process.argv[6] + ': ' + error.message);
            process.exit(1);
        }
    })();
    " "$url" "$selector" "$output_file" "$extract_mode" "$description"
}

echo ""
echo "📋 ЭТАП 1: АНАЛИЗ ГЛАВНОЙ СТРАНИЦЫ"
echo "----------------------------------------"

# 1. Головная страница - общая информация
echo "1️⃣ ГЛАВНАЯ СТРАНИЦА - ОБЩАЯ ИНФОРМАЦИЯ"
extract_section "https://zolotayabalka.ru" "networkidle" "$OUTPUT_DIR/main_page.txt" "Главная страница" "text"

# 2. О компании
echo ""
echo "2️⃣ О КОМПАНИИ"
extract_section "https://zolotayabalka.ru" ".about, .company-info, #about, [class*='about']" "$OUTPUT_DIR/about_company.txt" "Информация о компании" "text"

# 3. Наши виноградники 
echo ""
echo "3️⃣ НАШИ ВИНОГРАДНИКИ И СОРТА"
extract_section "https://zolotayabalka.ru/company/sort/" ".sorts-list, .varieties, #sorts, [class*='sort'], [class*='variety']" "$OUTPUT_DIR/grape_varieties.txt" "Список сортов винограда" "text"

# 4. Наши вина
echo ""
echo "4️⃣ НАШИ ВИНА"
extract_section "https://zolotayabalka.ru" ".wines, .product-list, #wines, [class*='wine']" "$OUTPUT_DIR/wines.txt" "Информация о винах" "text"

# 5. Туристический комплекс
echo ""
echo "5️⃣ ТУРИСТИЧЕСКИЙ КОМПЛЕКС"
extract_section "https://zolotayabalka.ru" ".tourism, .hotel, #tourism, [class*='tourism']" "$OUTPUT_DIR/tourism.txt" "Информация о туристическом комплексе" "text"

# 6. Ресторан
echo ""
echo "6️⃣ РЕСТОРАН"
extract_section "https://zolotayabalka.ru" ".restaurant, .menu, #restaurant, [class*='restaurant']" "$OUTPUT_DIR/restaurant.txt" "Информация о ресторане" "text"

# 7. Новости и события
echo ""
echo "7️⃣ НОВОСТИ И СОБЫТИЯ"
extract_section "https://zolotayabalka.ru" ".news, .events, #news, [class*='news']" "$OUTPUT_DIR/news.txt" "Новости и события" "text"

# 8. Контакты
echo ""
echo "8️⃣ КОНТАКТЫ"
extract_section "https://zolotayabalka.ru" ".contacts, .address, #contacts, [class*='contact']" "$OUTPUT_DIR/contacts.txt" "Контактная информация" "text"

echo ""
echo "🔬 ЭТАП 2: ГЛУБОКИЙ СТРУКТУРИРОВАННЫЙ АНАЛИЗ"
echo "--------------------------------------------------"

# 9. Структурированный анализ главной страницы
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
        await page.waitForTimeout(3000);
        
        const structuredData = await page.evaluate(() => {
            const data = {};
            
            // Основная информация о компании
            const titleElements = document.querySelectorAll('h1, h2, h3, .title, .heading, [class*=\'title\']');
            data.titles = Array.from(titleElements)
                .map(el => el.textContent.trim())
                .filter(t => t.length > 0 && !t.includes('\n\t\t\t\t')); // фильтруем служебные переносы
            
            // Контактная информация
            const allText = document.body.innerText;
            
            // Телефоны (более точный паттерн)
            const phoneRegex = /\+?\d[\d\s\-\(\)]{10,}/g;
            const phones = [...allText.matchAll(phoneRegex)].map(m => m[0].trim())
                .filter(p => p.length >= 10); // минимум 10 символов для телефонa
            
            // Убираем дублираты и очищаем
            data.phones = [...new Set(phones)]
                .map(p => p.replace(/\s+/g, ' ').trim())
                .filter(p => /\+?\d/.test(p));
            
            // Email адреса
            const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
            data.emails = [...new Set(allText.matchAll(emailRegex))].map(m => m[0]);
            
            // Социальные сети
            const socialLinks = Array.from(document.querySelectorAll('a[href]'))
                .map(link => link.href)
                .filter(href => 
                    href && (
                        /(facebook|instagram|vk|telegram|youtube)\.(com|ru)/.test(href) ||
                        href.includes('t.me') ||
                        href.includes('instagram.com') ||
                        href.includes('facebook.com') ||
                        href.includes('youtube.com')
                    )
                );
            data.socialLinks = [...new Set(socialLinks)];
            
            // Навигационные ссылки для понимания структуры сайта
            const navLinks = Array.from(document.querySelectorAll('nav a, .menu a, header a'))
                .map(link => ({
                    text: link.textContent.trim(),
                    href: link.href
                }))
                .filter(link => link.text && link.text.length > 0 && link.href.startsWith('http'));
            data.navigation = navLinks.slice(0, 10); // первые 10 для читаемости
            
            // Последние новости/обновления (ищем по датам или ключевым словам)
            const dateElements = Array.from(document.querySelectorAll('*'))
                .filter(el => 
                    /\d{1,2}[\.\-\/]\d{1,2}[\.\-\/]\d{2,4}/.test(el.textContent) ||
                    /(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)/i.test(el.textContent)
                )
                .slice(0, 5)
                .map(el => el.textContent.trim());
            data.recentDates = dateElements;
            
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

# Показываем что получили
if [ -d "$OUTPUT_DIR" ]; then
    echo "📄 Содержимое директории анализа:"
    ls -la "$OUTPUT_DIR"
    echo ""
    
    echo "📊 Размеры извлеченных файлов:"
    for file in "$OUTPUT_DIR"/*; do
        if [ -f "$file" ]; then
            size=$(wc -c < "$file" | tr -d ' ')
            name=$(basename "$file")
            echo "   📄 $name: $size байт"
        fi
    done
    echo ""
    
    # Показываем контактную информацию как пример успешного извлечения
    if [ -f "$OUTPUT_DIR/contacts.txt" ] && [ -s "$OUTPUT_DIR/contacts.txt" ]; then
        echo "📞 Пример извлеченной контактной информации:"
        echo "----------------------------------------"
        head -10 "$OUTPUT_DIR/contacts.txt"
        echo ""
    fi
    
    # Показываем структурированные данные если есть
    if [ -f "$OUTPUT_DIR/structured_data.json" ]; then
        echo "📋 Ключи в структурированных данных:"
        echo "----------------------------------------"
        jq -r 'keys | .[]' "$OUTPUT_DIR/structured_data.json" 2>/dev/null || \
        grep -o '"[^"]*":' "$OUTPUT_DIR/structured_data.json" | sed 's/"//g' | sed 's/://g'
        echo ""
    fi
    
    echo ""
    echo "💡 Для детального изучения используйте:"
    echo "   cat $OUTPUT_DIR/<имя_файла>.txt"
    echo "   jq . $OUTPUT_DIR/structured_data.json"
else
    echo "❌ Директория с результатами не создана"
fi