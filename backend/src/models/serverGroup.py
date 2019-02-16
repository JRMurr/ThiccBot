from src import db


class ServerGroup(db.Model):
    """A Sever group is a grouping of differnet chat servers that share info
    
    So for example a twitch chat could share the same commands as a discord server
    """

    __tablename__ = "servergroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

