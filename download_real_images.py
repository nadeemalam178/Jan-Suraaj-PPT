import urllib.request
import os

images = {
    'title': 'https://images.indianexpress.com/2024/10/Prashant-Kishor.jpg',
    'padyatra': 'https://images.indianexpress.com/2022/10/Prashant-Kishor-1.jpg',
    'party_launch': 'https://images.indianexpress.com/2024/10/Prashant-Kishor-1.jpg',
    'victory': 'https://images.indianexpress.com/2020/02/Prashant-Kishor.jpg',
    'ashram': 'https://images.indianexpress.com/2022/10/Prashant-Kishor-1.jpg',
    'campaign': 'https://images.indianexpress.com/2022/05/Prashant-Kishor-1.jpg',
    'bpsc_protest': 'https://images.indianexpress.com/2024/10/Prashant-Kishor.jpg',
    'timeline': 'https://images.indianexpress.com/2022/05/Prashant-Kishor-1.jpg'
}

IMG_DIR = r'c:\Users\alamn\Downloads\JS PPT\real_images'
os.makedirs(IMG_DIR, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for key, url in images.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            # We already updated create_jansuraaj_ppt.py to expect .jpg (except timeline, which is .png, so let's save timeline as .png)
            ext = '.png' if key == 'timeline' else '.jpg'
            path = os.path.join(IMG_DIR, f'{key}{ext}')
            with open(path, 'wb') as f:
                f.write(response.read())
            print(f'Successfully downloaded {key}')
    except Exception as e:
        print(f'Failed to download {key}: {e}')
