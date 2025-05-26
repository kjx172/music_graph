import spotipy
from spotipy.oauth2 import SpotifyOAuth

from Auth import spotify_connection
from GatherTracks import get_playlists, get_total_user_tracks

# Run authorization function to get connection
sp = spotify_connection()

# Query user on whether to collect songs
while True:
    update = input("Would you like to update your stored song list (if first time select yes): y/n?")
    if update == 'y':
        # Gets the list of user playlists based on username
        user_playlists = get_playlists(sp)

        # Gets a list of songs in each playlist
        get_total_user_tracks(sp, user_playlists)
        break

    elif update == 'n':
        print("understood using cached tracklist...")
        break

    else:
        print("Error: please enter y/n")
