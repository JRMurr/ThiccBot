from src import app, api
from src import db
from src.models import Alias, DiscordServer, ServerGroup
from flask_restplus import Resource, fields, abort
from src.utils import server_group_join, get_group_id

ns = api.namespace("api/alias", description="Alias operations")


aliasModel = ns.model("Alias", {"name": fields.String, "command": fields.String})


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class AliasList(Resource):
    """Shows all Aliases and lets you post to add a new one"""

    @ns.doc("list_aliases")
    @ns.marshal_with(aliasModel)
    def get(self, server_type, server_id):
        return server_group_join(Alias, server_type, server_id).all()

    @ns.doc("create_alias")
    @ns.expect(aliasModel)
    @ns.marshal_with(aliasModel, code=201)
    def post(self, server_type, server_id):
        """Create a new Alias"""
        form = ns.payload

        server_group_id = get_group_id(server_type, server_id)
        if (
            Alias.query.filter_by(
                server_group_id=server_group_id, name=form["name"]
            ).first()
            is not None
        ):
            abort(400, f"Alias {form['name']} already exists")
        alias = Alias(
            server_group_id=server_group_id, name=form["name"], command=form["command"]
        )
        db.session.add(alias)
        db.session.commit()
        return alias


def get_alias(server_type, server_id, alias_name):
    alias = (
        server_group_join(Alias, server_type, server_id).filter(
            Alias.name == alias_name
        )
    ).first()
    if alias is None:
        abort(404, f"Alias {alias_name} does not exist")
    else:
        return alias


@ns.route("/<server_type>/<int:server_id>/<alias_name>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("alias_name", "The name of the alias")
class AliasRoute(Resource):
    @ns.doc("get_alias")
    @ns.marshal_with(aliasModel)
    def get(self, server_type, server_id, alias_name):
        return get_alias(server_type, server_id, alias_name)

    @ns.doc("update_alias")
    @ns.expect(aliasModel)
    @ns.marshal_with(aliasModel)
    def put(self, server_type, server_id, alias_name):
        alias = get_alias(server_type, server_id, alias_name)
        alias.command = ns.payload["command"]
        db.session.commit()
        return alias

    @ns.doc("delete_alias")
    @ns.response(204, "Alias deleted")
    def delete(self, server_type, server_id, alias_name):
        alias = get_alias(server_type, server_id, alias_name)
        db.session.delete(alias)
        db.session.commit()
        return ""

