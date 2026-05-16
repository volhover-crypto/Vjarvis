#!/usr/bin/env python3
"""
Dynamic Web Fetch Script
Извлекает содержимое с динамических веб-страниц используя Playwright через Node.js
"""

import asyncio
import json
import sys
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional


def fetch_dynamic_content_nodejs(
    url: str,
    wait_for: Optional[str] = None,
    wait_timeout: int = 30000,
    extract_mode: str = "text",
    selector_type: str = "css",
    custom_script: Optional[str] = None
) -> Dict[str, Any]:
    """
    Извлекает содержимое с динамической веб-страницы используя Node.js Playwright
    
    Args:
        url: URL страницы для загрузки
        wait_for: Селектор или условие для ожидания (CSS селектор, XPath или 'networkidle')
        wait_timeout: Таймаут ожидания в миллисекундах
        extract_mode: Режим извлечения ('text', 'markdown', 'html')
        selector_type: Тип селектора ('css' или 'xpath')
        custom_script: Пользовательский JavaScript для выполнения после загрузки
        
    Returns:
        Словарь с результатом извлечения и метаданными
    """
    result = {
        "success": False,
        "url": url,
        "content": None,
        "extract_mode": extract_mode,
        "error": None,
        "metadata": {}
    }
    
    # Создаем временный файл для Node.js скрипта
    node_script = '''
const playwright = require('playwright-core');

async function fetchContent() {
    const browser = await playwright.chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    });
    
    const page = await context.newPage();
    page.setDefaultTimeout(waitTimeout);
    
    try {
        const response = await page.goto(process.argv[2], { waitUntil: 'commit' });
        if (!response || !response.ok()) {
            throw new Error(`HTTP ${response ? response.status() : 'Unknown'}: Failed to load page`);
        }
        
        // Ожидание условия загрузки
        const waitForArg = process.argv[3];
        const selectorTypeArg = process.argv[4];
        if (waitForArg !== null && waitForArg !== '' && waitForArg !== 'null') {
            if (waitForArg === 'networkidle') {
                await page.waitForLoadState('networkidle');
            } else if (selectorTypeArg === 'xpath') {
                await page.waitForSelector(waitForArg, { state: 'attached' });
            } else {
                await page.waitForSelector(waitForArg, { state: 'attached' });
            }
        }
        
        // Выполняем пользовательский скрипт если предоставлен
        const customScriptArg = process.argv[5];
        if (customScriptArg !== null && customScriptArg !== '' && customScriptArg !== 'null') {
            await page.evaluate(customScriptArg);
            await page.waitForTimeout(1000);
        }
        
        // Извлекаем содержимое
        const extractModeArg = process.argv[6];
        let content;
        if (extractModeArg === 'html') {
            content = await page.content();
        } else if (extractModeArg === 'markdown') {
            // Для markdown преобразования потребуется дополнительная библиотека
            // Пока возвращаем HTML и будем преобразовывать в Python
            content = await page.content();
        } else {
            content = await page.evaluate(() => document.body.innerText);
        }
        
        const title = await page.title();
        
        await browser.close();
        
        return {
            success: true,
            content: content,
            title: title,
            url: page.url()
        };
    } catch (error) {
        await browser.close();
        throw error;
    }
}

// Parse command line arguments
const url = process.argv[2];
const waitFor = process.argv[3] === 'null' ? null : process.argv[3];
const selectorType = process.argv[4] === 'null' ? 'css' : process.argv[4];
const customScript = process.argv[5] === 'null' ? null : process.argv[5];
const extractMode = process.argv[6] === 'null' ? 'text' : process.argv[6];

fetchContent()
    .then(result => {
        console.log(JSON.stringify(result));
    })
    .catch(error => {
        console.error(JSON.stringify({ success: false, error: error.message }));
        process.exit(1);
    });
'''
    
    try:
        # Запускаем Node.js скрипт с аргументами
        env = os.environ.copy()
        # Добавляем путь к установленному playwright-core
        env['NODE_PATH'] = '/usr/lib/node_modules/openclaw/node_modules'
        # Пытаемся использовать системные браузеры, отключая загрузку
        env['PLAYWRIGHT_BROWSERS_PATH'] = '0'  # Это может помочь использовать системную установку
        
        # Подготавливаем аргументы
        wait_for_arg = wait_for if wait_for else 'null'
        selector_type_arg = selector_type if selector_type else 'css'
        custom_script_arg = custom_script if custom_script else 'null'
        extract_mode_arg = extract_mode if extract_mode else 'text'
        
        result_process = subprocess.run(
            ['node', '-e', node_script, url, wait_for_arg, selector_type_arg, custom_script_arg, extract_mode_arg],
            capture_output=True,
            text=True,
            timeout=wait_timeout / 1000 + 30,  # Добавляем буфер к таймауту
            env=env
        )
        
        if result_process.returncode != 0:
            # Пытаемся распарсить ошибку как JSON
            try:
                error_data = json.loads(result_process.stderr.strip())
                result["error"] = error_data.get("error", result_process.stderr.strip())
            except json.JSONDecodeError:
                result["error"] = result_process.stderr.strip() or "Неизвестная ошибка Node.js скрипта"
            result["success"] = False
            return result
        
        # Парсим успешный результат
        try:
            node_result = json.loads(result_process.stdout.strip())
            result["success"] = True
            result["content"] = node_result.get("content")
            result["metadata"]["title"] = node_result.get("title", "")
            result["metadata"]["final_url"] = node_result.get("url", url)
            result["metadata"]["status_code"] = 200  # Предполагаем успех если получили содержимое
            
            # Если нужно преобразовать в markdown и мы получили HTML
            if extract_mode == "markdown" and result["content"]:
                # Простое преобразование HTML в текст для примера
                # В реальном сценарии здесь должна быть правильная библиотека
                import re
                # Удаляем скрипты и стили
                clean_html = re.sub(r'<script[^>]*>.*?</script>', '', result["content"], flags=re.DOTALL | re.IGNORECASE)
                clean_html = re.sub(r'<style[^>]*>.*?</style>', '', result["content"], flags=re.DOTALL | re.IGNORECASE)
                # Удаляем все HTML теги
                text_content = re.sub(r'<[^>]+>', '', clean_html)
                # Очищаем лишние пробелы
                text_content = re.sub(r'\\s+', ' ', text_content).strip()
                result["content"] = text_content
            
            result["metadata"]["content_length"] = len(result["content"]) if result["content"] else 0
            
        except json.JSONDecodeError as e:
            result["error"] = f"Не удалось распарсить вывод Node.js: {str(e)}"
            result["success"] = False
            
    except subprocess.TimeoutExpired:
        result["error"] = f"Превышен таймаут ожидания ({wait_timeout}мс)"
        result["success"] = False
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
    
    return result


def main():
    """Основная функция для запуска из командной строки"""
    if len(sys.argv) < 2:
        print("Usage: python fetch-dynamic-content.py <URL> [options]")
        print("Options:")
        print("  --wait-for <selector>   Селектор для ожидания (CSS или 'networkidle')")
        print("  --wait-timeout <ms>     Таймаут ожидания (по умолчанию 30000)")
        print("  --extract-mode <mode>   Режим извлечения: text, markdown, html (по умолчанию text)")
        print("  --selector-type <type>  Тип селектора: css или xpath (по умолчанию css)")
        print("  --custom-script <js>    Пользовательский JavaScript для выполнения")
        print("  --output-format <fmt>   Формат вывода: json или plain (по умолчанию json)")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Парсим аргументы командной строки
    wait_for = None
    wait_timeout = 30000
    extract_mode = "text"
    selector_type = "css"
    custom_script = None
    output_format = "json"
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--wait-for" and i + 1 < len(sys.argv):
            wait_for = sys.argv[i + 1]
            i += 2
        elif arg == "--wait-timeout" and i + 1 < len(sys.argv):
            try:
                wait_timeout = int(sys.argv[i + 1])
            except ValueError:
                print(f"Ошибка: wait-timeout должен быть числом, получено: {sys.argv[i + 1]}")
                sys.exit(1)
            i += 2
        elif arg == "--extract-mode" and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1].lower()
            if mode in ["text", "markdown", "html"]:
                extract_mode = mode
            else:
                print(f"Ошибка: extract-mode должен быть text, markdown или html, получено: {mode}")
                sys.exit(1)
            i += 2
        elif arg == "--selector-type" and i + 1 < len(sys.argv):
            stype = sys.argv[i + 1].lower()
            if stype in ["css", "xpath"]:
                selector_type = stype
            else:
                print(f"Ошибка: selector-type должен быть css или xpath, получено: {stype}")
                sys.exit(1)
            i += 2
        elif arg == "--custom-script" and i + 1 < len(sys.argv):
            custom_script = sys.argv[i + 1]
            i += 2
        elif arg == "--output-format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1].lower()
            if fmt in ["json", "plain"]:
                output_format = fmt
            else:
                print(f"Ошибка: output-format должен быть json или plain, получено: {fmt}")
                sys.exit(1)
            i += 2
        else:
            print(f"Неизвестный аргумент: {arg}")
            sys.exit(1)
    
    # Выполняем функцию
    result = fetch_dynamic_content_nodejs(
        url=url,
        wait_for=wait_for,
        wait_timeout=wait_timeout,
        extract_mode=extract_mode,
        selector_type=selector_type,
        custom_script=custom_script
    )
    
    # Выводим результат
    if output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:  # plain format
        if result["success"]:
            print(result["content"] or "")
        else:
            print(f"Ошибка: {result['error']}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()