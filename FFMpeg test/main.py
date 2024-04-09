
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

import json

from collections import namedtuple 


from dotenv import load_dotenv
load_dotenv()


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




@bot.command()
async def playSpotify(ctx, *searchTerms):
    # Check if the user is in a voice channel

    search = " ".join(searchTerms[:])
    searchSplit = search.split(",")

    songName = searchSplit[0]
    songName = songName.strip()
    artistName = ""
    if(len(searchSplit) > 1):
        artistName = searchSplit[1]
        artistName = artistName.strip()
    
    #change to an array of multiple songs, let the user pick
    spotipySongs = await getSongsSpotify(artistName, songName)
    songOptions = []
    for song in spotipySongs:
        print(song)
        songOptions.append(song['name'] + ' by ' + song['artists'][0]['name'])


    embed = discord.Embed(title="Which song is it?", description="Chooose")
    select = discord.ui.Select(
        placeholder="Select a song"
    )
    count = 0
    for song in songOptions:
        
        count += 1
        select.add_option(
            label = str(count) + ". " + song
        )
    
    async def callback(interaction): # the function called when the user is done selecting options
            await interaction.response.send_message(f"Ok you selected {(select.values[0])[3:]}!")
            songChoiceIndex = int(select.values[0][0]) - 1
            songChoice = spotipySongs[songChoiceIndex]
            song = songChoice['name'] + ', ' + songChoice['artists'][0]['name']
            await play(ctx, song)

    select.callback = callback
    view = discord.ui.View()
    view.add_item(select)

    #could add to database here. would be helpful, while I still have the spotipy stuff
    await ctx.send("Choose a song!", view = view, embed = embed)


@bot.command()
async def stop(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect() 
        await ctx.send('Im gone')
    else: 
        await ctx.send("Not in a voice channel")

queues = {}


SongFile = namedtuple('SongFile', ['fileName', 'name', 'artist'])
#currently no artist, will fill in when spotipy works good
async def addToQueue(song: SongFile, guild):
    if(not guild.id in queues):
        queues[guild.id] = []
    queues[guild.id].append(song)


@bot.command()
async def remove(ctx, queueN):
    queueNumber = int(queueN)
    serverQueue = queues[ctx.guild.id]

    deleteSong(serverQueue[queueNumber])
    serverQueue.pop(queueNumber)

async def deleteSong(song: SongFile):
    os.remove(song.fileName)

#in the final implementation, should probably first search for the song on Spotify and show it to the user, so they can choose it. 
#It'll then search by the proper name on Spotify
@bot.command()
async def play(ctx, *searchTerms):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    
    #serarch for song on spotify, gets full name with artist + song name
    #I'll use this for now, Spotify search thing is really really bad im not sure why
    fullName = " ".join(searchTerms[:])
    
    #searches on youtube with the full name, and downloads it
    link, fileName = await download(fullName) 
    
    addSong = SongFile(fileName, fullName, "Default Author")

    await addToQueue(addSong, ctx.guild)

    if(len(queues[ctx.guild.id]) > 1):
        return
    # Get the voice channel of the user
    voice_channel = ctx.author.voice.channel

    while(len(queues[ctx.guild.id]) > 0):
        print("trying my best to play", len(queues[ctx.guild.id]))
        try:
            # Connect to the voice channel
            nextSong = queues[ctx.guild.id][0]
            
            #at this point, I'd probably make a call to add this song to the database
            
            voice_client = await voice_channel.connect()

            # Play the audio file. Had to set executable to the path, wasn't recognizign for some reason. Weird
            audio_source = FFmpegPCMAudio(executable = 'ffmpeg.exe',source = nextSong.fileName)
            voice_client.play(audio_source)

            # Wait for the audio to finish playing or everyone else to leave, check every 1 second
            while voice_client.is_playing() and len(voice_channel.members) > 1:
                await asyncio.sleep(1)
            # Disconnect from the voice channel after the audio finishes playing. 
            await voice_client.disconnect()
            os.remove(nextSong.fileName)
            queues[ctx.guild.id].pop(0)
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while playing the audio.")
    
@bot.command()
async def queue(ctx):
    
    serverQueue = queues[ctx.guild.id]
    listMsg = "```"
    listMsg += "---------Now Playing----------- \n"
    listMsg += serverQueue[0].name + " - " + serverQueue[0].artist + "\n"
    listMsg += "-------------------------------\n"
    for i in range(1, min(10, len(serverQueue))):
        listMsg += str(i) + ". " + serverQueue[i].name + " - " + serverQueue[i].artist
        listMsg += "\n"
    listMsg += "```"    
    await ctx.send(listMsg)
        


#shouldn't be called by the user, it's just a bot command for me to test
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
    return link, fileName + '.mp3'

async def get_first_result(search):
    results = YoutubeSearch(search, max_results=1).to_dict()

    print(results[0])
    return results[0]






@bot.command()
async def getSongsSpotify(artist, song):
    result = spotifyTest.search(artist, song)
    print(result)
    return result['tracks']['items']

#command to end playback

# Would probably want to hide token later, but should work fine for testing
bot.run(os.getenv("DISCORD_TOKEN"))