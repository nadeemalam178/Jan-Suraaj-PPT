import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re

def download_google_image(query, filename):
    print(f"Searching Google Images for: {query}")
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google images puts image URLs in scripts or src of img tags. 
        # For a basic requests scrape, img tags often have thumbnail URLs (data:image or encrypted-tbn0)
        # Let's find the first valid http image URL.
        img_tags = soup.find_all('img')
        img_url = None
        for img in img_tags:
            src = img.get('src')
            if src and src.startswith('http') and 'gstatic' in src:
                # This is a google thumbnail, it's small but it's guaranteed to be relevant.
                img_url = src
                break
            elif src and src.startswith('http'):
                img_url = src
                break
                
        # If we didn't find one in src, look for it in scripts
        if not img_url:
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'http' in script.string:
                    matches = re.findall(r'(https?://[^"\']+\.(?:jpg|jpeg|png))', script.string, re.IGNORECASE)
                    if matches:
                        img_url = matches[0]
                        break
                        
        if img_url:
            print(f"Found image for {query}: {img_url[:50]}...")
            img_data = requests.get(img_url, headers=headers).content
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Successfully downloaded {filename}")
            return True
        else:
            print(f"Could not extract image URL for {query}")
            return False
    except Exception as e:
        print(f"Error for {query}: {e}")
        return False

queries = {
    "title": "Prashant Kishor Jan Suraaj portrait high resolution",
    "padyatra": "Prashant Kishor Padyatra walking crowd Jan Suraaj Bihar",
    "party_launch": "Prashant Kishor Jan Suraaj party launch stage 2 October 2024",
    "victory": "Prashant Kishor celebrating election victory flowers",
    "ashram": "Bhitiharwa Gandhi Ashram West Champaran Bihar",
    "campaign": "Prashant Kishor addressing rally crowd Jan Suraaj",
    "bpsc_protest": "Bihar BPSC student protest Patna",
    "timeline": "Bihar political map infographic"
}

IMG_DIR = r"c:\Users\alamn\Downloads\JS PPT\scraped_images"
os.makedirs(IMG_DIR, exist_ok=True)

for key, query in queries.items():
    filename = os.path.join(IMG_DIR, f"{key}.jpg")
    download_google_image(query, filename)

print("DOWNLOAD COMPLETE")
