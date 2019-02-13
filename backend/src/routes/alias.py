from src import app
from flask import request, abort
from src import db
from src.models import Alias, DiscordServer, ServerGroup
from src.utils import jsonModel
from pprint import pformat


@app.route("/api/alias", methods=["POST"])
def aliasPost():
    form = request.get_json()
    app.logger.info(f"form: {pformat(form)}")

    server_group_id = None
    if "discord_id" in form:
        server_group_id = DiscordServer.query.get(form["discord_id"]).server_group_id
    else:
        server_group_id = form["server_group_id"]
    alias = Alias(
        server_group_id=server_group_id, name=form["name"], command=form["command"]
    )
    db.session.add(alias)
    db.session.commit()
    return jsonModel(alias)


# @app.route("/api/alias/<int:server_id>/<alias_name>", defaults={"server_type": None})
@app.route("/api/alias/<int:server_id>/<alias_name>/<server_type>")
def aliasGet(server_id, alias_name, server_type):
    alias = None

    if server_type is None:
        alias = Alias.query.filter_by(server_id=server_id, name=alias_name).first()
    else:
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
        return jsonModel(alias)
