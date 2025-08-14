import logging

from bot.utils import find_username

from asyncpraw import Reddit
from asyncpraw.models.reddit.subreddit import SubredditFlair

from bot.constants import (
    SUBREDDIT,
    ALL_BELTS,
    MY_REDDIT_CLIENT_ID,
    MY_REDDIT_SECRET,
    MY_NAME,
    MY_REDDIT_PW,
    USER_AGENT,
)


logger = logging.getLogger(__name__)


REDDIT = None


async def set_reddit_flair(username, belt):
    global REDDIT
    if REDDIT is None:
        REDDIT = Reddit(
            client_id=MY_REDDIT_CLIENT_ID,
            client_secret=MY_REDDIT_SECRET,
            user_agent=USER_AGENT,
            username=MY_NAME,
            password=MY_REDDIT_PW,
        )

    belt = ALL_BELTS.get(belt)

    if not belt or not belt.get("flair_text"):
        return False

    subreddit = await REDDIT.subreddit(SUBREDDIT)
    subreddit_flair = SubredditFlair(subreddit)

    logger.info(
        f"flairing {username} -> {belt['flair_text']}, {belt['css_class']}, {belt['reddit_id']}"
    )

    await subreddit_flair.set(
        username,
        flair_template_id=belt["reddit_id"],
    )

    return True


async def reddit_flair_user(ctx, username, belt):
    if username := find_username(username):
        try:
            maybe_flaired = await set_reddit_flair(username, belt)
        except Exception as e:
            logger.error("Error setting reddit flair: %s", e, exc_info=True)
        else:
            if maybe_flaired:
                return f"\n{username} you have been flaired on reddit by {ctx.author.mention} :)"

    if username:
        return f"\n{ctx.author.mention} I was unable to flair {username} :O"

