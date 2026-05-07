# Google Calendar — Интеграция

## Статус: ✅ Подключено

## Учётные данные
- Конфиг: `/root/.openclaw/workspace/google-oauth.json`
- Календарь: `volhoverdzarvis@gmail.com`

## Возможности
- Просмотр событий на день/неделю/месяц
- Создание событий
- Изменение/удаление событий
- Напоминания о встречах

## Как использовать
Через Python-скрипт с google-api-python-client:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials(token=None, refresh_token=REFRESH_TOKEN, ...)
service = build('calendar', 'v3', credentials=creds)

# События на сегодня
events = service.events().list(calendarId='primary', timeMin=..., timeMax=...).execute()

# Создать событие
service.events().insert(calendarId='primary', body={
    'summary': 'Встреча',
    'start': {'dateTime': '2026-04-02T10:00:00+05:00'},
    'end': {'dateTime': '2026-04-02T11:00:00+05:00'},
}).execute()
```

## Дата подключения
2026-04-01
