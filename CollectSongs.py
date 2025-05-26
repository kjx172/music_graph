import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ================================ Auth ======================================== #
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

# ================================ Auth ======================================== #

# Prompt user for Spotify username
username = input("Enter Spotify username (user ID): ")

# Fetch user’s playlists
results = sp.user_playlists(username)

# Extract and print playlist names
print(f"\nPlaylists for {username}:")
for idx, item in enumerate(results['items']):
    print(f"{idx + 1}. {item['name']} ({item['tracks']['total']} tracks)")
