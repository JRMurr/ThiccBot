from imgurpython import ImgurClient
from pprint import pprint
import json
import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

imgurClient = ImgurClient(
    os.environ["IMGUR_CLIENT_ID"], os.environ["IMGUR_CLIENT_SECRET"]
)
imgurClient.set_user_auth(
    os.environ["IMGUR_ACCESS_TOKEN"], os.environ["IMGUR_REFRESH_TOKEN"]
)


def get_albums():
    res = {}
    for album in imgurClient.get_account_albums("me"):
        images = imgurClient.get_album_images(album.id)
        res[album.title] = [x.link for x in images]
    pprint(res)
    file_path = os.path.join(THIS_DIR, "images.json")
    with open(file_path, "w") as fp:
        json.dump(res, fp, indent=4)


get_albums()
