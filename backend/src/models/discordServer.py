from src import db
from sqlalchemy.dialects.postgresql import BIGINT, ARRAY
from sqlalchemy.ext.mutable import MutableList


class DiscordServer(db.Model):
    __tablename__ = "discordserver"
    id = db.Column(BIGINT, primary_key=True, autoincrement=False)
    server_group_id = db.Column(db.Integer, db.ForeignKey("servergroup.id"))
    name = db.Column(db.String, nullable=False)
    command_prefixes = db.Column(
        MutableList.as_mutable(ARRAY(db.String)), nullable=True
    )
    # a message prefix is a regex string that would be applied to the message
    # before being processed. The regex would just be the prefix to the message
    # so whatever is matched would be removed.
    # its undefined what regex would be applied
    # if two regexes match the same message
    message_prefixes = db.Column(
        MutableList.as_mutable(ARRAY(db.String)), nullable=True
    )
    admin_role = db.Column(BIGINT, nullable=True)

    server_group = db.relationship("ServerGroup")
