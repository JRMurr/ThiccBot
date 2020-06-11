from discord.ext import commands
from thiccBot.cogs.utils import checks
from discord.ext import menus


class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        return await channel.send(f"Hello {ctx.author}")

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
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="roles", aliases=["role"])
    @commands.guild_only()
    async def roles(self, ctx):
        """Commands for creating and mangaging role assignment messages"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help roles")

    @roles.command(name="tmp")
    async def tmp(self, ctx):
        m = MyMenu()
        await m.start(ctx)


def setup(bot):
    bot.add_cog(Roles(bot))
