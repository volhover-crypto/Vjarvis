---
name: whisper-stt
version: 1.0.0
description: Локальная транскрибация аудио/видео через OpenAI Whisper. Бесплатный, без API-ключей. Поддерживает русский, английский и другие языки. Форматы вывода: txt, json, srt, vtt.
---

# Whisper STT — Голос в текст

## Быстрый старт

```bash
python3 /root/.openclaw/workspace/skills/whisper-stt/scripts/transcribe.py audio.mp3
```

## Параметры

| Параметр | По умолчанию | Описание |
|----------|--------------|----------|
| `--model` | small | Модель: tiny, base, small, medium, large, large-v3-turbo |
| `--lang` | auto | Язык: ru, en, zh, ja, auto |
| `--format` | txt | Формат: json, txt, srt, vtt |
| `-o` | stdout | Файл вывода |

## Рекомендации по моделям

| Модель | Размер | Скорость | Качество | Когда использовать |
|--------|--------|----------|----------|-------------------|
| tiny | ~75 MB | ⚡⚡⚡ | Базовое | Быстрые тесты, английский |
| base | ~140 MB | ⚡⚡ | Хорошее | Быстрая транскрибация |
| small | ~460 MB | ⚡ | Отличное | **Рекомендуется для русского** |
| medium | ~1.5 GB | 🐢 | Отличное | Длинные записи, высокое качество |
| large | ~3 GB | 🐢🐢 | Максимальное | Максимальная точность |

## Примеры

```bash
# Русская речь, текст
python3 transcribe.py voice.mp3 --model small --lang ru

# Субтитры
python3 transcribe.py video.mp4 --model medium --format srt -o subs.srt

# Полный JSON с таймкодами
python3 transcribe.py meeting.mp3 --model large --format json -o result.json
```

## Зависимости
- `openai-whisper` (pip install openai-whisper)
- `torch` (устанавливается вместе с whisper)
- `ffmpeg` (системный пакет)
