from discord.ext import commands
import discord
import logging
from pprint import pprint
from copy import copy
log = logging.getLogger(__name__)


class Alias:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_alias_command(self, message: discord.Message):
        if message.guild is None:
            return
        for prefix in self.bot.get_command_prefixes(message):
            if message.content.startswith(prefix):
                alias_name = message.content[len(prefix):]
                if alias_name in self.bot.commands:
                    continue
                server_id = message.guild.id
                async with self.bot.backend_request('get', f'/alias/{server_id}/{alias_name}') as r:
                    if r.status == 200:
                        data = await r.json()
                        msg = copy(message)
                        msg.content = prefix + data['command']
                        await self.bot.process_commands(msg)
                    elif r.status == 403:
                        log.error('error making alias get request') #TODO: error info
                break

    async def on_message(self, message: discord.Message):
        author = message.author
        if author.id == self.bot.user.id:
            return
        alias_info = await self.get_alias_command(message)


    # @commands.is_owner()
    @commands.command()
    @commands.guild_only()
    async def alias(self, ctx, name : str, *, args: str):
        """Creates a alias command

            ex: alias sayHi say hi"""
        if name in self.bot.commands or name is "help":
            await ctx.send("dont overwrite big boi commands")
        else:
            pass
            server_id = ctx.guild.id
            async with self.bot.backend_request('post','/alias', json={'name': name, 'command': args, 'server_id': server_id}) as r:
                if r.status == 200:
                    await ctx.send("Created alias " + name)
                else:
                    await ctx.send("Error creating alias")
                    log.error('error sending request to server : ') #TODO: error msg


def setup(bot):
    bot.add_cog(Alias(bot))