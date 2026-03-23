#!/usr/bin/env python3
"""
Spotify bypass downloader - scarica brani Spotify senza usare l'API
Usa scraping della pagina web per ottenere i metadati
"""

import sys
import re
import requests
from pathlib import Path
import yt_dlp

def get_spotify_metadata(spotify_url):
    """Ottiene metadati da Spotify via scraping della pagina web"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(spotify_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html = response.text
        
        # Estrai titolo dalla meta tag og:title
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        title = title_match.group(1) if title_match else None
        
        # Estrai descrizione che contiene l'artista
        desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        description = desc_match.group(1) if desc_match else None
        
        # Estrai artista dalla descrizione (formato: "Song · Artist · Year")
        artist = None
        if description:
            parts = description.split(' · ')
            if len(parts) >= 2:
                artist = parts[1]
        
        if not title or not artist:
            # Fallback: cerca nel JSON-LD
            jsonld_match = re.search(r'<script type="application/ld\+json">(.+?)</script>', html, re.DOTALL)
            if jsonld_match:
                import json
                try:
                    data = json.loads(jsonld_match.group(1))
                    if isinstance(data, list):
                        for item in data:
                            if item.get('@type') == 'MusicRecording':
                                title = title or item.get('name')
                                if item.get('byArtist'):
                                    artist = artist or item['byArtist'].get('name')
                except:
                    pass
        
        return title, artist
        
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
        return None, None

def search_and_download_youtube(query, output_dir=".", audio_format="mp3"):
    """Cerca e scarica da YouTube"""
    try:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }],
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'default_search': 'ytsearch1',  # Cerca su YouTube
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n🔍 Ricerca su YouTube: {query}")
            info = ydl.extract_info(query, download=True)
            
            if 'entries' in info:
                # È una playlist/ricerca
                video = info['entries'][0]
                title = video['title']
            else:
                title = info['title']
            
            print(f"✅ Scaricato: {title}")
            return True
            
    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python spotify_bypass_downloader.py <spotify_url> [output_dir] [formato]")
        print("Esempio: python spotify_bypass_downloader.py 'https://open.spotify.com/track/...' ./downloads mp3")
        sys.exit(1)
    
    spotify_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    audio_format = sys.argv[3] if len(sys.argv) > 3 else "mp3"
    
    # Valida URL Spotify
    if "open.spotify.com" not in spotify_url or "track" not in spotify_url:
        print("❌ URL Spotify non valido")
        sys.exit(1)
    
    print(f"🎵 Elaborazione brano Spotify...")
    print(f"📁 Cartella output: {output_dir}")
    print(f"🎼 Formato: {audio_format}\n")
    
    # Ottieni metadati
    title, artist = get_spotify_metadata(spotify_url)
    
    if not title or not artist:
        print("❌ Impossibile ottenere i metadati da Spotify")
        print("💡 Suggerimento: fornisci manualmente 'Artista - Titolo'")
        sys.exit(1)
    
    print(f"📝 Trovato: {artist} - {title}")
    
    # Cerca e scarica da YouTube
    query = f"{artist} - {title}"
    success = search_and_download_youtube(query, output_dir, audio_format)
    
    if success:
        print(f"\n✅ Completato!")
    else:
        print(f"\n❌ Download fallito")
        sys.exit(1)

if __name__ == "__main__":
    main()
