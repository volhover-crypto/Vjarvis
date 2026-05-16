# Извлечение таблиц

После загрузки страницы часто требуется извлечь табличные данные для дальнейшего анализа.

## Подходы к извлечению таблиц

### 1. Извлечение через innerText/innerHTML

Простейший способ - получить содержимое таблицы как текст:

```javascript
const tableText = await page.evaluate(() => {
  const table = document.querySelector('table.data-table');
  return table ? table.innerText : '';
});
```

### 2. Преобразование в массив объектов

Более структурированный подход - преобразовать таблицу в массив объектов:

```javascript
const tableData = await page.evaluate(() => {
  const table = document.querySelector('table.data-table');
  if (!table) return [];
  
  const headers = Array.from(table.querySelectorAll('th'))
    .map(th => th.innerText.trim());
  
  const rows = Array.from(table.querySelectorAll('tbody tr'))
    .map(tr => {
      const cells = Array.from(tr.querySelectorAll('td'))
        .map(td => td.innerText.trim());
      
      const rowObject = {};
      headers.forEach((header, index) => {
        rowObject[header] = cells[index] || '';
      });
      
      return rowObject;
    });
    
  return rows;
});
```

### 3. Использование внешних библиотек

Для сложных таблиц можно использовать библиотеки вроде `tabletojson` или `xlsx`:

```javascript
// Пример с tabletojson (нужно предварительно добавить на страницу)
await page.addScriptTag({url: 'https://cdn.jsdelivr.net/npm/tabletojson'});
const tableJson = await page.evaluate(() => {
  return Tabletojson.convert(document.querySelector('table'));
});
```

### 4. Извлечение с сохранением форматирования

Для сохранения структуры таблицы можно извлечь HTML и преобразовать его позже:

```javascript
const tableHtml = await page.evaluate(() => {
  const table = document.querySelector('table.data-table');
  return table ? table.outerHTML : '';
});
```

## Обработка специальных случаев

### Пагинация

Для таблиц с пагинацией нужно пройтись по всем страницам:

```javascript
let allData = [];
let hasNextPage = true;

while (hasNextPage) {
  // Извлекаем данные текущей страницы
  const pageData = await extractTableData();
  allData = [...allData, ...pageData];
  
  // Проверяем наличие следующей страницы
  hasNextPage = await page.evaluate(() => {
    const nextButton = document.querySelector('.pagination .next:not(.disabled)');
    return !!nextButton;
  });
  
  if (hasNextPage) {
    await page.click('.pagination .next');
    await page.waitForLoadState('networkidle');
  }
}
```

### Динамическая высота строк

Таблицы с изменяемой высотой строк (разворачиваемые детали):

```javascript
const tableData = await page.evaluate(() => {
  const rows = [];
  const tableRows = document.querySelectorAll('table tr');
  
  tableRows.forEach((tr, index) => {
    // Проверяем, является ли строка основной или детальной
    const isDetail = tr.classList.contains('detail-row');
    
    if (!isDetail) {
      const cells = Array.from(tr.querySelectorAll('td'))
        .map(td => td.innerText.trim());
      rows.push(cells);
    }
    // Детальные строки можно объединить с предыдущей или обработать отдельно
  });
  
  return rows;
});
```

### Скрытые столбцы

Некоторые таблицы имеют скрытые столбцы (через CSS `display: none` или `width: 0`):

```javascript
const visibleColumns = await page.evaluate(() => {
  const headerRow = document.querySelector('table thead tr');
  const headers = Array.from(headerRow.querySelectorAll('th'))
    .filter(th => {
      const computedStyle = window.getComputedStyle(th);
      return computedStyle.display !== 'none' && 
             computedStyle.width !== '0px' &&
             !th.hidden;
    })
    .map(th => th.innerText.trim());
  
  return visibleColumns;
});
```

## Преобразование в markdown

Извлеченные табличные данные можно преобразовать в markdown таблицу:

```javascript
function toMarkdownTable(headers, rows) {
  if (!headers.length) return '';
  
  // Заголовок
  const headerRow = `| ${headers.join(' | ')} |`;
  
  // Разделитель
  const separatorRow = `| ${headers.map(() => '---').join(' | ')} |`;
  
  // Тело таблицы
  const dataRows = rows.map(row => {
    // Обеспечиваем одинаковое количество ячеек
    const paddedRow = row.slice(0, headers.length);
    while (paddedRow.length < headers.length) {
      paddedRow.push('');
    }
    return `| ${paddedRow.map(cell => 
      String(cell || '').replace(/[\n|]/g, ' ') // Экранируем спецсимволы
    ).join(' | ')} |`;
  });
  
  return [headerRow, separatorRow, ...dataRows].join('\n');
}
```

## Лучшие практики

1. **Проверяйте существование элемента** перед попыткой извлечения
2. **Обрабатывайте пустые таблицы** gracefully
3. **Учитывайте локализацию** при работе с числами и датами
4. **Очищайте данные** от лишних пробелов и спецсимволов
5. **Проверяйте типы данных** если планируете дальнейшую обработку
6. **Используйте ожидание** перед извлечением если таблица загружается динамически