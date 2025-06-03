import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from Auth import spotify_connection
from GatherTracks import get_playlists, get_total_user_tracks
from GetAudioFiles import download_tracks_from_df, num_downloaded_tracks
from DivideAudioFiles import split_mp3_files
from GraphData import visualize_data

# Run authorization function to get connection
sp = spotify_connection()
total_tracks = None

# Ask user on whether to collect songs
while True:
    update_tracklist = input("Would you like to update your stored song list (if first time select yes): y/n?")
    if update_tracklist == 'y':
        # Gets the list of user playlists based on username
        user_playlists = get_playlists(sp)

        # Gets a list of songs in each playlist
        total_tracks = get_total_user_tracks(sp, user_playlists)
        break

    # Uses cached tracks
    elif update_tracklist == 'n':
        total_tracks = pd.read_csv('unique_user_tracks.csv')
        print("understood using cached tracklist...")
        break

    else:
        print("Error: please enter y/n")

print("You have", len(total_tracks), "spotify tracks collected total")
print()

# Ask user if wants to download updated tracklist
while True:
    update_downloads = input ("Would you like to update your downloaded songs list (if updated tracklist select yes): y/n?")
    if update_downloads == 'y':
        # Downloads the users tracks from dataframe
        download_tracks_from_df(total_tracks)
        break

    # Uses cached downloads
    elif update_downloads == 'n':
        print("understood using cached downloads...")
        break

    else:
        print("Error: please enter y/n")

print("You have", num_downloaded_tracks(), "tracks downloaded")

# Asks user if wants to split downloaded tracks into clips
while True:
    update_clips = input ("Would you like to update your downloaded clips (if updated downloads select yes): y/n?")
    if update_clips == 'y':
        # Splits downloaded songs into mp3 files
        split_mp3_files()
        break

    # Uses cached clips
    elif update_clips == 'n':
        print("understood using cached clips...")
        break

    else:
        print("Error: please enter y/n")

# Asks user if want to run audio models on clips

while True:
    ran_models = input ("Have you ran RunAudioModels.py within WSL or other linux subsystem?")
    if ran_models == 'y':
        # Runs the visualization function
        visualize_data()

    
    elif ran_models == 'n':
        print("Please Exit code and run RunAudioModels.py within WSL or other linux subsystem to extract audio embeddings")
        break

    else:
        print("Error: please enter y/n")
