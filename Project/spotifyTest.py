import requests
import spotipy
import pandas as pd
import asyncio
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
load_dotenv()
import os
from dotenv import load_dotenv
import sqlite3
from collections import defaultdict
load_dotenv('keys.env')



client_id = '06e96c265aed4f81b22f190fda0046d5'
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
client = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client)

SongDict = {}
PlaylistDict = {}

def clearDict():
    SongDict.clear()
    


def search(artist_name, song):
    query = f"artist:{artist_name} track:{song}" # using f string to format the query properly for the web API
    result = sp.search(q= query, type = ["track"], limit = 5) # returns the first result of the song lookup, can be changed by adjusting the limit variable
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



async def suggest(numSongs):
    connection = sqlite3.connect(os.getenv("DATA_PATH"))
    c = connection.cursor()
    rows = c.execute('SELECT * FROM Songs')
    artists = defaultdict(int)
    tracks = defaultdict(int)
    
    for song in rows:
        artists[song[0]] += 1
        tracks[song[1]] += 1

    #artists = sorted(artists.items(), key=lambda item: item[1])
    tracks = sorted(tracks.items(), key=lambda item: item[1]) # lambda tells my sorting function that I want to sort by the second part of the tuple (the value, instead of the key)
    #topArtists = artists[:5] 
    topTracks = tracks[:5]
    reccommendedArts = []
    reccommendedTracks = []
    #for artist, _ in topArtists:
        #reccommendedArts.append(artist)
    for track, _ in topTracks: #underscore is just because im not using the second part of the tuples
        reccommendedTracks.append(track)

    results = sp.recommendations(seed_tracks= reccommendedTracks, limit = numSongs) #Limit ranges from 1-100 and returns n amount of songs, so set as desired (such as if ur gonna queue n amount of songs from this function)

    connection.close()
    return results


    