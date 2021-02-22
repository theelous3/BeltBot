__all__ = ["on_message"]


import logging

from bot.bot import BOT
from bot.bazaar import bazaar_on_message


_HANDLERS = [
    # bazaar_on_message
]


@BOT.event
async def on_message(message):
    for handler in _HANDLERS:
        await handler(message)
    await BOT.process_commands(message)


@BOT.event
async def on_command(ctx):
    logging.info(ctx.message)
    logging.info(ctx.message.content)
