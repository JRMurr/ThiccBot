from flask_restplus import Namespace
from flask_restplus import Resource, abort
from flask import send_file
from src.utils import LastFmHelper
from src import CONSTANTS

ns = Namespace("api/lastFM", description="LastFM operations")

lastFmHelper = LastFmHelper()


@ns.route("/grid/<lastfm_user>", defaults={"period": CONSTANTS.LAST_FM.PERIOD_7DAYS})
@ns.route("/grid/<lastfm_user>/<period>")
class GridMaker(Resource):
    """Makes a grid image of the user's LastFm scrobbles"""

    @ns.doc("get_grid")
    @ns.produces(["image/png"])
    def get(self, lastfm_user, period=CONSTANTS.LAST_FM.PERIOD_7DAYS):
        """List all albums on this server"""
        return send_file(lastFmHelper.grid(lastfm_user, period), mimetype="image/jpeg")
