from discord.ext import commands
import discord
import logging
from pprint import pprint

log = logging.getLogger(__name__)


class Basics:
    """Basic/simple commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, args: str):
        """The bot says what you want it to"""
        await ctx.send(args)

    @commands.command()
    async def about(self, ctx):
        """Tells you information about the bot itself."""

        embed = discord.Embed(description="big doinks")
        embed.title = "nice meme"
        embed.url = "https://niceme.me"
        embed.colour = discord.Colour.blurple()

        owner = self.bot.get_user(self.bot.owner_id)
        embed.set_author(name=str(owner), icon_url=owner.avatar_url)

        # statistics
        total_members = sum(1 for _ in self.bot.get_all_members())
        total_online = len(
            {
                m.id
                for m in self.bot.get_all_members()
                if m.status is not discord.Status.offline
            }
        )
        total_unique = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        embed.add_field(
            name="Members",
            value=f"{total_members} total\n{total_unique} unique\n{total_online} unique online",
        )
        embed.add_field(
            name="Channels", value=f"{text + voice} total\n{text} text\n{voice} voice"
        )

        embed.add_field(name="Guilds", value=len(self.bot.guilds))
        embed.set_footer(
            text="Made with discord.py", icon_url="http://i.imgur.com/5BFecvA.png"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Basics(bot))
