from src import db
from sqlalchemy.dialects.postgresql import ARRAY


class KeyWords(db.Model):
    __tablename__ = "keywords"
    id = db.Column(db.Integer, primary_key=True)
    server_group_id = db.Column(
        db.Integer, db.ForeignKey("servergroup.id"), nullable=False
    )
    name = db.Column(db.String, doc="name of the keyword")
    match_case = db.Column(
        db.Boolean,
        default=False,
        doc="If true then the key word must match on case",
    )
    responses = db.Column(ARRAY(db.String), doc="list of keyword responses")

    server = db.relationship("ServerGroup")
