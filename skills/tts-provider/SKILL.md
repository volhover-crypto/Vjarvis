---
name: tts-provider
version: 1.0.0
description: Управление TTS-провайдерами: Edge TTS (бесплатно), ElevenLabs (API-ключ). Переключение голосов, генерация аудио, отправка в Telegram.
---

# TTS Provider — Управление голосовым выводом

## Доступные провайдеры

### Edge TTS (бесплатный, по умолчанию)
- Русские голоса: Dmitry (мужской), Svetlana (женский)
- Английские: Guy, Tony, Jenny, Sara и др.
- Без API-ключа

### ElevenLabs (платный, лучше качества)
- Множество голосов, включая русские
- Требует API-ключ
- Free tier: 10K символов/мес

## Команды

### Сгенерировать аудио через Edge TTS
```bash
~/.openclaw/workspace/voice-messages/bin/python -c "
import edge_tts, asyncio
async def tts():
    text = 'Текст для озвучки'
    voice = 'ru-RU-DmitryNeural'
    tts = edge_tts.Communicate(text, voice)
    await tts.save('/root/.openclaw/workspace/output.ogg')
    print('OK')
asyncio.run(tts())
"
```

### Отправить аудио в Telegram
```bash
openclaw message send --channel telegram --target <chat_id> --media /root/.openclaw/workspace/output.ogg
```

## Доступные голоса Edge TTS

### Русские
- `ru-RU-DmitryNeural` — мужской (Dmitry)
- `ru-RU-SvetlanaNeural` — женский (Svetlana)

### Английские (мужские)
- `en-US-GuyNeural` — глубокий мужской
- `en-US-TonyNeural` — средний мужской
- `en-US-DavisNeural` — молодой мужской
- `en-US-JasonNeural` — спокойный мужской
- `en-GB-RyanNeural` — британский мужской

### Английские (женские)
- `en-US-JennyNeural` — женский
- `en-US-SaraNeural` — женский
- `en-US-MichelleNeural` — женский

## Настройка ElevenLabs (опционально)

1. Зарегистрируйся на https://elevenlabs.io
2. Получи API-ключ в настройках профиля
3. Сохрани ключ: `echo 'ELEVENLABS_API_KEY=sk_xxx' >> ~/.openclaw/workspace/voice-messages/.env`
4. Добавь в openclaw.json:
```json5
{
  "messages": {
    "tts": {
      "provider": "elevenlabs",
      "elevenlabs": {
        "apiKey": "sk_xxx",
        "voiceId": "your_voice_id",
        "model": "eleven_multilingual_v2"
      }
    }
  }
}
```
