import yt_dlp
import pandas as pd

def download_track(track_name, artist_name, album_name, output_dir="downloads"):
    query = f"ytsearch1:{track_name} {artist_name} {album_name} official audio"
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'ffmpeg_location': r'C:\Program Files\ffmpeg\bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([query])
    
def download_tracks_from_df(total_tracks):
    # Loop through each row in the df
    for row in total_tracks.itertuples():
         print(f"Track name: {row.track_name}, artist: {row.artist}, album: {row.album}")

