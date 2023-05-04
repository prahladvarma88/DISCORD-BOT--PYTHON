
# import liberies 
import sqlite3
import asyncio
import re
import discord
from discord.ext import commands
import random
import aiohttp
import youtube_dl
import urllib.request



client = commands.Bot(command_prefix='!',intents=discord.Intents.all())



@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome to the server, {member.mention}!')

   
    # Get the role to assign
    role = discord.utils.get(member.guild.roles, name="New Member")
    
    # Assign the role to the new member
    await member.add_roles(role)
    
    # Send a welcome message to the new member
    channel = client.get_channel(772044927060279309) # Replace with the ID of your welcome channel
    await channel.send(f"Welcome to the server, {member.mention}! You have been assigned the {role.name} role.")


    #assign role 



@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'{member.mention}, has left a server!')







@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'hello':
        await message.channel.send('Hello!')
        await message.author.send('Hello!')

    await client.process_commands(message)

    if message.content == 'server':
        await message.delete()
        await message.channel.send('Dont send it  again otherwise you will get direct ban from the server')


# Below code is for playing stone paper scissors game 


    if message.content.startswith('rps'):
        options = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(options)
        
        user_input = message.content.split()
        if len(user_input) < 2:
            await message.channel.send('Please enter rock, paper, or scissors after rps.')
            return
        user_choice = user_input[1].lower()

        if user_choice not in options:
            await message.channel.send('Invalid choice! Please choose from rock, paper, or scissors.')
        else:
            if user_choice == computer_choice:
                result = 'Tie!'
            elif user_choice == 'rock' and computer_choice == 'scissors':
                result = 'You win!'
            elif user_choice == 'paper' and computer_choice == 'rock':
                result = 'You win!'
            elif user_choice == 'scissors' and computer_choice == 'paper':
                result = 'You win!'
            else:
                result = 'You lose!'
                
            await message.channel.send(f'You choose {user_choice}. I choose {computer_choice}. {result}')


    if message.content.startswith('guess'):
        await message.channel.send('Guess a number between 1 and 100!')

        def check(msg):
            return msg.author == message.author and msg.content.isdigit()

        guess = await client.wait_for('message', check=check)
        answer = random.randint(1, 100)

        if int(guess.content) == answer:
            await message.channel.send('You got it right!')
        else:
            await message.channel.send('Sorry, the answer was {}.'.format(answer))       





    

    
            





#assign role 

@client.command()
@commands.has_permissions(administrator=True) # only allow admins to use this command
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{role.name} role has been added to {member.mention}.")

@client.command()
@commands.has_permissions(administrator=True) # only allow admins to use this command
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{role.name} role has been removed from {member.mention}.")


    

async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="List of available commands:", color=0x00ff00)
    embed.add_field(name="!help", value="Displays this help message", inline=False)
    embed.add_field(name="!ban", value="-ban members", inline=False)
    embed.add_field(name="!info", value="Displays information about the bot", inline=False)
    await ctx.send(embed=embed)





@client.command()
async def kick(ctx, member: discord.Member, * , reason = None):
    await member.kick(reason = reason)
    channel = discord.utils.get(member.guild.channels, name='general')
    await ctx.send(f'{member} has been kicked for {reason}')

@client.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f'{member} has been banned.')



@client.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.send(f'{member} has been muted.')


@client.command()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    await ctx.send(f'{member} has been unmuted.')


@client.command()
async def clear(ctx,amount = 5):
    await ctx.channel.purge(limit= amount)

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes.json") as r:
            memes = await r.json()
            embed = discord.Embed(
                color=discord.Colour.purple()  # fix here
            )
            embed.set_image(url=memes["data"]["children"][random.randint(0,25)]["data"]["url"])
            embed.set_footer(text=f"Powered  by r/memes | Meme requested by {ctx.author}")
            await ctx.send(embed=embed)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'noplaylist':'True'}).extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else youtube_dl.utils.sanitize_filename(data['title'], restrict_chars=True)

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

ffmpeg_options = {
    'options': '-vn'
}

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in voice channel , you must  be in voice channel to you this command! ")


@client.command(pass_context = True)
async def disconnect(ctx):
    if (ctx.voice_client):
        await ctx.voice_client.disconnect()
        await ctx.send("I left the voice channnel! ")
    else:
        await ctx.send("I am not in a voice channel! ")
    
@client.command(pass_context=True)
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel!")
        return
    else:
        channel = ctx.author.voice.channel

    try:
        await channel.connect()
    except:
        pass

    query = search.strip('<>')

    if "youtube.com" in query or "youtu.be" in query:
        url = query
    else:
        try:
            query = search.replace(' ', '+')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            url = "https://www.youtube.com/watch?v=" + video_ids[0]
        except:
            await ctx.send("Error: could not find a video with that name or URL.")
            return

    try:
        player = await YTDLSource.from_url(url, loop=client.loop)
    except youtube_dl.utils.DownloadError:
        await ctx.send("Error: could not play audio from the provided URL.")
        return

    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send("Now playing: {}".format(player.title))

    
@client.command(pass_context=True)
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Playback paused.")
    else:
        await ctx.send("I am not currently playing anything.")

@client.command(pass_context=True)
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Playback resumed.")
    else:
        await ctx.send("Playback is not currently paused.")








# Create or connect to database
conn = sqlite3.connect('level.db')
c = conn.cursor()

# Create table for storing user levels
c.execute('''CREATE TABLE IF NOT EXISTS levels
             (user_id integer PRIMARY KEY, level integer)''')

# Default level to set for new users
DEFAULT_LEVEL = 1


# Function to get user's current level
def get_user_level(user_id):
    c.execute('SELECT level FROM levels WHERE user_id=?', (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return DEFAULT_LEVEL


# Function to set user's level
def set_user_level(user_id, level):
    c.execute('INSERT OR REPLACE INTO levels (user_id, level) VALUES (?, ?)', (user_id, level))
    conn.commit()





@client.event
async def on_member_join(member):
    # Set default level for new users
    set_user_level(member.id, DEFAULT_LEVEL)


@client.command()
async def level(ctx, user: discord.Member = None):
    if not user:
        user = ctx.author
    level = get_user_level(user.id)
    await ctx.send(f'{user.name} is level {level}.')


@client.command()
@commands.has_permissions(administrator=True)
async def setlevel(ctx, user: discord.Member, level: int):
    set_user_level(user.id, level)
    await ctx.send(f'Set {user.name}\'s level to {level}.')






client.run("MTA4NDE2ODA5NzM4NjIyMTYwOA.G6Nk27.sY83mZLisT4_d4Zwnca8zFXGjYqlCu9AwEtMZo")