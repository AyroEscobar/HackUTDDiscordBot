import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

#Documentation Link: https://discordpy.readthedocs.io/en/stable/
#source venv/bin/activate   to activate virtual environment

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

#parameters filename, encoding, mode (write)
handler = logging.FileHandler('discord.log', 'utf-8', 'w')
intents = discord.Intents.default()
#If an intent is not working you might need to manually enable it
intents.message_content = True
intents.members = True






