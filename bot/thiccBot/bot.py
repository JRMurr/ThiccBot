from discord.ext import commands
import discord
import traceback
import sys
from pprint import pprint
import logging
from thiccBot.cogs.utils.requestHelp import requestHelp
description = '''THICC BOI'''
log = logging.getLogger(__name__)

def _prefix_callable(bot, msg, config):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    if msg.guild is None:
        base.append(config['command_prefix'])
    else:
        base.extend(bot.prefixes.get(msg.guild.id, [config['command_prefix']]))
    return base

class ThiccBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix=(lambda bot, msg: _prefix_callable(bot, msg, config)),
                        description=description, pm_help=None, owner_id=config['bot_admin'])
        self.config = config
        self.prefixes = {}
        # self.add_command(self.do)
        for extension in config['initial_extensions']:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    def addGuild(self, guild):
        r = requestHelp.post('/servers', data={'name': guild.name, 'id': guild.id})
        data = r.json()
        if 'command_prefix' in data:
            # TODO: check if command prefix is list and make it one if not
            self.prefixes[data['id']] = data['command_prefix'] 
            log.info(f'server: {data['name']}({data['id']}), has command_prefix: {data['command_prefix']}')

    async def on_ready(self):
        for guild in self.guilds:
            self.addGuild(guild)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        await self.process_commands(message)
