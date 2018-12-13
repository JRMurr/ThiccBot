import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from src.database.alias import Alias as AliasModel

class Alias(SQLAlchemyObjectType):
    class Meta:
        model = AliasModel
        interfaces = (relay.Node, )


# class AliasConnection(relay.Connection):
#     class Meta:
#         node = Alias