#!/usr/bin/env python3
"""
Knowledge Pipeline — автоматизированное пополнение знаний агента.
Источники: web, файлы, ссылки, тексты.
Результат: структурированные знания в vault + эмбеддинги в gbrain.
"""

import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

# ─── Конфигурация ───────────────────────────────────────────────
VAULT_DIR = "/root/vault"
WORKSPACE = "/root/.openclaw/workspace"
KNOWLEDGE_DIR = f"{VAULT_DIR}/knowledge"
PROCESSED_LOG = f"{WORKSPACE}/memory/processed_sources.json"

# Домены знаний для мониторинга
KNOWLEDGE_DOMAINS = {
    "agronomy": {
        "keywords": ["агрономия", "точное земледелие", "виноградарство", "почва", "удобрения", "полив", "фенофазы", "GDD", "ETc", "SWD"],
        "sources": ["pubmed", "scholar", "agronomy journals"],
        "vault_path": "knowledge/agronomy/",
    },
    "viticulture": {
        "keywords": ["виноградарство", "сорта винограда", "ампелография", "терруir", "шаптализация", "Крым", "виноградник"],
        "sources": ["oiv.int", "wine research", "viticulture journals"],
        "vault_path": "knowledge/viticulture/",
    },
    "iot": {
        "keywords": ["IoT", "датчики", "сенсоры", "MQTT", "мониторинг", "ESP32", "Arduino", "автоматизация"],
        "sources": ["github", "hackster", "instructables"],
        "vault_path": "knowledge/iot/",
    },
    "ai_ml": {
        "keywords": ["LLM", "AI agents", "RAG", "MCP", "OpenClaw", "machine learning", "deep learning"],
        "sources": ["arxiv", "github", "huggingface"],
        "vault_path": "knowledge/ai-ml/",
    },
    "agritech": {
        "keywords": ["AgriTech", "precision agriculture", "smart farming", "дроны", "NDVI", "дистанционный мониторинг"],
        "sources": ["agritech news", "research papers"],
        "vault_path": "knowledge/agritech/",
    },
}

# ─── Утилиты ────────────────────────────────────────────────────

def load_processed():
    """Загружает лог обработанных источников."""
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG) as f:
            return json.load(f)
    return {"processed": [], "stats": {"total": 0, "last_run": None}}

def save_processed(data):
    """Сохраняет лог обработанных источников."""
    with open(PROCESSED_LOG, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def file_hash(filepath):
    """Вычисляет хеш файла."""
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def url_hash(url):
    """Вычисляет хеш URL."""
    return hashlib.md5(url.encode()).hexdigest()

def ensure_dir(path):
    """Создаёт директорию если нет."""
    Path(path).mkdir(parents=True, exist_ok=True)

# ─── Компоненты pipeline ────────────────────────────────────────

class KnowledgePipeline:
    def __init__(self):
        self.processed = load_processed()
        self.stats = {"added": 0, "updated": 0, "skipped": 0, "errors": 0}
    
    def is_processed(self, source_id):
        """Проверяет был ли источник уже обработан."""
        return any(p["id"] == source_id for p in self.processed["processed"])
    
    def mark_processed(self, source_id, title, source_type, vault_file=None):
        """Отмечает источник как обработанный."""
        self.processed["processed"].append({
            "id": source_id,
            "title": title,
            "type": source_type,
            "vault_file": vault_file,
            "processed_at": datetime.utcnow().isoformat(),
        })
        self.processed["stats"]["total"] = len(self.processed["processed"])
        self.processed["stats"]["last_run"] = datetime.utcnow().isoformat()
    
    # ── Источник 1: Web-страница по URL ──
    
    def process_url(self, url, domain=None, tags=None):
        """Обрабатывает web-страницу и сохраняет знания."""
        sid = url_hash(url)
        if self.is_processed(sid):
            print(f"  ⏳ Уже обработано: {url}")
            self.stats["skipped"] += 1
            return None
        
        print(f"  🌐 Обработка URL: {url}")
        
        # Скачиваем страницу
        try:
            result = subprocess.run(
                ["python3", "-c", f"""
import urllib.request
import sys
req = urllib.request.Request('{url}', headers={{'User-Agent': 'Mozilla/5.0'}})
try:
    resp = urllib.request.urlopen(req, timeout=30)
    print(resp.read().decode('utf-8', errors='replace')[:50000])
except Exception as e:
    print(f'ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
"""],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                print(f"  ❌ Ошибка загрузки: {result.stderr[:200]}")
                self.stats["errors"] += 1
                return None
            html_content = result.stdout
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            self.stats["errors"] += 1
            return None
        
        # Определяем домен если не указан
        if not domain:
            domain = self._detect_domain(html_content)
        
        # Сохраняем сырой контент
        vault_path = KNOWLEDGE_DOMAINS.get(domain, {}).get("vault_path", "knowledge/misc/")
        ensure_dir(f"{VAULT_DIR}/{vault_path}")
        
        # Генерируем имя файла
        from urllib.parse import urlparse
        parsed = urlparse(url)
        slug = parsed.path.split('/')[-1][:50] or "index"
        filename = f"{slug}.md"
        filepath = f"{VAULT_DIR}/{vault_path}{filename}"
        
        # Записываем markdown
        with open(filepath, 'w') as fout:
            fout.write("# " + str(slug) + "\n\n")
            fout.write("> Источник: " + str(url) + "\n")
            fout.write("> Обработано: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
            fout.write("> Домен: " + str(domain) + "\n\n")
            if tags:
                fout.write("**Теги:** {', '.join(tags)}\n\n")
            fout.write("---\n\n")
            # Упрощённый текст (без HTML тегов)
            import re
            text = re.sub(r'<[^>]+>', ' ', html_content)
            text = re.sub(r'\s+', ' ', text).strip()
            f(text[:10000])  # Первые 10000 символов
        
        self.mark_processed(sid, slug, "url", filepath)
        self.stats["added"] += 1
        print(f"  ✅ Сохранено: {filepath}")
        return filepath
    
    # ── Источник 2: Файл ──
    
    def process_file(self, filepath, domain=None, tags=None):
        """Обрабатывает локальный файл."""
        if not os.path.exists(filepath):
            print(f"  ❌ Файл не найден: {filepath}")
            self.stats["errors"] += 1
            return None
        
        sid = file_hash(filepath)
        if self.is_processed(sid):
            print(f"  ⏳ Уже обработан: {filepath}")
            self.stats["skipped"] += 1
            return None
        
        print(f"  📄 Обработка файла: {filepath}")
        
        # Читаем файл
        with open(filepath, 'r', errors='replace') as f:
            content = f.read()
        
        # Определяем домен
        if not domain:
            domain = self._detect_domain(content)
        
        vault_path = KNOWLEDGE_DOMAINS.get(domain, {}).get("vault_path", "knowledge/misc/")
        ensure_dir(f"{VAULT_DIR}/{vault_path}")
        
        filename = os.path.basename(filepath)
        dest = f"{VAULT_DIR}/{vault_path}{filename}"
        
        # Копируем с метаданными
        with open(dest, 'w') as fout:
            fout.write("> Оригинал: " + str(filepath) + "\n")
            fout.write("> Обработано: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
            fout.write("> Домен: " + str(domain) + "\n\n")
            if tags:
                fout.write("**Теги:** {', '.join(tags)}\n\n")
            fout.write("---\n\n")
            fout.write(content)
        
        self.mark_processed(sid, filename, "file", dest)
        self.stats["added"] += 1
        print(f"  ✅ Сохранено: {dest}")
        return dest
    
    # ── Источник 3: Текст напрямую ──
    
    def process_text(self, text, title, domain=None, tags=None, source=None):
        """Обрабатывает текст напрямую."""
        sid = hashlib.md5(f"{title}:{text[:100]}".encode()).hexdigest()
        if self.is_processed(sid):
            print(f"  ⏳ Уже обработано: {title}")
            self.stats["skipped"] += 1
            return None
        
        if not domain:
            domain = self._detect_domain(text)
        
        vault_path = KNOWLEDGE_DOMAINS.get(domain, {}).get("vault_path", "knowledge/misc/")
        ensure_dir(f"{VAULT_DIR}/{vault_path}")
        
        # Генерируем имя файла
        slug = title.lower().replace(' ', '_')[:50]
        filename = f"{slug}.md"
        filepath = f"{VAULT_DIR}/{vault_path}{filename}"
        
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        tag_line = ""
        if tags:
            tag_line = "**Теги:** " + ', '.join(tags) + "\n\n"
        source_line = ""
        if source:
            source_line = "> Источник: " + str(source) + "\n"
        
        content = (
            "# " + str(title) + "\n\n"
            + source_line
            + "> Обработано: " + now + "\n"
            + "> Домен: " + str(domain) + "\n\n"
            + tag_line
            + "---\n\n"
            + text
        )
        
        with open(filepath, 'w') as fout:
            fout.write(content)
        
        self.mark_processed(sid, title, "text", filepath)
        self.stats["added"] += 1
        print(f"  ✅ Сохранено: {filepath}")
        return filepath
    
    # ── Источник 4: arXiv paper ──
    
    def process_arxiv(self, arxiv_id, tags=None):
        """Обрабатывает статью с arXiv."""
        sid = f"arxiv:{arxiv_id}"
        if self.is_processed(sid):
            print(f"  ⏳ Уже обработан: {arxiv_id}")
            self.stats["skipped"] += 1
            return None
        
        print(f"  📚 Обработка arXiv: {arxiv_id}")
        
        # Скачиваем через arxiv API
        url = f"https://arxiv.org/abs/{arxiv_id}"
        try:
            result = subprocess.run(
                ["python3", "-c", f"""
import urllib.request, json, sys
# Пробуем получить через API
api_url = 'https://export.arxiv.org/api/query?id_list={arxiv_id}'
req = urllib.request.Request(api_url, headers={{'User-Agent': 'Mozilla/5.0'}})
try:
    resp = urllib.request.urlopen(req, timeout=30)
    print(resp.read().decode('utf-8', errors='replace'))
except Exception as e:
    print(f'ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
"""],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                print(f"  ❌ Ошибка: {result.stderr[:200]}")
                self.stats["errors"] += 1
                return None
            xml_content = result.stdout
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            self.stats["errors"] += 1
            return None
        
        # Парсим XML (упрощённо)
        import re
        title = re.search(r'<title>(.*?)</title>', xml_content, re.DOTALL)
        title = title.group(1).strip().replace('\n', ' ') if title else arxiv_id
        summary = re.search(r'<summary>(.*?)</summary>', xml_content, re.DOTALL)
        summary = summary.group(1).strip().replace('\n', ' ') if summary else ""
        
        domain = self._detect_domain(title + " " + summary)
        vault_path = KNOWLEDGE_DOMAINS.get(domain, {}).get("vault_path", "knowledge/papers/")
        ensure_dir(f"{VAULT_DIR}/{vault_path}")
        
        filename = f"arxiv_{arxiv_id.replace('/', '_')}.md"
        filepath = f"{VAULT_DIR}/{vault_path}{filename}"
        
        with open(filepath, 'w') as fout:
            fout.write("# " + str(title) + "\n\n")
            fout.write("> Источник: https://arxiv.org/abs/" + str(arxiv_id) + "\n")
            fout.write("> Обработано: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
            fout.write("> Домен: " + str(domain) + "\n\n")
            if tags:
                fout.write("**Теги:** {', '.join(tags)}\n\n")
            fout.write("---\n\n")
            fout.write("## Аннотация\n\n" + str(summary) + "\n")
        
        self.mark_processed(sid, title, "arxiv", filepath)
        self.stats["added"] += 1
        print(f"  ✅ Сохранено: {filepath}")
        return filepath
    
    # ── Вспомогательные методы ──
    
    def _detect_domain(self, text):
        """Автоматически определяет домен по ключевым словам."""
        text_lower = text.lower()
        scores = {}
        for domain, config in KNOWLEDGE_DOMAINS.items():
            score = sum(1 for kw in config["keywords"] if kw.lower() in text_lower)
            if score > 0:
                scores[domain] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "misc"
    
    def sync_to_gbrain(self):
        """Синхронизирует новые файлы с GBrain."""
        print("\n🔄 Синхронизация с GBrain...")
        
        # gbrain sync
        result = subprocess.run(
            ["gbrain", "sync", "--repo", VAULT_DIR],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("  ✅ GBrain sync завершён")
        else:
            print(f"  ⚠️ GBrain sync: {result.stderr[:200]}")
        
        # Генерируем эмбеддинги для новых чанков
        embed_script = f"{WORKSPACE}/projects/gbrain-embed-local/embed_local.py"
        if os.path.exists(embed_script):
            result = subprocess.run(
                ["python3", embed_script],
                capture_output=True, text=True, timeout=600
            )
            if result.returncode == 0:
                print("  ✅ Эмбеддинги обновлены")
            else:
                print(f"  ⚠️ Embeddings: {result.stderr[:200]}")
    
    def save(self):
        """Сохраняет состояние."""
        save_processed(self.processed)
    
    def print_stats(self):
        """Выводит статистику."""
        print(f"\n📊 Статистика:")
        print(f"  Добавлено: {self.stats['added']}")
        print(f"  Обновлено: {self.stats['updated']}")
        print(f"  Пропущено: {self.stats['skipped']}")
        print(f"  Ошибки: {self.stats['errors']}")
        print(f"  Всего в базе: {self.processed['stats']['total']}")


# ─── CLI ─────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Knowledge Pipeline")
    sub = parser.add_subparsers(dest="command")
    
    # URL
    p_url = sub.add_parser("url", help="Обработать URL")
    p_url.add_argument("url")
    p_url.add_argument("--domain", default=None)
    p_url.add_argument("--tags", nargs="*", default=None)
    
    # File
    p_file = sub.add_parser("file", help="Обработать файл")
    p_file.add_argument("path")
    p_file.add_argument("--domain", default=None)
    p_file.add_argument("--tags", nargs="*", default=None)
    
    # Text
    p_text = sub.add_parser("text", help="Обработать текст")
    p_text.add_argument("title")
    p_text.add_argument("--file", default=None)  # прочитать из файла
    p_text.add_argument("--domain", default=None)
    p_text.add_argument("--tags", nargs="*", default=None)
    p_text.add_argument("--source", default=None)
    
    # arXiv
    p_arxiv = sub.add_parser("arxiv", help="Обработать arXiv статью")
    p_arxiv.add_argument("id")
    p_arxiv.add_argument("--tags", nargs="*", default=None)
    
    # Sync
    sub.add_parser("sync", help="Синхронизировать с GBrain")
    
    # Stats
    sub.add_parser("stats", help="Показать статистику")
    
    args = parser.parse_args()
    
    pipeline = KnowledgePipeline()
    
    if args.command == "url":
        pipeline.process_url(args.url, args.domain, args.tags)
    elif args.command == "file":
        pipeline.process_file(args.path, args.domain, args.tags)
    elif args.command == "text":
        if args.file:
            with open(args.file) as fin:
                text = fin.read()
        else:
            text = sys.stdin.read()
        pipeline.process_text(text, args.title, args.domain, args.tags, args.source)
    elif args.command == "arxiv":
        pipeline.process_arxiv(args.id, args.tags)
    elif args.command == "sync":
        pipeline.sync_to_gbrain()
    elif args.command == "stats":
        pass
    else:
        parser.print_help()
    
    pipeline.save()
    pipeline.print_stats()

if __name__ == "__main__":
    main()
