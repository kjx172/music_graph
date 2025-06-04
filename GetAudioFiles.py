import yt_dlp
import pandas as pd
import time
import random
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

def empty_folder(folder_path):
    """Empties a folder by removing all its contents."""
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path) # Deletes the folder and everything inside
            os.makedirs(folder_path) # Recreates the folder
        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"Error: Folder '{folder_path}' does not exist.")

def num_downloaded_tracks(target_dir="downloads"):
    '''Return how many tracks are in the downloads directory'''
    if not os.path.exists(target_dir):
        return 0
    
    return sum(
        1 for entry in os.scandir(target_dir) if entry.is_file()
    )

def download_track(row, output_dir="downloads"):
    '''Download tracks using yt_dlp'''

    query = f"ytsearch1:{row.track_name} {row.artist} {row.album} official audio" # Youtube search
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'ffmpeg_location': r'C:\Program Files\ffmpeg\bin',
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([query])
        return True, row.track_name
    except Exception as e:
        return False, f"{row.track_name} → {e}"
    
def download_tracks_from_df(total_tracks, max_workers=3):
    '''Outputs how many tracks have been downloaded from df (excluding already downloaded tracks)'''
    successes, fails = 0, []

    # Empties the folder of previous downloads
    empty_folder("downloads")

    # Utilizes threads to reduce amount of time downloading takes
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(download_track, row) for row in total_tracks.itertuples()]
        for fut in as_completed(futures):
            ok, msg = fut.result()
            if ok:
                successes += 1
            else:
                fails.append(msg)
            time.sleep(random.uniform(0.5, 1.0))    # light throttle

    print(f"✅ Downloaded {successes}/{len(total_tracks)} tracks")
    if fails:
        print("⚠️  Failed downloads:")
        for f in fails:
            print("   •", f)

