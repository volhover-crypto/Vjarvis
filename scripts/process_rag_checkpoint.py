#!/usr/bin/env python3
"""
Продолжение обработки RAG с чекпоинтами.
Этот скрипт работает с уже скачанными файлами и:
1. Конвертирует оставшиеся файлы в HTML
2. Загружает все HTML на Google Drive
3. Создаёт RAG-индекс
"""

import os
import sys
import json
import io
import re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

WORKSPACE = Path.home() / '.openclaw' / 'workspace'
TEMP_DIR = WORKSPACE / 'temp_rag_processing'
HTML_OUTPUT_DIR = TEMP_DIR / 'html'
RAG_OUTPUT_DIR = WORKSPACE / 'self-improving' / 'projects' / 'rag-indexed'
ISTOHNIKI_FOLDER_ID = '1n9gjvZk5YNQC5_JhgJDifqOp4sUvywac'
HTML_FOLDER_ID = '1jp1BGCifzlqkTpEZk3iS7L7elFAhmVog'

TOPICS = {
    'agro-meteo': ['агро', 'метео', 'метеорология', 'погода', 'климат', 'температура', 'осадки', 'ветер', 'черков', 'chirkov', 'агроклимат', 'гидротерм'],
    'viticulture': ['виноград', 'виноградарств', 'винодели', 'энолог', 'ягод', 'лоз', 'сорт', 'аксенов', 'энциклопед'],
    'infrastructure': ['сервер', 'код', 'скрипт', 'bash', 'python', 'docker', 'api', 'it ', 'инфраструктур'],
    'economics': ['эконом', 'финанс', 'бюджет', 'доход', 'расход', 'инвестиц', 'акчурин'],
    'education': ['учебник', 'энциклопед', 'книга', 'теория', 'образован', 'аксенова'],
    'datasets': ['данные', 'dataset', 'csv', 'excel', 'таблиц', 'лист', 'baza', 'локация', 'пост', 'метеотчет'],
    'geology': ['геолог', 'геология', 'минерал', 'пород', 'грунт', 'почв'],
    'biology': ['биолог', 'биология', 'растен', 'животн', 'эколог'],
    'other': []
}

def get_drive_service():
    with open(WORKSPACE / 'google-oauth.json') as f:
        creds_data = json.load(f)
    creds = Credentials(
        token=None,
        refresh_token=creds_data['refresh_token'],
        client_id=creds_data['client_id'],
        client_secret=creds_data['client_secret'],
        token_uri=creds_data['token_uri']
    )
    return build('drive', 'v3', credentials=creds)

def convert_existing_files_to_html():
    """Конвертирует уже скачанные файлы в HTML"""
    print("\n🔄 Конвертация скачанных файлов в HTML...")
    
    converted = 0
    skipped = 0
    
    # Обходим все скачанные файлы
    for file_path in TEMP_DIR.rglob('*'):
        if not file_path.is_file():
            continue
        
        # Пропускаем уже сконвертированные HTML
        if file_path.suffix.lower() == '.html':
            continue
        
        # Пропускаем бинарные файлы OCR
        if file_path.suffix.lower() in ['.frdat', '.bin', '.dat', '.hdr', '.ico', '.pac', '.xml', '.cache']:
            continue
        
        # Определяем выходной HTML файл
        html_name = file_path.stem + '.html'
        html_path = HTML_OUTPUT_DIR / html_name
        
        # Если HTML уже существует, пропускаем
        if html_path.exists():
            continue
        
        print(f"  Конвертация: {file_path.name}...")
        
        try:
            ext = file_path.suffix.lower()
            
            # CSV/TXT
            if ext in ['.csv', '.txt']:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{file_path.name}</title></head>
<body><pre>{content[:50000]}</pre></body></html>"""
                with open(html_path, 'w') as f:
                    f.write(html_content)
                converted += 1
            
            # DOCX
            elif ext == '.docx':
                try:
                    import docx2txt
                    text = docx2txt.process(str(file_path))
                    html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{file_path.name}</title></head>
<body><div>{text[:50000]}</div></body></html>"""
                    with open(html_path, 'w') as f:
                        f.write(html_content)
                    converted += 1
                except Exception as e:
                    print(f"    ⚠️ Ошибка DOCX: {e}")
                    skipped += 1
            
            # PDF
            elif ext == '.pdf':
                try:
                    import pdfplumber
                    text = ""
                    with pdfplumber.open(str(file_path)) as pdf:
                        for page in pdf.pages[:50]:  # Ограничиваем 50 страницами
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                    
                    html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{file_path.name}</title></head>
<body><div>{text[:100000]}</div></body></html>"""
                    with open(html_path, 'w') as f:
                        f.write(html_content)
                    converted += 1
                except Exception as e:
                    print(f"    ⚠️ Ошибка PDF: {e}")
                    skipped += 1
            
            # XLSX
            elif ext == '.xlsx':
                try:
                    import pandas as pd
                    excel_file = pd.ExcelFile(file_path)
                    html_tables = ""
                    for sheet_name in excel_file.sheet_names[:5]:  # Макс 5 листов
                        df = pd.read_excel(excel_file, sheet_name=sheet_name, nrows=1000)
                        html_tables += f"<h2>{sheet_name}</h2>\n{df.to_html()}\n"
                    
                    html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{file_path.name}</title></head>
<body>{html_tables}</body></html>"""
                    with open(html_path, 'w') as f:
                        f.write(html_content)
                    converted += 1
                except Exception as e:
                    print(f"    ⚠️ Ошибка XLSX: {e}")
                    skipped += 1
            
            else:
                skipped += 1
        
        except Exception as e:
            print(f"    ❌ Ошибка: {e}")
            skipped += 1
    
    print(f"  ✅ Конвертировано: {converted}, Пропущено: {skipped}")
    return converted

def upload_html_files_to_drive():
    """Загружает все HTML файлы на Google Drive"""
    print("\n⬆️  Загрузка HTML файлов на Google Drive...")
    
    drive = get_drive_service()
    uploaded = 0
    
    html_files = list(HTML_OUTPUT_DIR.glob('*.html'))
    print(f"  Найдено HTML файлов: {len(html_files)}")
    
    for html_path in html_files:
        try:
            file_metadata = {
                'name': html_path.name,
                'parents': [HTML_FOLDER_ID]
            }
            media = MediaFileUpload(str(html_path), resumable=True)
            drive.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            uploaded += 1
            if uploaded % 10 == 0:
                print(f"  Загружено: {uploaded}/{len(html_files)}")
        except Exception as e:
            print(f"  ⚠️ Ошибка загрузки {html_path.name}: {e}")
    
    print(f"  ✅ Загружено файлов: {uploaded}")
    return uploaded

def classify_topic(file_name):
    """Классификация файла по тематике"""
    text = file_name.lower()
    
    scores = {}
    for topic, keywords in TOPICS.items():
        if topic == 'other':
            continue
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[topic] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return 'other'

def create_rag_index():
    """Создаёт RAG-индекс с сортировкой по темам"""
    print("\n📚 Создание RAG-индекса...")
    
    RAG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    rag_by_topic = {}
    total_files = 0
    
    html_files = list(HTML_OUTPUT_DIR.glob('*.html'))
    
    for html_path in html_files:
        try:
            # Читаем HTML
            with open(html_path, 'r', errors='ignore') as f:
                html_content = f.read()
            
            # Извлекаем текст
            text = re.sub('<[^<]+?>', '', html_content)
            text = text.strip()[:10000]  # Ограничиваем размер
            
            if not text:
                continue
            
            # Классифицируем
            topic = classify_topic(html_path.stem)
            
            if topic not in rag_by_topic:
                rag_by_topic[topic] = []
            
            # Создаем метаданные
            metadata = {
                'source_file': html_path.stem,
                'topic': topic,
                'processed_date': '2026-04-05',
                'word_count': len(text.split())
            }
            
            # Создаем RAG-документ
            safe_name = re.sub(r'[^\w\s-]', '', html_path.stem)[:100]
            rag_content = f"""---
# RAG Knowledge Base Entry
```json
{json.dumps(metadata, indent=2, ensure_ascii=False)}
```
---

# {html_path.stem}

**Тематика:** {topic}  
**Слов:** {metadata['word_count']}

---

## Содержание

{text}
"""
            
            # Сохраняем
            topic_dir = RAG_OUTPUT_DIR / topic
            topic_dir.mkdir(parents=True, exist_ok=True)
            
            rag_file = topic_dir / f"{safe_name}.md"
            with open(rag_file, 'w', encoding='utf-8') as f:
                f.write(rag_content)
            
            rag_by_topic[topic].append(html_path.stem)
            total_files += 1
        
        except Exception as e:
            print(f"  ⚠️ Ошибка RAG для {html_path.name}: {e}")
    
    # Создаем оглавление
    index_file = RAG_OUTPUT_DIR / 'INDEX.md'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# 📚 RAG Knowledge Base - Индекс\n\n")
        f.write(f"**Дата обработки:** 2026-04-05\n")
        f.write(f"**Источник:** Google Drive / istohniki\n")
        f.write(f"**Всего файлов:** {total_files}\n\n")
        f.write("---\n\n")
        
        for topic, files in sorted(rag_by_topic.items()):
            f.write(f"## {topic.upper()} ({len(files)} файлов)\n\n")
            for fname in files[:20]:  # Показываем первые 20
                f.write(f"- {fname}\n")
            if len(files) > 20:
                f.write(f"- ... и ещё {len(files) - 20}\n")
            f.write("\n")
    
    print(f"  ✅ Создано RAG-записей: {total_files}")
    print(f"  📂 Тем: {len(rag_by_topic)} ({', '.join(sorted(rag_by_topic.keys()))})")
    print(f"  📄 Индекс: {index_file}")
    
    return total_files

def main():
    print("=" * 80)
    print("🚀 Продолжение обработки RAG (с чекпоинтами)")
    print("=" * 80)
    
    # Шаг 1: Конвертация оставшихся файлов
    convert_existing_files_to_html()
    
    # Шаг 2: Загрузка HTML на Drive
    upload_html_files_to_drive()
    
    # Шаг 3: Создание RAG-индекса
    create_rag_index()
    
    print("\n" + "=" * 80)
    print("✅ ЗАВЕРШЕНО!")
    print("=" * 80)

if __name__ == '__main__':
    main()
