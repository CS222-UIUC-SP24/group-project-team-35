import spotipy
import sys
from auth import spotify_oauth, access_token

# consider making a spotipy global object

# assuming input from stdin
if len(sys.argv) == 0:
    print('No song selected')

query = ''.join(sys.argv[1])
print('Query: ', query)

possible_targets = ['album', 'artist', 'track', 'episode']

sp = spotipy.Spotify(auth=access_token, oauth_manager=spotify_oauth)

results = sp.search(q=query, type=possible_targets)

# each has useful properties: id, href, name
tracks = results['tracks']['items']
artists = results['artists']['items']
albums = results['albums']['items']
episodes = results['episodes']['items']

print(results)

