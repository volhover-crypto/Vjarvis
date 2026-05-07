#!/usr/bin/env python3
import argparse
from faster_whisper import WhisperModel

def transcribe(audio_path: str, model_name: str = "small", lang: str = "ru", device: str = "cpu") -> str:
    model = WhisperModel(
        model_name,
        device=device,
        compute_type="int8" if device == "cpu" else "float16",
    )
    segments, _ = model.transcribe(audio_path, language=lang, vad_filter=True)
    text = " ".join(seg.text.strip() for seg in segments if seg.text and seg.text.strip()).strip()
    return text

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audio", required=True)
    p.add_argument("--model", default="small")
    p.add_argument("--lang", default="ru")
    p.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    args = p.parse_args()
    text = transcribe(args.audio, args.model, args.lang, args.device)
    print(text if text else "")

if __name__ == "__main__":
    main()
