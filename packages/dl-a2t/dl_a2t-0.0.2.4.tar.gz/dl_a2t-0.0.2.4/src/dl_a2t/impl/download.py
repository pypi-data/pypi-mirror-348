from pathlib import Path

from ..utils.cache import audio_cache


def _extract_audio(url: str, output_path: str):
    from yt_dlp import YoutubeDL

    ydl_opts = {"format": "bestaudio/best", "outtmpl": output_path}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def extract_audio(url: str, output_path: str):
    path = Path(output_path)
    try:
        path.write_bytes(audio_cache[url])
    except KeyError:
        _extract_audio(url, output_path)
        audio_cache[url] = path.read_bytes()
