from discord.ext import commands
from discord.ext.commands import Cog
from discord import File
import discord
import logging
from thiccBot.bot import ThiccBot
from aiohttp import ClientResponse
from io import BytesIO

log = logging.getLogger(__name__)


class Lastfm(Cog):
    def __init__(self, bot: ThiccBot):
        self.bot = bot

    @commands.group()
    async def lastfm(self, ctx):
        """Commands for getting lastfm grids"""
        if ctx.invoked_subcommand is None:
            await ctx.send("run lastm grid 'lastfm_user_name'")

    @lastfm.command()
    async def grid(self, ctx: commands.Context, lastfm_name: str):
        message = await ctx.send("Making last fm grid, this will take a sec")

        async def on_200(r: ClientResponse):
            f = File(BytesIO(await r.read()), "image.jpeg")
            await ctx.send(file=f)
            await message.delete()

        async with ctx.typing():
            await self.bot.request_helper(
                "get",
                f"/lastFM/grid/{lastfm_name}",
                ctx,
                error_prefix="Error getting last fm grid",
                success_function=on_200,
            )


def setup(bot):
    bot.add_cog(Lastfm(bot))
