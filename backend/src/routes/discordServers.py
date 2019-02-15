from src import app, api
from flask import request, abort, g
from pprint import pformat
from src import db
from src.models import DiscordServer, ServerGroup
from flask import url_for
from flask_dance.contrib.discord import discord as dAuth
from flask_restplus import Resource, fields
from pprint import pprint

ns = api.namespace("api/discord", description="Discord Server operations")


serverModel = ns.model(
    "DiscordServer",
    {
        "name": fields.String,
        "command_prefixes": fields.List(fields.String),
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
                    abort(400)  # TODO: error message for bad id
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


@ns.route("/<int:server_id>")
class DiscordRoute(Resource):
    @ns.marshal_with(serverModel)
    def get(self, server_id):
        return DiscordServer.query.get_or_404(server_id)

    @ns.expect(serverModel)
    @ns.marshal_with(serverModel)
    def put(self, server_id):
        form = ns.payload
        server = DiscordServer.query.get_or_404(server_id)
        if form["admin_role"]:
            server.admin_role = form["admin_role"]
        db.session.commit()
        return server

