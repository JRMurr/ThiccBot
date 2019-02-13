from flask import jsonify


def jsonModel(model):
    """calls `.serialize` on model and returns it as json"""
    return jsonify(model.serialize)
