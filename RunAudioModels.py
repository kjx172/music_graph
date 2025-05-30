### RUN IN WSL, ENSURE MODELS ARE DOWNLOADED (requires Essentia-TensorFlow wrappers) ###

import os
import pandas as pd
from collections import defaultdict
from essentia.standard import (
    MonoLoader, FrameGenerator, Windowing, Spectrum, MelBands,
    TensorflowPredictEffnetDiscogs, TensorflowPredictMusiCNN,
)
import numpy as np

CLIP_DIR = '/mnt/c/Users/kisit/projects/Music visualizer/clips'

# ──────────────── helpers ─────────────────────────────────────────

def make_effnet_patches(audio, sr=16000):
    '''Converts raw audio into log-mel spectogram patches to feed into effnet based tensorflow models'''

    # Define processing algorithims
    win  = Windowing(type='hann') # Utilize a Hann window to reduce spectral leakage (artifacts introduced due to discontinuities in time series data window)
    spec = Spectrum(size=512) # Sets window size to 512 samples resulting in a spectrum of 256 frequency bins (or lines)
    mel  = MelBands(
        numberBands=128,
        sampleRate=sr,
        inputSize=257,
        lowFrequencyBound=30,
        highFrequencyBound=sr/2
    ) # Map frequency bins to a mel scale, which is more acurate to perception of frequency rather than actual frequency

    # Splits the 1D audio signal into overlapping frames
    frames = FrameGenerator(
        audio, frameSize=512, hopSize=160, startFromZero=True
    )

    # Apply Hann window, then FFT, and finally Mel filter to each frame. results in a list of vectors T x 128, one per time frame
    mel_frames = [mel(spec(win(f))) for f in frames]
    if not mel_frames:
        return np.empty((0, 1280), np.float32)

    # Stack the mel vectors into a 2D array and convert to a log-mel scale (like human hearing)
    m = np.log10(np.maximum(1e-10, np.vstack(mel_frames)))

    # Group 10 consecutive frames to form a patch of 1280 values and only keep full groups of 10
    # Each patch corresponds to ~640ms of audio
    n_full = m.shape[0] // 10
    m = m[: n_full * 10].reshape(n_full, 10 * 128)

    # Return the final shape (N_patches, 1280) as a float32 which is needed by the tensorflow models
    return m.astype(np.float32)


def make_musicnn_patches(audio, sr=16000):
    '''Converts raw audio into log-mel spectogram patches to feed into musicnn based tensorflow models'''

    # Splits the audio into overlapping nframes of 512 samples (~32ms at 16kHz) with a hop of 256 samples (50% overlap)
    frames = FrameGenerator(audio, frameSize=512, hopSize=256, startFromZero=True)

    # Applies a hann window to reduce spectal leakage and computes the FFT of each frame)
    window = Windowing(type='hann')
    spectrum = Spectrum(size=512)

    # Converts the 257 frequency bins from FFT to 96 mel bans covering the full range (up until the Nyquist frequency)
    mel = MelBands(numberBands=96, sampleRate=sr, inputSize=257, highFrequencyBound=sr/2)

    # Converts mel spectogram values to log scale (closer to human frequency interpretation) and stacks melframes list into a matrix
    mel_frames = []
    for frame in frames:
        spec = spectrum(window(frame))
        mel_spec = mel(spec)
        log_mel = np.log10(np.maximum(mel_spec, 1e-6))
        mel_frames.append(log_mel)

    mel_frames = np.array(mel_frames)  # (T, 96)

    # Chunk into patches of 187 frames (≈1 second)
    n = mel_frames.shape[0] // 187
    if n == 0:
        return np.empty((0, 187, 96), dtype=np.float32)
    return mel_frames[:n * 187].reshape(n, 187, 96).astype(np.float32)

# ──────────────── model instances ────────────────────────────────
# Load all models
effnet_models = {
    'genre_discogs400': TensorflowPredictEffnetDiscogs(
        graphFilename='/home/kjx172/essentia-models/genre_model/genre_discogs400-discogs-effnet-1.pb',
        input='serving_default_model_Placeholder',
        output='PartitionedCall:0'
    ),
    
    'danceability': TensorflowPredictEffnetDiscogs(
        graphFilename='/home/kjx172/essentia-models/danceability_model/danceability-discogs-effnet-1.pb',
        input='model/Placeholder',
        output='model/dense/BiasAdd'
    ),
    'engagement': TensorflowPredictEffnetDiscogs(
        graphFilename='/home/kjx172/essentia-models/engagement_model/engagement_regression-discogs-effnet-1.pb',
        input='model/Placeholder',
        output='model/dense/BiasAdd'
    ),
    'approachability': TensorflowPredictEffnetDiscogs(
        graphFilename='/home/kjx172/essentia-models/approachability_model/approachability_regression-discogs-effnet-1.pb',
        input='model/Placeholder',
        output='model/dense/BiasAdd'
    )
}

musicnn_models = {
    'mtg_jamendo_moodtheme': TensorflowPredictMusiCNN(
            graphFilename='/home/kjx172/essentia-models/mood_model/mtg_jamendo_moodtheme-discogs-effnet-1.pb',
            input='model/Placeholder',
            output='model/dense_1/BiasAdd'
        ),
    'mtg_jamendo_instrument': TensorflowPredictMusiCNN(
            graphFilename='/home/kjx172/essentia-models/Instrument_model/mtg_jamendo_instrument-discogs-effnet-1.pb',
            input='model/Placeholder',
            output='model/dense/BiasAdd'
        )
}


# ──────────────── aggregate predictions ──────────────────────────

# Prepare storage
aggregated_results = defaultdict(lambda: defaultdict(list))

# Go through each clip and ensure its a mp3 file
for file in os.listdir(CLIP_DIR):
    if file.endswith('.mp3'):
        # Loads each file as mono, 16kHz audio using essentias monoloader
        audio = MonoLoader(filename=os.path.join(CLIP_DIR, file),
                        sampleRate=16000)()

        # Gets songs base name (without being split into 30s clips)
        base = file.split('--')[0]

        # Computes log-mel patches
        patches = make_effnet_patches(audio)

        # for each model: apply the model to each patch, average the predictions fpr all patches in the clip
        if patches.size:
            for name, mdl in effnet_models.items():
                preds = [mdl(v) for v in patches]         # list of (out_dim,) arrays
                aggregated_results[base][name].append(np.mean(preds, axis=0))


        # Computes log-mel patches
        patches96 = make_musicnn_patches(audio)

        # For each model: apply the model to each patch (flatten to a vector first) and average predictions across all patches in the clip
        if patches96.size:
            for name, mdl in musicnn_models.items():
                preds = [mdl(p.flatten()) for p in patches96]
                aggregated_results[base][name].append(np.mean(preds, axis=0))



# ──────────────── average across 30-s segments ───────────────────
'''Averages all 30s song clips results that share a base name, effectively running the whole song through the model'''
rows = []
for song, feats in aggregated_results.items():
    row = {'base_name': song}
    for name, vecs in feats.items():
        v = np.mean(vecs, axis=0)
        if v.size == 1:
            row[name] = float(v)
        else:
            row[name] = ','.join(f'{x:.4f}' for x in v)
    rows.append(row)

pd.DataFrame(rows).to_csv('averaged_clip_features.csv', index=False)
print('✅ Features saved to averaged_clip_features.csv')