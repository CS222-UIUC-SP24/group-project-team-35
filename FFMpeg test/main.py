
from __future__ import unicode_literals

import discord
import os
import asyncio

from discord.ext import commands
from discord import FFmpegPCMAudio

from discord import Intents


from youtube_search import YoutubeSearch

import yt_dlp

import os
import spotifyTest



# Create an instance of a bot. Has intents to do everything for now, just to test
bot = commands.Bot(command_prefix='!', intents = Intents.all())

#not sure how to pass in ffmpeg location sooooooo ffmpeg.exe is in the same location for now
#default settings. for yt_dlp
yt_opts = {
    'format': 'bestaudio/best',
     'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    
}

#in the final implementation, should probably first search for the song on Spotify and show it to the user, so they can choose it. 
#It'll then search by the proper name on Spotify
@bot.command()
async def play(ctx, *searchTerms):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    
    songName = "".join(searchTerms[:])
    
    #searches for song with the search terms, and downloads it
    fileName = await download(songName) 
    # Get the voice channel of the user
    voice_channel = ctx.author.voice.channel

    try:
        # Connect to the voice channel
        voice_client = await voice_channel.connect()

        # Play the audio file. Had to set executable to the path, wasn't recognizign for some reason. Weird
        audio_source = FFmpegPCMAudio(executable = 'ffmpeg.exe',source = fileName)
        voice_client.play(audio_source)

        # Wait for the audio to finish playing or everyone else to leave, check every 1 second
        while voice_client.is_playing() and len(voice_channel.members) > 1:
            await asyncio.sleep(1)
        # Disconnect from the voice channel after the audio finishes playing. 
        await voice_client.disconnect()
        os.remove(fileName)

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while playing the audio.")

@bot.command()
async def download(songName="creep by radiohead"):
    
    song = await get_first_result(songName)
    fileName = 'songs/' + song['title']
    link = 'https://www.youtube.com' + song['url_suffix']
    
    try:
        yt_opts['outtmpl'] = fileName
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(e)
    return fileName + '.mp3'

async def get_first_result(search):
    results = YoutubeSearch(search, max_results=10).to_dict()

    print(results[0])
    return results[0]

@bot.command()
async def getSongSpotify(artist, song):
    result = spotifyTest.search(artist, song)
    print(result)

# Would probably want to hide token later, but should work fine for testing
bot.run("MTIwOTQwNzQ3MzIwMzgxMDMyNA.Ggoj_F.UNtYsPOJUO2Q1WlrVKp2i_ZW8iETJnuvkIEz0c")