import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv
load_dotenv()

def spotify_connection():
    # Spotify credentials
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    REDIRECT_URI = 'https://www.google.com/'

    # Set scope for accessing playlists
    SCOPE = 'user-library-read playlist-read-private playlist-read-collaborative'

    # Authenticate
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    return sp