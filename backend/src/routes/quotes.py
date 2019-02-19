from src import app, api
from flask import request
from src import db
from src.models import Quotes, DiscordServer, ServerGroup
from flask_restplus import Resource, fields, abort
from sqlalchemy.sql import func
from src.utils import server_group_join, get_group_id


ns = api.namespace("api/quotes", description="Quoute operations")

quoteModel = ns.model(
    "quote",
    {
        "quote": fields.String(attribute="quote_str"),
        "author": fields.String,
        "id": fields.Integer,
    },
)


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class QuoteList(Resource):
    "Shows all Quotes and lets you post to add a new one"

    @ns.doc("list_quotes")
    @ns.marshal_with(quoteModel)
    def get(self, server_type, server_id):
        return server_group_join(Quotes, server_type, server_id).all()

    @ns.doc("create_quote")
    @ns.expect(quoteModel)
    @ns.marshal_with(quoteModel, code=201)
    def post(self, server_type, server_id):
        """Create a new Quote"""
        form = ns.payload
        print(f"server_type: {server_type}, server_id: {server_id}")
        server_group_id = get_group_id(server_type, server_id)

        quote = Quotes(
            server_group_id=server_group_id,
            quote_str=form["quote"],
            author=form["author"],
        )
        db.session.add(quote)
        db.session.commit()
        return quote


def get_quote(server_type, server_id, quote_id):
    quote = (
        server_group_join(Quotes, server_type, server_id).filter(Quotes.id == quote_id)
    ).first()
    if quote is None:
        abort(404, f"quote with id {quote_id} does not exist")
    else:
        return quote


@ns.route("/<server_type>/<int:server_id>/<int:quote_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("quote_id", "The id of the quote")
class QuoteIdRoute(Resource):
    @ns.doc("get_quote")
    @ns.marshal_with(quoteModel)
    def get(self, server_type, server_id, quote_id):
        return get_quote(server_type, server_id, quote_id)

    @ns.doc("delete_quote")
    @ns.response(204, "Key word deleted")
    def delete(self, server_type, server_id, quote_id):
        keyWord = get_quote(server_type, server_id, quote_id)
        db.session.delete(keyWord)
        db.session.commit()
        return ""


@ns.route("/<server_type>/<int:server_id>/<search_str>")
class QuiteSearchRoute(Resource):
    @ns.doc("get_search_quote")
    @ns.marshal_with(quoteModel)
    def get(self, server_type, server_id, search_str):
        search_str = search_str.lower()
        searchOr = func.lower(Quotes.quote_str).like(f"%{search_str}%") | func.lower(
            Quotes.author
        ).like(f"%{search_str}%")
        quotes = (
            server_group_join(Quotes, server_type, server_id).filter(searchOr).all()
        )
        if quotes is None or len(quotes) == 0:
            abort(404, f"quote not found")
        else:
            return quotes
