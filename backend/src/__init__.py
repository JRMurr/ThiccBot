from flask import Flask, request, abort, redirect, url_for, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api
import os
from .config import Config
from .constants import CONSTANTS


# from flask_dance.contrib.discord import make_discord_blueprint, discord as dAuth

db = SQLAlchemy()
migrate = Migrate()
api = Api()
from src.routes import (
    aliasNs,
    discordNs,
    keyNs,
    quotesNs,
    albumsNs,
    lastFmNs,
    counterNs,
)

namespaces = [aliasNs, discordNs, keyNs, quotesNs, albumsNs, lastFmNs, counterNs]
isDev = os.environ["FLASK_ENV"] == "development"
BOT_API_TOKEN = os.environ["BOT_API_TOKEN"]
# DISCORD_ID = os.environ["DISCORD_CLIENT_ID"]
# DISCORD_SECRET = os.environ["DISCORD_CLIENT_SECRET"]


def create_app(config_class=Config):
    myApp = Flask(__name__)
    myApp.config.from_object(config_class)
    api.init_app(myApp)
    for ns in namespaces:
        api.add_namespace(ns)
    db.init_app(myApp)
    migrate.init_app(myApp, db)
    if "SECRET_KEY" in os.environ:
        myApp.secret_key = os.environ["SECRET_KEY"]
    else:
        myApp.logger.warning(
            "PLEASE SET A SECRET KEY, USING A DEFAULT KEY IS SAD TIMES"
        )
        myApp.secret_key = "supersekrit"
    # blueprint = make_discord_blueprint(
    #     client_id=DISCORD_ID, client_secret=DISCORD_SECRET, scope=["identify", "guilds"]
    # )
    # app.register_blueprint(blueprint, url_prefix="/login")

    return myApp


app = create_app(Config)

from src.models import (
    Alias,
    DiscordServer,
    ServerGroup,
    KeyWords,
    Quotes,
    Album,
    AlbumEntry,
    Counter,
)

# db.create_all(app=app)


@app.route("/api/health")
def healthRoute():
    return jsonify(CONSTANTS)


@app.before_request
def before_request():
    is_user = False  # dAuth.authorized
    api_key_passed = request.headers.get("bot-token", "")
    allow_debug = app.config["TESTING"] or (
        isDev and request.headers.get("Host", "") == "localhost:5000"
    )
    g.is_bot = api_key_passed == BOT_API_TOKEN
    # if (api_key_passed == '') and (not is_user) and request.endpoint not in ('login', 'discord.login', 'discord.authorized'):
    #     return redirect(url_for("login"))
    if not allow_debug and not (is_user or g.is_bot):
        return abort(403)  # a token was passed and it was bad
    g.is_bot = api_key_passed == BOT_API_TOKEN
