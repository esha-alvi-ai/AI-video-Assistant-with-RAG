import os
from dotenv import load_dotenv

load_dotenv()

mistral_api_key = os.getenv("mistral_api_key")

DOWNLOAD_DIR = "downloads"
UPLOAD_DIR = "uploads"
SUBTITLE_DIR = "subtitles"
OUTPUT_DIR = "outputs"
CHROMA_DIR = "chroma_db"

FFMPEG_DIR = (
    r"C:\Users\ABC\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.1-full_build\bin"
)

SUPPORTED_LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "urdu": "ur",
    "en": "en",
    "hi": "hi",
    "ur": "ur",
}

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".mov", ".avi", ".webm"]
AUDIO_EXTENSIONS = [".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"]
SUBTITLE_EXTENSIONS = [".srt"]