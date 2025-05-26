import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Simple query example: Search for an artist
results = sp.search(q='artist:Drake', type='artist')

# Display artist information
for idx, artist in enumerate(results['artists']['items']):
    print(f"{idx + 1}. {artist['name']} - Popularity: {artist['popularity']}")
