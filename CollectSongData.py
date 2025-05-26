import pandas as pd
import time
import os

from spotipy.exceptions import SpotifyException


def get_track_attributes(sp, df, cache_file='user_tracks_with_audio_features.csv', max_age_sec=86400):
    # If a features csv file has been generated in the past 24 hours use that
    if os.path.exists(cache_file):
        file_age = time.time() - os.path.getmtime(cache_file)
        if file_age < max_age_sec:
            print("Loading cached audio features from file...")
            return pd.read_csv(cache_file)

    # Otherwise run API calls   
    print("Fetching fresh audio features from Spotify...")

    # Convert the df to a list of track ids
    track_ids = [tid for tid in df['track_id'] if pd.notna(tid) and isinstance(tid, str) and tid.strip()]
    audio_features_list = []

    # API allow for a max of 100 track IDs to be searched
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        if not batch:
            continue
        assert len(batch) <= 100
        
        try:
            features = sp.audio_features(batch)

            # Ensures missing tracks are ignored
            for feature in features:
                if feature:
                    audio_features_list.append(feature)
        except SpotifyException as e:
            print(f"Error (status {e.http_status}) on batch {i}-{i+100}: {e}")
            time.sleep(5)

    # Convert and merge with original df
    features_df = pd.DataFrame(audio_features_list)
    merged_df = df.merge(features_df, left_on='track_id', right_on='id', how='left')

    # Save for future use
    merged_df.to_csv(cache_file, index=False)
    print(f"Audio features saved to: {cache_file}")

    return merged_df