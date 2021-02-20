import discord
from discord.ext import commands


INTENTS = discord.Intents.default()
INTENTS.members = True
BOT = commands.Bot(command_prefix=commands.when_mentioned, intents=INTENTS)
