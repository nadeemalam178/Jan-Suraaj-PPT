import yt_dlp
import cv2
import os
import sys
import codecs

# Fix console encoding issues for windows
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

url = 'https://youtu.be/uCKZMAqA4CY'

ydl_opts = {
    'format': 'bestvideo/best', 
    'quiet': True,
    'no_warnings': True,
}

IMG_DIR = r"c:\Users\alamn\Downloads\JS PPT\documentary_stills"
os.makedirs(IMG_DIR, exist_ok=True)

# Define 8 specific timestamps in the video to extract (in seconds)
# Assuming a ~40 min video, let's sample at evenly spaced interesting points
# 2 min (intro), 5 min, 10 min, 15 min, 20 min, 25 min, 30 min, 35 min
timestamps = [120, 300, 600, 900, 1200, 1500, 1800, 2100]
filenames = ["title.jpg", "padyatra.jpg", "party_launch.jpg", "victory.jpg", 
             "ashram.jpg", "campaign.jpg", "bpsc_protest.jpg", "timeline.jpg"]

print("Extracting video stream URL...")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get('url', None)
        fps = info_dict.get('fps', 30)

    if video_url:
        print("Stream URL acquired. Extracting frames...")
        cap = cv2.VideoCapture(video_url)
        
        for i, ts in enumerate(timestamps):
            # Calculate frame number
            frame_no = int(ts * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            
            if ret:
                save_path = os.path.join(IMG_DIR, filenames[i])
                cv2.imwrite(save_path, frame)
                print(f"Saved frame {i+1}/8: {filenames[i]} at {ts}s")
            else:
                print(f"Failed to read frame at {ts}s")
                
        cap.release()
        print("Frame extraction complete.")
    else:
        print("Could not find a valid video stream URL.")
except Exception as e:
    print(f"Error occurred: {e}")
