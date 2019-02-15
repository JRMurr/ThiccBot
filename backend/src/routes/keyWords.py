from src import app, api
from flask import request, abort
from src import db
from src.models import KeyWords, DiscordServer, ServerGroup
from flask_restplus import Resource, fields


ns = api.namespace("api/keyWords", description="Keyword operations")

keyWordModel = ns.model(
    "KeyWord", {"name": fields.String, "responses": fields.List(fields.String)}
)


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class KeyWordList(Resource):
    "Shows all Aliases and lets you post to add a new one"

    def get(self, server_type, server_id):
        pass

    @ns.doc("create_keyword")
    @ns.expect(keyWordModel)
    @ns.marshal_with(keyWordModel, code=201)
    def post(self, server_type, server_id):
        """Create a new KeyWord"""
        form = ns.payload
        server_group_id = None
        # TODO:make util for getting group id from server_type
        if server_type == "discord":
            server_group_id = DiscordServer.query.get(server_id).server_group_id
        else:
            server_group_id = server_id
        if (
            KeyWords.query.filter_by(
                server_group_id=server_group_id, name=form["name"]
            ).first()
            is not None
        ):
            abort(400)  # key word already exist
        keyWords = KeyWords(
            server_group_id=server_group_id,
            name=form["name"],
            responses=form["responses"],
        )
        db.session.add(keyWords)
        db.session.commit()
        return keyWords


@ns.route("/<server_type>/<int:server_id>/<key_name>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("key_name", "The name of the alias")
class AliasRoute(Resource):
    @ns.marshal_with(keyWordModel)
    def get(self, server_type, server_id, key_name):
        keyWords = None
        if server_type is None:
            keyWords = KeyWords.query.filter_by(
                server_id=server_id, name=key_name
            ).first()
        else:
            # TODO: add constants for accepted server type
            if server_type == "discord":
                keyWords = (
                    KeyWords.query.join(ServerGroup)
                    .join(DiscordServer)
                    .filter(DiscordServer.id == server_id, KeyWords.name == key_name)
                ).first()
            else:
                abort(400)
        if keyWords is None:
            abort(404)
        else:
            return keyWords
