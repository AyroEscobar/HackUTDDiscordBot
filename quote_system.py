import random
import requests
from discord.ext import commands

# Define the functions FIRST, before using them
async def get_random_joke():
    """Get a random joke from API or fallback to local"""
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single")
        data = response.json()
        
        if data.get('error'):
            return get_random_joke_local()
        
        return data['joke']
    except:
        return get_random_joke_local()

async def get_random_quote():
    """Get a random quote from API or fallback to local"""
    try:
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        
        return f'"{data["content"]}" - {data["author"]}'
    except:
        return get_random_quote_local()

def get_random_joke_local():
    """Fallback jokes if API fails"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't programmers like nature? It has too many bugs.",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? He was outstanding in his field!"
    ]
    return random.choice(jokes)

def get_random_quote_local():
    """Fallback tech/motivational quotes if API fails"""
    tech_quotes = [
        '"The only way to do great work is to love what you do." - Steve Jobs',
        '"Innovation distinguishes between a leader and a follower." - Steve Jobs',
        '"Code is like humor. When you have to explain it, it\'s bad." - Cory House',
        '"First, solve the problem. Then, write the code." - John Johnson',
        '"Experience is the name everyone gives to their mistakes." - Oscar Wilde',
        '"In order to be irreplaceable, one must always be different." - Coco Chanel',
        '"Java is to JavaScript what car is to Carpet." - Chris Heilmann',
        '"The best error message is the one that never shows up." - Thomas Fuchs',
        '"Simplicity is the soul of efficiency." - Austin Freeman',
        '"Make it work, make it right, make it fast." - Kent Beck',
        '"The computer was born to solve problems that did not exist before." - Bill Gates',
        '"Talk is cheap. Show me the code." - Linus Torvalds',
        '"Programs must be written for people to read, and only incidentally for machines to execute." - Harold Abelson'
    ]
    return random.choice(tech_quotes)

# NOW define the setup function that uses those functions
def setup_quote_commands(bot):
    """Function that is going to be for random joke maker"""
    
    @bot.command(name='joke')
    async def joke_command(ctx):
        """Sending a random joke"""
        joke = await get_random_joke()  # Now this function is defined above!
        await ctx.send(joke)
    
    @bot.command(name='quote')
    async def quote_command(ctx):
        """Send a random quote"""
        quote = await get_random_quote()
        await ctx.send(quote)