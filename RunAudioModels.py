### RUN IN WSL, ENSURE MODELS ARE DOWNLOADED ###

import os
import pandas as pd
from collections import defaultdict
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredictMusiCNN
import numpy as np

CLIP_DIR = '/mnt/c/Users/kisit/projects/Music visualizer/clips'
# Load all models
models = {
    'genre_discogs400': TensorflowPredictEffnetDiscogs(
        graphFilename='home\kjx172\essentia-models\genre_model\genre_discogs400-discogs-effnet-1.pb',
        output='predictions',
        poolingType='avg'
    ),
    'mtg_jamendo_moodtheme': TensorflowPredictMusiCNN(
        graphFilename='home\kjx172\essentia-models\mood_model\mtg_jamendo_moodtheme-discogs-effnet-1.pb',
        output='predictions',
        poolingType='avg'
    ),
    'danceability': TensorflowPredictEffnetDiscogs(
        graphFilename='home\kjx172\essentia-models\danceability_model\danceability-discogs-effnet-1.pb',
        output='prediction',
        poolingType='avg'
    ),
    'engagement': TensorflowPredictEffnetDiscogs(
        graphFilename='home\kjx172\essentia-models\engagement_model\engagement_regression-discogs-effnet-1.pb',
        output='prediction',
        poolingType='avg'
    ),
    'approachability': TensorflowPredictEffnetDiscogs(
        graphFilename='home\kjx172\essentia-models\approachability_model\approachability_regression-discogs-effnet-1.pb',
        output='prediction',
        poolingType='avg'
    ),
    'mtg_jamendo_instrument': TensorflowPredictMusiCNN(
        graphFilename='home\kjx172\essentia-models\Instrument_model\mtg_jamendo_instrument-discogs-effnet-1.pb',
        output='predictions',
        poolingType='avg'
    )
}

# Prepare storage
aggregated_results = defaultdict(lambda: defaultdict(list))

# Go through each clip
for file in os.listdir(CLIP_DIR):
    if file.endswith('.mp3'):
        path = os.path.join(CLIP_DIR, file)
        audio = MonoLoader(filename=path)()

        # Extract base name from format: name--1--.mp3
        base_name = file.split('--')[0]

        for model_name, model in models.items():
            result = model(audio)
            if isinstance(result, float):  # Scalar prediction
                aggregated_results[base_name][model_name].append(result)
            else:  # Vector prediction
                aggregated_results[base_name][model_name].append(np.array(result))

# Average results across segments
final_results = []

for base_name, model_outputs in aggregated_results.items():
    row = {'base_name': base_name}

    for model_name, values in model_outputs.items():
        if isinstance(values[0], np.ndarray):
            avg_vector = np.mean(values, axis=0)
            row[model_name] = ','.join(f"{v:.4f}" for v in avg_vector)
        else:
            row[model_name] = round(float(np.mean(values)), 4)

    final_results.append(row)

# Output to CSV
df = pd.DataFrame(final_results)
df.to_csv('averaged_clip_features.csv', index=False)
print("✅ Features saved to averaged_clip_features.csv")
