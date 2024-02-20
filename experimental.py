import spotipy
import spotipy.oauth2 as SpotifyOAuth
import os

application_scopes = "streaming" # add other scopes as necessary

spotify_oauth = SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                             client_secret=os.getenv('CLIENT_SECRET'),
                             redirect_uri=os.getenv('REDIRECT_URI'),
                             scope=application_scopes)

auth_url = spotify_oauth.get_authorize_url()

# change these from prints to work with the discord api as needed
print('Follow this url to authorize access and input the auth code below: ', auth_url)
auth_code = input("Enter authorization code: ")

token_info = spotify_oauth.get_access_token(auth_code)
if token_info:
    access_token = token_info['access_token']
    print("Succcessfully logged in with token: ", access_token)
else:
    print("Authorization failed")


