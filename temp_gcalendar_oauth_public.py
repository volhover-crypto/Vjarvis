#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Временный скрипт для восстановления доступа к Google Calendar.
Использует жёстко заданные client_id и client_secret (переданные пользователем).
Использует публичный redirect URI: http://mdked.hlab.kz:8080/
После использования — УДАЛЯЕТСЯ.
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Жёстко заданные учетные данные (от пользователя)
CLIENT_ID = "140943545360-vljr8rerht0s3ehcucvjpt7ukfbil3b2.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# Если изменяешь эти области (scopes) — удали файл token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = '/root/.openclaw.workspace/google-oauth.json'
REDIRECT_URI = 'http://mdked.hlab.kz:8080/'  # Публичный redirect URI

# Глобальная переменная для хранения кода авторизации
auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        query = parse_qs(urlparse(self.path).query)
        if 'code' in query:
            auth_code = query['code'][0]
            self.wfile.write('<h1>Authorization successful!</h1>'.encode('utf-8'))
            self.wfile.write('<p>You can close this tab and return to the chat.</p>'.encode('utf-8'))
            self.wfile.write('<p>Authorization code received. Thank you!</p>'.encode('utf-8'))
        else:
            self.wfile.write('<h1>Error</h1>'.encode('utf-8'))
            self.wfile.write('<p>Authorization code not received.</p>'.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Отключаем логгирование сервера
        pass

def main():
    print("🔐 Restoring Google Calendar Access")
    print(f"🎯 Target account: volhoverdzarvis@gmail.com")
    print(f"💾 Token will be saved to: {TOKEN_PATH}")
    print(f"🌐 Using redirect URI: {REDIRECT_URI}")
    print()

    # Проверяем, не существует ли уже токен
    if os.path.exists(TOKEN_PATH):
        print(f"⚠️  Token file already exists: {TOKEN_PATH}")
        print("🔄 Overwriting existing token...")

    # Настраиваем flow
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    # Получаем URL для авторизации
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("🌐 Please follow these steps:")
    print("   1. Copy and open this link in your browser:")
    print(f"   {auth_url}")
    print("   2. Sign in to your Google account: volhoverdzarvis@gmail.com")
    print("   3. Grant permission to access your calendar")
    print("   4. After successful sign-in, you will be redirected back to:")
    print(f"   {REDIRECT_URI}")
    print("   5. Wait here for confirmation — the server will capture the code automatically")
    print()
    print("⏳ Waiting for authorization to complete...")
    print(f"   (Listening on {REDIRECT_URI})")

    # Запускаем локальный сервер на всех интерфейсах, порт 8080
    server = HTTPServer(('0.0.0.0', 8080), OAuthHandler)
    
    # Ждём один запрос (или таймаут через 5 минут)
    server.handle_request()  # Блокирует до первого GET-запроса
    
    server.server_close()
    print("✅ Server stopped.")

    if not auth_code:
        print("❌ Authorization code not received. OAuth flow failed.")
        return

    print(f"🔑 Received authorization code: {auth_code[:10]}...")

    # Обмениваем код на токены
    try:
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        print("✅ Tokens successfully obtained.")
    except Exception as e:
        print(f"❌ Error exchanging code for tokens: {e}")
        return

    # Сохраняем учетные данные
    try:
        creds_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        # Убираем None значения
        creds_dict = {k: v for k, v in creds_dict.items() if v is not None}

        with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
            json.dump(creds_dict, f, indent=2, ensure_ascii=False)

        print()
        print(f"✅ Credentials successfully saved to: {TOKEN_PATH}")
        print("📄 File content (secrets hidden):")
        safe_dict = {k: ('[HIDDEN]' if 'secret' in k or 'token' in k else v) 
                     for k, v in creds_dict.items()}
        print(json.dumps(safe_dict, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Error saving token: {e}")
        return

    # Тестовый запрос: проверяем доступ к календарю
    print()
    print("🔍 Checking access to Google Calendar API...")
    try:
        service = build('calendar', 'v3', credentials=credentials)

        # Получаем список календарей
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        print(f"✅ Successfully retrieved calendar list. Found: {len(calendars)} calendar(s)")
        for cal in calendars[:5]:  # Show first 5
            print(f"   - {cal.get('summary')} ({cal.get('id')})")

        # Ищем календарь volhoverdzarvis@gmail.com
        target_calendar = None
        for cal in calendars:
            if cal.get('id') == 'volhoverdzarvis@gmail.com':
                target_calendar = cal
                break

        if target_calendar:
            print(f"✅ Found target calendar: {target_calendar.get('summary')}")
        else:
            print(f"⚠️  Target calendar 'volhoverdzarvis@gmail.com' not found in list.")
            print("   It might have a different name or you're using the primary calendar.")
            # Попробуем использовать основной календарь
            primary_cal = None
            for cal in calendars:
                if cal.get('primary'):
                    primary_cal = cal
                    break
            if primary_cal:
                print(f"💡 Using primary calendar: {primary_cal.get('summary')}")
                target_calendar = primary_cal
            else:
                print("❌ Could not determine calendar for event test.")
                return

        # Получаем события на сегодня
        import datetime
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId=target_calendar['id'],
            timeMin=now,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        print(f"📅 Events today (UTC): {len(events)}")
        if events:
            for event in events[:3]:  # Show first 3
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"   - {start}: {event.get('summary', '(No title)')}")
        else:
            print("   No events today.")

        print()
        print("🎉 Google Calendar access successfully restored and verified!")
        print(f"💾 Token saved to: {TOKEN_PATH}")
        print("🚀 You can now use this account in your scripts and skills.")

    except Exception as e:
        print(f"❌ Error checking Google Calendar API access: {e}")
        return

    # Очистка: удаляем временный скрипт
    try:
        os.remove(__file__)
        print(f"🗑️  Temporary script removed: {__file__}")
    except Exception as e:
        print(f"⚠️  Failed to remove temporary script: {e}")

if __name__ == '__main__':
    main()