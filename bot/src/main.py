import discord
from yaml import load
import os

with open('config.yml', 'r') as stream:
    config = load(stream)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(os.environ['DISCORD_ID'])