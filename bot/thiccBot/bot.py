from discord.ext import commands
import discord
import traceback
import sys
from pprint import pprint
import logging
import aiohttp
import asyncio
import os
import functools
import copy
from thiccBot.cogs.utils.logError import get_error_str

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


def message_checks(delete_check=False):
    def actualDec(f):
        @functools.wraps(f)
        async def wrapper(*args, **kw):
            args = list(args)
            message = copy.copy(args[1])  # 0 is self
            if message.author.bot:
                return
            deleteMessage = False
            if message.content.lower().endswith("-del"):
                deleteMessage = delete_check
                message.content = message.content[:-4].strip()
                args[1] = message
            await f(*args, **kw)
            if deleteMessage:
                await args[1].delete()  # use the 'real' message to call delete

        return wrapper

    return actualDec


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

    async def get_guild(self, guild):
        async with self.backend_request("get", f"/discord/{guild.id}") as r:
            if r.status == 200:
                return await r.json()
            else:
                return None

    async def add_guild(self, guild):
        async with self.backend_request(
            "post", "/discord", json={"name": guild.name, "id": guild.id}
        ) as r:
            if r.status == 200:
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
            else:
                log.error(get_error_str(r, "Error adding guild: "))

    async def on_ready(self):
        for guild in self.guilds:
            if not await self.get_guild(guild):
                await self.add_guild(guild)
        print("Logged on as {0}!".format(self.user))

    async def close(self):
        await super().close()
        await self.session.close()

    # https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        print("ERRROR")
        print(error)
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except:
                pass

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

    @message_checks(delete_check=True)
    async def on_message(self, message):
        await self.process_commands(message)
