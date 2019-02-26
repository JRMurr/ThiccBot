from src import app, api
from flask_restplus import Resource, abort
from flask import url_for
from src.utils import LastFmHelper
from src import CONSTANTS

ns = api.namespace("api/lastFM", description="LastFM operations")

lastFmHelper = LastFmHelper()


@ns.route("/grid/<lastfm_user>", defaults={"period": CONSTANTS.LAST_FM.PERIOD_7DAYS})
@ns.route(
    "/grid/<lastfm_user>/<period>", defaults={"period": CONSTANTS.LAST_FM.PERIOD_7DAYS}
)
class GridMaker(Resource):
    """Makes a grid image of the user's LastFm scrobbles"""

    @ns.doc("get_grid")
    def get(self, lastfm_user, period):
        """List all albums on this server"""
        image_path = lastFmHelper.grid(lastfm_user, period)
        return url_for(image_path)
