"""
Author: theelous3.net
Bot config:
    Requires priviledged intent `members`.
    Requires; [
        "Manage Roles",
        "Send Messages",
        "Read Message History"
    ]
"""


import json
import logging
from os import getenv
from uuid import uuid4
from re import compile
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps, partial
from contextlib import contextmanager
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.utils import get as discord_find
from discord.ext.commands.errors import UserInputError, CommandNotFound

import asyncpraw
from asyncpraw.models.reddit.subreddit import SubredditFlair


logging.basicConfig(level=logging.INFO)


MY_NAME = "LPUBeltbot"
MY_REDDIT_PW = getenv("BELTBOT_REDDIT_PW")
MY_REDDIT_CLIENT_ID = getenv("BELTBOT_REDDIT_CID")
MY_REDDIT_SECRET = getenv("BELTBOT_REDDIT_KEY")

USER_AGENT = "LPUBeltbot_v0.1"

DATA_FILE = "belt_requests.json"

INTENTS = discord.Intents.default()
INTENTS.members = True

TOKEN = getenv("BELTBOT_TOKEN")

BOT = commands.Bot(command_prefix=commands.when_mentioned, intents=INTENTS)

# ========== LPU discord and reddit belt data ==========

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
    "HoF": {"name": "Hall of Fame", "flair_text": None, "css_class": None},
}

HUMAN_READABLE_BELTS = ", ".join([belt for belt in VALID_BELTS])

# ========== Special requests ==========


@dataclass
class HoF:
    name = VALID_BELTS["HoF"]["name"]


SPECIAL_REQUESTS = {"HoF": HoF.name + " entry"}


# ========== REDDIT JUNK ==========

REDDIT = asyncpraw.Reddit(
    client_id=MY_REDDIT_CLIENT_ID,
    client_secret=MY_REDDIT_SECRET,
    user_agent=USER_AGENT,
    username=MY_NAME,
    password=MY_REDDIT_PW,
)


async def set_reddit_flair(username, belt):

    beltinfo = VALID_BELTS.get(belt)
    if not beltinfo or not beltinfo.get("flair_text"):
        return False

    subreddit = await REDDIT.subreddit(SUBREDDIT)
    subreddit_flair = SubredditFlair(subreddit)

    await subreddit_flair.set(
        username, text=beltinfo["flair_text"], css_class=beltinfo["css_class"]
    )

    return True


_username_re = r = compile(r"/u/[A-Za-z0-9_-]+")


def find_username(text):
    if match := _username_re.search(text):
        found_text = match.group(0)
        name_only = found_text[3:]
        return name_only


async def reddit_flair_user(text, belt):
    if username := find_username(text):
        try:
            maybe_flaired = await set_reddit_flair(username, belt)
        except:
            return f"\nI was unable to flair {username}"
        else:
            if maybe_flaired:
                return f"\nYou have also been flaired on reddit :)"


# ========== UTILITY FUNCTIONS ==========


def suppress_exceptions(awaitable=True):
    """
    Normally horrible, but bots should be borderline invincible
    to maintain as much functionality as possible in adverse circumstances.
    """
    async def confused_middleman(callable):
        @wraps(callable)
        async def inner(*args, **kwargs):
            try:
                if awaitable:
                    return await callable(*args, **kwargs)
                else:
                    return callable(*args, **kwargs)
            except Exception as e:
                logging.error(e)

        return inner

    return confused_middleman


def check_authz(ctx, role_name):
    matching_role = get_role_by_name(ctx, role_name)
    approver_roles = ctx.author.roles

    if matching_role in approver_roles:
        return True

    return False


def requires_role(role_name):
    def bleep_bloop(coro):
        @wraps(coro)
        async def inner(ctx, *args, **kwargs):
            if check_authz(ctx, role_name):
                return await coro(ctx, *args, **kwargs)
            else:
                await ctx.send(
                    (
                        f"{ctx.author.display_name}, you don't have the permissions required"
                        f" for the command `{ctx.command.qualified_name}`."
                    )
                )

        return inner

    return bleep_bloop


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(datetime_):
    return datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S")


def write_json(data=None):
    with open(DATA_FILE) as jf:
        last_known_good_data = json.load(jf)

    try:
        with open(DATA_FILE, "w+") as jf:
            json.dump(data, jf)
    except Exception as e:
        with open(DATA_FILE, "w+") as jf:
            json.dump(last_known_good_data, jf)
        raise e


# ========== BOT LOGIC ==========


def get_role_by_name(ctx, role_name):
    roles = ctx.message.guild.roles
    return next((role for role in roles if role.name == role_name), None)


def log_request(request):
    with open(DATA_FILE) as jf:
        j = json.load(jf)

    j["belt_requests"].append(request)

    write_json(j)

    logging.info(f"Logged belt request {request}")


def update_request(request):
    with open(DATA_FILE) as jf:
        j = json.load(jf)

    index, _ = next((i, __) for i, __ in enumerate(j["belt_requests"]))
    j["belt_requests"][index] = request

    write_json(j)

    logging.info(f"Updated belt request {request}")


def load_requests(sort="oldest"):
    with open(DATA_FILE) as jf:
        j = json.load(jf)

    requests = [request for request in j["belt_requests"]]

    requests = sorted(requests, key=lambda request: request["created_at"])

    if sort == "oldest":
        requests = list(reversed(requests))

    return requests


def load_raw_json():
    with open(DATA_FILE) as jf:
        j = json.load(jf)
        return j


def get_request(request_id):
    requests = load_requests()

    return next(
        (request for request in requests if request["request_id"] == request_id), None
    )


def remove_request(request_id):
    with open(DATA_FILE) as jf:
        j = json.load(jf)

    found_at = None

    for index, request in enumerate(j["belt_requests"]):
        if request["request_id"] == request_id:
            found_at = index
            break

    if found_at is not None:
        del j["belt_requests"][index]

    write_json(j)


def format_requests(requests):
    formatted_requests = []
    for request in requests:
        formatted_requests.append(
            (
                f"Created: {request['created_at']}"
                f"\nID: {request['request_id']}"
                f"\nUser: `@{request['author']}`"
                f"\nBelt: {request['colour']}"
                f"\nMessage: {request['body']}"
                f"\nURL: {request['jump_url']}"
            )
            + (
                f"\nUnder review by: {request['reviewer']}"
                if request.get("reviewer")
                else ""
            )
        )
    return "\n\n==========\n\n".join(formatted_requests)


_beltrequest_help = "Include your username in the format `/u/username_here` anywhere in the message body to be flaired on reddit!"


@suppress_exceptions
@BOT.command(name="beltrequest", help=_beltrequest_help)
async def beltrequest_handler(ctx, colour, spacer, *body):
    if colour not in VALID_BELTS:
        await ctx.send(
            (
                f"{ctx.message.author.mention} I don't think {colour} is a real belt :( \n"
                f"Try one of these: {HUMAN_READABLE_BELTS}"
            ),
            mention_author=True,
        )
        return

    await ctx.send(
        f"{ctx.message.author.mention} thanks for your {VALID_BELTS[colour]['name']} request!",
        mention_author=True,
    )

    body = " ".join(body) or ""
    request = {
        "request_id": str(uuid4())[-12:],
        "author": ctx.author.display_name,
        "author_id": ctx.author.id,
        "colour": colour,
        "created_at": get_now(),
        "body": body,
        "jump_url": ctx.message.jump_url,
    }

    log_request(request)


@suppress_exceptions
@BOT.command(name="beltlist")
async def list_handler(ctx, sort="oldest"):
    if sort not in ["oldest", "newest"]:
        await ctx.send(
            (
                f"You can sort by either `oldest` or `newest`. I don't understand `{sort}`"
                "I'm going to return you the requests sorted by oldest first anyway :)"
            )
        )
        sort = "oldest"

    requests = load_requests(sort)

    if not requests:
        await ctx.send("There are no belt requests waiting for approval :D")
        return

    await ctx.send(
        f"Active requests, sorted by {sort}:\n\n{format_requests(requests)}",
        mention_author=True,
    )


@suppress_exceptions
@BOT.command(name="beltapprove")
@requires_role("Mods")
async def approval_handler(ctx, request_id, *reason):
    request = get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await ctx.message.guild.fetch_member(request["author_id"])

    if member is None:
        await ctx.send(
            f"No member found. They've left the server, or have been removed."
        )
        remove_request(request_id)
        return

    role_name = VALID_BELTS[request["colour"]]["name"]
    try:
        role = get_role_by_name(ctx, role_name)
        await member.add_roles(role)
    except AttributeError:
        role = SPECIAL_REQUESTS[request["colour"]]

    flair_text = await reddit_flair_user(request["body"], request["colour"])

    message = (
        f"{member.mention}, {ctx.author.mention} has reviewed and approved your request. "
        f"Congrats on your {role.name}!"
    )
    if reason:
        message += " ".join(reason_part for reason_part in reason)
    if flair_text:
        message += flair_text

    await ctx.send(message)

    remove_request(request_id)


@suppress_exceptions
@BOT.command(name="beltreject")
@requires_role("Mods")
async def rejection_handler(ctx, request_id, *reason):
    request = get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    if not reason:
        await ctx.send("You need to provide a reason!")
        return

    member = await ctx.message.guild.fetch_member(request["author_id"])

    if member is None:
        await ctx.send(
            f"No member found. They've left the server, or have been removed."
        )
        remove_request(request_id)
        return

    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{member.mention}, {ctx.author.mention} has reviewed and denied your request "
            f"for {role.name}."
            f"\nNotes: {' '.join(reason_part for reason_part in reason)}"
        )
    )

    remove_request(request_id)


@suppress_exceptions
@BOT.command(name="beltmoreinfo")
@requires_role("Mods")
async def moreinfo_handler(ctx, request_id, *reason):
    guild = ctx.message.guild
    request = get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    if not reason:
        await ctx.send("You need to provide more information!")
        return

    member = await guild.fetch_member(request["author_id"])

    if member is None:
        await ctx.send(
            f"No member found. They've left the server, or have been removed."
        )
        remove_request(request_id)
        return

    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{member.mention}, {ctx.author.mention} has reviewed your request for"
            f" {role.name} but needs more information. Please update your"
            f" request here: {request['jump_url']}"
            f"\nNotes: {' '.join(reason_part for reason_part in reason)}"
        )
    )


@suppress_exceptions
@BOT.command(name="beltreview")
@requires_role("Mods")
async def beltreview_handler(ctx, request_id):
    guild = ctx.message.guild
    request = get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await guild.fetch_member(request["author_id"])
    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    request["reviewer"] = ctx.author.display_name

    await ctx.send(
        (
            f"{ctx.author.mention} is reviewing `{member.display_name}`'s request for"
            f" {role.name}"
        )
    )

    update_request(request)


@suppress_exceptions
@BOT.command(name="beltunreview")
@requires_role("Mods")
async def beltunreview_handler(ctx, request_id):
    guild = ctx.message.guild
    request = get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await guild.fetch_member(request["author_id"])
    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    del request["reviewer"]

    await ctx.send(
        (
            f"{ctx.author.mention} *stopped* the review on `{member.display_name}`'s request for"
            f" {role.name}"
        )
    )

    update_request(request)


@suppress_exceptions
@BOT.command(name="getrawjson")
@requires_role("BeltBotMaintainer")
async def getrawjson_handler(ctx):
    j = load_raw_json()
    await ctx.send(f"Hey boss, here ya go:\n```{json.dumps(j)}```")


@suppress_exceptions
@BOT.command(name="insertrawjson", rest_is_raw=True)
@requires_role("BeltBotMaintainer")
async def insertrawjson_handler(ctx, *, j):
    print(j)
    j = json.loads(j)
    write_json(j)
    ctx.send("I have updated the internal json. `.getrawjson` to see.")


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("No such command. Try `.help` to see my commands :D")
    elif isinstance(error, UserInputError):
        command = ctx.invoked_with
        await ctx.send(f"I don't understand. Try `.help {command}` to learn more :D")
    else:
        ctx.send("You've confused the bot :(")


def ensure_file_and_format():
    with open(DATA_FILE) as jf:
        j = json.load(jf)
    if not isinstance(j["belt_requests"], list):
        raise SystemExit("Your data file is corrupted, mothafuka.")


@BOT.event
async def on_ready():
    logging.info("BeltBot's a ready")
    for guild in BOT.guilds:
        logging.info(f"Connected to: {guild}")

    ensure_file_and_format()


BOT.run(TOKEN)
