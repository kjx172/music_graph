import spotipy
from spotipy.oauth2 import SpotifyOAuth

def spotify_connection():
    # Spotify credentials
    client_id = 'ce390915e2f4405ab2e0574b4e8f43b5'
    client_secret = '48466a59bf8845f5a219fd52ee7eec67'
    REDIRECT_URI = 'https://www.google.com/'

    # Set scope for accessing playlists
    SCOPE = 'playlist-read-private playlist-read-collaborative'

    # Authenticate
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    return sp