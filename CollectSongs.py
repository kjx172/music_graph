import spotipy
from spotipy.oauth2 import SpotifyOAuth

from Auth import spotify_connection
from GatherPlaylists import get_playlists, get_total_user_tracks

# Run authorization function to get connection
sp = spotify_connection()

# Gets the list of user playlists based on username
user_playlists = get_playlists(sp)

# Gets a list of songs in each playlist
get_total_user_tracks(sp, user_playlists)