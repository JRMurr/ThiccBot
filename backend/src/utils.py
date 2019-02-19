from flask import jsonify
from src import db
from src.models import DiscordServer, ServerGroup
from flask_restplus import abort


def jsonModel(model):
    """calls `.serialize` on model and returns it as json"""
    return jsonify(model.serialize)


def server_group_join(model, server_type, server_id):
    if server_type == "GROUP":
        return model.query.join(ServerGroup)  # .filter(ServerGroup.id == server_id)
    elif server_type == "discord":
        return model.query.join(ServerGroup).join(DiscordServer)
    else:
        abort(400, f"server type {server_type} is not supported")


def get_group_id(server_type, server_id):
    if server_type == "GROUP":
        return server_id
    elif server_type == "discord":
        return DiscordServer.query.get(server_id).server_group_id
    else:
        abort(400, f"server type {server_type} is not supported")
