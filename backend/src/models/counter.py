from src import db


class Counter(db.Model):
    __tablename__ = "counter"
    id = db.Column(db.Integer, primary_key=True)
    server_group_id = db.Column(
        db.Integer, db.ForeignKey("servergroup.id"), nullable=False
    )
    name = db.Column(db.String, doc="the name of the counter")
    count = db.Column(db.Integer, doc="the author of the quote")
    response = db.Column(db.String, doc="a custom response string for the count")

    server = db.relationship("ServerGroup")
