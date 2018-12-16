from discord.ext import commands
import discord
from yaml import load
import traceback
import os
import sys
BOT_ID = os.environ['DISCORD_ID']
with open(f'{os.path.dirname(os.path.abspath(__file__))}/config.yml', 'r') as stream:
    config = load(stream)

description = '''THICC BOI'''

initial_extensions = [
    'cogs.alias'
]

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    base.append(config['command_prefix'])
    # TODO: get prefix from backend for servers
    # if msg.guild is None:
    #     base.append('!')
    #     base.append('?')
    # else:
    #     base.extend(bot.prefixes.get(msg.guild.id, ['?', '!']))
    return base

class ThiccBot(commands.Bot):
    def __init__(self):
        # command_prefix=_prefix_callable
        super().__init__(command_prefix=_prefix_callable, description=description,
                        pm_help=None, owner_id=config['bot_admin'])

        # self.add_command(self.do)

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        await self.process_commands(message)

bot = ThiccBot()
bot.run(BOT_ID)