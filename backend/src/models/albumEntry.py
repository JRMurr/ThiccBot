from src import db


class AlbumEntry(db.Model):
    __tablename__ = "albumentry"
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    link = db.Column(db.String, doc="the url to the picture")

    album = db.relationship("Album")
