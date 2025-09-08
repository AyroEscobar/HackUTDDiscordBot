from better_profanity import profanity

def setup_profanity_filter(bot):
    """Setup profanity filter for the given bot instance"""
    
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        if profanity.contains_profanity(message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} - don't use that word!")

        # Need to call this so that the overriding functions can keep being called
        await bot.process_commands(message)