from discord.ext import commands
import discord
import traceback
import sys
from pprint import pprint
import logging
import aiohttp
import asyncio
import os

BOT_ADMIN = int(os.environ["BOT_ADMIN"])

BACKEND_URL = os.environ["BACKEND_URL"]
BOT_API_TOKEN = os.environ["BOT_API_TOKEN"]
if not BACKEND_URL.endswith("/"):
    BACKEND_URL += "/"


description = """THICC BOI"""
log = logging.getLogger(__name__)


def _prefix_callable(bot, msg):
    config = bot.config
    user_id = bot.user.id
    base = [f"<@!{user_id}> ", f"<@{user_id}> "]
    if msg.guild is None:
        base.append(config["command_prefix"])
    else:
        base.extend(bot.prefixes.get(msg.guild.id, [config["command_prefix"]]))
    return base


class ThiccBot(commands.Bot):
    def __init__(self, config):
        super().__init__(
            command_prefix=_prefix_callable,
            description=description,
            pm_help=None,
            owner_id=BOT_ADMIN,
        )
        self.config = config
        self.prefixes = {}
        headers = {"bot-token": BOT_API_TOKEN}
        self.session = aiohttp.ClientSession(headers=headers, loop=self.loop)
        # self.add_command(self.do)
        for extension in config["initial_extensions"]:
            try:
                self.load_extension(extension)
            except Exception:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()

    def get_command_prefixes(self, msg):
        return _prefix_callable(self, msg)

    def backend_request(
        self, method: str, api_end_point: str, **kwargs
    ) -> aiohttp.ClientResponse:
        """prepends backend server base url to an an api request"""
        if api_end_point.startswith("/"):
            api_end_point = api_end_point[1:]
        url = BACKEND_URL + api_end_point
        # TODO: auth stuff
        return self.session.request(method, url, **kwargs)

    async def add_guild(self, guild):
        async with self.backend_request(
            "post", "/discordServers", json={"name": guild.name, "id": guild.id}
        ) as r:
            data = await r.json()
            if "command_prefix" in data and data["command_prefix"] is not None:
                # TODO: check if command prefix is list and make it one if not
                self.prefixes[data["id"]] = data["command_prefix"]
                log.info(
                    "server: %s, id: %s, has command_prefix: %s",
                    data["name"],
                    data["id"],
                    data["command_prefix"],
                )

    async def on_ready(self):
        for guild in self.guilds:
            await self.add_guild(guild)
        print("Logged on as {0}!".format(self.user))

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_message(self, message):
        await self.process_commands(message)
        # try:
        #     await self.process_commands(message)
        # except commands.CommandNotFound:
        #     # swallow not found errors since all aliases are not 'real' commands
        #     pass
