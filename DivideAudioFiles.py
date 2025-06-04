import os
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import which
from functools import partial
from concurrent.futures import ProcessPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()

# Ensures PyDub knows where to find ffmpeg
AudioSegment.converter = which("ffmpeg") or os.getenv("FFMPEG_PATH")

def split_one_mp3(file_path: str, clip_len_s: int, out_dir: str) -> str:
    ''' Woker function to split one mp3, save clips, and return filename on success'''

    # Loads the audio file into a pydub.AdudioSegment object for manipulation
    audio = AudioSegment.from_mp3(file_path)

    # Get the duration of the audio and calculate the number of clips needed for a 30s long clip window
    duration_ms = len(audio)
    clip_length_ms = clip_len_s * 1000
    num_clips = duration_ms // clip_length_ms + (1 if duration_ms % clip_length_ms != 0 else 0) # Add extra clip if remainder after dividng by 30

    # Gets the file name for the audio file
    base_name = Path(file_path).stem

    # Slices 30s segments from audio and formats the clip names
    for i in range(num_clips):
        start = i * clip_length_ms
        end = min(start + clip_length_ms, duration_ms)
        clip = audio[start:end]
        
        output_name = f"{base_name}--{i + 1}--.mp3"
        clip.export(Path(out_dir) / output_name, format="mp3")
    
    return base_name

def split_mp3_files(source_dir="downloads", clip_length_sec=30, output_dir="clips", max_workers = 3):
    '''Splits mp3 files into 30s clips to be passed into the models'''

    # Make a clips output directory if one doesnt exist already
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Gets a list of the files in the downloads directory
    mp3_files = [str(Path(source_dir, f))
                 for f in os.listdir(source_dir)
                 if f.lower().endswith(".mp3")]

    # Outlines that the split file will have the same paramaters for each worker
    worker = partial(split_one_mp3,
                     clip_len_s=clip_length_sec,
                     out_dir=output_dir)
    
    done, failed = 0, []

    # On Windows / WSL always guard multiprocessing code!
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(worker, fp): fp for fp in mp3_files}
        for fut in as_completed(futures):
            try:
                base = fut.result()
                done += 1
                print(f"✅  {base} - done")
            except Exception as e:
                failed.append((futures[fut], e))

    print(f"\nFinished: {done}/{len(mp3_files)} files")
    if failed:
        print("⚠️  Failures:")
        for f, err in failed:
            print("   ", f, "→", err)

if __name__ == "__main__":
    split_mp3_files(
        source_dir="downloads",
        clip_length_sec=30,
        output_dir="clips",
        max_workers=3
    )