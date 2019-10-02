from discord.ext import commands
import discord
from thiccBot.cogs.utils.logError import log_with_ctx
import logging
from pprint import pprint

log = logging.getLogger(__name__)


def bool_or_bot_owner(ctx, pred_bool):
    owner_id = ctx.bot.owner_id
    author = ctx.message.author
    return pred_bool or author.id == owner_id


def is_bot_admin():
    """Checks if the user has the server bot admin role.

    If it is not set checks if they have manage role permissions"""

    async def predicate(ctx: commands.Context):
        command_name = ctx.command.name
        if not ctx.message.guild:
            return False
        bot = ctx.bot
        author = ctx.message.author
        server_id = ctx.message.guild.id
        async with bot.backend_request("get", f"/discord/{server_id}") as r:
            if r.status == 200:
                data = await r.json()
                if data["admin_role"]:
                    admin_role = ctx.message.guild.get_role(data["admin_role"])
                    highest_role = author.roles[-1]
                    return bool_or_bot_owner(ctx, highest_role >= admin_role)
            elif r.status == 404:
                await log_with_ctx(
                    log,
                    r,
                    ctx,
                    f"Error checking roles, Server with id {server_id} found: ",
                )
            else:
                await log_with_ctx(log, r, ctx, "Error checking roles: ")
        # if there was an error just see if they can manage roles
        return bool_or_bot_owner(ctx, author.guild_permissions.manage_roles)

    return commands.check(predicate)


def is_server_owner():
    """Checks if the user is the owner of the server"""

    async def predicate(ctx: commands.Context):
        if not ctx.message.guild:
            return False
        owner = server_id = ctx.message.guild.owner
        author = ctx.message.author
        return bool_or_bot_owner(ctx, author == owner)

    return commands.check(predicate)
