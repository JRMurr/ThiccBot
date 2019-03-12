from src import app, api
from flask import request, g
from src import db
from src.models import ServerGroup
from flask_dance.contrib.discord import discord as dAuth
from flask_restplus import Resource, fields, abort
from src.utils import IdType


ns = api.namespace("api/serverGroup", description="Server Group operations")
serverModel = ns.model("DiscordServer", {"name": fields.String, "id": IdType})


@ns.route("")
class ServerGroupList(Resource):
    """Shows all Discord Server and lets you post to add a new one"""

    @ns.doc("server_list")
    @ns.marshal_with(serverModel)
    def get(self):
        """Lists all discord servers"""
        return ServerGroup.query.all()

    @ns.doc("create_discord_server")
    @ns.expect(serverModel)
    @ns.marshal_with(serverModel, code=200)
    def post(self):
        form = ns.payload
        serverGroup = ServerGroup.query.filter_by(name=form["name"])
        if serverGroup is None:
            serverGroup = ServerGroup(name=form["name"])
            db.session.add(serverGroup)
            db.session.commit()
            return serverGroup
        else:
            abort(400, f"server group with name {form['name']} already exists")
