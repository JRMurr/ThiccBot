from src import app
from flask import request
from pprint import pprint
@app.route("/server", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        pprint(request.form)
    else:
        return 'big doinks'