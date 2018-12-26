from src import db
from sqlalchemy.dialects.postgresql import BIGINT

class DiscordServer(db.Model):
    __tablename__ = 'discordserver'
    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(db.String, nullable=False)
    command_prefix = db.Column(db.String, nullable=True) #TODO: make array for multiple prefixes?

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'command_prefix': self.command_prefix
       }
