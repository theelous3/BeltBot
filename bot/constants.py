from os import getenv
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


MY_NAME = "LPUBeltbot"

MY_REDDIT_PW = getenv("BELTBOT_REDDIT_PW")

MY_REDDIT_CLIENT_ID = getenv("BELTBOT_REDDIT_CID")

MY_REDDIT_SECRET = getenv("BELTBOT_REDDIT_KEY")

USER_AGENT = "LPUBeltbot_v0.1.1"

TOKEN = getenv("BELTBOT_TOKEN")

SUBREDDIT = "lockpicking"

VALID_BELTS = {
    "white": {
        "name": "White Belt",
        "flair_text": "White Belt Picker :WhiteBelt:",
        "css_class": "whitebelt",
    },
    "yellow": {
        "name": "Yellow Belt",
        "flair_text": "Yellow Belt Picker :YellowBelt:",
        "css_class": "yellowbelt",
    },
    "orange": {
        "name": "Orange Belt",
        "flair_text": "Orange Belt Picker :OrangeBelt:",
        "css_class": "orangebelt",
    },
    "green": {
        "name": "Green Belt",
        "flair_text": "Green Belt Picker :GreenBelt:",
        "css_class": "greenbelt",
    },
    "blue": {
        "name": "Blue Belt",
        "flair_text": "Blue Belt Picker :BlueBelt:",
        "css_class": "bluebelt",
    },
    "purple": {
        "name": "Purple Belt",
        "flair_text": "Purple Belt Picker :PurpleBelt:",
        "css_class": "purplebelt",
    },
    "brown": {
        "name": "Brown Belt",
        "flair_text": "Brown Belt Picker :BrownBelt:",
        "css_class": "brownbelt",
    },
    "red": {
        "name": "Red Belt",
        "flair_text": "Red Belt Picker :RedBelt:",
        "css_class": "redbelt",
    },
    "black": {
        "name": "Black Belt",
        "flair_text": "Black Belt Picker :BlackBelt:",
        "css_class": "blackbelt",
    },
    "1st": {"name": "1st Dan", "flair_text": None, "css_class": None},
    "2nd": {"name": "2nd Dan", "flair_text": None, "css_class": None},
    "3rd": {"name": "3rd Dan", "flair_text": None, "css_class": None},
    "4th": {"name": "4th Dan", "flair_text": None, "css_class": None},
    "5th": {"name": "5th Dan", "flair_text": None, "css_class": None},
    "6th": {"name": "6th Dan", "flair_text": None, "css_class": None},
    "7th": {"name": "7th Dan", "flair_text": None, "css_class": None},
    "8th": {"name": "8th Dan", "flair_text": None, "css_class": None},
    "9th": {"name": "9th Dan", "flair_text": None, "css_class": None},
    "10th": {"name": "10th Dan", "flair_text": None, "css_class": None},
    "HoF": {"name": "Hall of Fame entry", "flair_text": None, "css_class": None},
}

HUMAN_READABLE_BELTS = ", ".join([belt for belt in VALID_BELTS])

# ========== Special requests ==========


@dataclass
class HoF:
    name = VALID_BELTS["HoF"]["name"]


SPECIAL_REQUESTS = {"HoF": HoF}
