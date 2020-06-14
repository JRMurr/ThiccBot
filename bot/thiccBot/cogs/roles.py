from discord.ext import commands, menus
from discord import Guild
from thiccBot.cogs.utils import checks
from thiccBot.bot import ThiccBot
from thiccBot.cogs.utils.logError import get_error_str, log_and_send_error
import logging

log = logging.getLogger(__name__)


class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        tmp = await channel.send(f"Hello {ctx.author}")
        print(tmp)
        return tmp

    @menus.button("\N{THUMBS UP SIGN}")
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f"Thanks {self.ctx.author}!")

    @menus.button("\N{THUMBS DOWN SIGN}")
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, payload):
        self.stop()


class Roles(commands.Cog):
    def __init__(self, bot: ThiccBot):
        # TODO: add on unload to stop menus
        self.bot = bot
        self.initialized_guilds = set()
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            await self.setup_message_listener(guild)

    async def setup_message_listener(self, guild: Guild):
        if guild in self.initialized_guilds:
            return
        async with self.bot.backend_request(
            "get", f"/discord/roles/{guild.id}"
        ) as r:
            if r.status == 200:
                data = await r.json()
                for info in data:
                    # get channel and message objects from ids (discord.util.find/get might work)
                    pass
                self.initialized_guilds.add(guild)
            else:
                log.error(
                    await get_error_str(
                        r,
                        f"Error initializing message listeners for guild ({guild}): ",
                    )
                )

    @commands.group(name="roles", aliases=["role"])
    @commands.guild_only()
    async def roles(self, ctx):
        """Commands for creating and mangaging role assignment messages"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help roles")

    @roles.command(name="tmp")
    async def tmp(self, ctx):
        m = MyMenu()
        data = {
            "role_id": 1,  # TODO: get role id
            "message_id": m.message.id,
            "channel_id": ctx.channel.id,
        }
        async with self.bot.backend_request(
            "POST", f"/discord/roles/{ctx.guild.id}", json=data
        ) as r:
            if r.status == 200:
                await m.start(ctx)
            else:
                log_and_send_error(
                    log, r, ctx, f"Error setting up role message: "
                )


def setup(bot):
    bot.add_cog(Roles(bot))
