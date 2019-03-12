from flask_restplus import fields
from flask import g


class IdType(fields.Raw):
    __schema_format__ = "integer"
    __schema_type__ = "integer"

    def format(self, value):
        if not g.is_bot:
            return str(value)
        return value
