from discord.ext import commands
from thiccBot.cogs.utils.requestHelp import requestHelp

class Alias:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        author = message.author
        if author.id == self.bot.user.id:
            return


    # @commands.is_owner()
    @commands.command()
    async def alias(self, ctx, name : str, *, args: str):
        """Creates a alias command

            ex: alias sayHi say hi"""
        if name in self.bot.commands or name is "help":
            await ctx.send("dont overwrite big boi commands you goon")
        else:
            requestHelp.post('/alias', data={'name': name, 'args': args})
            await ctx.send("Created alias " + name)
    
    @commands.command()
    async def say(self, ctx, *, args: str):
        await ctx.send(args)


def setup(bot):
    bot.add_cog(Alias(bot))