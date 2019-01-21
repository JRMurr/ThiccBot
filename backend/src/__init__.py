from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.discord import make_discord_blueprint
app = Flask(__name__)
app.secret_key = "supersekrit" #TODO: do good things here
import os
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']
DISCORD_ID = os.environ['DISCORD_CLIENT_ID']
DISCORD_SECRET = os.environ['DISCORD_CLIENT_SECRET']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}'
blueprint = make_discord_blueprint(
    client_id=DISCORD_ID,
    client_secret=DISCORD_SECRET,
    scope=['identify', 'guilds']
)
app.register_blueprint(blueprint, url_prefix="/login")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from src.models import Alias, DiscordServer
db.create_all(app=app)
from src.routes import alias as aRoute, servers as sRoute, login as loginRoute
