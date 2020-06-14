from discord.ext import commands
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.bot import ThiccBot
import logging

log = logging.getLogger(__name__)


def format_quote(quote):
    return f'"{quote["quote"]}" - {quote["author"]}'


class Quotes(commands.Cog):
    def __init__(self, bot: ThiccBot):
        self.bot = bot

    async def get_rand_quote(self, ctx):
        server_id = ctx.guild.id

        async def on_200(r):
            quote = await r.json()
            await ctx.send(format_quote(quote))

        async def on_404(r):
            await ctx.send("No quotes")

        await self.bot.request_helper(
            "get",
            f"/quotes/discord/{server_id}/random",
            ctx,
            error_prefix="Error getting quotes",
            success_function=on_200,
            error_handler={404: on_404},
        )

    @commands.group(name="quotes", aliases=["quote"])
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def quotes(self, ctx):
        """Commands for creating and mangaging quotes"""
        if ctx.invoked_subcommand is None:
            await self.get_rand_quote(ctx)

    @quotes.command(name="search")
    async def quote_search(self, ctx, search: str):
        server_id = ctx.guild.id

        async def on_200(r):
            quote = await r.json()
            await ctx.send(format_quote(quote))

        async def on_404(r):
            await ctx.send("No quotes")

        await self.bot.request_helper(
            "get",
            f"/quotes/discord/{server_id}/random?search={search}",
            ctx,
            error_prefix="Error searching for quotes",
            success_function=on_200,
            error_handler={404: on_404},
        )

    @quotes.command(name="list")
    async def quotes_list(self, ctx):
        """List all the quotes for this server"""
        server_id = ctx.guild.id

        def quote_page_entry(quote_info):
            return f"{quote_info['id']}: {format_quote(quote_info)}"

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
        await self.get_rand_quote(ctx)

    @quotes.command(name="save", aliases=["create"])
    @checks.is_bot_admin()
    async def quote_save(self, ctx, quote_str: str, author: str):
        """Creates a quote

            ex: quote save \"some quote\" \"some author\""""
        server_id = ctx.guild.id

        async def on_200(r):
            quote = await r.json()
            await ctx.send(f"Saved quote: {format_quote(quote)}")

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

            Pass the quote id to delete, you can get them by using
            \"quote list\"
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
