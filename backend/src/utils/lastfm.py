import pylast
import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask_restplus import abort
from typing import List
from src import CONSTANTS

API_KEY = os.getenv("LAST_FM_API_KEY", "LAST_FM_API_KEY")
SECRET_KEY = os.getenv("LAST_FM_SECRET", "LAST_FM_SECRET")

PERIODS = [
    CONSTANTS.LAST_FM.PERIOD_OVERALL,
    CONSTANTS.LAST_FM.PERIOD_7DAYS,
    CONSTANTS.LAST_FM.PERIOD_1MONTH,
    CONSTANTS.LAST_FM.PERIOD_3MONTHS,
    CONSTANTS.LAST_FM.PERIOD_6MONTHS,
    CONSTANTS.LAST_FM.PERIOD_12MONTHS,
]
PERIOD_STR = ", ".join(PERIODS)

FONT_PATH = "fonts/Montserrat-ExtraBoldItalic.ttf"
FONT_SIZE = 14
IMAGE_SIZE = 300


class LastFmHelper:
    def __init__(self):
        self.network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=SECRET_KEY)
        self.font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        self.user_cache = {}

    def get_image(self, url) -> Image.Image:
        if url is None or len(url) == 0:
            return Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE))
        response = requests.get(url)
        img: Image.Image = Image.open(BytesIO(response.content))
        img.thumbnail((IMAGE_SIZE, IMAGE_SIZE))
        return img

    def image_text(self, img: Image, text, x_pos=0, y_pos=0) -> Image.Image:
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

    def row_text(self, text: List[str]):
        txt_img = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
        d = ImageDraw.Draw(txt_img)
        d.text((0, 0), "\n\n\n".join(text), font=self.font, fill=(255, 255, 255, 255))
        return txt_img

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
        IMG_SPACING = int(IMAGE_SIZE * 0.05)
        NUM_IMAGES = GRID_SIZE ** 2
        albums = user.get_top_albums(period, limit=NUM_IMAGES + 1)
        if len(albums) < NUM_IMAGES:
            abort(400, f"{username} does not have enough albums to make a grid")
        GRID_WIDTH = GRID_SIZE + 1
        new_im = Image.new(
            "RGB",
            (
                (GRID_WIDTH * IMAGE_SIZE) + (GRID_SIZE * IMG_SPACING),
                (GRID_SIZE * IMAGE_SIZE) + ((GRID_SIZE - 1) * IMG_SPACING),
            ),
        )
        for y_idx in range(0, GRID_SIZE):
            row_text = []
            for x_idx in range(0, GRID_SIZE + 1):
                grid_img = None
                if x_idx == GRID_SIZE:
                    # Make text image
                    grid_img = self.row_text(row_text)
                else:
                    album_idx = y_idx * 3 + x_idx
                    album = albums[album_idx].item
                    try:
                        imgUrl = album.get_cover_image(size=4)
                    except pylast.WSError as e:
                        imgUrl = None

                    grid_img = self.get_image(imgUrl)
                    text = "{}\n{}".format(
                        album.get_artist().get_name(), album.get_title()
                    )
                    row_text.append(text)
                x_offset = IMG_SPACING * x_idx
                y_offset = IMG_SPACING * y_idx
                new_im.paste(
                    grid_img,
                    ((x_idx * IMAGE_SIZE) + x_offset, (y_idx * IMAGE_SIZE) + y_offset),
                )
                grid_img.close()
        img_io = BytesIO()
        new_im.save(img_io, format="PNG")
        img_io.seek(0)
        new_im.close()
        return img_io
