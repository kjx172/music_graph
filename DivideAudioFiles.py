import os
from pydub import AudioSegment
from pydub.utils import which

from dotenv import load_dotenv
load_dotenv()

# Ensures PyDub knows where to find ffmpeg
AudioSegment.converter = which("ffmpeg") or os.getenv("FFMPEG_PATH")

def split_mp3_files(source_dir="downloads", clip_length_sec=30, output_dir="clips"):
    '''Splits mp3 files into 30s clips to be passed into the models'''

    # Make a clips output directory if one doesnt exist already
    os.makedirs(output_dir, exist_ok=True)

    # For every mp3 file in clips
    for filename in os.listdir(source_dir):
        if filename.lower().endswith('.mp3'):

            # Loads the audio file into a pydub.AdudioSegment object for manipulation
            filepath = os.path.join(source_dir, filename)
            audio = AudioSegment.from_mp3(filepath)

            # Get the duration of the audio and calculate the number of clips needed for a 30s long clip window
            duration_ms = len(audio)
            clip_length_ms = clip_length_sec * 1000
            num_clips = duration_ms // clip_length_ms + (1 if duration_ms % clip_length_ms != 0 else 0) # Add extra clip if remainder after dividng by 30
            
            # Gets the file name for the audio file
            base_name = os.path.splitext(filename)[0]
            
            # Slices 30s segments from audio and formats the clip names
            for i in range(num_clips):
                start_ms = i * clip_length_ms
                end_ms = min(start_ms + clip_length_ms, duration_ms)
                clip = audio[start_ms:end_ms]
                
                output_name = f"{base_name}--{i + 1}--.mp3"
                output_path = os.path.join(output_dir, output_name)
                clip.export(output_path, format="mp3")
                print(f"✅ Saved: {output_name}")