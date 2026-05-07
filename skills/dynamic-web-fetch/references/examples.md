# Примеры использования

Практические примеры применения навыка dynamic-web-fetch для различных сценариев.

## Пример 1: Извлечение списка продуктов с интернет-магазина

**Задача:** Получить список продуктов с их ценами из каталога, который загружается через AJAX.

```javascript
// Ожидаем загрузки каталога продуктов
await page.waitForSelector('.products-grid', { state: 'visible' });

// Прокручиваем страницу чтобы загрузить все продукты (если используется бесконечная прокрутка)
let lastHeight = await page.evaluate('document.body.scrollHeight');
while (true) {
  await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
  await page.waitForTimeout(2000); // Ждем загрузки
  
  const newHeight = await page.evaluate('document.body.scrollHeight');
  if (newHeight === lastHeight) break;
  lastHeight = newHeight;
}

// Извлекаем данные продуктов
const products = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.product-card')).map(card => {
    return {
      name: card.querySelector('.product-name')?.innerText.trim() || '',
      price: card.querySelector('.price')?.innerText.trim() || '',
      rating: card.querySelector('.rating')?.innerText.trim() || ''
    };
  });
});

// Преобразуем в markdown таблицу
const markdownTable = `
| Название | Цена | Рейтинг |
|----------|------|---------|
${products.map(p => `| ${p.name} | ${p.price} | ${p.rating} |`).join('\n')}
`;
```

## Пример 2: Извлечение финансовых данных с дашборда

**Задача:** Получить текущие показатели KPI с корпоративного дашборда, требующего авторизации и динамической загрузки графиков.

```javascript
// После авторизации (предполагается, что уже выполнено)
await page.waitForLoadState('networkidle');

// Ожидаем появления виджетов с данными
await page.waitForSelector('.kpi-widget', { state: 'attached' });

// Извлекаем значения KPI
const kpiData = await page.evaluate(() => {
  const widgets = {};
  
  document.querySelectorAll('.kpi-widget').forEach(widget => {
    const title = widget.querySelector('.kpi-title')?.innerText.trim() || 'Unknown';
    const value = widget.querySelector('.kpi-value')?.innerText.trim() || 'N/A';
    const change = widget.querySelector('.kpi-change')?.innerText.trim() || '0%';
    
    widgets[title] = {
      value: value,
      change: change,
      timestamp: new Date().toISOString()
    };
  });
  
  return widgets;
});

// Форматируем вывод
const formattedOutput = Object.entries(kpiData).map(([title, data]) => 
  `${title}: ${data.value} (${data.change})`
).join('\n');
```

## Пример 3: Извлечение таблицы результатов поиска

**Задача:** Получить результаты поиска с сайта вакансий, где результаты загружаются порциями.

```javascript
// Вводим поисковый запрос
await page.fill('#search-input', 'Python разработчик');
await page.click('#search-button');

// Ожидаем загрузки первых результатов
await page.waitForSelector('.job-results-table', { state: 'visible' });

// Собираем результаты со всех страниц
let allJobs = [];
let currentPage = 1;
const maxPages = 5; // Ограничиваем для примера

while (currentPage <= maxPages) {
  // Извлекаем текущую страницу результатов
  const pageJobs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.job-results-table tbody tr')).map(row => {
      const cells = Array.from(row.querySelectorAll('td'));
      return {
        title: cells[0]?.innerText.trim() || '',
        company: cells[1]?.innerText.trim() || '',
        location: cells[2]?.innerText.trim() || '',
        salary: cells[3]?.innerText.trim() || '',
        posted: cells[4]?.innerText.trim() || ''
      };
    });
  });
  
  allJobs = [...allJobs, ...pageJobs];
  
  // Проверяем наличие следующей страницы
  const hasNextPage = await page.evaluate(() => {
    const nextBtn = document.querySelector('.pagination .next:not(.disabled)');
    return !!nextBtn;
  });
  
  if (!hasNextPage) break;
  
  // Переходим к следующей странице
  await page.click('.pagination .next');
  await page.waitForLoadState('networkidle');
  currentPage++;
}

// Формируем markdown отчет
 خسضع```markdown
# Результаты поиска вакансий
**Запрос:** Python разработчик  
**Найдено вакансий:** ${allJobs.length}  
**Дата:** ${new Date().toLocaleDateString()}

| Должность | Компания | Местоположение | Зарплата | Дата публикации |
|-----------|----------|----------------|----------|-----------------|
${allJobs.map(job => 
  `| ${job.title} | ${job.company} | ${job.location} | ${job.salary} | ${job.posted} |`
).join('\n')}
```
```

## Пример 4: Извлечение данных с интерактивного графика

**Задача:** Получить данные точки на интерактивном графике после наведения курсора.

```javascript
// Переходим к странице с графиком
await page.goto('https://example.com/analytics-chart');

// Ожидаем загрузки графика
await page.waitForSelector('#chart-container', { state: 'attached' });

// Наводим курсор на конкретную точку графика
await page.hover('.chart-point[data-date="2026-04-15"]');

// Ожидаем появления тултипа с данными
await page.waitForSelector('.chart-tooltip', { state: 'visible' });

// Извлекаем данные из тултипа
const tooltipData = await page.evaluate(() => {
  const tooltip = document.querySelector('.chart-tooltip');
  if (!tooltip) return null;
  
  const dateEl = tooltip.querySelector('.date');
  const valueEl = tooltip.querySelector('.value');
  const changeEl = tooltip.querySelector('.change');
  
  return {
    date: dateEl?.innerText.trim() || '',
    value: valueEl?.innerText.trim() || '',
    change: changeEl?.innerText.trim() || ''
  };
});

// Формируем результат
const result = tooltipData ? 
  `Дата: ${tooltipData.date}, Значение: ${tooltipData.value}, Изменение: ${tooltipData.change}` :
  'Не удалось получить данные графика';
```

## Пример 5: Работа с теневым DOM и iframe

**Задача:** Извлечь данные из компонента, расположенного внутри shadow DOM или iframe.

```javascript
// Для shadow DOM
const shadowData = await page.evaluate(() => {
  const host = document.querySelector('.custom-element');
  if (!host || !host.shadowRoot) return null;
  
  const dataElement = host.shadowRoot.querySelector('.data-display');
  return dataElement ? dataElement.innerText.trim() : null;
});

// Для iframe
const iframeData = await page.evaluate(() => {
  const iframe = document.querySelector('#data-frame');
  if (!iframe || !iframe.contentDocument) return null;
  
  const dataElement = iframe.contentDocument.querySelector('.stats-number');
  return dataElement ? dataElement.innerText.trim() : null;
});

// Обрабатываем результаты
const finalData = shadowData || iframeData || 'Данные не найдены';
```

## Лучшие практики из примеров

1. **Всегда проверяйте наличие элементов** перед взаимодействием с ними
2. **Используйте ожидания** соответствующие типу контента (DOM vs сеть)
3. **Ограничивайте количество запросов/страниц** чтобы избежать бесконечных циклов
4. **Очищайте и валидируйте извлеченные данные**
5. **Обрабатывайте edge cases** - пустые результаты, измененная структура страницы
6. **Добавляйте метаданные** - время извлечения, URL источника, параметры запроса