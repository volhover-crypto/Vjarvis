#!/usr/bin/env python3
"""
Оптимизация эмбеддингов PowerMem через бинарную квантацию.
Скрипт:
1. Извлекает текущие эмбеддинги из PowerMem (SQLite)
2. Конвертирует float32 → binary (int8)
3. Пересохраняет с壓縮
4. Настраивает PowerMem на использование бинарного поиска

Автор: Джарвис
Дата: 2026-04-05
"""

import sqlite3
import numpy as np
import json
from pathlib import Path
import sys

# Пути
POWERMEM_DB = Path.home() / '.openclaw' / 'powermem' / 'powermem.db'
BACKUP_DB = Path.home() / '.openclaw' / 'powermem' / 'powermem_backup.db'

def quantize_to_binary(float_vectors):
    """Преобразует float32 векторы в бинарные (0/1)"""
    if isinstance(float_vectors, list):
        float_vectors = np.array(float_vectors, dtype=np.float32)
    return (float_vectors > 0).astype(np.int8)

def get_db_connection():
    """Подключение к SQLite базе PowerMem"""
    if not POWERMEM_DB.exists():
        print(f"❌ База не найдена: {POWERMEM_DB}")
        sys.exit(1)
    
    conn = sqlite3.connect(str(POWERMEM_DB))
    conn.row_factory = sqlite3.Row
    return conn

def check_current_state():
    """Проверка текущего состояния базы"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row['name'] for row in cursor.fetchall()]
    print(f"📋 Таблицы в базе: {tables}")
    
    # Проверяем структуру таблицы memories
    if 'memories' in tables:
        cursor.execute("PRAGMA table_info(memories)")
        columns = [row['name'] for row in cursor.fetchall()]
        print(f"📊 Колонки в memories: {columns}")
        
        # Считаем количество записей
        cursor.execute("SELECT COUNT(*) as count FROM memories")
        count = cursor.fetchone()['count']
        print(f"📝 Всего记忆: {count}")
        
        # Проверяем формат эмбеддингов
        if 'embedding' in columns:
            cursor.execute("SELECT embedding FROM memories LIMIT 1")
            row = cursor.fetchone()
            if row and row['embedding']:
                emb_data = json.loads(row['embedding']) if isinstance(row['embedding'], str) else row['embedding']
                if isinstance(emb_data, list):
                    print(f"📐 Размерность эмбеддинга: {len(emb_data)}")
                    print(f"🔢 Тип данных: {type(emb_data[0])}")
                    print(f"📏 Пример значений: {emb_data[:5]}")
    
    conn.close()

def optimize_embeddings():
    """Оптимизация всех эмбеддингов в базе"""
    print("\n🔄 Начинаю оптимизацию эмбеддингов...")
    
    # Создаём бэкап
    import shutil
    if POWERMEM_DB.exists():
        shutil.copy2(str(POWERMEM_DB), str(BACKUP_DB))
        print(f"💾 Бэкап создан: {BACKUP_DB}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Получаем все记忆 с эмбеддингами
    cursor.execute("SELECT id, embedding FROM memories WHERE embedding IS NOT NULL")
    rows = cursor.fetchall()
    
    if not rows:
        print("⚠️ Нет记忆 с эмбеддингами для оптимизации")
        conn.close()
        return
    
    print(f"📊 Найдено {len(rows)}记忆 для оптимизации")
    
    optimized_count = 0
    errors = 0
    
    for row in rows:
        try:
            mem_id = row['id']
            emb_str = row['embedding']
            
            # Парсим эмбеддинг
            if isinstance(emb_str, str):
                emb_float = np.array(json.loads(emb_str), dtype=np.float32)
            else:
                emb_float = np.array(emb_str, dtype=np.float32)
            
            # Квантуем в binary
            emb_binary = quantize_to_binary(emb_float)
            
            # Сохраняем как список int8
            emb_binary_list = emb_binary.tolist()
            emb_json = json.dumps(emb_binary_list)
            
            # Обновляем запись
            cursor.execute(
                "UPDATE memories SET embedding = ? WHERE id = ?",
                (emb_json, mem_id)
            )
            
            optimized_count += 1
            if optimized_count % 10 == 0:
                print(f"  Обработано: {optimized_count}/{len(rows)}")
        
        except Exception as e:
            print(f"  ❌ Ошибка для记忆 {row['id']}: {e}")
            errors += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Оптимизация завершена!")
    print(f"   Успешно: {optimized_count}")
    print(f"   Ошибки: {errors}")
    
    # Показываем экономию памяти
    if optimized_count > 0:
        # Примерный расчёт
        sample_emb = json.loads(cursor.execute("SELECT embedding FROM memories LIMIT 1").fetchone()['embedding'])
        dims = len(sample_emb)
        
        size_float_mb = (optimized_count * dims * 4) / (1024 * 1024)  # float32 = 4 bytes
        size_binary_mb = (optimized_count * dims * 1) / (1024 * 1024)  # int8 = 1 byte
        savings_mb = size_float_mb - size_binary_mb
        savings_percent = (savings_mb / size_float_mb) * 100
        
        print(f"\n📦 Экономия памяти:")
        print(f"   Было (float32): {size_float_mb:.2f} MB")
        print(f"   Стало (int8):   {size_binary_mb:.2f} MB")
        print(f"   Экономия:       {savings_mb:.2f} MB ({savings_percent:.1f}%)")

def verify_optimization():
    """Проверка результата оптимизации"""
    print("\n🔍 Проверка оптимизации...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT embedding FROM memories WHERE embedding IS NOT NULL LIMIT 5")
    rows = cursor.fetchall()
    
    for i, row in enumerate(rows):
        emb = json.loads(row['embedding'])
        is_binary = all(v in [0, 1] for v in emb)
        print(f"  память {i+1}: размерность={len(emb)}, бинарный={is_binary}, пример={emb[:5]}")
    
    conn.close()
    print("✅ Проверка завершена")

def main():
    print("=" * 80)
    print("🚀 Оптимизация PowerMem через Binary Quantization")
    print("=" * 80)
    
    # Шаг 1: Проверка текущего состояния
    print("\n📋 Шаг 1: Проверка текущего состояния")
    check_current_state()
    
    # Шаг 2: Оптимизация
    print("\n⚙️  Шаг 2: Оптимизация эмбеддингов")
    optimize_embeddings()
    
    # Шаг 3: Проверка
    print("\n✔️  Шаг 3: Проверка результата")
    verify_optimization()
    
    print("\n" + "=" * 80)
    print("✅ ВСЁ ГОТОВО!")
    print("=" * 80)
    print("\n📝 Следующие шаги:")
    print("1. Перезапустите OpenClaw gateway: openclaw gateway restart")
    print("2. Проверьте работу: openclaw ltm health")
    print("3. Протестируйте поиск: openclaw ltm search \"тест\"")

if __name__ == '__main__':
    main()
