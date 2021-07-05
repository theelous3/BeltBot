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


_USERNAME_RE = compile(r"[ | /]u/[A-Za-z0-9_-]+")


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
        found_text = match.group(0)
        name_only = found_text[2:]
        return name_only
