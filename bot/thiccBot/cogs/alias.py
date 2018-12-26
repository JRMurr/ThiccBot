from discord.ext import commands
from thiccBot.cogs.utils.requestHelp import requestHelp
import logging
log = logging.getLogger(__name__)


class Alias:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        author = message.author
        if author.id == self.bot.user.id:
            return


    # @commands.is_owner()
    @commands.command()
    @commands.guild_only()
    async def alias(self, ctx, name : str, *, args: str):
        """Creates a alias command

            ex: alias sayHi say hi"""
        if name in self.bot.commands or name is "help":
            await ctx.send("dont overwrite big boi commands")
        else:
            server_id = ctx.guild.id
            r = requestHelp.post('/alias', data={'name': name, 'args': args, 'server_id': server_id})
            if r.status_code == 200:
                await ctx.send("Created alias " + name)
            else:
                await ctx.send("Error creating alias")
                log.error('error sending request to server : ') #TODO: error msg

    @commands.command()
    async def say(self, ctx, *, args: str):
        await ctx.send(args)


def setup(bot):
    bot.add_cog(Alias(bot))