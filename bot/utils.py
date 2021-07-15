import logging
from datetime import datetime
from functools import wraps
from re import compile


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


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(datetime_):
    return datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S")


def format_requests(requests):
    formatted_requests = []
    for request in requests:
        formatted_requests.append(
            (
                f"Created: {request['created_at']}"
                f"\nID: {request['_id']}"
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


def when_mentioned(bot, msg):
    """A hacky rewrite of the commands.when_mentioned prefix callable, because the original one
    is trash.
    """
    return [
        bot.user.mention + "  ",
        bot.user.mention + " ",
        f"<@!{bot.user.id}>  ",
        f"<@!{bot.user.id}> ",
        f"<@!{bot.user.id}>",
    ]

def find_username(text):
    _USERNAME_RE = compile(r"(reddit.com|^|[^\w/])/?u/(?P<name>\w+)")
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
#https://reddit.com/u/theelous3
#
    if match := _USERNAME_RE.search(text):
        return match.group('name')
