from src import app
from flask import redirect, url_for, request
from flask_dance.contrib.discord import discord


@app.route("/login")
def login():
    app.logger.info(f'poop')
    if not discord.authorized:
        app.logger.info(f'no auth')
        return redirect(url_for("discord.login"))
    # resp = discord.get("/api/v6")
    app.logger.info(f'double poop')
    # assert resp.ok, resp.text
    # return "You are {dong}".format(dong=resp.json())
    return "poop"
