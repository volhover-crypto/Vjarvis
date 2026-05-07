# N8N Voice Transcriber — Документация

## Что делает

Хук автоматически распознаёт голосовые сообщения из Telegram через n8n webhook + Gemini API.

## Как работает

1. Пользователь отправляет голосовое сообщение в Telegram
2. OpenClaw получает событие `message:received` с контентом `<media:audio>`
3. Хук находит самый свежий аудио-файл в `/root/.openclaw/media/inbound/`
4. Конвертирует OGG/OPUS в WAV через ffmpeg (16kHz mono)
5. Кодирует WAV в base64
6. Отправляет POST на n8n webhook: `https://mdked.fvds.ru/webhook/transcribe`
7. n8n передаёт base64 в Gemini для распознавания речи
8. n8n возвращает JSON: `{"transcript": "...", "status": "ok"}`
9. Хук выводит транскрипцию в чат через `event.messages.push()`

## Архитектура

```
Telegram → OpenClaw Gateway → hook (message:received)
  → ffmpeg OGG→WAV → base64 → n8n webhook → Gemini API
  → transcript → event.messages.push() → чат
```

## Файлы

- **HOOK.md**: `/root/.openclaw/hooks/n8n-voice-transcriber/HOOK.md`
- **handler.ts**: `/root/.openclaw/hooks/n8n-voice-transcriber/handler.ts`
- **Логи**: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (ищет `n8n-voice`)

## Конфигурация в handler.ts

| Параметр | Значение |
|----------|----------|
| N8N_WEBHOOK_URL | `https://mdked.fvds.ru/webhook/transcribe` |
| N8N_API_KEY | (в секрете) |
| TELEGRAM_BOT_TOKEN | (в секрете) |
| MEDIA_DIR | `/root/.openclaw/media/inbound` |

## Авторизация

n8n использует кастомный Header Auth:
- Header name: `clawVoice`
- Header value: API ключ из n8n credentials

## Управление

```bash
# Статус хука
openclaw hooks list

# Проверка eligibility
openclaw hooks check

# Перезагрузка после изменений handler.ts
openclaw gateway restart
# или
systemctl --user restart openclaw-gateway
```

## Известные особенности

- На этапе `message:received` контекст НЕ содержит `mediaPath` — файл ищется по времени модификации
- Если приходят несколько аудио одновременно, может быть race condition (берётся самый свежий файл)
- OGG конвертируется в WAV для совместимости с Gemini; MP3/AAC/WAV отправляются как есть
- n8n workflow должен возвращать JSON с полем `transcript`

## Пример ответа n8n

```json
{
  "transcript": "Раз, два, три, четыре, пять, вышел зайчик погулять.",
  "status": "ok"
}
```

## Дата создания

2026-03-31

## Автор

Джарвис (по запросу Александра)
