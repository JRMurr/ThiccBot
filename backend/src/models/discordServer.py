from src import db


class DiscordServer(db.Model):
    __tablename__ = 'discordserver'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String, nullable=False)
    command_prefix = db.Column(db.String, nullable=True) #TODO: make array for multiple prefixes?
    