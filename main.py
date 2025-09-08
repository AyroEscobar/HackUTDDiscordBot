import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from better_profanity import profanity


#Documentation Link: https://discordpy.readthedocs.io/en/stable/
#source venv/bin/activate   to activate virtual environment

#Multi Block Comments
'''
Things required of the bot
#Announcements through the bot
#Having commands to go back through information (displaying workshop schedule, locations of mentors, previous winners)
? Add verification of hackers through the bot (that they are not bots, so no mass sending a bunch of messages)
Add Roles Mentors, Hackers, Sponsors, Organizers, MLH Coach, 
Add a command for a ping pong game little thing


'''

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

#parameters filename, encoding, mode (write)
handler = logging.FileHandler( filename ='discord.log', encoding = 'utf-8', mode ='w')
intents = discord.Intents.default()
#If an intent is not working you might need to manually enable it
intents.message_content = True
intents.members = True

#parameters command_prefix, intent
bot = commands.Bot(command_prefix ='!', intents = intents)

#Decorator in python 
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if profanity.contains_profanity(message.content):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't use that word!")

    #Need to call this so that the overriding functions can keep being called
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")
    

    

#Parameters token for discord, log_handler, log_level
bot.run(token, log_handler = handler, log_level = logging.DEBUG)






