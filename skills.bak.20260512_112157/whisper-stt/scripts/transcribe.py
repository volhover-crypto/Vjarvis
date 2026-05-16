#!/usr/bin/env python3
"""
Whisper STT — транскрибация аудио/видео через OpenAI Whisper.
Использование:
  python3 transcribe.py <file> [--model tiny|base|small|medium|large|large-v3-turbo] [--lang ru|en|auto] [--format json|txt|srt|vtt]
"""

import argparse
import json
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Whisper STT транскрибация")
    parser.add_argument("file", help="Путь к аудио/видео файлу")
    parser.add_argument("--model", default="small", 
                        choices=["tiny", "base", "small", "medium", "large", "large-v3-turbo"],
                        help="Модель Whisper (по умолчанию: small)")
    parser.add_argument("--lang", default="auto", help="Язык (ru, en, auto)")
    parser.add_argument("--format", default="txt", 
                        choices=["json", "txt", "srt", "vtt"],
                        help="Формат вывода (по умолчанию: txt)")
    parser.add_argument("--output", "-o", help="Файл вывода (по умолчанию: stdout)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Ошибка: файл не найден: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        import whisper
    except ImportError:
        print("Ошибка: openai-whisper не установлен. Установите: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)
    
    print(f"Загрузка модели {args.model}...", file=sys.stderr)
    model = whisper.load_model(args.model)
    
    print(f"Транскрибация: {args.file}", file=sys.stderr)
    lang = None if args.lang == "auto" else args.lang
    result = model.transcribe(args.file, language=lang)
    
    output = format_output(result, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Результат сохранён: {args.output}", file=sys.stderr)
    else:
        print(output)

def format_output(result, fmt):
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    elif fmt == "txt":
        return result["text"]
    elif fmt == "srt":
        return to_srt(result["segments"])
    elif fmt == "vtt":
        return to_vtt(result["segments"])
    return result["text"]

def to_srt(segments):
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_time(seg["start"], srt=True)
        end = format_time(seg["end"], srt=True)
        lines.append(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n")
    return "\n".join(lines)

def to_vtt(segments):
    lines = ["WEBVTT\n"]
    for seg in segments:
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        lines.append(f"{start} --> {end}\n{seg['text'].strip()}\n")
    return "\n".join(lines)

def format_time(seconds, srt=False):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    if srt:
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

if __name__ == "__main__":
    main()
