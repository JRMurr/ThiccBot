from discord.ext import commands
from discord.ext.commands import Cog
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import random
import logging
from pprint import pprint

from thiccBot.cogs.player import Player, YTDLSource

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


    async def get_player(self, ctx):
        """"Get the guild's player (create it if needed)"""
        gid = ctx.guild.id
        # create the guild's player if it doesn't exist
        if gid not in self.players:
            # auto join the users channel
            voice = ctx.author.voice
            if voice is None or voice.channel is None:
                await ctx.send("Join a voice channel to begin playing music")
                return

            await voice.channel.connect()
            self.players[gid] = Player(ctx)
            await ctx.send(f"Playing music in {voice.channel.name}")
        return self.players[gid]

    async def cleanup(self, guild):
        """Get rid of the guilds player"""
        try:
            await guild.voice_client.disconnet()
        except AttributeError:
            pass

        if guild.id in self.players:
            del self.players[guild.id]

    @playlist.command(name="play")
    async def playlist_play(self, ctx, search: str):
        """Start or resume player for this server or queue another song

           ex: playlist play https://www.youtube.com/watch?v=FTQbiNvZqaY """

        player = await self.get_player(ctx)

        if search:
            source = await YTDLSource.create_source(ctx, search, loop=ctx.bot.loop, download=True)
            await player.queue.put(source)

    # @playlist.command(name="list")
    # @checks.is_bot_admin()
    # async def playlist_list(self, ctx):
    #     """List songs in the playlist"""
    #     server_id = ctx.guild.id

    #     if server_id not in self.playlists or len(self.playlists[server_id]) == 0:
    #         await ctx.send(f"No songs are in the playlist")
    #     else:
    #         queue = "\n".join(self.playlists[server_id])
    #         pprint(f"listing on {server_id}")
    #         await ctx.send(f"Songs in playlist:\n{queue}")

    @playlist.command(name="add")
    @checks.is_bot_admin()
    async def playlist_add(self, ctx, search: str):
        """Adds link to a playlist

            ex: playlist add https://www.youtube.com/watch?v=FTQbiNvZqaY """
        player = await self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=ctx.bot.loop, download=False)
        await player.queue.put(source)

    @playlist.command(name="stop")
    @checks.is_bot_admin()
    async def playlist_stop(self, ctx):
        """Stops the music and exits the voice channel

            ex: playlist stop"""
        await self.cleanup(ctx.guild)

    # @entries.command(name="delete")
    # async def playlist_entry_delete(self, ctx, entry_id: int):
    #     """Deletes the specified entry in the playlist

    #     To get the id of the entry to delete run "playlist entries list <playlist name>"
    #     """
    #     server_id = ctx.guild.id

    #     async def on_200(r):
    #         await ctx.send(f"Deleted entry: {entry_id}")

    #     await self.bot.request_helper(
    #         "delete",
    #         f"/playlists/discord/{server_id}/entry/{entry_id}",
    #         ctx,
    #         error_prefix="Error deleting entry",
    #         success_function=on_200,
    #     )


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
