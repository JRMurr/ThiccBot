import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from src.schemas import alias, discordServer

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    server = graphene.relay.Node.Field(discordServer.DiscordServer)
    all_Servers = SQLAlchemyConnectionField(discordServer.DiscordServer, sort=None)

    aliases = graphene.relay.Node.Field(alias.Alias)
    all_Aliases = SQLAlchemyConnectionField(alias.Alias, sort=None)

schema = graphene.Schema(query=Query)