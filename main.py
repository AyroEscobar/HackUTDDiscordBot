import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from better_profanity import profanity
from profanity_filter import setup_profanity_filter  # Import your function
from quote_system import setup_quote_commands
from verification_system import setup_verification_system, handle_member_join




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

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    # Set up verification for all guilds
    for guild in bot.guilds:
        await setup_verification_system(guild)

@bot.event
async def on_member_join(member):
    await handle_member_join(member)

gamerRole = "Gamer"

#Decorator in python 
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}")


setup_profanity_filter(bot)
setup_quote_commands(bot)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name = gamerRole)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {gamerRole}")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name = gamerRole)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {gamerRole} removed ")
    else:
        await ctx.send("Role doesn't exist")
    

    

#Parameters token for discord, log_handler, log_level
bot.run(token, log_handler = handler, log_level = logging.DEBUG)






