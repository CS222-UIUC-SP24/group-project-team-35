import requests
import spotipy
import pandas as pd
import asyncio
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
load_dotenv()
import os



client_id = '06e96c265aed4f81b22f190fda0046d5'
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
client = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client)

SongDict = {}


def clearDict():
    SongDict.clear()
    


def search(artist_name, song):
    query = f"artist:{artist_name} track:{song}" # using f string to format the query properly for the web API
    result = sp.search(q= query, type = ["track"], limit = 1) # returns the first result of the song lookup, can be changed by adjusting the limit variable
    print(result)
    SongDict[song] = result
    return result




def search_song(artist_name, track_name):
    base_url = "https://api.spotify.com/v1/search"
    query = f"artist:{artist_name} track:{track_name}" 
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }
    params = {
        "q": query,
        "type": "track"
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error:", response.status_code)

