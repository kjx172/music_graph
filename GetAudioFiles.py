import yt_dlp
import pandas as pd
import time
import random
import os

def is_track_downloaded(track_name, output_dir="downloads"):
    if not os.path.exists(output_dir):
        return -1
    
    for filename in os.listdir(output_dir):
        if track_name.lower() in filename.lower():
            return True
    return False

def num_downloaded_tracks(target_dir="downloads"):
    if not os.path.exists(target_dir):
        return 0
    
    return sum(
        1 for entry in os.scandir(target_dir) if entry.is_file()
    )

def download_track(track_name, artist_name, album_name, output_dir="downloads"):
    '''Download tracks using yt_dlp'''
    query = f"ytsearch1:{track_name} {artist_name} {album_name} official audio"
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
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([query])
    
def download_tracks_from_df(total_tracks):
    count = 0

    # Loop through each row in the df and download the track
    for row in total_tracks.itertuples():

        # If track has already been downloaded skip download
        if is_track_downloaded(row.track_name):
            print(f"Skipping (already downloaded): {row.track_name}")
            continue

        try:
            print(f"Downloading: {row.track_name} by {row.artist}")
            download_track({row.track_name}, {row.artist}, {row.album})
            count += 1 # Track how many downloaded
            time.sleep(random.uniform(2, 4))  # Random delay download to prevent rate limiting
        except Exception as e:
            print("unable to download track: ", {row.track_name})

    print("total tracks downloaded: ", count)
