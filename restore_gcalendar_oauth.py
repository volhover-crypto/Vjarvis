#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для восстановления доступа к Google Calendar через OAuth 2.0.
Запускает поток авторизации и сохраняет учетные данные.
"""

import json
import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Если изменяешь эти области (scopes) — удали файл token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = '/root/.openclaw.workspace/google-oauth.json'

def main():
    print("🔐 Восстановление доступа к Google Calendar")
    print(f"📎 Целевой аккаунт: volhoverdzarvis@gmail.com")
    print(f"💾 Токен будет сохранён в: {TOKEN_PATH}")
    print()

    # Проверяем, не существует ли уже токен (на случай, если мы пропустили его ранее)
    if os.path.exists(TOKEN_PATH):
        print(f"⚠️  Файл токена уже существует: {TOKEN_PATH}")
        answer = input("Перезаписать его? (y/N): ").strip().lower()
        if answer != 'y':
            print("❌ Операция отменена пользователем.")
            return
        else:
            print("🗑️  Удаляем старый токен...")

    # Запускаем поток авторизации
    # Для этого нам нужны client_id и client_secret.
    # Поскольку их нет в файле (файл токена отсутствует), 
    # мы попробуем взять их из переменных окружения или запросить у тебя.
    #
    # Альтернатива: спросить у тебя client_id и client_secret напрямую.
    print("📝 Для запуска OAuth- потока нужны:")
    print("   - client_id")
    print("   - client_secret")
    print()
    print("💡 Их можно получить в Google Cloud Console:")
    print("   1. Перейти в https://console.cloud.google.com/")
    print("   2. Выбрать или создать проект")
    print("   3. Перейти в APIs & Services → Credentials")
    print("   4. Создать OAuth 2.0 Client ID (тип: Desktop app)")
    print("   5. Скопировать client_id и client_secret")
    print()

    # Запрашиваем у тебя эти данные
    client_id = input("🔑 Введите client_id: ").strip()
    if not client_id:
        print("❌ client_id не может быть пустым.")
        return

    client_secret = input("🔐 Введите client_secret: ").strip()
    if not client_secret:
        print("❌ client_secret не может быть пустым.")
        return

    # Создаём объект flow из client_config
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }

    flow = InstalledAppFlow.from_client_config(
        client_config=client_config,
        scopes=SCOPES,
        redirect_uri="http://localhost"
    )

    print()
    print("🌐 Запускаю локальный сервер для OAuth- обратного вызова...")
    print("📢 Пожалуйста, выполните следующие шаги:")
    print("   1. Откройте в браузере ссылку, которая появится ниже")
    print("   2. Войдите в аккаунт Google: volhoverdzarvis@gmail.com")
    print("   3. Предоставьте разрешения на доступ к календарю")
    print("   4. После успешного входа скопируйте код из адресной строки")
    print("      (он будет выглядеть примерно так: 4/0AY0e-g....)")
    print("   5. Вставьте этот код здесь и нажмите Enter")
    print()

    try:
        # Запускаем локальный сервер и ждём ответа
        credentials = flow.run_local_server(
            port=0,
            authorization_prompt_message='Перейдите по этой ссылке: {url}',
            success_message='Авторизация успешна! Вы можете закрыть эту вкладку.',
            open_browser=False  # Не открываем браузер автоматически (мы в терминале/SSH)
        )
    except Exception as e:
        print(f"❌ Ошибка во время OAuth- потока: {e}")
        return

    # Сохраняем учетные данные
    try:
        # Credentials 객체をディクショナリーに変換して保存
        creds_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        # None 값을 제거 (token이 None일 수 있음)
        creds_dict = {k: v for k, v in creds_dict.items() if v is not None}

        with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
            json.dump(creds_dict, f, indent=2, ensure_ascii=False)

        print()
        print(f"✅ Учетные данные успешно сохранены в: {TOKEN_PATH}")
        print("📄 Содержание файла (без секретов):")
        # Показываем структуру без секретных данных
        safe_dict = {k: ('[HIDDEN]' if 'secret' in k or 'token' in k else v) 
                     for k, v in creds_dict.items()}
        print(json.dumps(safe_dict, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Ошибка при сохранении токена: {e}")
        return

    # Тестовый запрос: проверяем доступ к календарю
    print()
    print("🔍 Проверяю доступ к Google Calendar API...")
    try:
        service = build('calendar', 'v3', credentials=credentials)

        # Получаем список календарей
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        print(f"✅ Успешно получен список календарей. Найдено: {len(calendars)} календар(я/ей)")
        for cal in calendars[:5]:  # Показываем первые 5
            print(f"   - {cal.get('summary')} ({cal.get('id')})")

        # Ищем календарь volhoverdzarvis@gmail.com
        target_calendar = None
        for cal in calendars:
            if cal.get('id') == 'volhoverdzarvis@gmail.com':
                target_calendar = cal
                break

        if target_calendar:
            print(f"✅ Найден целевой календарь: {target_calendar.get('summary')}")
        else:
            print(f"⚠️  Целевой календарь 'volhoverdzarvis@gmail.com' не найден в списке.")
            print("   Возможно, он называется иначе или используется основной календарь.")
            # Попробуем использовать основной календарь
            primary_cal = None
            for cal in calendars:
                if cal.get('primary'):
                    primary_cal = cal
                    break
            if primary_cal:
                print(f"💡 Используем основной календарь: {primary_cal.get('summary')}")
                target_calendar = primary_cal
            else:
                print("❌ Не удалось определить календарь для теста событий.")
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

        print(f"📅 Событий на сегодня (UTC): {len(events)}")
        if events:
            for event in events[:3]:  # Показываем первые 3
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"   - {start}: {event.get('summary', '(Без названия)')}")
        else:
            print("   Сегодня нет событий.")

        print()
        print("🎉 Доступ к Google Calendar успешно восстановлен и проверен!")
        print(f"💾 Токен сохранён в: {TOKEN_PATH}")
        print("🚀 Теперь ты можешь использовать этот аккаунт в своих скриптах и навыках.")

    except Exception as e:
        print(f"❌ Ошибка при проверке доступа к Google Calendar API: {e}")
        print("   Возможно, токен некорректен или API не включён.")
        return

if __name__ == '__main__':
    main()