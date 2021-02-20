import logging


from bot.bot import BOT
from bot.constants import TOKEN
from bot.beltbot import *


logging.basicConfig(level=logging.INFO)


BOT.run(TOKEN)
