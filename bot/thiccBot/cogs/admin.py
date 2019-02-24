from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Admin(commands.Cog):
    """Admin commands to manage the bot in each server"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_server_owner()
    async def set_bot_admin(self, ctx, role_name: str):
        """Sets the bot admin role in this server

        Users with this role can run commands to edit the bots config for this server"""
        guild = ctx.message.guild
        server_roles = guild.roles
        desired_role = next((x for x in server_roles if x.name == role_name), None)
        if desired_role is None:
            await ctx.send(
                f"role with name ({role_name}) not found, make sure spelling and capitalization are the same"
            )
            return

        async def on_200(r):
            await ctx.send(
                f"set the bot admin role to {desired_role.name}, any one who has this role or one above it can run any admin only command"
            )

        await self.bot.request_helper(
            "put",
            f"/discord/{guild.id}",
            ctx,
            json={"admin_role": desired_role.id},
            error_prefix="Error setting admin role",
            success_function=on_200,
        )

    @commands.group()
    @checks.is_bot_admin()
    async def command_prefix(self, ctx):
        """Commands for mangaging command prefixes"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help add_command_prefix")

    @command_prefix.command(name="add")
    async def add_command_prefix(self, ctx, prefix: str):
        """Adds a command prefix to the list of possible command prefixes"""
        server_id = ctx.message.guild.id

        async def on_200(r):
            data = await r.json()
            self.bot.prefixes[server_id] = data["command_prefixes"]
            await ctx.send(
                f"({prefix}) has been added to the list of possible command prefixes"
            )

        await self.bot.request_helper(
            "put",
            f"/discord/{server_id}",
            ctx,
            json={"command_prefix": prefix},
            error_prefix="Error adding command prefix",
            success_function=on_200,
        )

    @command_prefix.command(name="list")
    async def list_command_prefix(self, ctx):
        """List all command prefixes"""
        server_id = ctx.message.guild.id

        async def on_200(r):
            data = await r.json()
            prefixes = data["command_prefixes"]
            if prefixes is None:
                prefixes = []
            # TODO: show the @botuser prefix?
            if len(prefixes) > 0:
                rows = [f"({x})" for x in data["command_prefixes"]]
                p = Pages(ctx, entries=rows, per_page=10)
                await p.paginate()
            else:
                msg = "This server has no command_prefixes set, "
                msg += f"currently using default prefix ({self.bot.config['command_prefix']})"

        await self.bot.request_helper(
            "get",
            f"/discord/{server_id}",
            ctx,
            error_prefix="Error getting command prefixes",
            success_function=on_200,
        )

    @command_prefix.command(name="delete")
    async def delete_command_prefix(self, ctx, prefix: str):
        """Removes a prefix from list of command prefixes for this sever"""
        server_id = ctx.message.guild.id
        async with self.bot.backend_request(
            "put", f"/discord/{server_id}", json={"delete_command_prefix": prefix}
        ) as r:
            if r.status == 200:
                data = await r.json()
                self.bot.prefixes[server_id] = data["command_prefixes"]
                await ctx.send(
                    f"({prefix}) has been removed from the list of command_prefixes"
                )
            else:
                await log_and_send_error(log, r, ctx, "Error deleting command prefix")


def setup(bot):
    bot.add_cog(Admin(bot))
