import yt_dlp

def download_track(track_name, output_dir="downloads"):
    query = f"ytsearch1:{track_name} audio"
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

download_track("Daft Punk - One More Time")