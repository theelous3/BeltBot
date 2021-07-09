from re import compile

import asyncpraw
from asyncpraw.models.reddit.subreddit import SubredditFlair

from bot.constants import (
    SUBREDDIT,
    STANDARD_BELTS,
    MY_REDDIT_CLIENT_ID,
    MY_REDDIT_SECRET,
    MY_NAME,
    MY_REDDIT_PW,
    USER_AGENT,
)

_USERNAME_RE = compile(r"(^|[^\w/])/?u/(?P<name>\w+)")
#1st capture group = (^|[^\w/]) - 1st Alternative ^, ^ asserts position at start of a line, (| signifies or) 2nd Alternative [^\w\/]
#Match a single character not present in the list below [^\w\/]
#\w matches any word character (equivalent to [a-zA-Z0-9_])
#\/ matches the character / literally (case sensitive)
#\/ matches the character / literally (case sensitive)
#? matches the previous token between zero and one times, as many times as possible, giving back as needed (greedy)
#u matches the character u literally (case sensitive)
#\/ matches the character / literally (case sensitive)
#Named Capture Group name (?P<name>\w+)
#\w matches any word character (equivalent to [a-zA-Z0-9_])
#+ matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
#examples that get matched:
#/u/user
# /u/user
#text /u/user
#
#u/user
# u/user
#text u/user

REDDIT = asyncpraw.Reddit(
    client_id=MY_REDDIT_CLIENT_ID,
    client_secret=MY_REDDIT_SECRET,
    user_agent=USER_AGENT,
    username=MY_NAME,
    password=MY_REDDIT_PW,
)


async def set_reddit_flair(username, belt):

    beltinfo = STANDARD_BELTS.get(belt)

    if not beltinfo or not beltinfo.get("flair_text"):
        return False

    subreddit = await REDDIT.subreddit(SUBREDDIT)
    subreddit_flair = SubredditFlair(subreddit)

    await subreddit_flair.set(
        username, text=beltinfo["flair_text"], css_class=beltinfo["css_class"]
    )

    return True


async def reddit_flair_user(text, belt):
    if username := find_username(text):
        try:
            maybe_flaired = await set_reddit_flair(username, belt)
        except Exception as e:
            return f"\nI was unable to flair {username}"
        else:
            if maybe_flaired:
                return f"\nYou have also been flaired on reddit :)"


def find_username(text):
    if match := _USERNAME_RE.search(text):
        return match.group('name')
