import logging


from bot.bot import BOT
from bot.constants import TOKEN
from bot.beltbot import *
from bot.on_message_handlers import *


logging.basicConfig(level=logging.INFO)


BOT.run(TOKEN)
