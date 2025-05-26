import pandas as pd
import time
import os

def get_playlists(sp):
    print("Enter Spotify username (user ID): ")

    while True:
        # Prompt user for Spotify username
        username = input()

        # Attempt to fetch user’s playlists
        try:
            user_playlists = sp.user_playlists(username)
            break
        except:
            print("Error: please enter valid username")

    return user_playlists

    '''
    # Extract and print playlist names
    print(f"\nPlaylists for {username}:")
    for idx, item in enumerate(user_playlists['items']):
        print(f"{idx + 1}. {item['name']} ({item['tracks']['total']} tracks)")
    '''

def get_all_tracks_from_playlist(sp, playlist_id):
    """Helper function to fetch all tracks from a playlist with pagination."""
    all_tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
        items = response['items']
        if not items:
            break
        all_tracks.extend(items)
        offset += 100
    return all_tracks

def get_total_user_tracks(sp, user_playlists):
    # Storage
    track_set = set()  # To prevent duplicates
    track_data = []    # To build a DataFrame

    # Loop through each playlist in the users list of playlists
    for playlist in user_playlists['items']:
        
        # Get the playlist id for this playlist and extrack tracks
        playlist_id = playlist['id']

        # Fetch ALL tracks from this playlist, even if it has > 100
        playlist_tracks = get_all_tracks_from_playlist(sp, playlist_id)

        # For each track in the playlists tracklist
        for item in playlist_tracks:
            # Get the track
            track = item['track']
            if not track:
                continue  # skip if local file or deleted
            
            # Get track id and add it to list if not seen before
            track_id = track['id']
            if track_id and track_id not in track_set:
                track_set.add(track_id)
                track_data.append({
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'track_id': track_id
                })
    # Convert to DataFrame
    df = pd.DataFrame(track_data)

    # Export df to csv to reduce api calls
    df.to_csv('unique_user_tracks.csv', index=False)

    return df

    # print(f"Collected {len(df)} unique tracks.")

def load_or_fetch_user_tracks(sp, user_playlists, cache_file='unique_user_tracks.csv', max_age_sec=86400):
    '''Check if a csv file has been generated in the last 24 hours'''

    # If recent csv file has been generated use that to reduce api calls
    if os.path.exists(cache_file):
        age = time.time() - os.path.getmtime(cache_file)
        if age < max_age_sec:
            print("Loading tracks from cache...")
            return pd.read_csv(cache_file)

    # Otherwise query spotify
    print("Fetching fresh data from Spotify...")
    df = get_total_user_tracks(sp, user_playlists)
    return df