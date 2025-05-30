import pandas as pd
import time
import os

def get_playlists(sp):
    '''Gets the playlists under a users username'''
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

def get_all_tracks_from_playlist(sp, playlist_id):
    """Helper function to fetch all tracks from a playlist with pagination."""

    # Initialize variables to store tracks and offsets
    all_tracks = []
    offset = 0

    # Queries spotify for 100 songs at a time until no response is recieved
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

        # Fetch ALL tracks from this playlist
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
                })
    # Convert to DataFrame
    df = pd.DataFrame(track_data)

    # Export df to csv to reduce api calls
    df.to_csv('unique_user_tracks.csv', index=False)

    print(f"Collected {len(df)} unique tracks.")

    return df