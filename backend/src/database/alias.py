from src.database.base import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.database.discordServer import DiscordServer
class Alias(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey(DiscordServer.id))
    name = Column(String, doc="name of the alias")
    command = Column(String, doc="the command with args that the alias maps to")

    server = relationship("DiscordServer")