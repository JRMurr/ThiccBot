from src import db
from sqlalchemy.dialects.postgresql import BIGINT

class Alias(db.Model):
    __tablename__ = 'alias'
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(BIGINT, db.ForeignKey('discordserver.id'))
    name = db.Column(db.String, doc="name of the alias")
    command = db.Column(db.String, doc="the command with args that the alias maps to")

    server = db.relationship('DiscordServer') # ,backref=db.backref('aliases', lazy=True)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'server_id': self.server_id,
           'name': self.name,
           'command': self.command,
       }
       