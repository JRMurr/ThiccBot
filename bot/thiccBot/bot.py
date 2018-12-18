from discord.ext import commands
import discord
import traceback
import sys

description = '''THICC BOI'''

initial_extensions = [
    'cogs.alias'
]

def _prefix_callable(bot, msg, config):
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
    def __init__(self, config):
        super().__init__(command_prefix=(lambda bot, msg: _prefix_callable(bot, msg, config)),
                        description=description, pm_help=None, owner_id=config['bot_admin'])
        self.config = config
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
