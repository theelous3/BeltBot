import discord
from discord.ext import commands

from bot.utils import when_mentioned


INTENTS = discord.Intents.default()
INTENTS.members = True
BOT = commands.Bot(command_prefix=when_mentioned, intents=INTENTS)
