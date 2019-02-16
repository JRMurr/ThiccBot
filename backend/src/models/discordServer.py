from src import db
from sqlalchemy.dialects.postgresql import BIGINT, ARRAY


class DiscordServer(db.Model):
    __tablename__ = "discordserver"
    id = db.Column(BIGINT, primary_key=True, autoincrement=False)
    server_group_id = db.Column(db.Integer, db.ForeignKey("servergroup.id"))
    name = db.Column(db.String, nullable=False)
    command_prefix = db.Column(ARRAY(db.String), nullable=True)
    admin_role = db.Column(BIGINT, nullable=True)
    server_group = db.relationship("ServerGroup")
