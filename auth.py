import spotipy.oauth2 as SpotifyOAuth
import os

# THIS PROBABLY IS UNNECESSARY BECAUSE DOCKER SHOULD HANDLE ENV VARIABLES
from dotenv import load_dotenv
load_dotenv()

application_scopes = "streaming" # add other scopes as necessary

spotify_oauth = SpotifyOAuth.SpotifyOAuth(
                             client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                             client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                             redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
                             scope=application_scopes)

# redirect uri must be changed

auth_url = spotify_oauth.get_authorize_url()

# change these from prints to work with the discord api as needed
print('Follow this url to authorize access and input the auth code below: ', auth_url)
auth_code = input("Enter authorization code: ")

token_info = spotify_oauth.get_access_token(auth_code)
access_token = None
if token_info:
    access_token = token_info['access_token']
    print("Successfully logged in with token: ", access_token)
else:
    print("Authorization failed")


