from src import app
from flask import request, abort, g
from pprint import pformat
from src import db
from src.models import DiscordServer
from flask import jsonify
from flask_dance.contrib.discord import discord as dAuth


prefix = "/api/discordServers"


def id_to_str(serverJson):
    # The reason front end has issues with big int
    # so if not the bot conver the id to a string
    if not g.is_bot:
        serverJson["id"] = str(serverJson["id"])
    return serverJson


@app.route(prefix, methods=["GET", "POST"])
def serverRoute():
    if request.method == "POST":
        form = request.form
        serverId = int(form["id"])
        serverName = form["name"]
        server = DiscordServer.query.get(serverId)
        if server is None:
            server = DiscordServer(id=serverId, name=serverName)
            db.session.add(server)
            db.session.commit()
            app.logger.info(f"added server: {server}")
        else:
            app.logger.info(f"already had server: {server}")
        return jsonify(id_to_str(server.serialize))
    else:
        return jsonify([id_to_str(x.serialize) for x in DiscordServer.query.all()])


@app.route(prefix + "<int:server_id>", methods=["PUT", "GET"])
def getServer(server_id):
    server = DiscordServer.query.get_or_404(server_id)
    if request.method == "PUT":
        form = request.get_json()
        if form["admin_role"]:
            server.admin_role = form["admin_role"]
        db.session.commit()
    return jsonify(id_to_str(server.serialize))
