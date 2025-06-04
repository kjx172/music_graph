import pandas as pd
from Auth import spotify_connection
from GatherTracks import get_playlists, get_list_of_tracks
from GetAudioFiles import download_tracks_from_df, num_downloaded_tracks
from DivideAudioFiles import split_mp3_files
from GraphData import visualize_data

if __name__ == "__main__":
    # Run authorization function to get connection
    sp = spotify_connection()
    total_tracks = None

    # Ask user on whether to collect songs
    while True:
        update_tracklist = input("Would you like to download a playlist: y/n? ")
        if update_tracklist == 'y':
            # Gets the list of user playlists based on username
            user_playlists = get_playlists(sp)

            print("Retrieved user playlists: ")
            for i, playlist in enumerate(user_playlists['items']):
                print(i, ": ", playlist['name'])

            while True:
                target_playlist_num = int(input("Which playlist would you like to download? (enter a number): "))

                if target_playlist_num < len(user_playlists['items']):
                    # Gets a list of songs in each playlist
                    total_tracks = get_list_of_tracks(sp, user_playlists, target_playlist_num)
                    break
                else:
                    print("Error, please enter a number")
                
            break

        # Uses cached tracks
        elif update_tracklist == 'n':
            total_tracks = pd.read_csv('collected_track_list.csv')
            print("understood using cached tracklist...")
            break

        else:
            print("Error: please enter y/n")

    print("You have", len(total_tracks), "spotify tracks collected total")
    print()

    # Ask user if wants to download updated tracklist (now downloading each playlist seperatly)
    while True:
        update_downloads = input ("Would you like to update your downloaded songs from tracklist: y/n?")
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
    print()

    # Asks user if wants to split downloaded tracks into clips
    while True:
        update_clips = input ("Would you like to divide your downloads into clips: y/n?")
        if update_clips == 'y':
            # Splits downloaded songs into mp3 files
            split_mp3_files(
                source_dir="downloads",
                clip_length_sec=30,
                output_dir="clips",
                max_workers=3
            )
            break

        # Uses cached clips
        elif update_clips == 'n':
            print("understood using cached clips...")
            break

        else:
            print("Error: please enter y/n")

    ### RUN MODEL IN WSL RIGHT HERE ###

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
