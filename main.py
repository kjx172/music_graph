import spotipy
from spotipy.oauth2 import SpotifyOAuth

from Auth import spotify_connection
from GatherTracks import get_playlists, load_or_fetch_user_tracks
from CollectSongData import get_track_attributes

# Run authorization function to get connection
sp = spotify_connection()

# Gets the list of user playlists based on username
user_playlists = get_playlists(sp)

# Gets a list of songs in each playlist
df = load_or_fetch_user_tracks(sp, user_playlists)

# Get the track attributes for all of the tracks
#expanded_df = get_track_attributes(sp, df)

test_ids = [
    "11dFghVXANMlKmJXsNCbNl",  # Example valid Spotify track ID
    "6rqhFgbbKwnb9MLmUQDhG6"
]
print(sp.audio_features(test_ids))