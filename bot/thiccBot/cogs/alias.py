from discord.ext import commands
import discord
from thiccBot.cogs.utils import checks
from thiccBot.cogs.utils.paginator import Pages
from thiccBot.cogs.utils.logError import get_error_str
from thiccBot import message_checks
import logging
from pprint import pprint
from copy import copy

log = logging.getLogger(__name__)


def get_alias_str(alias_info, show_commands):
    s = f"{alias_info['name']}"
    if show_commands:
        s += f" -> {alias_info['command']}"
    return s


class Alias:
    def __init__(self, bot):
        self.bot = bot

    async def get_alias_command(self, message: discord.Message):
        if message.guild is None:
            return
        for prefix in self.bot.get_command_prefixes(message):
            if message.content.startswith(prefix):
                alias_name = message.content[len(prefix) :].split(" ")[0]
                comand_names = [x.name for x in self.bot.commands]
                if alias_name in comand_names:
                    continue
                server_id = message.guild.id
                async with self.bot.backend_request(
                    "get", f"/alias/discord/{server_id}/{alias_name}"
                ) as r:
                    if r.status == 200:
                        data = await r.json()
                        msg = copy(message)
                        msg.content = prefix + data["command"]
                        await self.bot.process_commands(msg)
                    elif not r.status == 404:
                        log.error(get_error_str(r, "error making alias get request: "))
                break

    @message_checks()
    async def on_message(self, message: discord.Message):
        alias_info = await self.get_alias_command(message)

    async def create_or_update_alias(self, ctx, name, args, is_update=False):
        server_id = ctx.guild.id
        http_method = "put" if is_update else "post"
        url = f"/alias/discord/{server_id}"
        jsonData = {"command": args}
        if is_update:
            url += f"/{name}"
        else:
            jsonData["name"] = name
        if name in self.bot.commands or name is "help":
            await ctx.send(f"Alias {name} is a built in bot command")
        else:
            async with self.bot.backend_request(http_method, url, json=jsonData) as r:
                if r.status == 200:
                    verb = "Updated" if is_update else "Created"
                    await ctx.send(f"{verb} alias {name}")
                elif (r.status == 400 and not is_update) or (
                    is_update and r.status == 404
                ):
                    msg = f"Alias with name {name} "
                    if is_update:
                        msg += "does not exist."
                        msg += f"\nIf you want to create the alias use '{ctx.prefix}alias create {name} {args}'"
                    else:
                        msg += "already exists."
                        msg += f"\nIf you want to update the alias use '{ctx.prefix}alias update {name} {args}'"
                    await ctx.send(msg)
                else:
                    verb = "updating" if is_update else "creating"
                    await ctx.send(f"Error {verb} alias")
                    log.error(get_error_str(r, f"error {verb} alias {name}: "))

    @commands.group()
    @commands.guild_only()
    @checks.is_bot_admin()
    async def alias(self, ctx):
        """Commands for creating and mangaging aliases"""
        if ctx.invoked_subcommand is None:  # or ctx.subcommand_passed == 'box':
            await ctx.send(
                "to create alias run 'alias create <alias_name> <command_to_run>'"
            )

    @alias.group(name="create", aliases=["set", "make"])
    async def alias_create(self, ctx, name: str, *, args: str):
        """Creates a alias command

            ex: alias create sayHi say hi"""
        await self.create_or_update_alias(ctx, name, args)

    @alias.group(name="update")
    async def alias_update(self, ctx, name: str, *, args: str):
        """Updates a alias command

            ex: alias update sayHi say hi"""
        await self.create_or_update_alias(ctx, name, args, True)

    @alias.group(name="list")
    async def alias_list(self, ctx, show_command: bool = False):
        """List all the aliases for this server"""
        server_id = ctx.guild.id
        async with self.bot.backend_request("get", f"/alias/discord/{server_id}") as r:
            if r.status == 200:
                data = await r.json()

                rows = [get_alias_str(x, show_command) for x in data]
                p = Pages(ctx, entries=rows, per_page=10)
                await p.paginate()
            else:
                await ctx.send("Error getting aliases")
                log.error(get_error_str(r, "error creating alias {name}: "))

    @alias.group(name="delete")
    async def alias_delete(self, ctx, alias_name):
        """Deletes the specified alias"""
        server_id = ctx.guild.id
        async with self.bot.backend_request(
            "delete", f"/alias/discord/{server_id}/{alias_name}"
        ) as r:
            if r.status == 200:
                await ctx.send(f"deleted alias {alias_name}")
            elif not r.status == 404:
                await ctx.send(f"Error deleting alias {alias_name}")
                log.error(get_error_str(r, "error making alias delete request: "))
            else:
                await ctx.send(f"{alias_name} not found")


def setup(bot):
    bot.add_cog(Alias(bot))
