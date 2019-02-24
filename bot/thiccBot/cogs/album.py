from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import random
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Album(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def album(self, ctx):
        """Commands for creating and mangaging albums"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help album")

    @album.command(name="list")
    async def album_list(self, ctx):
        """List all the albums for this server"""
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            rows = [x["name"] for x in data]
            p = Pages(ctx, entries=rows, per_page=10)
            await p.paginate()

        await self.bot.request_helper(
            "get",
            f"/albums/discord/{server_id}",
            ctx,
            error_prefix="Error getting albums",
            success_function=on_200,
        )

    @album.command(name="create")
    @checks.is_bot_admin()
    async def album_create(self, ctx, album_name: str):
        """Creates an album

            ex: album create "Nice Memes" """
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"Created Album: {album_name}")

        await self.bot.request_helper(
            "post",
            f"/albums/discord/{server_id}",
            ctx,
            json={"name": album_name},
            error_prefix="Error creating album",
            success_function=on_200,
        )

    @album.command(name="add")
    @checks.is_bot_admin()
    async def album_entry_add(self, ctx, album_name: str, entry: str):
        """Adds link to an album

            ex: album add "Nice Memes" https://i.imgur.com/s8Zf1Qn.jpg """
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"Added entry {entry} to {album_name}")

        await self.bot.request_helper(
            "post",
            f"/albums/discord/{server_id}/{album_name}/entries",
            ctx,
            json={"link": entry},
            error_prefix="Error adding entry",
            success_function=on_200,
        )

    @album.command(name="get")
    async def album_entry(self, ctx, album_name: str):
        """Returns random entry in the album"""
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            entry = random.choice(data)
            await ctx.send(entry["link"])

        await self.bot.request_helper(
            "get",
            f"/albums/discord/{server_id}/{album_name}/entries",
            ctx,
            error_prefix="Error getting entries",
            success_function=on_200,
        )

    @album.group(name="entries")
    async def entries(self, ctx):
        """Commands for listing and deleting entries"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help album entries")

    @entries.command(name="list")
    async def album_entry_list(self, ctx, album_name: str):
        """List all the entries in the album """
        server_id = ctx.guild.id

        async def on_200(r):
            data = await r.json()
            rows = [f"{x['id']}: {x['link']}" for x in data]
            p = Pages(ctx, entries=rows, per_page=10, show_index=False)
            await p.paginate()

        await self.bot.request_helper(
            "get",
            f"/albums/discord/{server_id}/{album_name}/entries",
            ctx,
            error_prefix="Error getting entries",
            success_function=on_200,
        )

    @entries.command(name="delete")
    async def album_entry_delete(self, ctx, entry_id: int):
        """Deletes the specified entry in the album
        
        To get the id of the entry to delete run "album entries list <album name>"
        """
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"Deleted entry: {entry_id}")

        await self.bot.request_helper(
            "delete",
            f"/albums/discord/{server_id}/entry/{entry_id}",
            ctx,
            error_prefix="Error deleting entry",
            success_function=on_200,
        )


def setup(bot):
    bot.add_cog(Album(bot))
