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

# Developing 

While this uses docker to run the bot and flask backend, you can make a conda enviorment so your ide (vsCode) can have autocomplete for the packges.
```bash
conda create -n thiccBot python=3.7 pip
source activate thiccBot
cd bot
pip install -r requirements.txt
cd ..
cd backend
pip install -r requirements.txt
```

## Run
```sh
docker-compose up
```
if you want to run the web interface locally you can do
```sh
docker-compose up

# in a different tab
./runWeb.sh
```


## DB migrate
```sh
docker-compose run flask flask db migrate
docker-compose run flask flask db upgrade
```