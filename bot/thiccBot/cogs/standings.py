from discord.ext import commands
from texttable import Texttable

COLUMNS = {
    "nhl": [
        ("abbr", "Team"),
        ("wins", "Wins"),
        ("losses", "Losses"),
        ("otl", "OTL"),
    ]
}


def make_table():
    table = Texttable()
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    return table


class Standings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="standings")
    async def standings(self, ctx, league: str):
        """Get sports league standings"""

        async def on_200(r):
            standings = await r.json()
            tables = []  # list of (group_name, Texttable)

            for group_name, records in standings.items():
                columns = COLUMNS[league]
                table = make_table()
                table.header([label for key, label in columns])
                table.add_rows(
                    [
                        [record[key] for key, label in columns]
                        for record in records
                    ],
                    header=False,
                )
                tables.append((group_name, table))

            tables_str = "\n".join(
                f"{group_name}\n{table.draw()}" for group_name, table in tables
            )
            await ctx.send(f"```\n{tables_str}```")

        async def on_404(r):
            await ctx.send("Unknown league")

        await self.bot.request_helper(
            "get",
            f"/standings/{league}?grouping=division",
            ctx,
            error_prefix="Error getting standings",
            success_function=on_200,
            error_handler={404: on_404},
        )


def setup(bot):
    bot.add_cog(Standings(bot))
