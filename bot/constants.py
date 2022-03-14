from os import getenv
from dataclasses import dataclass
from collections import ChainMap

from dotenv import load_dotenv

from bot.structs import CaseInsensitiveDict


load_dotenv()


MY_NAME = "LPUBeltbot"

MY_REDDIT_PW = getenv("BELTBOT_REDDIT_PW")

MY_REDDIT_CLIENT_ID = getenv("BELTBOT_REDDIT_CID")

MY_REDDIT_SECRET = getenv("BELTBOT_REDDIT_KEY")

USER_AGENT = "LPUBeltbot_v0.1.1"

TOKEN = getenv("BELTBOT_TOKEN")

SUBREDDIT = "lockpicking"

STANDARD_BELTS = CaseInsensitiveDict(
    **{
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
    }
)

ADDON_BELTS = CaseInsensitiveDict(
    **{
        "1st": {"name": "1st Dan", "flair_text": "Black Belt 1st Dan :BlackBelt:", "css_class":"1stDan"},
        "2nd": {"name": "2nd Dan", "flair_text": "Black Belt 2nd Dan :BlackBelt:", "css_class": "2ndDan"},
        "3rd": {"name": "3rd Dan", "flair_text": "Black Belt 3rd Dan :BlackBelt:", "css_class": "3rdDan"},
        "4th": {"name": "4th Dan", "flair_text": "Black Belt 4th Dan :BlackBelt:", "css_class": "4thDan"},
        "5th": {"name": "5th Dan", "flair_text": "Black Belt 5th Dan :BlackBelt:", "css_class": "5thDan"},
        "6th": {"name": "6th Dan", "flair_text": "Black Belt 6th Dan :BlackBelt:", "css_class": "6thDan"},
        "7th": {"name": "7th Dan", "flair_text": "Black Belt 7th Dan :BlackBelt:", "css_class": "7thDan"},
        "8th": {"name": "8th Dan", "flair_text": "Black Belt 8th Dan :BlackBelt:", "css_class": "8thDan"},
        "9th": {"name": "9th Dan", "flair_text": "Black Belt 9th Dan :BlackBelt:", "css_class": "9thDan"},
        "10th": {"name": "10th Dan", "flair_text": "Black Belt 10th Dan :BlackBelt:", "css_class": "10thDan"},
       "11th": {"name": "11th Dan", "flair_text": "Black Belt 11th Dan :BlackBelt:", "css_class": "11thDan"},
       "12th": {"name": "12th Dan", "flair_text": "Black Belt 12th Dan :BlackBelt:", "css_class": "12thDan"},
       "13th": {"name": "13th Dan", "flair_text": "Black Belt 13th Dan :BlackBelt:", "css_class": "13thDan"},
       "14th": {"name": "14th Dan", "flair_text": "Black Belt 14th Dan :BlackBelt:", "css_class": "14thDan"},
       "15th": {"name": "15th Dan", "flair_text": "Black Belt 15th Dan :BlackBelt:", "css_class": "15thDan"},
       "16th": {"name": "16th Dan", "flair_text": "Black Belt 16th Dan :BlackBelt:", "css_class": "16thDan"},
       "17th": {"name": "17th Dan", "flair_text": "Black Belt 17th Dan :BlackBelt:", "css_class": "17thDan"},
       "18th": {"name": "18th Dan", "flair_text": "Black Belt 18th Dan :BlackBelt:", "css_class": "18thDan"},
       "19th": {"name": "19th Dan", "flair_text": "Black Belt 19th Dan :BlackBelt:", "css_class": "19thDan"},
       "20th": {"name": "20th Dan", "flair_text": "Black Belt 20th Dan :BlackBelt:", "css_class": "20thDan"},
    }
)

NON_BELTS = CaseInsensitiveDict(
    **{
        "HoF": {"name": "Hall of Fame", "flair_text": None, "css_class": None},
    }
)

ALL_BELTS = ChainMap(STANDARD_BELTS, ADDON_BELTS, NON_BELTS)

BELT_ROLE_NAMES = [v["name"] for v in reversed(list(ALL_BELTS.values()))]
STANDARD_BELT_NAMES = [v["name"] for v in reversed(list(STANDARD_BELTS.values()))]
ADDON_BELT_NAMES = [v["name"] for v in reversed(list(ADDON_BELTS.values()))]
NON_BELT_NAMES = [v["name"] for v in reversed(list(ALL_BELTS.values()))]

HUMAN_READABLE_BELTS = ", ".join([belt for belt in reversed(list(ALL_BELTS))])
