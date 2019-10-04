from discord.ext import commands
from discord.ext.commands import Cog
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import random
import logging
from pprint import pprint

from thiccBot.cogs.player import Player

log = logging.getLogger(__name__)

class Playlist(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlists = {}; # @TODO actually use db instead (for back up)
        self.players = {}

    @commands.group()
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def playlist(self, ctx):
        """Commands for creating and mangaging the servers music playlist"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help playlist")

    @playlist.command(name="play")
    async def playlist_play(self, ctx):
        """Start or resume the music playlists for this server

           ex: playlist play "Voice Channel" """
        server_id = ctx.guild.id

        # create the guild's player if it doesn't exist
        if server_id not in self.players:
            # auto join the users channel
            voice = ctx.author.voice
            if voice is None or voice.channel is None:
                await ctx.send("user is not in a voice channel")
                return

            await voice.channel.connect()
            self.players[server_id] = Player(voice.channel)
            await self.players[server_id].play(ctx)

        await ctx.send("Playing music in {voice_channel}")

    @playlist.command(name="list")
    @checks.is_bot_admin()
    async def playlist_list(self, ctx):
        """List songs in the playlist"""
        server_id = ctx.guild.id

        if server_id not in self.playlists or len(self.playlists[server_id]) == 0:
            await ctx.send(f"No songs are in the playlist")
        else:
            list = "\n".join(self.playlists[server_id])
            pprint(f"listing on {server_id}")
            await ctx.send(f"Songs in playlist:\n{list}")

    @playlist.command(name="add")
    @checks.is_bot_admin()
    async def playlist_add(self, ctx, link: str):
        """Adds link to a playlist

            ex: playlist add https://www.youtube.com/watch?v=FTQbiNvZqaY """
        server_id = ctx.guild.id

        if server_id not in self.playlists:
            self.playlists[server_id] = []
        self.playlists[server_id].append(link)

        pprint(f"added {link} to {server_id} playlist")


def setup(bot):
    OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
    for lib in OPUS_LIBS:
        try:
            discord.opus.load_opus(lib)
            pprint(f"loaded opus: {lib}")
        except OSError:
            pass

    if not discord.opus.is_loaded():
        pprint("libopus failed to load, playlist is disabled")
        return
    bot.add_cog(Playlist(bot))
