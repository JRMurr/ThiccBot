import os
import asyncio
from thiccBot.bot import ThiccBot
from yaml import load
import logging
from contextlib import contextmanager, asynccontextmanager
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

BOT_ID = os.environ['DISCORD_ID']
with open(f'{os.path.dirname(os.path.abspath(__file__))}/config.yml', 'r') as stream:
    config = load(stream)

@contextmanager
def setup_logging():
    try:
        # __enter__
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='thiccBot.log', encoding='utf-8', mode='w')
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)
        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    with setup_logging():
        bot = ThiccBot(config)
        try:
            loop.run_until_complete(bot.start(BOT_ID))
        except KeyboardInterrupt:
            loop.run_until_complete(bot.logout())
            loop.run_until_complete(bot.close_sessions())
        finally:
            loop.close()