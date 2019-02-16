from src import db


class Quotes(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    server_group_id = db.Column(db.Integer, db.ForeignKey("servergroup.id"))
    quote_str = db.Column(db.String, doc="the actual quoute")
    author = db.Column(db.String, doc="the author of the quote")

    server = db.relationship("ServerGroup")
