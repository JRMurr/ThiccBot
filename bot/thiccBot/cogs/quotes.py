from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import random
import logging
from pprint import pprint

log = logging.getLogger(__name__)


def get_str(quote_str, author):
    return f'"{quote_str}" - "{author}"'


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_rand_quote(self, ctx):
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            quoute_info = random.choice(data)
            await ctx.send(get_str(quoute_info["quote"], quoute_info["author"]))

        await self.bot.request_helper(
            "get",
            f"/quotes/discord/{server_id}",
            ctx,
            error_prefix="Error getting quotes",
            success_function=on_200,
        )

    @commands.group(name="quotes", aliases=["quote"])
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def quotes(self, ctx):
        """Commands for creating and mangaging quotes"""
        self.get_rand_quote(ctx)

    @quotes.command(name="search")
    async def quote_search(self, ctx, search: str):
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            chosen = random.choice(data)
            await ctx.send(get_str(chosen["quote"], chosen["author"]))

        await self.bot.request_helper(
            "get",
            f"/quotes/discord/{server_id}/{search}",
            ctx,
            error_prefix="Error searching for quotes",
            success_function=on_200,
        )

    @quotes.command(name="list")
    async def quotes_list(self, ctx):
        """List all the quotes for this server"""
        server_id = ctx.guild.id

        def quote_page_entry(quoute_info):
            return f"{quoute_info['id']}: {get_str(quoute_info['quote'], quoute_info['author'])}"

        async def on_200(r):
            data = await r.json()
            rows = [quote_page_entry(x) for x in data]
            p = Pages(ctx, entries=rows, per_page=10, show_index=False)
            await p.paginate()

        await self.bot.request_helper(
            "get",
            f"/quotes/discord/{server_id}",
            ctx,
            error_prefix="Error getting quotes",
            success_function=on_200,
        )

    @quotes.command(name="get")
    async def quote_get(self, ctx):
        """Get random quote from this server"""
        self.get_rand_quote(ctx)

    @quotes.command(name="save", aliases=["create"])
    @checks.is_bot_admin()
    async def quote_save(self, ctx, quote_str: str, author: str):
        """Creates a quote

            ex: quote save \"some quote\" \"some author\""""
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"Saved quote: {get_str(quote_str, author)}")

        await self.bot.request_helper(
            "post",
            f"/quotes/discord/{server_id}",
            ctx,
            error_prefix="Error saving quote",
            json={"quote": quote_str, "author": author},
            success_function=on_200,
        )

    @quotes.command(name="delete")
    @checks.is_bot_admin()
    async def quote_delete(self, ctx, quote_id):
        """Deletes the specified quote
        
            Pass the quote id to delete, you can get them by using \"quote list\"
        """
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"deleted quote {quote_id}")

        async def on_404(r):
            await ctx.send(f"{quote_id} not found")

        await self.bot.request_helper(
            "delete",
            f"/quotes/discord/{server_id}/{quote_id}",
            ctx,
            error_prefix=f"Error deleting quote {quote_id}",
            success_function=on_200,
            error_handler={404: on_404},
        )


def setup(bot):
    bot.add_cog(Quotes(bot))
