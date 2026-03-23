# YouTube Audio Downloader

Mini tool standalone per scaricare audio da YouTube, basato su `yt-dlp` (la stessa libreria usata da spotify-downloader).

## Requisiti

- Python 3.10+
- yt-dlp
- ffmpeg (per la conversione MP3)

## Installazione dipendenze

```powershell
pip install yt-dlp
```

Per MP3, serve anche **ffmpeg**. Su Windows:
```powershell
# Con chocolatey
choco install ffmpeg

# Oppure scarica da https://ffmpeg.org/download.html
```

## Utilizzo

### Scarica il video predefinito

```powershell
python youtube_audio_downloader.py
```

Scarica l'audio dal video predefinito: https://www.youtube.com/watch?v=-UmsDdkoy7A

### Scarica un video specifico

```powershell
python youtube_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Specifica directory e formato

```powershell
# Sintassi: python youtube_audio_downloader.py [URL] [OUTPUT_DIR] [FORMAT]
python youtube_audio_downloader.py "https://www.youtube.com/watch?v=-UmsDdkoy7A" "./my_music" "m4a"
```

## Formati supportati

- `mp3` (default) - richiede ffmpeg
- `m4a` - formato nativo, non richiede conversione
- `opus` - alta qualità, formato WebM

## Esempi

```powershell
# Download in MP3 (default)
python youtube_audio_downloader.py

# Download in M4A (più veloce, no conversione)
python youtube_audio_downloader.py "https://www.youtube.com/watch?v=-UmsDdkoy7A" "./downloads" "m4a"

# Download in OPUS (massima qualità)
python youtube_audio_downloader.py "https://www.youtube.com/watch?v=-UmsDdkoy7A" "./downloads" "opus"

# Download in cartella specifica
python youtube_audio_downloader.py "https://www.youtube.com/watch?v=-UmsDdkoy7A" "C:/Music"
```

## Output

I file vengono salvati nella cartella specificata (default: `./downloads`) con il nome del video originale.

## Note

- Il tool usa le stesse tecniche di spotify-downloader per garantire qualità audio ottimale
- La velocità di download dipende dalla connessione e dalla qualità audio richiesta
- M4A è generalmente più veloce perché non richiede conversione post-download
