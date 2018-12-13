from src.database.base import Base
from sqlalchemy import *

class DiscordServer(Base):
    __tablename__ = 'discordserver'
    id = Column(Integer, primary_key=True)
    name = Column(String)