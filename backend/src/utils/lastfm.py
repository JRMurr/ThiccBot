import pylast
import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask_restplus import abort
from src import CONSTANTS

API_KEY = os.environ["LAST_FM_API_KEY"]
SECRET_KEY = os.environ["LAST_FM_SECRET"]

PERIODS = [
    CONSTANTS.LAST_FM.PERIOD_OVERALL,
    CONSTANTS.LAST_FM.PERIOD_7DAYS,
    CONSTANTS.LAST_FM.PERIOD_1MONTH,
    CONSTANTS.LAST_FM.PERIOD_3MONTHS,
    CONSTANTS.LAST_FM.PERIOD_6MONTHS,
    CONSTANTS.LAST_FM.PERIOD_12MONTHS,
]
PERIOD_STR = ", ".join(PERIODS)

FONT_PATH = "fonts/Butler_ExtraBold.otf"
FONT_SIZE = 14


class LastFmHelper:
    def __init__(self):
        self.network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=SECRET_KEY)
        self.font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        self.user_cache = {}

    def get_image(self, url):
        if url is None or len(url) == 0:
            return Image.new("RGB", (300, 300))
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((300, 300))
        return img

    def image_text(self, img, text, x_pos=0, y_pos=0):
        """Adds text to the image at the specified location"""
        # Make blank image for text
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        # offset with black text to fake outline
        d.text((x_pos + 1, y_pos + 1), text, font=self.font, fill=(0, 0, 0, 255))
        d.text((x_pos + 1, y_pos), text, font=self.font, fill=(0, 0, 0, 255))
        d.text((x_pos, y_pos + 1), text, font=self.font, fill=(0, 0, 0, 255))
        # text in white
        d.text((x_pos, y_pos), text, font=self.font, fill=(255, 255, 255, 255))
        out = Image.alpha_composite(img.convert("RGBA"), txt)
        return out

    def get_user(self, username):
        if username in self.user_cache:
            return self.user_cache[username]
        user = self.network.get_user(username)
        try:
            user.get_country()
            self.user_cache[username] = user
            return user
        except:
            abort(400, f"username '{username}' not found")

    def grid(self, username, period=CONSTANTS.LAST_FM.PERIOD_7DAYS):
        """Returns a lastFM users 9 most played albums for the specified period in a grid image
        valid periods are overall, 7day, 1month, 3month, 6month, 12month
        """
        if period not in PERIODS:
            abort(400, "invalid period, valid options are: " + PERIOD_STR)

        user = self.get_user(username)

        GRID_SIZE = 3
        NUM_IMAGES = GRID_SIZE ** 2
        albums = user.get_top_albums(period, limit=NUM_IMAGES + 1)
        if len(albums) < NUM_IMAGES:
            abort(400, f"{username} does not have enough albums to make a grid")
        new_im = Image.new("RGB", (GRID_SIZE * 300, GRID_SIZE * 300))
        for y_idx in range(0, GRID_SIZE):
            for x_idx in range(0, GRID_SIZE):
                album_idx = y_idx * 3 + x_idx
                album = albums[album_idx].item
                try:
                    imgUrl = album.get_cover_image(size=4)
                except pylast.WSError as e:
                    imgUrl = None

                alb_image = self.get_image(imgUrl)
                text = "{}\n{}".format(album.get_artist().get_name(), album.get_title())
                alb_image = self.image_text(alb_image, text)
                new_im.paste(alb_image, (x_idx * 300, y_idx * 300))
                alb_image.close()
        img_io = BytesIO()
        new_im.save(img_io, format="JPEG")
        img_io.seek(0)
        new_im.close()
        return img_io

