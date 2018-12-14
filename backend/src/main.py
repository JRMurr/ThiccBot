from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}'
db = SQLAlchemy(app)
from src.models import alias, discordServer



@app.route("/")
def hello():
    return "Hello World from Flask"

if __name__ == "__main__":
    db.create_all()
    a = discordServer.DiscordServer(name='test')
    db.session.add(a)
    db.session.commit()
    # initDB.setupDB()
    app.run('0.0.0.0', 8000, debug=True)