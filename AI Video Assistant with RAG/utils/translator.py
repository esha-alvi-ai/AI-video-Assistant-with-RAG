from deep_translator import GoogleTranslator

from utils.config import SUPPORTED_LANGUAGES


def normalize_language(language: str) -> str:
    language = language.lower().strip()
    return SUPPORTED_LANGUAGES.get(language, language)


def translate_text_to_english(text: str, source_language: str) -> str:
    source_code = normalize_language(source_language)

    if source_code == "en":
        return text

    translator = GoogleTranslator(source=source_code, target="en")
    return translator.translate(text)