import spotipy
from spotipy.oauth2 import SpotifyOAuth

from Auth import spotify_connection
from GatherPlaylists import get_playlists

# Run authorization function to get connection
sp = spotify_connection()

get_playlists(sp)