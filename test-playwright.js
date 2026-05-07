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
    
    console.log('Переходим на тестовую страницу...');
    await page.goto('https://httpbin.org/html');
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    console.log(`Заголовок страницы: ${title}`);
    
    const content = await page.evaluate(() => document.body.innerText);
    console.log(`Получено ${content.length} символов текста`);
    
    await browser.close();
    console.log('Тест httpbin.org завершен успешно');
    
    // Тестируем целевой сайт
    console.log('Переходим на целевой сайт...');
    const browser2 = await playwright.chromium.launch({ 
        headless: true,
        executablePath: '/root/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'
    });
    const context2 = await browser2.newContext();
    const page2 = await context2.newPage();
    await page2.goto('https://zolotayabalka.ru/company/sort/');
    await page2.waitForLoadState('networkidle');
    await page2.waitForTimeout(5000);
    
    const title2 = await page2.title();
    console.log(`Заголовок целевого сайта: ${title2}`);
    
    const content2 = await page2.evaluate(() => {
        const element = document.querySelector('.sorts-list');
        return element ? element.innerText : 'Селектор .sorts-list не найден';
    });
    console.log(`Содержание селектора .sorts-list:\n${content2}`);
    
    await browser2.close();
})().catch(err => {
    console.error('Ошибка:', err);
    process.exit(1);
});