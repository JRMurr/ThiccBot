from discord.ext import commands
from discord.ext.commands import Cog
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error, get_error_str
import logging
from pprint import pprint
from copy import copy
import random

log = logging.getLogger(__name__)


class KeyWords(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_key_word(self, message: discord.Message):
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
                log.error(
                    await get_error_str(
                        r, "Error making key word get request: "
                    )
                )

    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author == self.bot.user:
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
        async with self.bot.backend_request(
            http_method, url, json=jsonData
        ) as r:
            if r.status == 200:
                verb = "Updated" if is_update else "Created"
                await ctx.send(f"{verb} key word {name}")
            elif (r.status == 400 and not is_update) or (
                is_update and r.status == 404
            ):
                msg = f"Alias with name {name} "
                if is_update:
                    msg += "does not exist."
                    f"\nIf you want to create the key word use '"
                    f"{ctx.prefix}keyWord create {name} {response}'"
                else:
                    msg += "already exists."
                    f"\nIf you want to update the key word use '"
                    f"{ctx.prefix}keyWord update {name} {response}'"
                await ctx.send(msg)
            else:
                verb = "updating" if is_update else "creating"
                await log_and_send_error(log, r, ctx, f"Error {verb} key word")

    @commands.group(name="keyWord", aliases=["keyword", "keywords", "keyWords"])
    @commands.guild_only()
    async def keyWord(self, ctx):
        """Commands for creating and mangaging key words"""
        if ctx.invoked_subcommand is None:  # or ctx.subcommand_passed == 'box':
            await ctx.send(
                "to create command run 'keyWord create <key_name> <response>'"
            )

    @keyWord.command(name="create", aliases=["set", "make", "add", "save"])
    @checks.is_bot_admin()
    async def key_create(self, ctx, name: str, *, response: str):
        """Creates a key word

            ex: keyWord create ayy lmao"""
        await self.create_or_update_key(ctx, name, response)

    @keyWord.command(name="update")
    @checks.is_bot_admin()
    async def key_update(self, ctx, name: str, *, response: str):
        """Updates a key word

            ex: keyWord update ayy lmao"""
        await self.create_or_update_key(ctx, name, response, True)

    @keyWord.command(name="set_case_match")
    @checks.is_bot_admin()
    async def key_set_case_match(self, ctx, key_name: str, match_case: bool):
        """Sets if the key should match case or not

            ex: `keyWord set_case_match ayy true` or
            `keyWord set_case_match ayy false`
        """
        server_id = ctx.guild.id

        async def on_200(r):
            if match_case:
                await ctx.send(f"{key_name} will now check if cases match")
            else:
                await ctx.send(f"{key_name} will not check if cases match")

        async def on_404(r):
            await ctx.send(f"{key_name} not found")

        await self.bot.request_helper(
            "put",
            f"/keyWords/discord/{server_id}/{key_name}",
            ctx,
            json={"match_case": match_case},
            error_prefix=f"Error updating case of key word {key_name}",
            success_function=on_200,
            error_handler={404: on_404},
        )

    @keyWord.command(name="list")
    async def key_list(self, ctx, show_response: bool = False):
        """List all the key word for this server"""
        server_id = ctx.guild.id

        def get_key_str(key_info, show_responses):
            s = f"{key_info['name']}"
            if show_responses:
                s += f" -> {key_info['responses']}"
            return s

        async def on_200(r):
            data = await r.json()
            rows = [get_key_str(x, show_response) for x in data]
            p = Pages(ctx, entries=rows, per_page=10)
            await p.paginate()

        await self.bot.request_helper(
            "get",
            f"/keyWords/discord/{server_id}",
            ctx,
            error_prefix="Error getting key words",
            success_function=on_200,
        )

    @keyWord.command(name="delete")
    @checks.is_bot_admin()
    async def key_delete(self, ctx, key_name):
        """Deletes the specified key word"""
        server_id = ctx.guild.id

        async def on_200(r):
            await ctx.send(f"deleted key word {key_name}")

        async def on_404(r):
            await ctx.send(f"{key_name} not found")

        await self.bot.request_helper(
            "delete",
            f"/keyWords/discord/{server_id}/{key_name}",
            ctx,
            error_prefix=f"Error deleting key word {key_name}",
            success_function=on_200,
            error_handler={404: on_404},
        )


def setup(bot):
    bot.add_cog(KeyWords(bot))
