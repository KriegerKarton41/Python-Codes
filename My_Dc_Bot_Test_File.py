# Not Working Right Now

import discord
from discord.ext import commands
from discord import interactions 

import youtube_dl

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = interactions (bot, sync_commands=True)  # Create an instance of SlashCommand

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

# Dictionary to hold information about the current song playing in each guild
current_song = {}

# Function to play music
async def play_music(ctx, url):
    guild = ctx.guild
    voice_client = guild.voice_client

    if voice_client is None:
        # If bot is not already in a voice channel, connect to the user's channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("Der bot ist nun verbunden.")
            return

    # Download and extract information about the video from the URL
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Play the audio
    source = discord.FFmpegPCMAudio(info['url'])
    voice_client.play(source)

    # Store the current song information
    current_song[guild.id] = {
        'title': info['title'],
        'url': url
    }

# Slash command to play music
@slash.slash(name="play", description="Play a song")
async def _play(ctx: interactions, url: str):
    await play_music(ctx, url)

# Slash command to stop the bot and disconnect from the voice channel
@slash.slash(name="stop", description="Stop the bot and disconnect from the voice channel")
async def _stop(ctx: interactions):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        current_song.pop(ctx.guild.id, None)
        await ctx.send("Der bot wurde gestoppt und vom Sprachkanal getrennt.")
    else:
        await ctx.send("Der bot ist nicht verbunden.")

# Slash command to show the currently playing song
@slash.slash(name="nowplaying", description="Show the currently playing song")
async def _now_playing(ctx: interactions):
    if ctx.guild.id in current_song:
        song = current_song[ctx.guild.id]
        await ctx.send(f"Jetzt spielt: {song['title']}")
    else:
        await ctx.send("Kein song spielt gerade.")

# Run the bot
bot.run('Your Token Here')
