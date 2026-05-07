import os
import pdfplumber
import json
import shutil
from pathlib import Path

# Пути
SOURCE_DIR = "/root/.openclaw/workspace/temp_n8n_rag"
TARGET_BASE = "/root/.openclaw/workspace/self-improving/projects/rag-indexed/n8n-orchestration"

# Категории для классификации (по ключевым словам в имени файла или содержании)
CATEGORIES = {
    "core_platform": ["n8n", "workflow", "automation", "platform", "architecture", "self-hosted"],
    "rag_theory": ["rag", "retrieval", "chunking", "indexing", "evaluation"],
    "ai_agents": ["agent", "llm", "autonomous", "multi-agent", "reasoning"],
    "mcp_integrations": ["mcp", "model context protocol", "integration"],
    "vector_databases": ["vector", "database", "embedding", "chroma", " Milvus", "pgvector"],
    "prompt_engineering": ["prompt", "engineering", "optimization", "chain-of-thought"]
}

def extract_text_from_pdf(pdf_path):
    """Извлечение текста из PDF"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Ошибка чтения {pdf_path}: {e}")
    return text[:5000]  # Берем первые 5000 символов для классификации

def classify_document(text, filename):
    """Определение категории документа"""
    lower_text = text.lower()
    lower_filename = filename.lower()
    
    scores = {}
    for category, keywords in CATEGORIES.items():
        score = 0
        for keyword in keywords:
            if keyword in lower_filename:
                score += 3  # Название файла важнее
            if keyword in lower_text:
                score += 1
        scores[category] = score
    
    # Выбираем категорию с максимальнымスコア
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "core_platform"  # По умолчанию
    return best_category

def convert_to_markdown(text, filename, category, source_file):
    """Создание Markdown-файла с метаданными"""
    # Очистка имени файла
    clean_name = Path(filename).stem.replace("+", " ").replace("_", " ").strip()
    
    md_content = f"""---
source_block: {category}
source_file: {source_file}
topic_tags: ["n8n", "{category.replace('_', ' ')}"]
---

# {clean_name}

{text}
"""
    return md_content

def sync_from_drive():
    """Синхронизация папки N8N с Google Drive"""
    print("Синхронизация с Google Drive (папка 'N 8 N')...")
    os.makedirs(SOURCE_DIR, exist_ok=True)
    # Используем rclone для синхронизации (только новые/измененные файлы)
    cmd = f'rclone sync "google_drive,volhoverdzarvis:N 8 N/" {SOURCE_DIR} --drive-root-folder-id 1KUL4QLvRK1oF0zu-hPa-LnaUqsvdEax8'
    os.system(cmd)
    print("Синхронизация завершена.")

def main():
    sync_from_drive()
    print("Начинаю обработку N8N RAG...")
    
    if not os.path.exists(SOURCE_DIR):
        print(f"Папка {SOURCE_DIR} не найдена!")
        return

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.pdf', '.docx'))]
    print(f"Найдено файлов: {len(files)}")

    for filename in files:
        source_path = os.path.join(SOURCE_DIR, filename)
        
        # 1. Извлечение текста
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(source_path)
        else:
            continue # Пока только PDF
            
        if not text.strip():
            print(f"Пропуск {filename}: пустой текст")
            continue

        # 2. Классификация
        category = classify_document(text, filename)
        print(f"Файл: {filename} -> Категория: {category}")

        # 3. Конвертация и сохранение
        md_content = convert_to_markdown(text, filename, category, filename)
        
        target_dir = os.path.join(TARGET_BASE, category)
        os.makedirs(target_dir, exist_ok=True)
        
        md_filename = filename.replace('.pdf', '.md').replace(' ', '_')
        target_path = os.path.join(target_dir, md_filename)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

    print("Обработка завершена!")

if __name__ == "__main__":
    main()