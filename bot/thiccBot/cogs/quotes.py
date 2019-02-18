from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.logError import get_error_str
import random
import logging
from pprint import pprint

log = logging.getLogger(__name__)


def get_str(quote_str, author):
    return f'"{quote_str}" - "{author}"'


class Quotes:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def quotes(self, ctx):
        """Commands for creating and mangaging quotes"""
        pass
        # if ctx.invoked_subcommand is None:  # or ctx.subcommand_passed == 'box':
        #     await ctx.send(
        #         "to create command run 'alias create <alias_name> <command_to_run>'"
        #     )

    @quotes.group(name="search")
    async def quote_search(self, ctx, search: str):
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "get", f"/quotes/discord/{server_id}/{search}"
        ) as r:
            if r.status == 200:
                data = await r.json()
                chosen = random.choice(data)
                await ctx.send(get_str(chosen["quote"], chosen["author"]))
            else:
                await ctx.send("Error searching for quotes")
                log.error(get_error_str(r, "error saving quote: "))

    @quotes.group(name="save")
    @checks.is_bot_admin()
    async def quote_save(self, ctx, quote_str: str, author: str):
        """Creates a quote

            ex: quote save \"some quote\" \"some author\""""
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "post",
            f"/quotes/discord/{server_id}",
            json={"quote": quote_str, "author": author},
        ) as r:
            if r.status == 200:
                data = await r.json()
                pprint(data)
                await ctx.send(f"Saved quote: {get_str(quote_str, author)}")
            else:
                await ctx.send("Error saving quote")
                log.error(get_error_str(r, "error saving quote: "))


def setup(bot):
    bot.add_cog(Quotes(bot))
