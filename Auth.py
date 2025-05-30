import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv
load_dotenv()

def spotify_connection():
    # Get spotify credentials from .env file
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")

    # Redirect URI set to google.com for now,
    REDIRECT_URI = 'https://www.google.com/'

    # Can read users saved songs and albums, private playlists, and collaborative playlists
    SCOPE = 'user-library-read playlist-read-private playlist-read-collaborative'

    # Authenticate app using the provided credentials
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    return sp