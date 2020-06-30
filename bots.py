import random
import json
import discord
from discord.ext import commands
import youtube_dl
import requests
from discord.utils import get
import asyncio


client = commands.Bot(command_prefix='#')
out = open('g_data.txt')
s = json.load(out)
kickl = open('k_list.txt')
updated_data = {}
bot = client
song_queue = []
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
try:
    kick_list = json.load(kickl)
except:
    kick_list = {"Noone": ""}
gain_list = open("gain_list.txt")
try:
    g_ist = json.load(gain_list)
except:
    g_ist = {}


@client.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over Noodles"))
    print("bot is ready")


@client.command()
async def clearm(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.command()
async def hell(ctx, arg="Hello"):
    await ctx.send("Hello from Devil")


@client.command(aliases=['gp', 'guildpoint'])
async def guild_point(ctx, *, arg="none"):
    msg = ""
    channel = ctx.message.channel
    avatarUrl = ctx.author.avatar_url
    username = ctx.author.display_name
    if arg == "none":
        await ctx.send("Whose Score?")
    else:
        for name, gp in s.items():
            u_name = name.upper()
            try:
                gains = g_ist[u_name]
            except:
                gains = 0
            if name.upper() == arg.upper():
                embed = discord.Embed(
                    title='The guildPoint Details of {} '.format(name),
                    colour=discord.Color.red()
                )
                embed.set_footer(text="GuildPoints will be updated in 24hrs.")
                embed.set_author(name=username, icon_url=avatarUrl)
                embed.add_field(name="Total GuildPoints",
                                value=int(gp), inline=True)
                embed.add_field(name="Gp earned in last 24hrs",
                                value=int(gains), inline=False)
                await channel.send(embed=embed)
                msg = "sdf"
                break
            else:
                msg = "err"
    if msg == "err":
        await ctx.send("No record found with that name")


@client.command(aliases=['tbk'])
async def kicklist(ctx):
    tbkick = ""
    channel = ctx.message.channel
    avatarUrl = ctx.author.avatar_url
    username = ctx.author.display_name
    embed = discord.Embed(
        title='The Kicklist for today',
        colour=discord.Color.red()
    )
    embed.set_author(name=username, icon_url=avatarUrl)
    for k, v in kick_list.items():
        embed.add_field(name=k,
                        value="{} Gp Gained".format(v), inline=True)
    await channel.send(embed=embed)


@client.command(aliases=['gain'])
async def gained(ctx, *, arg):
    arg_list = arg.split(" ")
    sep = " "
    d_name = sep.join(arg_list[:-1])

    d_score = int(arg_list[-1])
    channel = ctx.message.channel
    avatarUrl = ctx.author.avatar_url
    username = ctx.author.display_name
    for name, score in s.items():
        if name.upper() == d_name.upper():
            latest_score = d_score-int(score)
            embed = discord.Embed(
                title='Today\'s GP Detail of {} '.format(name),
                colour=discord.Color.red()
            )
            embed.set_footer(
                text="Guild point gained can be updated by you anytime.")
            embed.set_author(name=username, icon_url=avatarUrl)
            embed.add_field(name="Total GuildPoints",
                            value=int(score), inline=True)
            embed.add_field(name="Gp earned Today from 8AM",
                            value=int(latest_score), inline=False)
            await channel.send(embed=embed)


@client.command(aliases=['sk', 'sunakoti', 'sunkoti', 'sunkotha'])
async def sunakothi(ctx, *, arg):
    responses = ['Janxa Janxa Sunkothi ma batti <:momo:725210075131805787>', "Malai k Tha <:wut:725220360345354280> ", "IDK but momo noob ho <:momo:725210075131805787> ",
                 "Lyang Lyang na garr noob <:nangry:725220801007321138> ", "Janxa ni batti, Ta Lp khayera bass <:punchman:725220477672357960>"]
    if 'batti' in arg or 'Batti':
        await ctx.send("{}".format(random.choice(responses)))
    else:
        await ctx.send("Sunkothi ko batti bare ma sodh, aru kei haina <:nangry:725220801007321138>")


@client.command()
async def insults(ctx, arg="s"):
    lists = ["momo is gay", "momo is noob", "momo is panauti",
             "fuck you momo", "Rotten momo <:momo:725210075131805787>"]
    await ctx.send(random.choice(lists))


@client.command(aliases=['p'], brief='!play [url/key-words]', description='Plays youtube videos')
async def play(ctx, *arg):
    channel = ctx.message.author.voice.channel

    if channel:
        voice = get(bot.voice_clients, guild=ctx.guild)
        song = search(ctx.author.mention, arg)
        song_queue.append(song)
        print(song)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(
                song['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
            await ctx.send(embed=song['embed'])
        else:
            await ctx.send(f":white_check_mark: Music **{song['title']}** added to queue ({len(song_queue)-1} to go)", delete_after=song_queue[0]['duration'])
    else:
        await ctx.send("❌ Channel join gareko xaina, bot bhanera hepxas!")


def play_next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if len(song_queue) > 1:
        del song_queue[0]
        voice.play(discord.FFmpegPCMAudio(
            song_queue[0]['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
        voice.is_playing()
        asyncio.run_coroutine_threadsafe(ctx.send(
            embed=song_queue[0]['embed']), bot.loop)
    else:
        asyncio.run_coroutine_threadsafe(voice.disconnect(), bot.loop)


@ client.command(brief='!pause', description='Pauses or resumes the current song')
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        if voice.is_playing():
            await ctx.send('⏸️ Music paused')
            voice.pause()
        else:
            await ctx.send('⏯️ Music resumed')
            voice.resume()
    else:
        await ctx.send("❌ Channel join gareko xaina, bot bhanera hepxas!")


@ client.command(aliases=['s', 'fs', 'pass'], brief='!skip', description='Skips the current song')
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    if voice and voice.is_playing():
        await ctx.send('⏭️ Lu Lu arko sunn')
        voice.stop()
    else:
        await ctx.send("❌ Kei geet bajeko xaina skip kina gareko?")


@ client.command(aliases=['st', 'rok'], brief='!skip', description='Skips the current song')
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    if voice and voice.is_playing():
        await ctx.send('⏭️ Lu Lu NA sunn')
        song_queue.clear()
        voice.stop()
    else:
        await ctx.send("❌ Kei geet bajeko xaina skip kina gareko?")


def search(author, arg):
    ydl_opts = {'format': 'bestaudio',
                'noplaylist': 'True', 'audio-quality': 0}
    try:
        requests.get("".join(arg))
    except:
        arg = " ".join(arg)
    else:
        arg = "".join(arg)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{arg}", download=False)[
            'entries'][0]

    embed = (discord.Embed(title='🎵 Hunters Listening To:', description=f"{info['title']}", color=discord.Color.blue())
             .add_field(name='एल्से बाजाको', value=author)
             .add_field(name='Duration', value="{} mins".format(150/60))
             .add_field(name='Channel', value=f"[{info['uploader']}]({info['channel_url']})", inline=False)
             .add_field(name='URL', value=f"[Video Ne Herdine ho Youtube ma?]({info['webpage_url']})")
             .set_thumbnail(url=info['thumbnail']))

    return {'embed': embed, 'source': info['formats'][0]['url'],
            'title': info['title'], 'duration': info['duration']}


client.run("NzI0ODU1MjQ3MjU1NjMzOTIy.XvGQwQ.UhIoQdKCzU6gLD6JVQZaEtTZD9E")
