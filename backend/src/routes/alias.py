from src import app
from flask import request
from pprint import pformat
from src.models import Alias
from src import db

@app.route("/alias", methods=['POST', 'GET'])
def aliasRoute():
    if request.method == 'POST':
        form = request.form
        return 'small doinks'
    else:
        return 'big doinks'