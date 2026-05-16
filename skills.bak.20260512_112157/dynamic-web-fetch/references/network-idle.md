# Ожидание сетевого бездействия

Ожидание сетевого бездействия полезно когда страница продолжает делать AJAX-запросы после начальной загрузки DOM.

## Использование

Playwright предоставляет несколько методов ожидания сетевой активности:

### waitForLoadState

Ожидание различных состояний загрузки страницы:

```javascript
// Ожидание события DOMContentLoaded
await page.waitForLoadState('domcontentloaded');

// Ожидание события load (все ресурсы загружены)
await page.waitForLoadState('load');

// Ожидание отсутствия сетевой активности минимум 500мс
await page.waitForLoadState('networkidle');
```

### Параметры networkidle

Состояние `networkidle` имеет два варианта:

- `networkidle`: считается бездействием, когда нет больше сетевых соединений минимум 500мс
- `networkidle`: можно указать количество активных соединений (0 по умолчанию)

### waitForResponse / waitForRequest

Для более точного контроля можно ждать конкретных запросов/ответов:

```javascript
// Ожидание конкретного API ответа
const response = await page.waitForResponse(
  response => response.url().includes('/api/data') && response.status() === 200
);

// Ожидание окончания серии запросов
await Promise.all([
  page.waitForResponse(r => r.url().includes('/api/chunk')),
  page.waitForResponse(r => r.url().includes('/api/metadata'))
]);
```

### Комбинированные стратегии

Для сложных страниц часто комбинируют ожидание DOM и сети:

```javascript
// Ждем когда DOM готов и нет сетевой активности
await Promise.all([
  page.waitForLoadState('domcontentloaded'),
  page.waitForLoadState('networkidle')
]);

// Или ждем появления элемента после загрузки данных
await page.waitForLoadState('networkidle');
await page.waitForSelector('.data-loaded', { state: 'visible' });
```

### Таймауты и обработка ошибок

Все методы ожидания поддерживают параметр timeout:

```javascript
try {
  await page.waitForLoadState('networkidle', { timeout: 10000 });
} catch (error) {
  // Таймаут - сеть все еще активна
  console.warn('Сеть не успокоилась за отведённое время');
}
```

### Когда использовать networkidle

- Страницы с бесконечной прокруткой и подгрузкой данных
- SPA приложения с роутингом и ленивой загрузкой
- Дашборды с периодическими обновлениями данных
- Страницы с множеством внешних ресурсов (аналитика, реклама, виджеты)