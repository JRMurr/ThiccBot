from src import app
from flask import request
from pprint import pformat
from src import db
from src.models import DiscordServer
from flask import jsonify


@app.route("/servers", methods=['POST', 'GET'])
def serverRoute():
    if request.method == 'POST':
        form = request.form
        serverId = int(form['id'])
        serverName = form['name']
        server = DiscordServer.query.get(serverId)
        if server is None:
            server = DiscordServer(id=serverId, name=serverName)
            db.session.add(server)
            db.session.commit()
            app.logger.info(f'added server: {server}')
        return jsonify(server.serialize)
    else:
        # TODO: query with search params?
        return 'big doinks'