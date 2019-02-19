from src import app, api
from flask import request
from src import db
from src.models import Album, AlbumEntry, DiscordServer, ServerGroup
from flask_restplus import Resource, fields, abort
from src.utils import server_group_join, get_group_id

ns = api.namespace("api/albums", description="Album operations")


albumModel = ns.model("album", {"name": fields.String})


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class AlbumList(Resource):
    """Shows all Albums and lets you post to add a new one"""

    @ns.doc("list_albums")
    @ns.marshal_with(albumModel)
    def get(self, server_type, server_id):
        return server_group_join(Album, server_type, server_id).all()

    @ns.doc("create_album")
    @ns.expect(albumModel)
    @ns.marshal_with(albumModel, code=201)
    def post(self, server_type, server_id):
        """Create a new Album"""
        form = ns.payload

        server_group_id = get_group_id(server_type, server_id)
        if (
            Album.query.filter_by(
                server_group_id=server_group_id, name=form["name"]
            ).first()
            is not None
        ):
            abort(400, f"Album {form['name']} already exists")
        album = Album(server_group_id=server_group_id, name=form["name"])
        db.session.add(album)
        db.session.commit()
        return album


def get_album(server_type, server_id, album_name):
    album = (
        server_group_join(Album, server_type, server_id).filter(
            Album.name == album_name
        )
    ).first()
    if album is None:
        abort(404, f"Album {album_name} does not exist")
    else:
        return album


@ns.route("/<server_type>/<int:server_id>/<album_name>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("album_name", "The name of the album")
class AlbumRoute(Resource):
    @ns.doc("get_album")
    @ns.marshal_with(albumModel)
    def get(self, server_type, server_id, album_name):
        return get_album(server_type, server_id, album_name)

    @ns.doc("delete_album")
    @ns.response(204, "Alias deleted")
    def delete(self, server_type, server_id, album_name):
        album = get_album(server_type, server_id, album_name)
        db.session.delete(album)
        db.session.commit()
        return ""
