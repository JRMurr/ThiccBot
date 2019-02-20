from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import get_error_str
import random
import logging
from pprint import pprint

log = logging.getLogger(__name__)


def get_str(quote_str, author):
    return f'"{quote_str}" - "{author}"'


def quote_page_entry(quoute_info):
    return (
        f"{quoute_info['id']}: {get_str(quoute_info['quote'], quoute_info['author'])}"
    )


class Quotes:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def quotes(self, ctx):
        """Commands for creating and mangaging quotes"""
        # TODO: get rand quote
        if ctx.invoked_subcommand is None:  # or ctx.subcommand_passed == 'box':
            await ctx.send(
                "to create command run 'alias create <alias_name> <command_to_run>'"
            )

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

    @quotes.group(name="list")
    async def quotes_list(self, ctx):
        """List all the quotes for this server"""
        server_id = ctx.guild.id
        async with self.bot.backend_request("get", f"/quotes/discord/{server_id}") as r:
            if r.status == 200:
                data = await r.json()
                rows = [quote_page_entry(x) for x in data]
                p = Pages(ctx, entries=rows, per_page=10, show_index=False)
                await p.paginate()
            else:
                await ctx.send("Error getting quotes")
                log.error(get_error_str(r, "error getting quotes: "))

    @quotes.group(name="get")
    async def quote_get(self, ctx):
        """Get random quote from this server"""
        server_id = ctx.guild.id
        async with self.bot.backend_request("get", f"/quotes/discord/{server_id}") as r:
            if r.status == 200:
                data = await r.json()
                quoute_info = random.choice(data)
                await ctx.send(get_str(quoute_info["quote"], quoute_info["author"]))
            else:
                await ctx.send("Error getting quotes")
                log.error(get_error_str(r, "error getting quotes: "))

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
                await ctx.send(f"Saved quote: {get_str(quote_str, author)}")
            else:
                await ctx.send("Error saving quote")
                log.error(get_error_str(r, "error saving quote: "))

    @quotes.group(name="delete")
    @checks.is_bot_admin()
    async def quote_delete(self, ctx, quote_id):
        """Deletes the specified quote
        
            Pass the quote id to delete, you can get them by using \"quote list\"
        """
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "delete", f"/quotes/discord/{server_id}/{quote_id}"
        ) as r:
            if r.status == 200:
                await ctx.send(f"deleted quote {quote_id}")
            elif not r.status == 404:
                await ctx.send(f"Error deleting alias {quote_id}")
                log.error(get_error_str(r, "error making quote delete request: "))
            else:
                await ctx.send(f"{quote_id} not found")


def setup(bot):
    bot.add_cog(Quotes(bot))
