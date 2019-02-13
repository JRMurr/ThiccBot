from src import app
from flask import request, abort
from src import db
from src.models import Alias
from src.utils import jsonModel
from pprint import pformat


@app.route("/api/alias", methods=["POST"])
def aliasPost():
    form = request.get_json()
    app.logger.info(f"form: {pformat(form)}")
    alias = Alias(
        server_id=form["server_id"], name=form["name"], command=form["command"]
    )
    db.session.add(alias)
    db.session.commit()
    return jsonModel(alias)


@app.route("/api/alias/<int:server_id>/<alias_name>")
def aliasGet(server_id, alias_name):
    alias = Alias.query.filter_by(server_id=server_id, name=alias_name).first()
    if alias is None:
        abort(404)
    else:
        return jsonModel(alias)
