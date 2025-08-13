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

NEWBIE_ROLES = ["Chatter"]

STANDARD_BELTS = CaseInsensitiveDict(
    **{
        "white": {
            "name": "White Belt",
            "flair_text": "White Belt Picker :WhiteBelt:",
            "css_class": "whitebelt",
            "reddit_id": "b204087a-f539-11e6-8135-0ec5b066f456",
        },
        "yellow": {
            "name": "Yellow Belt",
            "flair_text": "Yellow Belt Picker :YellowBelt:",
            "css_class": "yellowbelt",
            "reddit_id": "ba14f740-f539-11e6-b21c-0e784077e922",
        },
        "orange": {
            "name": "Orange Belt",
            "flair_text": "Orange Belt Picker :OrangeBelt:",
            "css_class": "orangebelt",
            "reddit_id": "c091da0c-f539-11e6-9b84-0e5f5aaf8736",
        },
        "green": {
            "name": "Green Belt",
            "flair_text": "Green Belt Picker :GreenBelt:",
            "css_class": "greenbelt",
            "reddit_id": "c3c4554c-f539-11e6-aa74-0e5335022d94",
        },
        "blue": {
            "name": "Blue Belt",
            "flair_text": "Blue Belt Picker :BlueBelt:",
            "css_class": "bluebelt",
            "reddit_id": "c663ef6a-f539-11e6-a2f0-0e01b56c5d32",
        },
        "purple": {
            "name": "Purple Belt",
            "flair_text": "Purple Belt Picker :PurpleBelt:",
            "css_class": "purplebelt",
            "reddit_id": "c9da5d00-f539-11e6-8c0d-0e5335022d94",
        },
        "brown": {
            "name": "Brown Belt",
            "flair_text": "Brown Belt Picker :BrownBelt:",
            "css_class": "brownbelt",
            "reddit_id": "ccc8b426-f539-11e6-baab-0edf4f10e4d0",
        },
        "red": {
            "name": "Red Belt",
            "flair_text": "Red Belt Picker :RedBelt:",
            "css_class": "redbelt",
            "reddit_id": "cf47cf8e-f539-11e6-a585-0ecafa470a70",
        },
        "black": {
            "name": "Black Belt",
            "flair_text": "Black Belt Picker :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "d2312592-f539-11e6-ae73-0e01b56c5d32",
        },
    }
)

ADDON_BELTS = CaseInsensitiveDict(
    **{
        "1st": {
            "name": "1st Dan",
            "flair_text": "Black Belt 1st Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "f69cb3ce-9bf1-11ec-b84d-3a9f4e66f49f",
        },
        "2nd": {
            "name": "2nd Dan",
            "flair_text": "Black Belt 2nd Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "18e57574-9bf2-11ec-beb4-bacc87c0dd52",
        },
        "3rd": {
            "name": "3rd Dan",
            "flair_text": "Black Belt 3rd Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "43e0aff0-9bf2-11ec-97b5-d608a0e120df",
        },
        "4th": {
            "name": "4th Dan",
            "flair_text": "Black Belt 4th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "5ae1edcc-9bf2-11ec-a4ed-16a38658e11a",
        },
        "5th": {
            "name": "5th Dan",
            "flair_text": "Black Belt 5th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "83d92f6a-9bf2-11ec-ac17-e20e0f63c090",
        },
        "6th": {
            "name": "6th Dan",
            "flair_text": "Black Belt 6th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "aa3afb2a-9bf2-11ec-bffb-021447b001d8",
        },
        "7th": {
            "name": "7th Dan",
            "flair_text": "Black Belt 7th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "c57bedcc-9bf2-11ec-a129-62766e2987d1",
        },
        "8th": {
            "name": "8th Dan",
            "flair_text": "Black Belt 8th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "e69c7fe4-9bf2-11ec-9ce0-d2404496fe07",
        },
        "9th": {
            "name": "9th Dan",
            "flair_text": "Black Belt 9th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "876fbb7a-9bf3-11ec-8573-524f741564fa",
        },
        "10th": {
            "name": "10th Dan",
            "flair_text": "Black Belt 10th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "b9ef5998-9bf3-11ec-af31-aa5d1d961904",
        },
        "11th": {
            "name": "11th Dan",
            "flair_text": "Black Belt 11th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "dac32d5e-9bf6-11ec-9573-dae61490ee99",
        },
        "12th": {
            "name": "12th Dan",
            "flair_text": "Black Belt 12th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "8d45cc7a-9bf7-11ec-80b1-a2ab0b764f1f",
        },
        "13th": {
            "name": "13th Dan",
            "flair_text": "Black Belt 13th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "a79f8764-9bf7-11ec-a66c-0effb062df54",
        },
        "14th": {
            "name": "14th Dan",
            "flair_text": "Black Belt 14th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "bca86b4e-9bf7-11ec-9ee6-329a217cc110",
        },
        "15th": {
            "name": "15th Dan",
            "flair_text": "Black Belt 15th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "d39786d2-9bf7-11ec-adac-d2bb228e0cac",
        },
        "16th": {
            "name": "16th Dan",
            "flair_text": "Black Belt 16th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "eff3bd96-9bf7-11ec-a1fb-2adc34ee5f76",
        },
        "17th": {
            "name": "17th Dan",
            "flair_text": "Black Belt 17th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "04e5fb56-9bf8-11ec-8b00-9aee29017931",
        },
        "18th": {
            "name": "18th Dan",
            "flair_text": "Black Belt 18th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "16be1372-9bf8-11ec-a54e-0a383bad131c",
        },
        "19th": {
            "name": "19th Dan",
            "flair_text": "Black Belt 19th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "37716d9e-9bf8-11ec-a0e5-e29967a5b375",
        },
        "20th": {
            "name": "20th Dan",
            "flair_text": "Black Belt 20th Dan :BlackBelt:",
            "css_class": "blackbelt",
            "reddit_id": "4b8912f0-9bf8-11ec-8227-524f741564fa",
        },
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
