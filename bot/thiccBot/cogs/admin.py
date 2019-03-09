from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import log_and_send_error
import logging
from pprint import pprint

log = logging.getLogger(__name__)


def get_clean_prefix(prefix_type):
    if prefix_type == "command_prefix":
        return "command prefix"
    else:
        return "message prefix"


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

    async def add_prefix(self, ctx, prefix_type, prefix):
        server_id = ctx.message.guild.id
        clean_prefix_type = get_clean_prefix(prefix_type)

        async def on_200(r):
            data = await r.json()
            self.bot.update_prefixes(server_id, data)
            await ctx.send(
                f"({prefix}) has been added to the list of possible {clean_prefix_type}es"
            )

        jsonData = {}
        jsonData[prefix_type] = prefix
        await self.bot.request_helper(
            "put",
            f"/discord/{server_id}",
            ctx,
            json=jsonData,
            error_prefix=f"Error adding {clean_prefix_type}",
            success_function=on_200,
        )

    async def delete_prefix(self, ctx, prefix_type, prefix):
        server_id = ctx.message.guild.id
        clean_prefix_type = get_clean_prefix(prefix_type)

        async def on_200(r):
            data = await r.json()
            self.bot.update_prefixes(server_id, data)
            await ctx.send(
                f"({prefix}) has been removed from the list of possible {clean_prefix_type}es"
            )

        jsonData = {}
        jsonData[f"delete_{prefix_type}"] = prefix
        await self.bot.request_helper(
            "put",
            f"/discord/{server_id}",
            ctx,
            json=jsonData,
            error_prefix=f"Error deleting {clean_prefix_type}",
            success_function=on_200,
        )

    async def list_prefixes(self, ctx, prefix_type):
        server_id = ctx.message.guild.id
        clean_prefix_type = get_clean_prefix(prefix_type)

        async def on_200(r):
            data = await r.json()
            prefixes = data[f"{prefix_type}es"]
            if prefixes is None:
                prefixes = []
            # TODO: show the @botuser command prefix?
            if len(prefixes) > 0:
                if prefix_type == "command_prefix":
                    rows = [f"({x})" for x in prefixes]
                else:
                    rows = prefixes
                p = Pages(ctx, entries=rows, per_page=10)
                await p.paginate()
            elif prefix_type == "command_prefix":
                msg = "This server has no command_prefixes set, "
                msg += f"currently using default prefix ({self.bot.config['command_prefix']})"
                ctx.send(msg)
            else:
                ctx.send("This server has no message prefixes")

        await self.bot.request_helper(
            "get",
            f"/discord/{server_id}",
            ctx,
            error_prefix=f"Error getting {clean_prefix_type}es",
            success_function=on_200,
        )

    @commands.group()
    @checks.is_bot_admin()
    async def command_prefix(self, ctx):
        """Commands for mangaging command prefixes"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help command_prefix")

    @command_prefix.command(name="add")
    async def add_command_prefix(self, ctx, *, prefix: str):
        """Adds a command prefix to the list of possible command prefixes"""
        server_id = ctx.message.guild.id

        await self.add_prefix(ctx, "command_prefix", prefix)

    @command_prefix.command(name="list")
    async def list_command_prefix(self, ctx):
        await self.list_prefixes(ctx, "command_prefix")

    @command_prefix.command(name="delete")
    async def delete_command_prefix(self, ctx, *, prefix: str):
        """Removes a prefix from list of command prefixes for this sever"""
        await self.delete_prefix(ctx, "command_prefix", prefix)

    @commands.group()
    @checks.is_bot_admin()
    async def message_prefix(self, ctx):
        """Commands for mangaging message prefixes"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help message_prefix")

    @message_prefix.command(name="add")
    async def add_message_prefix(self, ctx, *, prefix: str):
        """Adds a command prefix to the list of possible message prefixes"""
        server_id = ctx.message.guild.id
        await self.add_prefix(ctx, "message_prefix", prefix)

    @message_prefix.command(name="list")
    async def list_message_prefix(self, ctx):
        await self.list_prefixes(ctx, "message_prefix")

    @message_prefix.command(name="delete")
    async def delete_message_prefix(self, ctx, *, prefix: str):
        """Removes a prefix from list of command message for this sever"""
        await self.delete_prefix(ctx, "message_prefix", prefix)


def setup(bot):
    bot.add_cog(Admin(bot))
