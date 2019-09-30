from flask_restplus import Namespace
from flask import request, current_app as app
from src import db
from src.models import Counter, DiscordServer, ServerGroup
from flask_restplus import Resource, fields, abort
from src.utils import server_group_join, get_group_id
from sqlalchemy.sql import func

ns = Namespace("api/counter", description="Counter operations")

counterModel = ns.model(
    "Counter",
    {"name": fields.String, "count": fields.Integer, "response": fields.String},
)


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class CounterList(Resource):
    "Shows all Counters and lets you post to add a new one"

    @ns.doc("list_counter")
    @ns.marshal_with(counterModel)
    def get(self, server_type, server_id):
        return server_group_join(Counter, server_type, server_id).all()

    @ns.doc("create_counter")
    @ns.expect(counterModel)
    @ns.marshal_with(counterModel, code=201)
    def post(self, server_type, server_id):
        """Create a new Counter"""
        form = ns.payload
        server_group_id = get_group_id(server_type, server_id)

        if (
            Counter.query.filter_by(server_group_id=server_group_id)
            .filter(func.lower(Counter.name) == form["name"].lower())
            .first()
            is not None
        ):
            abort(400, f"Counter {form['name']} already exists")
        response = None
        if "response" in form:
            response = form["response"]
        if response is None:
            # response could still be None from the post data
            response = f"Counter {form['name']}" + " is now at {}"
        counter = Counter(
            server_group_id=server_group_id,
            name=form["name"],
            count=form.get("count", 0),
            response=response,
        )
        db.session.add(counter)
        db.session.commit()
        return counter


def get_counter(server_type, server_id, counter_name):
    counter = (
        server_group_join(Counter, server_type, server_id).filter(
            func.lower(Counter.name) == counter_name.lower()
        )
    ).first()
    if counter is None:
        abort(404, f"Counter {counter_name} does not exist")
    else:
        return counter


@ns.route("/<server_type>/<int:server_id>/<counter_name>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("counter_name", "The name of the counter")
class CounterRoute(Resource):
    @ns.doc("get_counter")
    @ns.marshal_with(counterModel)
    def get(self, server_type, server_id, counter_name):
        return get_counter(server_type, server_id, counter_name)

    @ns.doc("update_counter")
    @ns.expect(counterModel)
    @ns.marshal_with(counterModel)
    def put(self, server_type, server_id, counter_name):
        counter = get_counter(server_type, server_id, counter_name)
        if ns.payload is not None and "count" in ns.payload:
            counter.count = ns.payload["count"]
        else:
            counter.count += 1
        db.session.commit()
        return counter

    @ns.doc("delete_counter")
    @ns.response(204, "Counter deleted")
    def delete(self, server_type, server_id, counter_name):
        counter = get_counter(server_type, server_id, counter_name)
        db.session.delete(counter)
        db.session.commit()
        return ""
