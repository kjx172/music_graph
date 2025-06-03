### RUN IN WSL, ENSURE MODELS ARE DOWNLOADED (requires Essentia-TensorFlow wrappers) ###

import os
import csv
import pandas as pd
from collections import defaultdict
import sys
sys.path.append("/usr/local/lib/python3/dist-packages")

from essentia.standard import (
    MonoLoader, TensorflowPredictEffnetDiscogs
)

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import contextlib


# Utilizing a smaller set of clips to test model functionality
CLIP_DIR = '/mnt/c/Users/kisit/projects/Music visualizer/testclips'

OUTPUT_PATH = '/mnt/c/Users/kisit/projects/Music visualizer/modeloutput/song_embeddings.csv'

# ──────────────── helpers ─────────────────────────────────────────

# ──────────────── model instances ────────────────────────────────
# Load all models (one for temp testing)
model = TensorflowPredictEffnetDiscogs(
        graphFilename='effnetdiscogs/effnetdiscogs-bs64-1.pb',
        input='serving_default_melspectrogram',
        output='PartitionedCall:1'
    )

# ──────────────── aggregate predictions ──────────────────────────

# Prepare storage
song_embeddings = defaultdict(list)

# Go through each clip and ensure its a mp3 file
for file in os.listdir(CLIP_DIR):
    if file.endswith('.mp3'):
        filepath = os.path.join(CLIP_DIR, file)

        # Load 30s clip at 16kHz mono
        audio = MonoLoader(filename=filepath, sampleRate=16000)()

        # Extract the base song name before '--'
        base = file.split('--')[0]

        # Run the model and extract embeddings, store as np array (N_patches, 1280)
        embs = np.asarray(model(audio))
        if embs.size == 0:                       # skip empty output (usually from short clips)
            continue

        clip_vec = embs.mean(axis=0)             # (1280,) collapses patches into one vector
        clip_vec /= np.linalg.norm(clip_vec)     # normalize vector (useful for cosine similarity)
        song_embeddings[base].append(clip_vec)   # append the clip to the base name

# Step 3: Average all clip vectors for each base song
final_embeddings = {}
for base, vecs in song_embeddings.items():
    vecs = np.stack(vecs, axis=0)      # guaranteed equal length vectors
    final_vec = vecs.mean(axis=0)
    final_vec /= np.linalg.norm(final_vec)
    final_embeddings[base] = final_vec
        
fieldnames = ["song_name"] + [f"d{i}" for i in range(1280)]

# Write header once
with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# Then append row by row (or in small chunks)
for song, vec in final_embeddings.items():
    row = {"song_name": song}
    for i, val in enumerate(vec):
        row[f"d{i}"] = float(val)
    with open(OUTPUT_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)