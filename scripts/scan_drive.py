import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_service():
    """Показывает список файлов на Google Drive."""
    creds = None
    # token.json хранит токены доступа и обновления пользователя.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Если валидных учетных данных нет, просим пользователя войти в систему.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Ошибка: файл credentials.json не найден. Скачайте его из Google Cloud Console.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
        # Сохраняем учетные данные для следующего запуска.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Ошибка при создании сервиса: {e}")
        sys.exit(1)

def list_files(service):
    """Рекурсивный обход папок."""
    results = []
    page_token = None
    while True:
        results_page = service.files().list(
            pageSize=1000,
            pageToken=page_token,
            fields="nextPageToken, files(id, name, mimeType, parents, size, modifiedTime)",
            orderBy="folder, name"
        ).execute()
        
        items = results_page.get('files', [])
        results.extend(items)
        
        page_token = results_page.get('nextPageToken')
        if not page_token:
            break
            
    return results

def print_tree(files):
    """Выводит структуру папок."""
    # Создаем словарь для быстрого поиска по ID
    file_map = {f['id']: f for f in files}
    
    # Находим корневые элементы (у которых нет parents или parent - это root drive)
    roots = [f for f in files if not f.get('parents') or f['parents'][0] == '0AHw...'] # Упрощенно
    
    # На самом деле у корня Drive parent может отсутствовать или быть специфичным.
    # Просто выведем всё списком с отступами, если сможем построить путь.
    
    print(f"Найдено элементов: {len(files)}")
    print("-" * 20)
    for f in files:
        is_folder = f['mimeType'] == 'application/vnd.google-apps.folder'
        prefix = "[DIR]  " if is_folder else "[FILE] "
        print(f"{prefix}{f['name']} (ID: {f['id']})")

if __name__ == '__main__':
    print("Запуск сканирования Google Drive...")
    service = get_service()
    files = list_files(service)
    print_tree(files)
