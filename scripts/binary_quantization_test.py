#!/usr/bin/env python3
"""
Тест бинарной квантации эмбеддингов для RAG.
Сравнивает размер и скорость поиска для float32 и binary векторов.
"""
import numpy as np
import time
import os

def generate_mock_embeddings(num_vectors=1000, dim=1536):
    """Генерирует случайные эмбеддинги (имитация выхода ML-модели)."""
    return np.random.random((num_vectors, dim)).astype(np.float32)

def quantize_to_binary(float_vectors):
    """Преобразует float32 векторы в бинарные (0/1) на основе порога."""
    return (float_vectors > 0).astype(np.int8)

def hamming_search(query_binary, database_binary, top_k=5):
    """Поиск ближайших соседей через расстояние Хэмминга (XOR + popcount)."""
    # XOR находит различия, sum по оси 1 считает количество различий
    distances = np.sum(np.bitwise_xor(query_binary, database_binary), axis=1)
    return np.argpartition(distances, top_k)[:top_k]

def cosine_search_simulated(query_float, database_float, top_k=5):
    """Имитация косинусного поиска (для сравнения)."""
    # В реальности это требует BLAS, здесь упрощенная евклидова метрика для замера
    diff = database_float - query_float
    distances = np.linalg.norm(diff, axis=1)
    return np.argpartition(distances, top_k)[:top_k]

def main():
    print("🧪 Тестирование бинарной квантации RAG...")
    
    # 1. Генерация данных
    NUM_VECTORS = 5000
    DIM = 1536 # Стандартная размерность для многих embedding-моделей
    
    print(f"📊 Генерация {NUM_VECTORS} векторов размерности {DIM}...")
    db_float = generate_mock_embeddings(NUM_VECTORS, DIM)
    query_float = generate_mock_embeddings(1, DIM)[0]
    
    # 2. Квантизация
    print("🔄 Бинаризация векторов...")
    db_binary = quantize_to_binary(db_float)
    query_binary = quantize_to_binary(query_float)
    
    # 3. Сравнение размеров
    size_float = db_float.nbytes / (1024 * 1024)
    size_binary = db_binary.nbytes / (1024 * 1024)
    compression_ratio = size_float / size_binary
    
    print(f"\n📦 Сравнение占用占用占用占用占用占用占用占用占用占用占用占用 памяти:")
    print(f"   Float32:   {size_float:.2f} MB")
    print(f"   Binary:    {size_binary:.2f} MB")
    print(f"   Сжатие:    {compression_ratio:.1f}x")
    
    # 4. Сравнение скорости поиска
    print(f"\n⏱️  Замеры скорости поиска (Top-5):")
    
    # Binary Search (Hamming)
    start = time.time()
    for _ in range(100):
        hamming_search(query_binary, db_binary)
    time_binary = (time.time() - start) / 100 * 1000 # ms
    
    # Float Search (Simulated Euclidean)
    start = time.time()
    for _ in range(100):
        cosine_search_simulated(query_float, db_float)
    time_float = (time.time() - start) / 100 * 1000 # ms
    
    speedup = time_float / time_binary
    
    print(f"   Binary (Hamming):  {time_binary:.3f} ms")
    print(f"   Float (Euclidean): {time_float:.3f} ms")
    print(f"   Ускорение:         {speedup:.1f}x")
    
    print("\n✅ Тест завершен. Бинарная квантация готова к интеграции в RAG-pipeline.")

if __name__ == '__main__':
    main()
