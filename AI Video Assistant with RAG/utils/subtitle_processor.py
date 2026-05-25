import os
import pysrt

from deep_translator import GoogleTranslator
from utils.config import OUTPUT_DIR
from utils.translator import normalize_language


def srt_to_plain_text(srt_path: str) -> str:
    subtitles = pysrt.open(srt_path, encoding="utf-8")
    lines = []

    for sub in subtitles:
        text = sub.text.strip().replace("\n", " ")
        if text:
            lines.append(text)

    return "\n".join(lines)


def translate_srt_to_english(
    input_srt: str,
    output_srt: str,
    source_language: str,
) -> str:
    os.makedirs(os.path.dirname(output_srt), exist_ok=True)

    source_code = normalize_language(source_language)
    subtitles = pysrt.open(input_srt, encoding="utf-8")

    if source_code == "en":
        subtitles.save(output_srt, encoding="utf-8")
        return output_srt

    translator = GoogleTranslator(source=source_code, target="en")

    for sub in subtitles:
        text = sub.text.strip().replace("\n", " ")

        if not text:
            continue

        try:
            sub.text = translator.translate(text)
        except Exception as error:
            print(f"Subtitle translation failed at index {sub.index}: {error}")
            sub.text = text

    subtitles.save(output_srt, encoding="utf-8")
    return output_srt


def process_subtitle_to_english_text(
    subtitle_path: str,
    source_language: str,
    output_dir: str = OUTPUT_DIR,
) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(subtitle_path))[0]
    english_srt_path = os.path.join(output_dir, f"{base_name}_english.srt")

    translate_srt_to_english(
        input_srt=subtitle_path,
        output_srt=english_srt_path,
        source_language=source_language,
    )

    english_text = srt_to_plain_text(english_srt_path)

    return {
        "english_srt_path": english_srt_path,
        "english_text": english_text,
    }


if __name__ == "__main__":
    print("subtitle_processor.py loaded successfully")