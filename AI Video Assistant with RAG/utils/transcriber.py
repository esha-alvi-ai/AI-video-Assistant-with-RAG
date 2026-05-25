import os
import math
import tempfile
from typing import Dict, List
from utils.config import FFMPEG_DIR
os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

import whisper
from pydub import AudioSegment

from utils.config import FFMPEG_DIR
from utils.translator import normalize_language

AudioSegment.converter = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(FFMPEG_DIR, "ffprobe.exe")

from utils.translator import normalize_language


def split_audio_into_chunks(
    audio_path: str,
    chunk_length_minutes: int = 5,
) -> List[str]:
    """
    Split one audio file into smaller WAV chunks.

    Example:
        60-minute meeting
        chunk_length_minutes=5
        → 12 audio chunks
    """

    audio = AudioSegment.from_file(audio_path)

    chunk_length_ms = chunk_length_minutes * 60 * 1000
    total_length_ms = len(audio)

    total_chunks = math.ceil(total_length_ms / chunk_length_ms)

    temp_dir = tempfile.mkdtemp(prefix="meeting_chunks_")
    chunk_paths = []

    for chunk_index in range(total_chunks):
        start_ms = chunk_index * chunk_length_ms
        end_ms = min(start_ms + chunk_length_ms, total_length_ms)

        chunk = audio[start_ms:end_ms]

        chunk_path = os.path.join(
            temp_dir,
            f"chunk_{chunk_index + 1:03d}.wav"
        )

        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)

    return chunk_paths


def transcribe_audio_to_english(
    audio_path: str,
    source_language: str,
    model_size: str = "base",
    chunk_length_minutes: int = 5,
) -> Dict:
    """
    Transcribe or translate audio to English using Whisper in chunks.

    English:
        task="transcribe"

    Hindi / Urdu:
        task="translate"

    Returns:
        {
            "language": "en/hi/ur",
            "task": "transcribe/translate",
            "english_text": "...",
            "segments": [...]
        }
    """

    language_code = normalize_language(source_language)

    if language_code == "en":
        task = "transcribe"
    else:
        task = "translate"

    model = whisper.load_model(model_size)

    chunk_paths = split_audio_into_chunks(
        audio_path=audio_path,
        chunk_length_minutes=chunk_length_minutes,
    )

    full_text_parts = []
    all_segments = []

    for index, chunk_path in enumerate(chunk_paths, start=1):
        print(f"Processing chunk {index}/{len(chunk_paths)}: {chunk_path}")

        result = model.transcribe(
            chunk_path,
            language=language_code,
            task=task,
            fp16=False,
        )

        chunk_text = result.get("text", "").strip()

        if chunk_text:
            full_text_parts.append(chunk_text)

        segments = result.get("segments", [])

        for segment in segments:
            segment["chunk_index"] = index

        all_segments.extend(segments)

    english_text = "\n\n".join(full_text_parts)

    return {
        "language": language_code,
        "task": task,
        "english_text": english_text,
        "segments": all_segments,
        "chunks_processed": len(chunk_paths),
    }


if __name__ == "__main__":
    result = transcribe_audio_to_english(
        audio_path="downloads/uMzUB89uSxU.wav",
        source_language="english",
        model_size="base",
        chunk_length_minutes=5,
    )

    print("Language:", result["language"])
    print("Task:", result["task"])
    print("Chunks processed:", result["chunks_processed"])
    print(result["english_text"])