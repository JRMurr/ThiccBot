from src import db
from sqlalchemy.dialects.postgresql import BIGINT


class Alias(db.Model):
    __tablename__ = "alias"
    id = db.Column(db.Integer, primary_key=True)
    server_group_id = db.Column(db.Integer, db.ForeignKey("servergroup.id"))
    name = db.Column(db.String, doc="name of the alias")
    command = db.Column(db.String, doc="the command with args that the alias maps to")

    server = db.relationship("ServerGroup")  # ,backref=db.backref('aliases', lazy=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "server_group_id": self.server_group_id,
            "name": self.name,
            "command": self.command,
        }
