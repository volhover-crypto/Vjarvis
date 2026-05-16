#!/usr/bin/env python3
"""Генерация эмбеддингов для GBrain через sentence_transformers + psql (peer auth)."""

import json
import time
import subprocess
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DB = "gbrain"

def psql(query, quiet=True):
    cmd = ["sudo", "-u", "postgres", "psql", "-d", DB, "-t", "-A", "-c", query]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 and not quiet:
        print(f"PSQL Error: {r.stderr.strip()}")
    return r.stdout.strip()

def run_sql(query):
    cmd = ["sudo", "-u", "postgres", "psql", "-d", DB, "-q", "-c", query]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0

def main():
    print("🧠 GBrain Local Embedding Generator")
    
    # 1. Загружаем модель
    print(f"📥 Загрузка {MODEL_NAME}...")
    t0 = time.time()
    model = SentenceTransformer(MODEL_NAME)
    print(f"✅ Модель загружена за {time.time()-t0:.1f}s")
    
    # 2. Считаем
    total = int(psql("SELECT COUNT(*) FROM content_chunks;"))
    pending = int(psql("SELECT COUNT(*) FROM content_chunks WHERE embedding IS NULL;"))
    print(f"📄 Всего: {total}, без эмбеддингов: {pending}")
    
    if pending == 0:
        print("🎉 Все эмбеддинги уже есть!")
        return
    
    # 3. Обрабатываем батчами
    batch_size = 20
    processed = 0
    start = time.time()
    
    while True:
        # Ищем незаполненные чанки
        rows = psql(f"""
            SELECT id, chunk_text FROM content_chunks 
            WHERE embedding IS NULL ORDER BY id LIMIT {batch_size};
        """)
        
        if not rows:
            break
        
        lines = rows.strip().split('\n')
        chunks = []
        for line in lines:
            if '|' in line:
                parts = line.split('|', 1)
                chunk_id = parts[0].strip()
                text = parts[1].strip() if len(parts) > 1 else ''
                if chunk_id and text:
                    chunks.append((chunk_id, text))
        
        if not chunks:
            break
        
        # Генерируем эмбеддинги
        texts = [c[1] for c in chunks]
        embeddings = model.encode(texts, show_progress_bar=False)
        
        # Сохраняем каждый
        for (chunk_id, _), emb in zip(chunks, embeddings):
            emb_json = json.dumps(emb.tolist())
            sql = f"""
                UPDATE content_chunks 
                SET embedding = '{emb_json}'::vector, 
                    embedded_at = now(), 
                    model = '{MODEL_NAME}'
                WHERE id = {chunk_id};
            """
            run_sql(sql)
        
        processed += len(chunks)
        elapsed = time.time() - start
        rate = processed / elapsed if elapsed > 0 else 0
        pct = processed / pending * 100 if pending > 0 else 0
        remaining = pending - processed
        eta = remaining / rate if rate > 0 else 0
        print(f"  ✅ {processed}/{pending} ({pct:.0f}%, {rate:.0f} chunks/m, ETA: {eta/60:.1f}m)")
    
    # Итог
    elapsed = time.time() - start
    done = int(psql("SELECT COUNT(*) FROM content_chunks WHERE embedding IS NOT NULL;"))
    print(f"\n🎉 Готово! {processed} эмбеддингов за {elapsed/60:.1f}min")
    print(f"📊 С эмбеддингами: {done}/{total}")
    
    if done == total:
        print("🔍 Семантический поиск gbrain query теперь работает!")

if __name__ == "__main__":
    main()
