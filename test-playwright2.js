const playwright = require('playwright-core');

(async () => {
    console.log('Запускаем браузер...');
    const browser = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    console.log('Браузер запущен успешно!');
    
    const context = await browser.newContext();
    const page = await context.newPage();
    
    console.log('Переходим на целевой сайт...');
    await page.goto('https://zolotayabalka.ru/company/sort/');
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    console.log(`Заголовок целевого сайта: ${title}`);
    
    // Давайте сначала посмотрим, что вообще есть на странице
    const pageContent = await page.evaluate(() => document.body.innerText);
    console.log(`Длина содержимого страницы: ${pageContent.length} символов`);
    console.log(`Первые 500 символов:\n${pageContent.substring(0, 500)}`);
    
    // Попробуем найти элементы с классом, содержащим "sort"
    const sortElements = await page.evaluate(() => {
        const elements = Array.from(document.querySelectorAll('*'));
        const matches = elements.filter(el => 
            el.className && el.className.includes('sort')
        );
        return matches.map(el => ({
            tagName: el.tagName,
            className: el.className,
            textContent: el.textContent.substring(0, 100)
        }));
    });
    console.log(`Найдено элементов с 'sort' в классе: ${sortElements.length}`);
    if (sortElements.length > 0) {
        console.log('Первые несколько совпадений:');
        sortElements.slice(0, 5).forEach((el, i) => {
            console.log(`  ${i+1}. ${el.tagName}.${el.className}: "${el.textContent}"`);
        });
    }
    
    // Попробуем подождать появления контента с более специфичным селектором
    console.log('Пытаемся найти контент сортов...');
    try {
        // Ждем появления любого элемента, который может содержать сорта
        await page.waitForSelector('text=/Сорт/i', { timeout: 10000 });
        console.log('Найден элемент с текстом содержащим "Сорт"');
        
        // Попробуем получить все текстовое содержимое после этой точки
        const sortContent = await page.evaluate(() => {
            // Ищем все элементы, содержащие слово "Сорт" в тексте
            const elements = Array.from(document.querySelectorAll('*'))
                .filter(el => el.textContent && el.textContent.includes('Сорт'));
            
            // Объединяем их текстовое содержимое
            return elements.map(el => el.textContent.trim()).filter(text => text.length > 10).join('\n\n');
        });
        
        console.log(`Содержимое, связанное с сортами:\n${sortContent}`);
    } catch (err) {
        console.log('Не удалось найти элемент с текстом "Сорт"');
        
        // Попробуем просто получить всё содержимое тела страницы
        const fullContent = await page.evaluate(() => document.body.innerText);
        console.log(`Полное содержимое страницы (первые 2000 символов):\n${fullContent.substring(0, 2000)}`);
    }
    
    await browser.close();
})().catch(err => {
    console.error('Ошибка:', err);
    process.exit(1);
});