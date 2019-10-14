from discord.ext import commands
import discord
import logging
import random
import copy
import emoji
from pprint import pprint

log = logging.getLogger(__name__)


class Basics(commands.Cog):
    """Basic/simple commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, args: str):
        """The bot says what you want it to"""
        await ctx.send(args)

    @commands.command(
        description="For when you wanna settle the score some other way"
    )
    async def choose(self, ctx, *choices: str):
        await ctx.send(random.choice(choices))

    @commands.command(description="Randomly shuffles your choices")
    async def choose_list(self, ctx, *choices: str):
        """Randomly shuffles your choices"""
        res = list(choices)
        random.shuffle(res)  # in-place shuffle
        print(res)
        await ctx.send(", ".join(res))

    @commands.command(name="do_multiple", aliases=["repeat"])
    async def do_multiple(self, ctx, numTimes: int, *, command: str):
        """does the passed command the specified number of times"""
        if command.startswith(("do_multiple", "repeat")):
            await ctx.send("u fukin thot")
            return
        msg = copy.copy(ctx.message)
        msg.content = f"{ctx.prefix}{command}"
        print(msg)
        if numTimes > 5:
            await ctx.send("thats too many times boi chill")
            return
        for i in range(numTimes):
            await self.bot.on_message(msg)

    @commands.command()
    async def meme_text(self, ctx, *args):
        msg = ""
        if len(args) < 1:
            return
        for word in args:
            for char in word:
                if char not in emoji.UNICODE_EMOJI:
                    msg += chr(0xFEE0 + ord(char))
                else:
                    msg += char
            msg += "  "
        await ctx.send(msg)

    def digit_to_word(self, digit):
        if not isinstance(digit, str):
            digit = str(digit)
        if not digit.isalnum():
            return ""
        if digit == "1":
            return "one"
        elif digit == "2":
            return "two"
        elif digit == "3":
            return "three"
        elif digit == "4":
            return "four"
        elif digit == "5":
            return "five"
        elif digit == "6":
            return "six"
        elif digit == "7":
            return "seven"
        elif digit == "8":
            return "eight"
        elif digit == "9":
            return "nine"
        elif digit == "0":
            return "zero"
        return digit

    @commands.command()
    async def emoji_text(self, ctx, *args):
        """Usage: emoji_text <Words to be returned in emoji characters>

        Uses discord regional indicators to return text as emojis
        """
        msg = ""
        if len(args) < 1:
            return
        for word in args:
            for char in word:
                if char.isalnum():
                    if char.isdigit():
                        msg += ":{}:".format(self.digit_to_word(char))
                    else:
                        msg += ":regional_indicator_{}:".format(char.lower())
                else:
                    msg += char
            if len(msg) >= 1500:
                await ctx.send(msg)
                msg = ""
            msg += "  "

        await ctx.send(msg)

    @commands.command()
    async def about(self, ctx):
        """Tells you information about the bot itself."""

        embed = discord.Embed(description="big doinks")
        embed.title = "nice meme"
        embed.url = "https://niceme.me"
        embed.colour = discord.Colour.blurple()

        owner = self.bot.get_user(self.bot.owner_id)
        if owner is not None:
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

        members_str = f"{total_members} total\n{total_unique} "
        members_str += f"unique\n{total_online}unique online"
        embed.add_field(name="Members", value=members_str)
        embed.add_field(
            name="Channels",
            value=f"{text + voice} total\n{text} text\n{voice} voice",
        )

        embed.add_field(name="Guilds", value=len(self.bot.guilds))
        embed.set_footer(
            text="Made with discord.py",
            icon_url="http://i.imgur.com/5BFecvA.png",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Basics(bot))
