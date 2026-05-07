#!/usr/bin/env python3
"""
Скрипт для обновления HTML-оглавления базы знаний RAG.
Считывает структуру папки RAG_Knowledge_Base в Google Drive и генерирует HTML.
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_credentials():
    cred_path = '/root/.openclaw/workspace/google-oauth.json'
    with open(cred_path, 'r') as f:
        data = json.load(f)
    return Credentials(
        token=None, 
        refresh_token=data['refresh_token'], 
        token_uri=data['token_uri'], 
        client_id=data['client_id'], 
        client_secret=data['client_secret']
    )

def get_tree(drive, folder_id, level=0):
    tree = []
    try:
        results = drive.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields='files(id, name, mimeType, webViewLink)',
            orderBy='folder,name'
        ).execute()
        items = results.get('files', [])
        
        for item in items:
            indent = '&nbsp;&nbsp;' * (level * 4)
            item_name = item['name']
            item_link = item.get('webViewLink', '#')
            
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                tree.append(f'{indent}📁 <b>{item_name}</b><br>')
                tree.extend(get_tree(drive, item['id'], level + 1))
            else:
                tree.append(f'{indent}<a href="{item_link}" target="_blank">📄 {item_name}</a><br>')
    except Exception as e:
        print(f"Error fetching folder {folder_id}: {e}")
    return tree

def main():
    # ID корневой папки RAG
    RAG_ROOT_ID = '1KUL4QLvRK1oF0zu-hPa-LnaUqsvdEax8'
    OUTPUT_FILE = '/root/.openclaw/workspace/rag_index.html'
    
    creds = get_credentials()
    drive = build('drive', 'v3', credentials=creds)
    
    print("🔍 Сканирование Google Drive...")
    html_content = get_tree(drive, RAG_ROOT_ID)
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG Knowledge Base</title>
    <style>
        body {{ font-family: "Georgia", serif; background-color: #f4f1ea; color: #333; padding: 40px; }}
        .book-container {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 50px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #8b4513; }}
        h1 {{ text-align: center; color: #8b4513; border-bottom: 2px solid #8b4513; padding-bottom: 10px; margin-bottom: 30px; }}
        a {{ text-decoration: none; color: #2c3e50; transition: color 0.3s; }}
        a:hover {{ color: #c0392b; text-decoration: underline; }}
        .meta {{ text-align: center; font-style: italic; color: #777; margin-bottom: 40px; }}
        .footer {{ text-align: center; margin-top: 50px; font-size: 0.8em; color: #999; }}
    </style>
</head>
<body>
    <div class="book-container">
        <h1>Оглавление Базы Знаний</h1>
        <div class="meta">Автоматически сгенерировано из Google Drive</div>
        <div class="content">
            {''.join(html_content)}
        </div>
        <div class="footer">Обновлено: {json.dumps(os.popen('date').read().strip())}</div>
    </div>
</body>
</html>'''

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Оглавление успешно обновлено: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
