import discord
import os
import asyncio

from discord.ext import commands
from discord import FFmpegPCMAudio

from discord import Intents

# Create an instance of a bot. Has intents to do everything for now, just to test
bot = commands.Bot(command_prefix='!', intents = Intents.all())

#Plays "creep.mp3" into the channel user is in. Can only play Creep by Radiohead
@bot.command()
async def play(ctx):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    
    # Get the voice channel of the user
    voice_channel = ctx.author.voice.channel

    try:
        # Connect to the voice channel
        voice_client = await voice_channel.connect()

        # Play the audio file. Had to set executable to the path, wasn't recognizign for some reason. Weird
        audio_source = FFmpegPCMAudio(executable = 'C:/ffmpeg/bin/ffmpeg.exe' , source = 'creep.mp3')
        voice_client.play(audio_source)

        # Wait for the audio to finish playing or everyone else to leave, check every 1 second
        while voice_client.is_playing() and len(voice_channel.members) > 1:
            await asyncio.sleep(1)
        # Disconnect from the voice channel after the audio finishes playing. 
        await voice_client.disconnect()

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while playing the audio.")

# Would probably want to hide token later, but should work fine for testing
bot.run("MTIwOTQwNzQ3MzIwMzgxMDMyNA.Ggoj_F.UNtYsPOJUO2Q1WlrVKp2i_ZW8iETJnuvkIEz0c")