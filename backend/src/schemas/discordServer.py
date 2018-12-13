import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.database.discordServer import DiscordServer as DiscordServerModel

class DiscordServer(SQLAlchemyObjectType):
    class Metas:
        model = DiscordServerModel
        interfaces = (relay.Node, )

# class DiscordServerConnection(relay.Connection):
#     class Meta:
#         node = DiscordServer