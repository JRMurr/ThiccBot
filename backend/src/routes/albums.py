from flask_restx import Namespace
from flask import request
from src import db
from src.models import Album, AlbumEntry, DiscordServer, ServerGroup
from flask_restx import Resource, fields, abort
from src.utils import server_group_join, get_group_id, get_server_group

ns = Namespace("api/albums", description="Album operations")


albumModel = ns.model("album", {"name": fields.String})

albumEntry = ns.model(
    "albumEntry", {"id": fields.Integer, "link": fields.String}
)


@ns.route("/<server_type>/<int:server_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class AlbumList(Resource):
    """Shows all Albums and lets you post to add a new one"""

    @ns.doc("list_albums")
    @ns.marshal_with(albumModel)
    def get(self, server_type, server_id):
        """List all albums on this server"""
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


def get_album_entries(server_type, server_id, album_name):
    album = get_album(server_type, server_id, album_name)
    return AlbumEntry.query.join(Album).filter(Album.id == album.id).all()


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
    @ns.response(204, "Album deleted")
    def delete(self, server_type, server_id, album_name):
        album = get_album(server_type, server_id, album_name)
        db.session.query(AlbumEntry).filter(album_id=album.id).delete()
        db.session.delete(album)
        db.session.commit()
        return ""


@ns.route("/<server_type>/<int:server_id>/<album_name>/entries")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
class AlbumEntryList(Resource):
    @ns.doc("get_album_entries")
    @ns.marshal_with(albumEntry)
    def get(self, server_type, server_id, album_name):
        return get_album_entries(server_type, server_id, album_name)

    @ns.doc("add_album_entry")
    @ns.expect(albumEntry)
    @ns.marshal_with(albumEntry, code=201)
    def post(self, server_type, server_id, album_name):
        album = get_album(server_type, server_id, album_name)
        entry = AlbumEntry(link=ns.payload["link"], album=album)
        db.session.add(entry)
        db.session.commit()
        return entry


@ns.route("/<server_type>/<int:server_id>/entry/<entry_id>")
@ns.param("server_type", "The sever type (discord, irc, etc)")
@ns.param("server_id", "The id of the server")
@ns.param("entry_id", "The Id of the entry")
class AlbumEntryRoute(Resource):
    @ns.doc("add_album_entry")
    @ns.doc("delete_album_entry")
    @ns.marshal_with(albumEntry, code=204)
    def delete(self, server_type, server_id, entry_id):
        entry = AlbumEntry.query.get(entry_id)
        server_group = get_server_group(server_type, server_id)
        if entry.album.server_group_id == server_group.id:
            db.session.delete(entry)
            db.session.commit()
            return entry
        else:
            abort(
                400,
                f"Album entry {entry_id} is not part "
                "of an album in the specified server",
            )
