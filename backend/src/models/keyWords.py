from src import db
from sqlalchemy.dialects.postgresql import ARRAY


class KeyWords(db.Model):
    __tablename__ = "keywords"
    id = db.Column(db.Integer, primary_key=True)
    server_group_id = db.Column(db.Integer, db.ForeignKey("servergroup.id"))
    name = db.Column(db.String, doc="name of the keyword")
    responses = db.Column(ARRAY(db.String), doc="list of keyword resposnes")

    server = db.relationship("ServerGroup")
