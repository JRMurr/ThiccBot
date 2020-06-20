from flask import request
from flask_restx import Namespace, Resource, fields, abort
from src import db
from src.models import DiscordRole
from sqlalchemy.sql import func
from src.utils import server_group_join, get_group_id


ns = Namespace("api/discord/roles", description="Role operations")

roleModel = ns.model(
    "role",
    {
        "role_id": fields.Integer,
        "message_id": fields.Integer,
        "channel_id": fields.Integer,
        "id": fields.Integer,
    },
)


@ns.route("/<int:server_id>")
@ns.param("server_id", "The id of the discord server")
class RoleList(Resource):
    "List messages ids and the roles they will assign to on react"

    @ns.doc("list_roles")
    @ns.marshal_with(roleModel)
    def get(self, server_id):
        return DiscordRole.query.filter(
            DiscordRole.discord_id == server_id
        ).all()

    @ns.doc("create_role")
    @ns.expect(roleModel)
    @ns.marshal_with(roleModel, code=201)
    def post(self, server_id):
        """Create a new role message listener"""
        form = ns.payload

        role = DiscordRole(
            discord_id=server_id,
            message_id=form["message_id"],
            channel_id=form["channel_id"],
            role_id=form["role_id"],
        )
        db.session.add(role)
        db.session.commit()
        return role


@ns.route("/<int:id>")
@ns.param("id", "The id for the role object")
class RoleIdRoute(Resource):
    @ns.doc("delete_role")
    @ns.marshal_with(roleModel, code=204)
    def delete(self, id):
        role = DiscordRole.query.filter(DiscordRole.id == id).first()
        db.session.delete(role)
        db.session.commit()
        return role
