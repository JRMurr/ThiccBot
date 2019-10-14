from discord.ext import commands
from discord.ext.commands import Cog
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import random
import logging
from pprint import pprint
from itertools import islice
import asyncio

from thiccBot.cogs.player import Player, YTDLSource

log = logging.getLogger(__name__)

class Playlist(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @commands.group()
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def playlist(self, ctx):
        """Commands for creating and mangaging the servers music playlist"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help playlist")

    async def get_player(self, ctx):
        """"Get the guild's player (create it if needed)"""
        gid = ctx.guild.id
        # create the guild's player if it doesn't exist
        if gid not in self.players:
            await self.summon(ctx)
            self.players[gid] = Player(ctx)
            await ctx.send(f"Playing music in {ctx.voice_client.channel.name}")
        return self.players[gid]

    async def cleanup(self, ctx):
        """Get rid of the guilds player"""
        if ctx.guild.id not in self.players:
            return await ctx.send("Not playing music")

        player = self.players[ctx.guild.id]
        await player.ctx.guild.voice_client.disconnect()
        del self.players[ctx.guild.id]

    async def add_source(self, ctx, search):
        player = await self.get_player(ctx)
        if not player:
            return
        source = await YTDLSource.create_source(ctx, search, loop=ctx.bot.loop, download=False)
        await player.queue.put(source)
        await ctx.send(f'```ini\n[Added {source["title"]} to the Queue.]\n```', delete_after=15)

    @playlist.command(name="play")
    async def playlist_play(self, ctx, search: str):
        """Start or resume player for this server or queue another song

           ex: playlist play https://www.youtube.com/watch?v=FTQbiNvZqaY
           ex: playlist play "smash mouth all star" """

        player = await self.get_player(ctx)

        if player and search:
            await self.add_source(ctx, search)

    @playlist.command(name="list", aliases=["queue"])
    @checks.is_bot_admin()
    async def playlist_list(self, ctx):
        """List songs in the playlist"""
        server_id = ctx.guild.id

        if server_id not in self.players or len(self.players[server_id].queue._queue) == 0:
            await ctx.send(f"No songs are in the playlist queue")
        else:
            queue = list(islice(self.players[server_id].queue._queue, 0, 10))
            names = "\n".join(map(lambda info: info["title"], queue))
            await ctx.send(f"Next {min(10, len(queue))} songs in queue:\n```{names}```")

    @playlist.command(name="volume", aliases=["vol"])
    @checks.is_bot_admin()
    async def playlist_volume(self, ctx, vol):
        """Set the players volume
           Should be a value between 1 and 100"""
        vc = await self.get_voice(ctx)
        if not vc:
            return
        vol = int(vol)
        if not 0 < vol < 101:
            return await ctx.send("Volume should be between 1 and 100")

        if vc.source:
            vc.source.volume = vol / 100

        player = await self.get_player(ctx)
        player.volume = vol / 100
        await ctx.send("**Volume set**")

    @playlist.command(name="add")
    @checks.is_bot_admin()
    async def playlist_add(self, ctx, search: str):
        """Adds link to a playlist

            ex: playlist add https://www.youtube.com/watch?v=FTQbiNvZqaY """
        await self.add_source(ctx, search)

    @playlist.command(name="pause")
    @checks.is_bot_admin()
    async def playlist_pause(self, ctx):
        """Pause music"""

        vc = await self.get_voice(ctx)
        if not vc:
            return
        if not vc.is_paused():
            vc.pause()
        await ctx.send("**Pausing music**")

    @playlist.command(name="resume")
    @checks.is_bot_admin()
    async def playlist_resume(self, ctx):
        """Resume music"""

        vc = await self.get_voice(ctx)
        if not vc:
            return
        if vc.is_paused():
            vc.resume()
        await ctx.send("**Resuming music**")

    @playlist.command(name="stop")
    @checks.is_bot_admin()
    async def playlist_stop(self, ctx):
        """Stops the music and exits the voice channel"""
        await self.cleanup(ctx)

    async def get_voice(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected:
            await ctx.send("Currently not connected to a voice channel")
        else:
            return vc

    @playlist.command(name="skip")
    @checks.is_bot_admin()
    async def playlist_skip(self, ctx):
        """Skips to the next song"""
        vc = await self.get_voice(ctx)
        if not vc:
            return

        vc.stop()
        await ctx.send("**Skipping song**")

    @playlist.command(name="now_playing", aliases=["np", "current", "currentsong", "playing"])
    @checks.is_bot_admin()
    async def playlist_np(self, ctx):
        """Displays current song"""
        vc = await self.get_voice(ctx)
        if not vc:
            return
        player = await self.get_player(ctx)
        if not player or not player.current_song:
            return await ctx.send("Currently not playing anything")

        current = player.current_song
        await ctx.send(f"**Now Playing:** {current['title']} requested by {current.requester}")

    async def summon(self, ctx):
        vc = ctx.voice_client
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("You must join a voice channel to summon the bot")

        if vc:
            if vc.channel.id == channel.id:
                return
            else:
                try:
                    await vc.move_to(channel)
                except asyncio.TimeoutError:
                    await ctx.send(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                await ctx.send(f'Connecting to channel: <{channel}> timed out.')

    @playlist.command(name="summon", aliases=["connect"])
    @checks.is_bot_admin()
    async def playlist_summon(self, ctx):
        """Summon the bot to your current channel"""
        await self.summon(ctx)
        await ctx.send(f"Connected to **{ctx.voice_client.channel}**")

def setup(bot):
    OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
    for lib in OPUS_LIBS:
        try:
            discord.opus.load_opus(lib)
        except OSError:
            pass

    if not discord.opus.is_loaded():
        pprint("libopus failed to load, playlist is disabled")
        return
    bot.add_cog(Playlist(bot))
