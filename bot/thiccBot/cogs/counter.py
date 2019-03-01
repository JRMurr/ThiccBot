from discord.ext import commands
from discord.ext.commands import Cog
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import random
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Counter(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def counter(self, ctx):
        """Commands for creating and mangaging counters"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help counter")

    @counter.command(name="list")
    async def counter_list(self, ctx):
        """List all the counters for this server"""
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            rows = [f"{x['name']}->{x['count']}" for x in data]
            p = Pages(ctx, entries=rows, per_page=10)
            await p.paginate()

        await self.bot.request_helper(
            "get",
            f"/counter/discord/{server_id}",
            ctx,
            error_prefix="Error getting counters",
            success_function=on_200,
        )

    @counter.command(name="create", aliases=["add"])
    @checks.is_bot_admin()
    async def counter_create(self, ctx, counter_name: str, start_count: int = 0):
        """Creates an counter

            ex: counter create "my count" """
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"Created Counter: {counter_name}")

        await self.bot.request_helper(
            "post",
            f"/counter/discord/{server_id}",
            ctx,
            json={"name": counter_name, "count": start_count},
            error_prefix="Error creating counter",
            success_function=on_200,
        )

    @counter.command(name="inc", aliases=["increment", "increase"])
    async def counter_increase(self, ctx, counter_name: str):
        """Increase the count by 1

            ex: counter inc "my count" """
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            await ctx.send(f"Count of {counter_name} is now {data['count']}")

        await self.bot.request_helper(
            "put",
            f"/counter/discord/{server_id}/{counter_name}",
            ctx,
            error_prefix="Error incrementing counter",
            success_function=on_200,
        )

    @counter.command(name="set")
    @checks.is_bot_admin()
    async def counter_set(self, ctx, counter_name: str, count: int):
        """sets the counter to the specified values

            ex: counter set "my count" 10 """
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            await ctx.send(f"Count of {counter_name} is now {data['count']}")

        await self.bot.request_helper(
            "put",
            f"/counter/discord/{server_id}/{counter_name}",
            ctx,
            json={"count": count},
            error_prefix="Error setting counter",
            success_function=on_200,
        )


def setup(bot):
    bot.add_cog(Counter(bot))
