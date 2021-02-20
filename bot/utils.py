import logging
from datetime import datetime
from functools import wraps


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
