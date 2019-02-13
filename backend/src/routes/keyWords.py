from src import app
from flask import request, abort
from src import db
from src.models import KeyWords, DiscordServer, ServerGroup
from src.utils import jsonModel
from pprint import pformat


@app.route("/api/keyWords", methods=["POST"])
def keyWordsPost():
    form = request.get_json()
    app.logger.info(f"form: {pformat(form)}")

    server_group_id = None
    if "discord_id" in form:
        server_group_id = DiscordServer.query.get(form["discord_id"]).server_group_id
    else:
        server_group_id = form["server_group_id"]
    keyWords = KeyWords(
        server_group_id=server_group_id, name=form["name"], responses=form["responses"]
    )
    db.session.add(keyWords)
    db.session.commit()
    return jsonModel(keyWords)


# @app.route("/api/alias/<int:server_id>/<key_name>", defaults={"server_type": None})
@app.route("/api/keyWords/<int:server_id>/<key_name>/<server_type>")
def keyWordsGet(server_id, key_name, server_type):
    keyWords = None

    if server_type is None:
        keyWords = KeyWords.query.filter_by(server_id=server_id, name=key_name).first()
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
        return jsonModel(keyWords)
