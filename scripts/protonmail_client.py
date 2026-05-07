#!/usr/bin/env python3
"""
Скрипт для работы с ProtonMail API.
Позволяет авторизовываться, получать входящие письма и отправлять новые сообщения.
Учетные данные читаются из /root/vikunja/protonmail_account.json.
"""

import json
import os
import sys
from protonmail import ProtonMail

# Путь к файлу с учетными данными
CREDENTIALS_PATH = "/root/vikunja/protonmail_account.json"

def load_credentials():
    """Загрузка учетных данных из JSON-файла"""
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            creds = json.load(f)
        # Используем полный email как логин для ProtonMail API
        return creds['email'], creds['password']
    except FileNotFoundError:
        print(f"[ERROR] Файл с учетными данными не найден: {CREDENTIALS_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Ошибка парсинга JSON: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"[ERROR] В файле отсутствует обязательное поле: {e}")
        sys.exit(1)

def initialize_client():
    """Инициализация и авторизация клиента ProtonMail"""
    username, password = load_credentials()
    try:
        client = ProtonMail(username, password)
        # Авторизация происходит при первом обращении к API
        # Проверим соединение, попытавшись получить информацию о пользователе
        user_info = client.get_user_info()
        email = user_info.get('Address', 'unknown')
        print(f"[INFO] Успешная авторизация в ProtonMail как {email}")
        return client
    except Exception as e:
        print(f"[ERROR] Ошибка при инициализации ProtonMail клиента: {e}")
        sys.exit(1)

def get_unread_messages(client, limit=10):
    """
    Получение списка непрочитанных писем.
    Возвращает список словарей с метаданными письма.
    """
    try:
        # Получаем папку Входящие (по умолчанию имеет ID 1)
        inbox = client.get_mailbox(1)
        messages = inbox.get_messages()
        
        unread = []
        for msg in messages:
            if not msg.get('IsRead', True):  # Если письмо непрочитанное
                unread.append({
                    'ID': msg.get('ID'),
                    'Subject': msg.get('Subject'),
                    'From': msg.get('From'),
                    'Date': msg.get('Date'),
                    'Size': msg.get('Size')
                })
                if len(unread) >= limit:
                    break
        return unread
    except Exception as e:
        print(f"[ERROR] Ошибка при получении писем: {e}")
        return []

def read_message(client, msg_id):
    """
    Чтение полного содержания письма по его ID.
    Возвращает словарь с полями: Subject, From, To, Date, Body.
    """
    try:
        message = client.get_message(msg_id)
        return {
            'ID': message.get('ID'),
            'Subject': message.get('Subject'),
            'From': message.get('From'),
            'To': message.get('To'),
            'Date': message.get('Date'),
            'Body': message.get('Body')
        }
    except Exception as e:
        print(f"[ERROR] Ошибка при чтении письма {msg_id}: {e}")
        return None

def send_message(client, to, subject, body):
    """
    Отправка нового письма.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        # Отправляем письмо
        client.send_message(
            To=to,
            Subject=subject,
            Body=body
        )
        print(f"[INFO] Письмо успешно отправлено на {to}")
        return True
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке письма: {e}")
        return False

# --- Пример использования (для тестирования) ---
if __name__ == "__main__":
    print("=== ПротонПочта Клиент ===")
    
    # Инициализация клиента
    print("[1] Инициализация клиента...")
    client = initialize_client()
    
    # Получение непрочитанных писем
    print("[2] Получение непрочитанных писем...")
    unread = get_unread_messages(client, limit=5)
    if unread:
        print(f"Найдено {len(unread)} непрочитанных писем:")
        for msg in unread:
            print(f"  - [{msg['ID']}] {msg['From']}: {msg['Subject']}")
    else:
        print("Непрочитанных писем не найдено.")
    
    # Пример отправки тестового письма (раскомментировать для использования)
    # print("[3] Отправка тестового письма...")
    # success = send_message(
    #     client,
    #     to="test@example.com",
    #     subject="Тестовое письмо от Джарвиса",
    #     body="Это тестовое сообщение, отправленное через ProtonMail API."
    # )
    # if success:
    #     print("Тестовое письмо отправлено успешно.")
    # else:
    #     print("Не удалось отправить тестовое письмо.")
    
    print("[Готово] Скрипт завершил работу.")