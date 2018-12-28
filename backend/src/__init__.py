from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
import os
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from src.models import Alias, DiscordServer
db.create_all(app=app)
from src.routes import alias as aRoute, servers as sRoute
