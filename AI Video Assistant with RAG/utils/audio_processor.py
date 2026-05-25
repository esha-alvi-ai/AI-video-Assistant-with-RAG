import os
import shutil
import subprocess
import yt_dlp

from utils.config import DOWNLOAD_DIR, FFMPEG_DIR


os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_template = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "ffmpeg_location": FFMPEG_DIR,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info)
        wav_file = os.path.splitext(downloaded_file)[0] + ".wav"

        if not os.path.exists(wav_file):
            raise FileNotFoundError(f"WAV file was not created: {wav_file}")

        return wav_file


def extract_audio_from_video(video_path: str) -> str:
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_audio = os.path.join(DOWNLOAD_DIR, f"{base_name}.wav")

    ffmpeg_exe = os.path.join(FFMPEG_DIR, "ffmpeg.exe")

    command = [
        ffmpeg_exe,
        "-y",
        "-i",
        video_path,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        output_audio,
    ]

    subprocess.run(command, check=True)

    if not os.path.exists(output_audio):
        raise FileNotFoundError(f"Audio was not created: {output_audio}")

    return output_audio


def save_uploaded_file(uploaded_file, save_dir: str) -> str:
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, uploaded_file.name)

    with open(file_path, "wb") as file:
        shutil.copyfileobj(uploaded_file, file)

    return file_path