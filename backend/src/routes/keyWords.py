from flask_restplus import Namespace
from flask import request
from src import db
from src.models import KeyWords, DiscordServer, ServerGroup
from flask_restplus import Resource, fields, abort
from src.utils import server_group_join, get_group_id
from sqlalchemy.sql import func

ns = Namespace("api/keyWords", description="Keyword operations")

keyWordModel = ns.model(
    "KeyWord",
    {
        "name": fields.String,
        "responses": fields.List(fields.String),
        "match_case": fields.Boolean,
    },
)


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class KeyWordList(Resource):
    "Shows all Key Words and lets you post to add a new one"

    @ns.doc("list_keywords")
    @ns.marshal_with(keyWordModel)
    def get(self, server_type, server_id):
        return server_group_join(KeyWords, server_type, server_id).all()

    @ns.doc("create_keyword")
    @ns.expect(keyWordModel)
    @ns.marshal_with(keyWordModel, code=201)
    def post(self, server_type, server_id):
        """Create a new KeyWord"""
        form = ns.payload
        server_group_id = get_group_id(server_type, server_id)

        if (
            KeyWords.query.filter_by(server_group_id=server_group_id)
            .filter(func.lower(KeyWords.name) == form["name"].lower())
            .first()
            is not None
        ):
            abort(400, f"Key word {form['name']} already exists")
        keyWord = KeyWords(
            server_group_id=server_group_id,
            name=form["name"],
            responses=form["responses"],
        )
        db.session.add(keyWord)
        db.session.commit()
        return keyWord


def get_keyword(server_type, server_id, key_name, check_case=True):
    keyWord = (
        server_group_join(KeyWords, server_type, server_id).filter(
            func.lower(KeyWords.name) == key_name.lower()
        )
    ).first()
    if keyWord is None:
        abort(404, f"Key word {key_name} does not exist")
    if check_case and keyWord.match_case and keyWord.name != key_name:
        abort(
            400,
            f"Key word {key_name} does not match the casing of {keyWord.name}",
        )
    else:
        return keyWord


@ns.route("/<server_type>/<int:server_id>/<key_name>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("key_name", "The name of the key word")
class KeyWordRoute(Resource):
    @ns.doc("get_keyword")
    @ns.marshal_with(keyWordModel)
    def get(self, server_type, server_id, key_name):
        return get_keyword(server_type, server_id, key_name)

    @ns.doc("update_keyword")
    @ns.expect(keyWordModel)
    @ns.marshal_with(keyWordModel)
    def put(self, server_type, server_id, key_name):
        keyWord = get_keyword(server_type, server_id, key_name, False)
        if "responses" in ns.payload:
            keyWord.responses = ns.payload["responses"]
        if "match_case" in ns.payload:
            keyWord.match_case = ns.payload["match_case"]
        db.session.commit()
        return keyWord

    @ns.doc("delete_keyword")
    @ns.response(204, "Key word deleted")
    def delete(self, server_type, server_id, key_name):
        keyWord = get_keyword(server_type, server_id, key_name)
        db.session.delete(keyWord)
        db.session.commit()
        return ""
