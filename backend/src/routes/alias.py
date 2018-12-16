from src import app
from flask import request
from pprint import pformat


@app.route("/alias", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        app.logger.info(pformat(request.form))
        app.logger.info('----')
        return 'small doinks'
    else:
        return 'big doinks'