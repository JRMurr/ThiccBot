from flask import request
from flask_restx import Namespace, Resource, fields, abort
from src import db
from src.models import Quotes
from sqlalchemy.sql import func
from src.utils import server_group_join, get_group_id


ns = Namespace("api/quotes", description="Quote operations")

quoteModel = ns.model(
    "quote",
    {
        "quote": fields.String(attribute="quote_str"),
        "author": fields.String,
        "id": fields.Integer,
    },
)


def apply_search_query(query, search):
    """
    Applies the given search string as a LIKE %% filter on the given query.
    If the search string is None/empty, returns the original query
    """
    if search:
        search_lower = search.lower()
        return query.filter(
            func.lower(Quotes.quote_str).like(f"%{search_lower}%")
            | func.lower(Quotes.author).like(f"%{search_lower}%")
        )
    return query


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The server type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class QuoteList(Resource):
    "Shows all Quotes and lets you post to add a new one"

    @ns.doc("list_quotes")
    @ns.marshal_with(quoteModel)
    def get(self, server_type, server_id):
        # Could potentially add a ?search= param here too, to filter the list
        return server_group_join(Quotes, server_type, server_id).all()

    @ns.doc("create_quote")
    @ns.expect(quoteModel)
    @ns.marshal_with(quoteModel, code=201)
    def post(self, server_type, server_id):
        """Create a new Quote"""
        form = ns.payload
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
        server_group_join(Quotes, server_type, server_id).filter(
            Quotes.id == quote_id
        )
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


@ns.route("/<server_type>/<int:server_id>/random")
@ns.param("server_type", "The server type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class QuoteRandomRoute(Resource):
    @ns.doc("get_random_quote")
    @ns.marshal_with(quoteModel)
    def get(self, server_type, server_id):
        search = request.args.get("search")
        quote = (
            apply_search_query(
                server_group_join(Quotes, server_type, server_id), search
            )
            .order_by(func.random())
            .limit(1)
            .first()
        )

        if quote:
            return quote
        abort(404, f"no quotes")
