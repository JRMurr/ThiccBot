from src.main import db


class DiscordServer(db.Model):
    __tablename__ = 'discordserver'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    