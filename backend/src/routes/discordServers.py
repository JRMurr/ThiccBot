from src import app, api
from flask import request, g
from pprint import pformat
from src import db
from src.models import DiscordServer, ServerGroup
from flask import url_for
from flask_dance.contrib.discord import discord as dAuth
from flask_restplus import Resource, fields, abort
from pprint import pprint

ns = api.namespace("api/discord", description="Discord Server operations")

# NOTE: discord bot assumes both command_prefixes and message_prefixes will always be returned
# this only matters for commands that updates prefixes
serverModel = ns.model(
    "DiscordServer",
    {
        "name": fields.String,
        "command_prefixes": fields.List(fields.String),
        "message_prefixes": fields.List(fields.String),
        "server_group_id": fields.Integer,
        "id": fields.Integer,
        "admin_role": fields.Integer,
    },
)


def id_to_str(serverJson):
    # The reason front end has issues with big int
    # so if not the bot convert the id to a string
    if not g.is_bot:
        serverJson["id"] = str(serverJson["id"])
    return serverJson


@ns.route("")
class ServerList(Resource):
    """Shows all Servers and lets you post to add a new one"""

    def get(self):
        return DiscordServer.query.all()

    @ns.doc("create_discord_server")
    @ns.expect(serverModel)
    @ns.marshal_with(serverModel, code=201)
    def post(self):
        form = ns.payload
        serverId = form["id"]
        serverName = form["name"]
        server = DiscordServer.query.get(serverId)
        if server is None:
            serverGroup = None
            if "server_group_id" in form:
                serverGroup = ServerGroup.query.get(form["server_group_id"])
                if serverGroup is None:
                    abort(400, "Passed server group does not exist")
            else:
                serverGroup = ServerGroup(name=f"{serverName}_group")
                db.session.add(serverGroup)

            server = DiscordServer(
                id=serverId, name=serverName, server_group=serverGroup
            )
            db.session.add(server)
            db.session.commit()
            app.logger.info(f"added server: {server}")
            return server
        else:
            abort(404)


POSSIBLE_PREFIXES = ["command_prefixes", "message_prefixes"]


def get_prefixes(server, prefix_type):
    if prefix_type not in POSSIBLE_PREFIXES:
        abort(500)
    if prefix_type == "command_prefixes":
        return server.command_prefixes if server.command_prefixes is not None else []
    else:
        return server.message_prefixes if server.message_prefixes is not None else []


def add_prefix(server, prefix_type, new_prefix):
    prefixes = get_prefixes(server, prefix_type)
    if new_prefix in prefixes:
        abort(400, f"({new_prefix}) is already a prefix")
    prefixes.append(new_prefix)
    if prefix_type == "command_prefixes":
        server.command_prefixes = prefixes
    else:
        server.message_prefixes = prefixes
    return server


def remove_prefix(server, prefix_type, delete_prefix):
    prefixes = get_prefixes(server, prefix_type)
    if delete_prefix in prefixes:
        prefixes.remove(delete_prefix)
    else:
        abort(400, f"({delete_prefix}) is not in the list of prefixes for this server")
    if prefix_type == "command_prefixes":
        server.command_prefixes = prefixes
    else:
        server.message_prefixes = prefixes
    return server


@ns.route("/<int:server_id>")
class DiscordRoute(Resource):
    @ns.marshal_with(serverModel)
    def get(self, server_id):
        return DiscordServer.query.get_or_404(server_id)

    @ns.expect(serverModel)
    @ns.marshal_with(serverModel)
    def put(self, server_id):
        server = DiscordServer.query.get_or_404(server_id)
        if "admin_role" in ns.payload:
            server.admin_role = ns.payload["admin_role"]
        if "command_prefix" in ns.payload:
            server = add_prefix(
                server, "command_prefixes", ns.payload["command_prefix"]
            )
        if "delete_command_prefix" in ns.payload:
            server = remove_prefix(
                server, "command_prefixes", ns.payload["delete_command_prefix"]
            )
        if "message_prefix" in ns.payload:
            server = add_prefix(
                server, "message_prefixes", ns.payload["message_prefix"]
            )
        if "delete_message_prefix" in ns.payload:
            server = remove_prefix(
                server, "message_prefixes", ns.payload["delete_message_prefix"]
            )
        db.session.commit()
        return server

