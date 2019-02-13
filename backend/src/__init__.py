from flask import Flask, request, abort, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.discord import make_discord_blueprint, discord as dAuth

app = Flask(__name__)
app.secret_key = "supersekrit"  # TODO: do good things here
import os

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DISCORD_ID = os.environ["DISCORD_CLIENT_ID"]
DISCORD_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
BOT_API_TOKEN = os.environ["BOT_API_TOKEN"]

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}"
blueprint = make_discord_blueprint(
    client_id=DISCORD_ID, client_secret=DISCORD_SECRET, scope=["identify", "guilds"]
)
app.register_blueprint(blueprint, url_prefix="/login")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from src.models import Alias, DiscordServer, serverGroup

db.create_all(app=app)
from src.routes import alias as aRoute, discordServers as dsRoute, login as loginRoute


@app.before_request
def before_request():
    is_user = dAuth.authorized
    api_key_passed = request.headers.get("bot-token", "")
    # if (api_key_passed == '') and (not is_user) and request.endpoint not in ('login', 'discord.login', 'discord.authorized'):
    #     return redirect(url_for("login"))
    if (not is_user) and api_key_passed != BOT_API_TOKEN and api_key_passed != "":
        return abort(403)  # a token was passed and it was bad
    g.is_bot = api_key_passed == BOT_API_TOKEN
