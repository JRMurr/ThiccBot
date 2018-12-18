import os
import asyncio
from thiccBot.bot import ThiccBot
from yaml import load
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

BOT_ID = os.environ['DISCORD_ID']
with open(f'{os.path.dirname(os.path.abspath(__file__))}/config.yml', 'r') as stream:
    config = load(stream)

bot = ThiccBot(config)
bot.run(BOT_ID)