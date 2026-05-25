import os

from utils.audio_processor import download_youtube_audio, extract_audio_from_video
from utils.config import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, SUBTITLE_EXTENSIONS
from utils.subtitle_processor import process_subtitle_to_english_text
from utils.transcriber import transcribe_audio_to_english


def detect_file_type(file_path: str) -> str:
    extension = os.path.splitext(file_path)[1].lower()

    if extension in VIDEO_EXTENSIONS:
        return "video"

    if extension in AUDIO_EXTENSIONS:
        return "audio"

    if extension in SUBTITLE_EXTENSIONS:
        return "subtitle"

    raise ValueError(f"Unsupported file type: {extension}")


def process_meeting_input(
    source: str,
    source_language: str,
    input_mode: str,
    model_size: str = "base",
) -> dict:
    """
    input_mode:
        youtube
        uploaded_video
        uploaded_audio
        uploaded_subtitle

    source_language:
        english / hindi / urdu
    """

    if input_mode == "youtube":
        audio_path = download_youtube_audio(source)

        transcription =transcribe_audio_to_english(
    audio_path=audio_path,
    source_language=source_language,
    model_size=model_size,
    chunk_length_minutes=5,
)

        return {
            "input_mode": input_mode,
            "source_language": source_language,
            "audio_path": audio_path,
            "english_text": transcription["english_text"],
            "segments": transcription["segments"],
            "english_srt_path": None,
        }

    if input_mode == "uploaded_video":
        audio_path = extract_audio_from_video(source)

        transcription = transcribe_audio_to_english(
    audio_path=audio_path,
    source_language=source_language,
    model_size=model_size,
    chunk_length_minutes=5,
)

        return {
            "input_mode": input_mode,
            "source_language": source_language,
            "audio_path": audio_path,
            "english_text": transcription["english_text"],
            "segments": transcription["segments"],
            "english_srt_path": None,
        }

    if input_mode == "uploaded_audio":
        transcription =transcribe_audio_to_english(
    audio_path=audio_path,
    source_language=source_language,
    model_size=model_size,
    chunk_length_minutes=5,
)

        return {
            "input_mode": input_mode,
            "source_language": source_language,
            "audio_path": source,
            "english_text": transcription["english_text"],
            "segments": transcription["segments"],
            "english_srt_path": None,
        }

    if input_mode == "uploaded_subtitle":
        subtitle_result = process_subtitle_to_english_text(
            subtitle_path=source,
            source_language=source_language,
        )

        return {
            "input_mode": input_mode,
            "source_language": source_language,
            "audio_path": None,
            "english_text": subtitle_result["english_text"],
            "segments": [],
            "english_srt_path": subtitle_result["english_srt_path"],
        }

    raise ValueError(f"Invalid input mode: {input_mode}")