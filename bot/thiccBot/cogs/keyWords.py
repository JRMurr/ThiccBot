from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import get_error_str
import logging
from pprint import pprint
from copy import copy
import random

log = logging.getLogger(__name__)


class KeyWords:
    def __init__(self, bot):
        self.bot = bot

    async def get_key_word(self, message: discord.Message):
        if message.guild is None:
            return
        for prefix in self.bot.get_command_prefixes(message):
            if message.content.startswith(prefix):
                return
        key_word = message.content.strip()
        server_id = message.guild.id
        async with self.bot.backend_request(
            "get", f"/keyWords/discord/{server_id}/{key_word}"
        ) as r:
            if r.status == 200:
                data = await r.json()
                return data["responses"]
            elif r.status == 403:
                log.error("error making key word get request")  # TODO: error info

    async def on_message(self, message: discord.Message):
        author = message.author
        if author.id == self.bot.user.id:
            return
        responses = await self.get_key_word(message)
        if responses:
            ctx = await self.bot.get_context(message)
            await ctx.send(random.choice(responses))

    async def create_or_update_key(self, ctx, name, response, is_update=False):
        server_id = ctx.guild.id
        http_method = "put" if is_update else "post"
        url = f"/keyWords/discord/{server_id}"
        jsonData = {"responses": [response]}
        if is_update:
            url += f"/{name}"
        else:
            jsonData["name"] = name
        async with self.bot.backend_request(http_method, url, json=jsonData) as r:
            if r.status == 200:
                verb = "Updated" if is_update else "Created"
                await ctx.send(f"{verb} key word {name}")
            elif (r.status == 400 and not is_update) or (is_update and r.status == 404):
                msg = f"Alias with name {name} "
                if is_update:
                    msg += "does not exist."
                    msg += f"\nIf you want to create the key word use '{ctx.prefix}keyWord create {name} {response}'"
                else:
                    msg += "already exists."
                    msg += f"\nIf you want to update the key word use '{ctx.prefix}keyWord update {name} {response}'"
                await ctx.send(msg)
            else:
                verb = "updating" if is_update else "creating"
                await ctx.send(f"Error {verb} key word")
                log.error(get_error_str(r, f"error {verb} key word {name}: "))

    @commands.group()
    @commands.guild_only()
    @checks.is_bot_admin()
    async def keyWord(self, ctx):
        """Commands for creating and mangaging key words"""
        if ctx.invoked_subcommand is None:  # or ctx.subcommand_passed == 'box':
            await ctx.send(
                "to create command run 'keyWord create <key_name> <response>'"
            )

    @keyWord.group(name="create", aliases=["set", "make"])
    async def key_create(self, ctx, name: str, *, response: str):
        """Creates a key word

            ex: keyWord create ayy lmao"""
        await self.create_or_update_key(ctx, name, response)

    @keyWord.group(name="update")
    async def key_update(self, ctx, name: str, *, response: str):
        """Updates a key word

            ex: keyWord update ayy lmao"""
        await self.create_or_update_key(ctx, name, response, True)

    @keyWord.group(name="delete")
    async def key_delete(self, ctx, key_name):
        """Deletes the specified key word"""
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "delete", f"/keyWords/discord/{server_id}/{key_name}"
        ) as r:
            if r.status == 200:
                await ctx.send(f"deleted key word {key_name}")
            elif not r.status == 404:
                await ctx.send(f"Error deleting key word {key_name}")
                log.error(get_error_str(r, "error making key word delete request: "))
            else:
                await ctx.send(f"{key_name} not found")


def setup(bot):
    bot.add_cog(KeyWords(bot))
