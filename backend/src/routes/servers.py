from src import app
from flask import request, abort
from pprint import pformat
from src import db
from src.models import DiscordServer
from flask import jsonify


@app.route("/servers", methods=['POST'])
def serverRoute():
    form = request.form
    serverId = int(form['id'])
    serverName = form['name']
    server = DiscordServer.query.get(serverId)
    if server is None:
        server = DiscordServer(id=serverId, name=serverName)
        db.session.add(server)
        db.session.commit()
        app.logger.info(f'added server: {server}')
    else:
        app.logger.info(f'already had server: {server}')
    return jsonify(server.serialize)

@app.route('/servers/<int:server_id>', methods=['PUT', 'GET'])
def getServer(server_id):
    server = DiscordServer.query.get_or_404(server_id)
    if request.method == 'PUT':
        server = DiscordServer.query.get_or_404(server_id)
        form = request.get_json()
        if form['admin_role']:
            server.admin_role = form['admin_role']
        db.session.commit()        
    return jsonify(server.serialize)