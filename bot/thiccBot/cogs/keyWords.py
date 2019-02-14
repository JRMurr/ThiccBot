from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
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
                log.error("error making alias get request")  # TODO: error info

    async def on_message(self, message: discord.Message):
        author = message.author
        if author.id == self.bot.user.id:
            return
        responses = await self.get_key_word(message)
        if responses:
            ctx = await self.bot.get_context(message)
            await ctx.send(random.choice(responses))

    @commands.command()
    @commands.guild_only()
    @checks.is_bot_admin()
    async def set_key_word(self, ctx, name: str, *, response: str):
        """Creates a keyword

            ex: keyword \"key\" \"response\""""
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "post",
            f"/keyWords/discord/{server_id}",
            json={"name": name, "responses": [response]},
        ) as r:
            if r.status == 200:
                await ctx.send(f"created keyword: <{name}>\nresponse: <{response}>")
            else:
                await ctx.send("Error creating keyword")
                log.error("error sending request to server : ")  # TODO: error msg


def setup(bot):
    bot.add_cog(KeyWords(bot))
