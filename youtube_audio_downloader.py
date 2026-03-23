#!/usr/bin/env python3
"""
Mini tool per scaricare audio da YouTube
Basato su yt-dlp come spotify-downloader
"""

import sys
import os
import shutil
from pathlib import Path
from yt_dlp import YoutubeDL


def _find_ffmpeg_bin() -> str | None:
    """
    Trova la cartella bin che contiene ffmpeg.exe e ffprobe.exe.

    Priorita:
    1) variabile ambiente FFMPEG_BIN
    2) ffmpeg nel PATH
    3) percorso WinGet noto in questo ambiente
    """

    env_bin = os.environ.get("FFMPEG_BIN")
    if env_bin:
        ffmpeg = Path(env_bin) / "ffmpeg.exe"
        ffprobe = Path(env_bin) / "ffprobe.exe"
        if ffmpeg.exists() and ffprobe.exists():
            return str(Path(env_bin))

    ffmpeg_on_path = shutil.which("ffmpeg")
    ffprobe_on_path = shutil.which("ffprobe")
    if ffmpeg_on_path and ffprobe_on_path:
        return str(Path(ffmpeg_on_path).parent)

    winget_bin = Path(
        "C:/Users/s.agostini/AppData/Local/Microsoft/WinGet/Packages/"
        "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/"
        "ffmpeg-8.1-full_build/bin"
    )
    if (winget_bin / "ffmpeg.exe").exists() and (winget_bin / "ffprobe.exe").exists():
        return str(winget_bin)

    return None


def download_audio(url: str, output_dir: str = "./downloads", format: str = "mp3"):
    """
    Scarica l'audio da un video YouTube
    
    Args:
        url: URL del video YouTube
        output_dir: Directory di output (default: ./downloads)
        format: Formato audio desiderato (mp3, m4a, opus)
    """
    
    # Crea la directory di output se non esiste
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Configura il formato in base all'estensione richiesta
    if format == "m4a":
        ytdl_format = "bestaudio[ext=m4a]/bestaudio/best"
    elif format == "opus":
        ytdl_format = "bestaudio[ext=webm]/bestaudio/best"
    else:
        ytdl_format = "bestaudio"
    
    # Opzioni per yt-dlp
    ydl_opts = {
        'format': ytdl_format,
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'extract_audio': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }] if format == 'mp3' else [],
    }

    ffmpeg_bin = _find_ffmpeg_bin()
    if ffmpeg_bin:
        ydl_opts['ffmpeg_location'] = ffmpeg_bin
    
    print(f"🎵 Downloading audio from: {url}")
    print(f"📁 Output directory: {output_path.absolute()}")
    print(f"🎼 Format: {format}")
    if ffmpeg_bin:
        print(f"🛠️  FFmpeg: {ffmpeg_bin}")
    elif format == "mp3":
        print("⚠️  FFmpeg non trovato: la conversione MP3 potrebbe fallire")
    print("-" * 60)
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Estrai info prima di scaricare
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"Title: {title}")
            print(f"Duration: {duration // 60}:{duration % 60:02d}")
            print("-" * 60)
            
            # Scarica
            ydl.download([url])
            
        print(f"\n✅ Download completato!")
        print(f"📂 File salvato in: {output_path.absolute()}")
        
    except Exception as e:
        print(f"\n❌ Errore durante il download: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # URL predefinito o da command line
    default_url = "https://www.youtube.com/watch?v=-UmsDdkoy7A"
    
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = default_url
        print(f"ℹ️  Nessun URL specificato, uso quello predefinito")
    
    # Parametri opzionali
    output_directory = sys.argv[2] if len(sys.argv) > 2 else "./downloads"
    audio_format = sys.argv[3] if len(sys.argv) > 3 else "mp3"
    
    print("=" * 60)
    print("🎧 YouTube Audio Downloader")
    print("=" * 60)
    
    download_audio(video_url, output_directory, audio_format)
