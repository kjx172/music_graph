import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_playlists(sp):
    print("Enter Spotify username (user ID): ")

    while True:
        # Prompt user for Spotify username
        username = input()

        # Attempt to fetch user’s playlists
        try:
            results = sp.user_playlists(username)
            break
        except:
            print("Error: please enter valid username")

    # Extract and print playlist names
    print(f"\nPlaylists for {username}:")
    for idx, item in enumerate(results['items']):
        print(f"{idx + 1}. {item['name']} ({item['tracks']['total']} tracks)")
