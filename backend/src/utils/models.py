from flask import jsonify
from src import db
from src.models import DiscordServer, ServerGroup
from flask_restplus import abort


def get_server_group(server_type, server_id):
    if server_type == "GROUP":
        return ServerGroup.query.get(server_id)
    elif server_type == "discord":
        return DiscordServer.query.get(server_id).server_group
    else:
        abort(400, f"server type {server_type} is not supported")


def server_group_join(model, server_type, server_id):
    if server_type == "GROUP":
        return model.query.join(ServerGroup).filter(ServerGroup.id == server_id)
    elif server_type == "discord":
        return (
            model.query.join(ServerGroup)
            .join(DiscordServer)
            .filter(DiscordServer.id == server_id)
        )
    else:
        abort(400, f"server type {server_type} is not supported")


def get_group_id(server_type, server_id):
    if server_type == "GROUP":
        return server_id
    elif server_type == "discord":
        return DiscordServer.query.get(server_id).server_group_id
    else:
        abort(400, f"server type {server_type} is not supported")
