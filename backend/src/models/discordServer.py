from src import db
from sqlalchemy.dialects.postgresql import BIGINT, ARRAY

class DiscordServer(db.Model):
    __tablename__ = 'discordserver'
    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(db.String, nullable=False)
    command_prefix = db.Column(ARRAY(db.String), nullable=True) #TODO: make array for multiple prefixes?
    admin_role = db.Column(BIGINT, nullable=True)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'command_prefixes': self.command_prefix,
           'admin_role': self.admin_role
       }
