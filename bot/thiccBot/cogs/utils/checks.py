from discord.ext import commands
from discord import utils
import logging

log = logging.getLogger(__name__)


def is_bot_admin():
    """Checks if the user is in the server bot admin role. If it is not set checks if they have manage role permissions"""

    async def predicate(ctx: commands.Context):
        command_name = ctx.command.name
        if not ctx.message.guild:
            log.info(f"attempted to run ${command_name} outside of a server")
            return False
        # if not ctx.command_failed:
        #     log.info(f'attempted to run ${command_name} but it failed')
        #     return False
        bot = ctx.bot
        author = ctx.message.author
        server_id = ctx.message.guild.id
        async with bot.backend_request("get", f"/servers/{server_id}") as r:
            if r.status == 200:
                data = await r.json()
                if data["admin_role"]:
                    admin_role = ctx.message.guild.get_role(data["admin_role"])
                    highest_role = author.roles[-1]
                    return highest_role >= admin_role
            elif r.status == 403:
                log.error(f"no server with id {server_id} found")
            else:
                pass
        return author.guild_permissions.manage_roles

    return commands.check(predicate)


def is_server_owner():
    """Checks if the user is the owner of the server"""

    async def predicate(ctx: commands.Context):
        owner = server_id = ctx.message.guild.owner
        author = ctx.message.author
        return author == owner

    return commands.check(predicate)
