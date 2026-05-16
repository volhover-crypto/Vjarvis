#!/usr/bin/env python3
"""Семантический поиск по GBrain vault через локальную модель."""

import json
import subprocess
import sys
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DB = "gbrain"

def psql(query):
    cmd = ["sudo", "-u", "postgres", "psql", "-d", DB, "-t", "-A", "-F", "|", "-c", query]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout.strip()

def search(query_text, top_k=5):
    model = SentenceTransformer(MODEL_NAME)
    
    # Генерируем эмбеддинг запроса
    query_emb = model.encode([query_text])[0]
    query_json = json.dumps(query_emb.tolist())
    
    # Ищем через cosine similarity в pgvector
    sql = f"""
        SELECT 
            cc.chunk_text,
            cc.chunk_source,
            cc.embedding <=> '{query_json}'::vector AS distance
        FROM content_chunks cc
        WHERE cc.embedding IS NOT NULL
        ORDER BY cc.embedding <=> '{query_json}'::vector
        LIMIT {top_k};
    """
    
    results = psql(sql)
    
    if not results:
        print("Ничего не найдено.")
        return
    
    print(f"🔍 Запрос: {query_text}\n")
    print(f"{'#':<4} {'Distance':<10} {'Source':<30} {'Text'}")
    print("-" * 100)
    
    for i, line in enumerate(results.split('\n'), 1):
        if '|' in line:
            parts = line.split('|', 2)
            if len(parts) >= 3:
                text = parts[0].strip()[:80]
                source = parts[1].strip()[:28]
                dist = parts[2].strip()[:8]
                print(f"{i:<4} {dist:<10} {source:<30} {text}")

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "агрономия виноградарство"
    search(query)
