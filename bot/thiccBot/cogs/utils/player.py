import discord
from enum import Enum
import logging

# YTDLSource from: https://gist.github.com/EvieePy/ab667b74e9758433b3eb806c53a19f34

import asyncio
from  async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from youtube_dl.utils import ExtractorError


log = logging.getLogger(__name__)


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if "entries" in data:
            # just a single video or only take first
            if not ctx.bot.config["allow_adding_playlists"] or len(data["entries"]) == 1:
                # take first item from a playlist
                data = data['entries'][0]
            else:
                return await YTDLSource.create_sources_from_playlist(ctx, data, download=download)

        try:
            source = YTDLSource._create_source(data, ctx, download=download)
        except ExtractorError as e:
            log.error(f"Failed to download source: {e}")
            await ctx.send(f'```ini\nFailed to add {data["title"]} from playlist {playlist_data["title"]}\n```', delete_after=15)
            return

        return source

    @staticmethod
    async def create_sources_from_playlist(ctx, playlist_data, *, download=False):
        results = {"title": playlist_data["title"], "sources": []}
        for data in playlist_data["entries"]:
            try:
                results["sources"].append(YTDLSource._create_source(data, ctx, download=download))
            except ExtractorError as e:
                log.error(f"Failed to download source: {e}")
                await ctx.send(f'```ini\nFailed to add {data["title"]} from playlist {playlist_data["title"]}\n```', delete_after=15)
                return
        return results

    @classmethod
    def _create_source(cls, data, ctx, *, download=False):
        if download:
            source = ytdl.prepare_filename(data)
            source = cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)
        else:
            source = {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        return source


    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)
    

class Player:
    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self.cog = ctx.cog

        self.current_song = None
        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.volume = .5

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy()

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.create_source(self.ctx, source['webpage_url'], loop=self.bot.loop, download=True)
                except Exception as e:
                    await self.ctx.channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current_song = source

            self.ctx.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            await self.ctx.send(f"**Now Playing:** {source.title} requested by {source.requester}")

            await self.next.wait()

            source.cleanup()
            self.current_song = None


    def destroy(self):
        self.current_song.cleanup()
        return self.bot.loop.create_task(self.cog.cleanup(self.ctx))
