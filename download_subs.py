import yt_dlp
import sys
import codecs

# Fix console encoding issues
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

ydl_opts = {
    'quiet': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['hi'],
    'skip_download': True,
}

url = 'https://youtu.be/uCKZMAqA4CY'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    print("Downloaded subtitle info.")
