import discord
from enum import Enum

class PlayerState(Enum):
    STOPPED = 0
    PLAYING = 1

class Player:
    def __init__(self, voice_client):
        self.state = PlayerState.STOPPED
        self.voice_client = voice_client

    async def play(self, ctx):
        await ctx.send("playing")
