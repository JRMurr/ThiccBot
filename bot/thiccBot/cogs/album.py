from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import get_error_str
import random
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Album:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    # @checks.is_bot_admin()
    async def album(self, ctx):
        """Commands for creating and mangaging albums"""
        pass
        # if ctx.invoked_subcommand is None:  # or ctx.subcommand_passed == 'box':
        #     await ctx.send(
        #         "to create command run 'alias create <alias_name> <command_to_run>'"
        #     )

    @album.group(name="list")
    async def album_list(self, ctx):
        """List all the albums for this server"""
        server_id = ctx.guild.id
        async with self.bot.backend_request("get", f"/albums/discord/{server_id}") as r:
            if r.status == 200:
                data = await r.json()
                rows = [x['name'] for x in data]
                p = Pages(ctx, entries=rows, per_page=10)
                await p.paginate()
            else:
                await ctx.send("Error getting albums")
                log.error(get_error_str(r, "error getting albums: "))

    @album.group(name="create")
    @checks.is_bot_admin()
    async def album_create(self, ctx, album_name: str):
        """Creates an album

            ex: album create "Nice Memes" """
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "post",
            f"/albums/discord/{server_id}",
            json={"name": album_name},
        ) as r:
            if r.status == 200:
                data = await r.json()
                await ctx.send(f"Created Album: {album_name}")
            else:
                await ctx.send("Error creating album")
                log.error(get_error_str(r, "error creating album: "))

    @album.group(name="add")
    @checks.is_bot_admin()
    async def album_entry_add(self, ctx, album_name: str, entry: str):
        """Adds link to an album

            ex: album add "Nice Memes" https://i.imgur.com/s8Zf1Qn.jpg """
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "post",
            f"/albums/discord/{server_id}/{album_name}/entries",
            json={"link": entry},
        ) as r:
            if r.status == 200:
                data = await r.json()
                await ctx.send(f"Added entry {entry} to {album_name}")
            else:
                await ctx.send("Error adding entry")
                log.error(get_error_str(r, "error adding entry: "))

    @album.group(name="entries")
    async def album_list(self, ctx, album_name: str):
        """List all the entries in the album """
        server_id = ctx.guild.id
        async with self.bot.backend_request("get", f"/albums/discord/{server_id}/{album_name}/entries") as r:
            if r.status == 200:
                data = await r.json()
                rows = [x['link'] for x in data]
                p = Pages(ctx, entries=rows, per_page=10)
                await p.paginate()
            else:
                await ctx.send("Error getting entries")
                log.error(get_error_str(r, "error getting entries: "))

    # @quotes.group(name="delete")
    # @checks.is_bot_admin()
    # async def alias_delete(self, ctx, quote_id):
    #     """Deletes the specified quote
        
    #         Pass the quote id to delete, you can get them by using \"quote list\"
    #     """
    #     server_id = ctx.guild.id
    #     async with self.bot.backend_request(
    #         "delete", f"/quotes/discord/{server_id}/{quote_id}"
    #     ) as r:
    #         if r.status == 200:
    #             await ctx.send(f"deleted quote {quote_id}")
    #         elif not r.status == 404:
    #             await ctx.send(f"Error deleting alias {quote_id}")
    #             log.error(get_error_str(r, "error making quote delete request: "))
    #         else:
    #             await ctx.send(f"{quote_id} not found")


def setup(bot):
    bot.add_cog(Album(bot))
