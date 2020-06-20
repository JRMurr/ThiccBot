import requests
from collections import defaultdict
from flask import request
from flask_restx import Namespace, Resource, abort

ns = Namespace("api/standings", description="Sports standings")


@ns.route("/nhl")
class StandingsNhl(Resource):
    API_URL = "http://statsapi.web.nhl.com/api/v1/standings"
    TEAM_ABBRS = {
        "Florida Panthers": "FLA",
        "Montréal Canadiens": "MTL",
        "Toronto Maple Leafs": "TOR",
        "Tampa Bay Lightning": "TBL",
        "Ottawa Senators": "OTT",
        "Boston Bruins": "BOS",
        "Buffalo Sabres": "BUF",
        "Detroit Red Wings": "DET",
        "Pittsburgh Penguins": "PIT",
        "Philadelphia Flyers": "PHI",
        "Washington Capitals": "WSH",
        "New York Rangers": "NYR",
        "Carolina Hurricanes": "CAR",
        "New Jersey Devils": "NJD",
        "New York Islanders": "NYI",
        "Columbus Blue Jackets": "CBJ",
        "St. Louis Blues": "STL",
        "Colorado Avalanche": "COL",
        "Dallas Stars": "DAL",
        "Winnipeg Jets": "WPG",
        "Minnesota Wild": "MIN",
        "Nashville Predators": "NSH",
        "Chicago Blackhawks": "CHI",
        "Edmonton Oilers": "EDM",
        "San Jose Sharks": "SJS",
        "Arizona Coyotes": "ARI",
        "Vancouver Canucks": "VAN",
        "Calgary Flames": "CGY",
        "Anaheim Ducks": "ANA",
        "Los Angeles Kings": "LAK",
        "Vegas Golden Knights": "VGK",
    }

    @staticmethod
    def convert_team_record(team_record):
        name = team_record["team"]["name"]
        league_record = team_record["leagueRecord"]
        # use .get so it doesn't crash when Seattle joins
        return {
            "name": name,
            "abbr": StandingsNhl.TEAM_ABBRS.get(name),
            "wins": league_record["wins"],
            "losses": league_record["losses"],
            "otl": league_record["ot"],
        }

    def group_league(records):
        # Build one big list with all teams
        team_records = (
            tr for division in records for tr in division["teamRecords"]
        )
        return {
            records[0]["league"]["name"]: [
                StandingsNhl.convert_team_record(tr)
                # Sort records by league rank before mapping
                for tr in sorted(
                    team_records, key=lambda tr: int(tr["leagueRank"])
                )
            ]
        }

    def group_conference(records):
        trs_by_conference = defaultdict(list)
        for division in records:
            trs_by_conference[division["conference"]["name"]] += division[
                "teamRecords"
            ]

        return {
            conf: [
                StandingsNhl.convert_team_record(tr)
                # Sort records by conference rank before mapping
                for tr in sorted(trs, key=lambda tr: int(tr["conferenceRank"]))
            ]
            for conf, trs in trs_by_conference.items()
        }

    def group_division(records):
        return {
            division["division"]["name"]: [
                StandingsNhl.convert_team_record(tr)
                # Sort records by division rank before mapping
                for tr in sorted(
                    division["teamRecords"],
                    key=lambda tr: int(tr["divisionRank"]),
                )
            ]
            for division in records
        }

    GROUPINGS = {
        "league": group_league,
        "conference": group_conference,
        "division": group_division,
    }

    def get(self):
        grouping = request.args.get("grouping", "division")
        try:
            grouping_func = self.GROUPINGS[grouping]
        except KeyError:
            abort(400, f"Invalid grouping: {grouping}")

        response = requests.get(self.API_URL)
        response.raise_for_status()
        raw_data = response.json()
        return grouping_func(raw_data["records"])
