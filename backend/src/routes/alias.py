from src import app, api
from flask import request, abort
from src import db
from src.models import Alias, DiscordServer, ServerGroup
from src.utils import jsonModel
from flask_restplus import Resource, fields
from pprint import pformat, pprint

ns = api.namespace("api/alias", description="Alias operations")


aliasModel = ns.model("Alias", {"name": fields.String, "command": fields.String})


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class AliasList(Resource):
    """Shows all Aliases and lets you post to add a new one"""

    def get(self, server_type, server_id):
        pass

    @ns.doc("create_alias")
    @ns.expect(aliasModel)
    @ns.marshal_with(aliasModel, code=201)
    def post(self, server_type, server_id):
        """Create a new Alias"""
        form = ns.payload
        app.logger.info(f"form: {pformat(form)}")

        server_group_id = None
        if "discord_id" in form:
            server_group_id = DiscordServer.query.get(
                form["discord_id"]
            ).server_group_id
        else:
            server_group_id = form["server_group_id"]
        if (
            Alias.query.filter_by(
                server_group_id=server_group_id, name=form["name"]
            ).first()
            is not None
        ):
            abort(400)  # alias already exitsts
        alias = Alias(
            server_group_id=server_group_id, name=form["name"], command=form["command"]
        )
        db.session.add(alias)
        db.session.commit()
        return alias


@ns.route("/<server_type>/<int:server_id>/<alias_name>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("alias_name", "The name of the alias")
class AliasRoute(Resource):
    @ns.marshal_with(aliasModel)
    def get(self, server_type, server_id, alias_name):
        alias = None
        # TODO: add constants for accepted server type
        if server_type == "discord":
            alias = (
                Alias.query.join(ServerGroup)
                .join(DiscordServer)
                .filter(DiscordServer.id == server_id, Alias.name == alias_name)
            ).first()
        else:
            abort(400)
        if alias is None:
            abort(404)
        else:
            return alias
