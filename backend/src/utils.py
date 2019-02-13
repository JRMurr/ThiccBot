from flask import jsonify


def jsonModel(model):
    """calls `.serialize` on model and returns it as json"""
    return jsonify(model.serialize)


# TODO: make dict for mapping of server client name (discord/irc/etc) to the actual model to make
#       joins general

