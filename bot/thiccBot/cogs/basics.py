from discord.ext import commands
import discord
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Basics:
    """Basic/simple commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, args: str):
        """The bot says what you want it to"""
        await ctx.send(args)


def setup(bot):
    bot.add_cog(Basics(bot))
