# ThiccBot
Python discord bot

This is a discord bot written in [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite). It has a flask backend so the bot can be configured through a web interface (coming soon™️)

# Bot setup
1. Set up your `.env` file, this stores all credentials/tokens that should not be checked into git. You can look at `example.env` for reference
    1. Copy your Discord bot token into the `DISCORD_ID` field (you can find/make a bot [here](https://discordapp.com/developers/applications/))
    2. setup all other environment variables as needed
    3. look at `bot/src/config.yml` and set any settings to what you want
2. Set `BOT_API_TOKEN` in `.env` to a random string, you can run the following to generate one 
    ```python
    import secrets
    print(secrets.token_urlsafe())
    ```
    use the same process to set `FLASK_SECRET_KEY`
3. Install docker and docker-compose https://docs.docker.com/compose/install/
4. Run `docker-compose up`

# Developing 

While this uses docker to run the bot and flask backend, you can make a conda environment so your ide (vsCode) can have autocomplete for the packages.
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
Run the following command when ever you change or add a model. Not all changes will be detected so look over the generated scripts. More info [here](https://flask-migrate.readthedocs.io/en/latest/)
```sh
docker-compose run flask flask db migrate
```
After looking over the scripts and it looks good run
```sh
docker-compose run flask flask db upgrade
```
If you are starting with a fresh container after changing models first build and run everything then run `docker-compose run flask flask db migrate`

If the db has data and the migration thinks the db is not on the latest migration version run 
`docker-compose run flask flask db stamp <last revision>` to get things working


## connect to db
```sh
source .env
docker exec -it thiccbot_postgres_1 psql -U $THICC_USER -w $THICC_PASSWORD -d $THICC_DB
```

## Python formatting
Use the python formatter black, install it with `pip install black`.
