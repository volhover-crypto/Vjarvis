import os
import sys
from groq import Groq

# Инициализация клиента Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

def transcribe_audio(file_path, language="ru"):
    """Транскрибация аудиофайла через Groq Whisper."""
    try:
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model="whisper-large-v3",
                language=language,
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"Ошибка транскрипции: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 groq_whisper.py <путь_к_файлу> [язык]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "ru"
    
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        sys.exit(1)
        
    print(f"Транскрибирую {file_path}...")
    result = transcribe_audio(file_path, language)
    print("\n--- Результат ---")
    print(result)
