from src import db

class Alias(db.Model):
    __tablename__ = 'alias'
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('discordserver.id'))
    name = db.Column(db.String, doc="name of the alias")
    command = db.Column(db.String, doc="the command with args that the alias maps to")

    server = db.relationship('DiscordServer') # ,backref=db.backref('aliases', lazy=True)