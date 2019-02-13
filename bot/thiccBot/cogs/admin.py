from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Admin:
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
                f"role with name ({role_name}) not found, make sure spelling and capitilization are the same"
            )
            return
        async with self.bot.backend_request(
            "put", f"/servers/{guild.id}", json={"admin_role": desired_role.id}
        ) as r:
            if r.status == 200:
                await ctx.send(
                    f"set the bot admin role to {desired_role.name}, any one who has this role or one above it can run any admin only command"
                )
            else:
                await ctx.send(f"error setting admin role")
                # TODO: log error


def setup(bot):
    bot.add_cog(Admin(bot))
