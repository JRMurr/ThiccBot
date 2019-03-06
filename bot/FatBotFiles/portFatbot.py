# This script is just for porting the old data from fatbot into thicc bot
# If this file is still in git after a few months pls send me rude messages

# TODO: clean keywords to sanitize @ keywords

import json
import os
import requests
import itertools
from pprint import pprint

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
BACKEND_URL = os.environ["BACKEND_URL"]
BOT_API_TOKEN = os.environ["BOT_API_TOKEN"]
SERVER_ID = "134506245569642496"
if not BACKEND_URL.endswith("/"):
    BACKEND_URL += "/"


def loadJson(filename) -> dict:
    file_path = os.path.join(THIS_DIR, filename)
    with open(file_path) as fp:
        return json.load(fp)


s = requests.Session()
s.headers.update({"bot-token": BOT_API_TOKEN})


def backend_request(method: str, api_end_point: str, **kwargs) -> requests.Response:
    if api_end_point.startswith("/"):
        api_end_point = api_end_point[1:]
    url = BACKEND_URL + api_end_point
    return s.request(method, url, **kwargs)


quotes = loadJson("quotes.json")


def add_key_words():
    key_words = loadJson("keyWords.json")
    url = f"/keyWords/discord/{SERVER_ID}"
    for key, value in key_words.items():
        if isinstance(value, list):
            if len(value) > 1:
                print(f"ignoring {key}")
                continue
            else:
                value = value[0]
        jsonData = {"name": key, "responses": [value]}
        r = backend_request("post", url, json=jsonData)


def add_images():
    albums = loadJson("images.json")
    album_create_url = f"/albums/discord/{SERVER_ID}"
    for album_name, links in albums.items():
        r = backend_request("post", album_create_url, json={"name": album_name})
        link_add_url = f"/albums/discord/{SERVER_ID}/{album_name}/entries"
        for link in links:
            backend_request("post", link_add_url, json={"link": link})


def add_quotes():
    quotes = loadJson("quotes.json")
    url = f"/quotes/discord/{SERVER_ID}"
    for quote in quotes:
        backend_request("post", url, json={"quote": quote[0], "author": quote[1]})


def add_aliases():
    simple_commands = ["meme_text", "say", "choose"]
    valid_commands = simple_commands + ["imgur"]
    url = f"/alias/discord/{SERVER_ID}"

    def group_aliases():
        aliases = loadJson("alias.json")
        tmp = []
        for key, value in aliases.items():
            tmp.append({"name": key, "command": value})
        tmp = sorted(tmp, key=lambda x: x["command"][0])
        grouped = {}
        for bot_command, group in itertools.groupby(tmp, key=lambda x: x["command"][0]):
            if bot_command in valid_commands:
                grouped[bot_command] = list(group)
        return grouped

    def add_simple_commands(lst):
        # lst is list of alias info
        for alias in lst:
            command = f"{alias['command'][0]} {alias['command'][1]}"
            jsonData = {"name": alias["name"], "command": command}
            backend_request("post", url, json=jsonData)

    def add_imgur_aliases(lst):
        for alias in lst:
            command = f"album get {alias['command'][1]}"
            jsonData = {"name": alias["name"], "command": command}
            backend_request("post", url, json=jsonData)

    grouped = group_aliases()
    for x in simple_commands:
        add_simple_commands(grouped[x])
    add_imgur_aliases(grouped["imgur"])


if __name__ == "__main__":
    pass
    add_key_words()
    add_images()
    add_quotes()
    add_aliases()
