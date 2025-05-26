import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_playlists(sp):
    # Prompt user for Spotify username
    username = input("Enter Spotify username (user ID): ")

    # Fetch user’s playlists
    results = sp.user_playlists(username)

    # Extract and print playlist names
    print(f"\nPlaylists for {username}:")
    for idx, item in enumerate(results['items']):
        print(f"{idx + 1}. {item['name']} ({item['tracks']['total']} tracks)")
