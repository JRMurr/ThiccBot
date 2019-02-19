from src import db


class Album(db.Model):
    """An Album is a group of links (hopefully to pictures) to be grouped together
    """

    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True)
    server_group_id = db.Column(db.Integer, db.ForeignKey("servergroup.id"))
    name = db.Column(db.String, nullable=False)
    server_group = db.relationship("ServerGroup")
