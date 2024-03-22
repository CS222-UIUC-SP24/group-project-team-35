import requests
import spotipy
import pandas as pd
import asyncio
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv('keys.env')

client_id = '06e96c265aed4f81b22f190fda0046d5'
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
print("this is the secret")
print(os.environ)
print(client_secret)
client = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client)

SongDict = {}
PlaylistDict = {}

def clearDict():
    SongDict.clear()
    


def search(artist_name, song):
    query = f"artist:{artist_name} track:{song}" # using f string to format the query properly for the web API
    result = sp.search(q= query, limit = 1, type='track') # returns the first result of the song lookup, can be changed by adjusting the limit variable
    print(result)
    SongDict[song] = result
    return result




def searchSong(artist_name, track_name):
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


def playlistCreationTest(user_id,):
    newPlayList = sp.user_playlist_create(user_id, "User Playlist for " + str(user_id), public=True, collaborative=False, description='') #idk if string concatenation is allowed in function parameters
    PlaylistDict[user_id] = newPlayList # the user_id is the key, and  the playlist object is the value inside of the dictionary. Ideally each user is only going to have one playlist in here at a time.

def helpPlaylistComparison(PlayListDict): 
    playlistList = []
    for playlist in PlayListDict.values(): # creates a copy of a the dictionary in an easier to use list that will be edited, rather than adjust the dictionary directly. 
        playlistList.append(playlist)
    return playlistList



def recursivePlaylistComparison(firstPlaylist, secondPlaylist, playListList, user_id): #for good practice, assume the user is the owner of the first playlist that is passed into the intial call of the function 
    if firstPlaylist == None:
        return secondPlaylist
    if secondPlaylist == None:
        return firstPlaylist
    recommendedPlaylist = sp.user_playlist_create(user_id, "SpotiPy group Playlist", public=True, collaborative=False, description='')
    firstPlaylistTracks = sp.playlist_items(recommendedPlaylist, firstPlaylist) 
    secondPlaylistTracks = sp.playlist_items(recommendedPlaylist,secondPlaylist)
    sp.playlist_add_items(firstPlaylistTracks) #I'm almost sure that the return type for xPlaylistTracks are song objects, but the documentation is not very clear about things like this. might need to parse each xPlaylistTracks and append individually
    sp.playlist_add_items(secondPlaylistTracks)
    if len(playListList) == 0:
        return recommendedPlaylist
    else:
        recursivePlaylistComparison(recommendedPlaylist,playListList.pop(0), playListList, user_id)
    return recommendedPlaylist
    """in here we can add functionality to either reccomend playlists progresivelly (call playlist.getRecommendations() every time the function recurses) or
    call at the end of the function when recursion finishes."""




    