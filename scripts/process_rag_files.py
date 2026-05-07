#!/usr/bin/env python3
"""
Скрипт для обработки файлов из папки istohniki на Google Drive:
1. Скачивает все файлы
2. Конвертирует в HTML
3. Загружает HTML обратно в папку HTML
4. Перерабатывает в RAG-формат с сортировкой по тематике
"""

import os
import sys
import json
import io
import subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# Пути
WORKSPACE = Path.home() / '.openclaw' / 'workspace'
TEMP_DIR = WORKSPACE / 'temp_rag_processing'
HTML_OUTPUT_DIR = TEMP_DIR / 'html'
RAG_OUTPUT_DIR = WORKSPACE / 'self-improving' / 'projects' / 'rag-indexed'

# Google Drive IDs
ISTOHNIKI_FOLDER_ID = '1n9gjvZk5YNQC5_JhgJDifqOp4sUvywac'
HTML_FOLDER_ID = '1jp1BGCifzlqkTpEZk3iS7L7elFAhmVog'

# Темы для классификации
TOPICS = {
    'agro-meteo': ['агро', 'метео', 'метеорология', 'погода', 'климат', 'температура', 'осадки', 'ветер'],
    'viticulture': ['виноград', 'виноградарств', 'винодели', 'энолог', 'ягод', 'лоз', 'сорт'],
    'infrastructure': ['ит ', 'сервер', 'код', 'скрипт', 'bash', 'python', 'docker', 'api'],
    'economics': ['эконом', 'финанс', 'бюджет', 'доход', 'расход', 'инвестиц'],
    'education': ['учебник', 'энциклопед', 'книга', 'теория', 'образован'],
    'datasets': ['данные', 'dataset', 'csv', 'excel', 'таблиц', 'лист'],
    'other': []
}

def get_drive_service():
    """Инициализация сервиса Google Drive"""
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

def list_all_files(drive, folder_id, parent_path=''):
    """Рекурсивный список всех файлов"""
    files_info = []
    results = drive.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields='files(id, name, mimeType)',
        pageSize=1000
    ).execute()
    
    files = results.get('files', [])
    for f in files:
        full_path = f"{parent_path}/{f['name']}" if parent_path else f['name']
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            # Рекурсивно обходим папки
            files_info.extend(list_all_files(drive, f['id'], full_path))
        else:
            files_info.append({
                'id': f['id'],
                'name': f['name'],
                'path': full_path,
                'mimeType': f['mimeType']
            })
    
    return files_info

def download_file(drive, file_id, file_name, local_path):
    """Скачивание файла с Google Drive"""
    try:
        request = drive.files().get_media(fileId=file_id)
        fh = io.FileIO(local_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.close()
        print(f"✅ Скачан: {file_name}")
        return True
    except Exception as e:
        print(f"❌ Ошибка скачивания {file_name}: {e}")
        return False

def convert_to_html(file_path, output_path):
    """Конвертация файла в HTML"""
    try:
        ext = Path(file_path).suffix.lower()
        
        # Текстовые файлы - просто оборачиваем в HTML
        if ext in ['.txt', '.md', '.csv']:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
            html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{Path(file_path).name}</title></head>
<body><pre>{content}</pre></body>
</html>"""
            with open(output_path, 'w') as f:
                f.write(html_content)
            return True
        
        # DOCX
        elif ext == '.docx':
            try:
                import docx2txt
                text = docx2txt.process(str(file_path))
                html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{Path(file_path).name}</title></head>
<body><div>{text}</div></body>
</html>"""
                with open(output_path, 'w') as f:
                    f.write(html_content)
                return True
            except ImportError:
                print("  ⚠️ docx2txt не установлен, пропускаем DOCX")
                return False
        
        # PDF - используя PyPDF2 или pdfplumber
        elif ext == '.pdf':
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(str(file_path)) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                
                html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{Path(file_path).name}</title></head>
<body><div>{text}</div></body>
</html>"""
                with open(output_path, 'w') as f:
                    f.write(html_content)
                return True
            except ImportError:
                print("  ⚠️ pdfplumber не установлен, пропускаем PDF")
                return False
        
        # Excel (.xlsx)
        elif ext == '.xlsx':
            try:
                import pandas as pd
                excel_file = pd.ExcelFile(file_path)
                html_tables = ""
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    html_tables += f"<h2>{sheet_name}</h2>\n"
                    html_tables += df.to_html() + "\n"
                
                html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{Path(file_path).name}</title></head>
<body>{html_tables}</body>
</html>"""
                with open(output_path, 'w') as f:
                    f.write(html_content)
                return True
            except ImportError:
                print("  ⚠️ pandas не установлен, пропускаем XLSX")
                return False
        
        # Пропускаем бинарные файлы изображений и временные файлы
        elif ext in ['.frdat', '.bin', '.dat', '.hdr', '.ico', '.pac', '.xml']:
            return False
        
        else:
            print(f"  ⚠️ Неизвестный формат: {ext}")
            return False
            
    except Exception as e:
        print(f"  ❌ Ошибка конвертации {Path(file_path).name}: {e}")
        return False

def classify_topic(file_name, file_path):
    """Классификация файла по тематике"""
    text = f"{file_name} {file_path}".lower()
    
    scores = {}
    for topic, keywords in TOPICS.items():
        if topic == 'other':
            continue
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[topic] = score
    
    if scores:
        best_topic = max(scores, key=scores.get)
        return best_topic
    
    return 'other'

def create_rag_entry(file_info, html_path, topic):
    """Создание RAG-записи в формате Markdown с метаданными"""
    try:
        # Читаем HTML контент
        with open(html_path, 'r', errors='ignore') as f:
            content = f.read()
        
        # Извлекаем текст из HTML (упрощенно)
        import re
        text = re.sub('<[^<]+?>', '', content)
        text = text.strip()
        
        # Создаем метаданные
        metadata = {
            'source_file': file_info['name'],
            'source_path': file_info['path'],
            'original_mime': file_info['mimeType'],
            'topic': topic,
            'processed_date': '2026-04-05',
            'html_file': str(html_path)
        }
        
        # Создаем RAG-документ
        rag_content = f"""---
# RAG Knowledge Base Entry
{json.dumps(metadata, indent=2, ensure_ascii=False)}
---

# {file_info['name']}

**Тематика:** {topic}
**Источник:** {file_info['path']}

---

## Содержание

{text[:10000]}
"""
        
        return rag_content
    
    except Exception as e:
        print(f"  ⚠️ Ошибка создания RAG для {file_info['name']}: {e}")
        return None

def upload_to_drive(drive, file_path, parent_id, file_name):
    """Загрузка файла на Google Drive"""
    try:
        file_metadata = {
            'name': file_name,
            'parents': [parent_id]
        }
        media = MediaFileUpload(str(file_path), resumable=True)
        file = drive.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"  ✅ Загружен на Drive: {file_name}")
        return file.get('id')
    except Exception as e:
        print(f"  ❌ Ошибка загрузки {file_name}: {e}")
        return None

def should_skip_file(file_info):
    """Проверка, стоит ли пропустить файл без скачивания"""
    skip_extensions = {'.frdat', '.bin', '.dat', '.hdr', '.ico', '.pac', '.xml', '.cache'}
    skip_patterns = ['synCache', 'header.bin', 'delStyles', 'docGDS', 'CoordinatesConverter', 
                     'DocumentRegion', 'DocumentParams', 'Color.frdat', 'BW.frdat', 'Gray.frdat']
    
    file_name = file_info['name'].lower()
    ext = Path(file_name).suffix.lower()
    
    if ext in skip_extensions:
        return True
    
    if any(pattern.lower() in file_name for pattern in skip_patterns):
        return True
    
    return False

def main():
    print("=" * 80)
    print("🚀 Запуск обработки файлов RAG из папки istohniki")
    print("=" * 80)
    
    # Создаем директории
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    HTML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Инициализация Drive
    print("\n📡 Подключение к Google Drive...")
    drive = get_drive_service()
    
    # Шаг 1: Получаем список всех файлов
    print("\n📋 Сканирование файлов...")
    all_files = list_all_files(drive, ISTOHNIKI_FOLDER_ID)
    print(f"   Найдено файлов: {len(all_files)}")
    
    # Фильтруем ненужные файлы
    filtered_files = [f for f in all_files if not should_skip_file(f)]
    print(f"   После фильтрации: {len(filtered_files)} файлов для обработки")
    
    # Шаг 2: Скачиваем и конвертируем в HTML
    print("\n⬇️  Скачивание и конвертация в HTML...")
    html_files = []
    for i, file_info in enumerate(filtered_files, 1):
        print(f"\n[{i}/{len(filtered_files)}] Обработка: {file_info['name']}")
        
        # Определяем локальный путь
        local_path = TEMP_DIR / file_info['path'].replace('/', '_')
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Скачиваем
        if not download_file(drive, file_info['id'], file_info['name'], local_path):
            continue
        
        # Конвертируем в HTML
        html_name = Path(file_info['name']).stem + '.html'
        html_path = HTML_OUTPUT_DIR / html_name
        
        if convert_to_html(local_path, html_path):
            html_files.append({
                'info': file_info,
                'html_path': html_path
            })
        else:
            print(f"  ⏭️  Пропущен (неподдерживаемый формат)")
    
    print(f"\n✅ Конвертировано в HTML: {len(html_files)} файлов")
    
    # Шаг 3: Загрузка HTML на Google Drive
    print("\n⬆️  Загрузка HTML файлов на Google Drive...")
    for item in html_files:
        upload_to_drive(drive, item['html_path'], HTML_FOLDER_ID, item['html_path'].name)
    
    # Шаг 4: Создание RAG-индекса с сортировкой по темам
    print("\n📚 Создание RAG-индекса с сортировкой по тематике...")
    rag_by_topic = {}
    
    for item in html_files:
        file_info = item['info']
        html_path = item['html_path']
        
        # Классифицируем
        topic = classify_topic(file_info['name'], file_info['path'])
        
        if topic not in rag_by_topic:
            rag_by_topic[topic] = []
        
        # Создаем RAG-запись
        rag_content = create_rag_entry(file_info, html_path, topic)
        if rag_content:
            rag_by_topic[topic].append({
                'file': file_info['name'],
                'content': rag_content
            })
    
    # Сохраняем RAG-файлы по темам
    for topic, entries in rag_by_topic.items():
        topic_dir = RAG_OUTPUT_DIR / topic
        topic_dir.mkdir(parents=True, exist_ok=True)
        
        for entry in entries:
            safe_name = Path(entry['file']).stem.replace(' ', '_')[:100]
            rag_file = topic_dir / f"{safe_name}.md"
            
            with open(rag_file, 'w', encoding='utf-8') as f:
                f.write(entry['content'])
            
            print(f"  📝 RAG: {topic}/{safe_name}.md")
    
    # Создаем оглавление
    index_file = RAG_OUTPUT_DIR / 'INDEX.md'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# 📚 RAG Knowledge Base - Индекс\n\n")
        f.write(f"**Дата обработки:** 2026-04-05\n")
        f.write(f"**Источник:** Google Drive / istohniki\n\n")
        f.write("---\n\n")
        
        for topic, entries in sorted(rag_by_topic.items()):
            f.write(f"## {topic.upper()}\n\n")
            for entry in entries:
                f.write(f"- {entry['file']}\n")
            f.write("\n")
    
    print(f"\n{'=' * 80}")
    print("✅ ЗАВЕРШЕНО!")
    print(f"{'=' * 80}")
    print(f"📊 Обработано файлов: {len(html_files)}")
    print(f"📂 Тем: {len(rag_by_topic)} ({', '.join(rag_by_topic.keys())})")
    print(f"📁 HTML файлы: {HTML_OUTPUT_DIR}")
    print(f"📁 RAG файлы: {RAG_OUTPUT_DIR}")
    print(f"📄 Индекс: {index_file}")

if __name__ == '__main__':
    main()
