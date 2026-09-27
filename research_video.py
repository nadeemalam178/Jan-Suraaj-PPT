import yt_dlp
import json

ydl_opts = {
    'quiet': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'skip_download': True,
    'dump_single_json': True
}

url = 'https://youtu.be/uCKZMAqA4CY'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    print("TITLE:", info.get('title'))
    print("\nDESCRIPTION:")
    print(info.get('description', 'No description'))
    
    # We can also check if subtitles are available
    subs = info.get('subtitles', {})
    auto_subs = info.get('automatic_captions', {})
    print(f"\nSubtitles available: {list(subs.keys())}")
    print(f"Auto subtitles available: {list(auto_subs.keys())}")
