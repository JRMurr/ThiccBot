from src import db
from sqlalchemy.dialects.postgresql import BIGINT


class DiscordRole(db.Model):
    __tablename__ = "discord_role"
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(
        BIGINT, db.ForeignKey("discordserver.id"), nullable=False
    )
    role_id = db.Column(
        BIGINT, doc="the id of the role a users can add/remove to themselves"
    )
    message_id = db.Column(
        BIGINT,
        doc="The id of the message that the user will react to get the role",
    )
    channel_id = db.Column(
        BIGINT, doc="The id of the channel that the message is in",
    )

    guild = db.relationship("DiscordServer")
