import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify credentials
client_id = 'ce390915e2f4405ab2e0574b4e8f43b5'
client_secret = '48466a59bf8845f5a219fd52ee7eec67'

# Authentication setup
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
