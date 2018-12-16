# ThiccBot
Python discord bot

This is a discord bot written in [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite). It has a flask backend so the bot can be configured through a web interface (coming soon™️)

# Bot setup
1. Set up your `.env` file, this stores all credientials/tokens that should not be checked into git. You can look at `example.env` for reference
    1. Copy your Discord bot token into the `DISCORD_ID` field (you can find/make a bot [here](https://discordapp.com/developers/applications/))
    2. setup all other enviorment variables as needed
    3. look at `bot/src/config.yml` and set any settings to what you want
2. Install docker and docker-compose https://docs.docker.com/compose/install/
3. Run `docker-compose up`


# Development stuff

- Discord python api [Docs](http://discordpy.readthedocs.io/en/rewrite/)
    - The rewrite branch is in active development and there will be breaking chanages
    - Join the discord [server](https://discord.gg/r3sSKJJ) to get notified of any breaking chnages
