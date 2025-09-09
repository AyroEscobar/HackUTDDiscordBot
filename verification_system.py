import discord
from discord.ext import commands

class WelcomeModal(discord.ui.Modal, title="HackUTD2025 - Welcome & Rules Agreement"):
    def __init__(self):
        super().__init__()
    
    # Text input for agreement
    agreement = discord.ui.TextInput(
        label="Type 'I AGREE' to accept the rules",
        placeholder="Type exactly: I AGREE",
        required=True,
        max_length=10
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.agreement.value.upper() == "I AGREE":
            # Remove unverified, add verified role
            unverified_role = discord.utils.get(interaction.guild.roles, name="Unverified")
            verified_role = discord.utils.get(interaction.guild.roles, name="Verified")
            
            if unverified_role:
                await interaction.user.remove_roles(unverified_role)
            if verified_role:
                await interaction.user.add_roles(verified_role)
            
            await interaction.response.send_message(
                "🎉 Welcome to HackUTD2025! You now have access to all channels. Let's build something amazing!", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Please type exactly 'I AGREE' to accept the rules.", 
                ephemeral=True
            )

class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view
    
    @discord.ui.button(label="📋 Read Rules & Verify", style=discord.ButtonStyle.blurple, emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WelcomeModal()
        await interaction.response.send_modal(modal)

async def send_welcome_message(channel):
    """Send the welcome embed with rules"""
    embed = discord.Embed(
        title="🚀 Welcome to HackUTD2025!",
        description="Welcome to our official Discord server! Please read our rules below and verify to gain access.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📋 Server Rules",
        value="""
        1. **Be respectful** - Treat everyone with kindness and respect
        2. **No spam** - Keep messages relevant and don't flood channels
        3. **Stay on topic** - Use appropriate channels for discussions
        4. **No NSFW content** - Keep all content appropriate
        5. **Ask for help** - Use #help channels when you need assistance
        6. **Have fun** - We're here to learn, build, and connect!
        """,
        inline=False
    )
    
    embed.add_field(
        name="🎯 Event Guidelines",
        value="""
        • Form teams respectfully in #team-formation
        • Share progress in #project-showcase
        • Mentors are here to help - don't hesitate to ask!
        • Submission deadline: [DATE] at [TIME]
        """,
        inline=False
    )
    
    embed.set_footer(text="Click the button below to verify and join the hackathon!")
    
    view = VerificationView()
    await channel.send(embed=embed, view=view)

async def setup_verification_system(guild):
    """Set up roles, channels, and permissions for verification system"""
    
    print(f"Setting up verification system for {guild.name}...")
    
    # Create Unverified role
    unverified_role = discord.utils.get(guild.roles, name="Unverified")
    if not unverified_role:
        unverified_role = await guild.create_role(
            name="Unverified", 
            color=discord.Color.red(),
            reason="Verification system setup"
        )
        print("Created Unverified role")
    
    # Create Verified role
    verified_role = discord.utils.get(guild.roles, name="Verified")
    if not verified_role:
        verified_role = await guild.create_role(
            name="Verified", 
            color=discord.Color.green(),
            reason="Verification system setup"
        )
        print("Created Verified role")
    
    # Create welcome channel
    welcome_channel = discord.utils.get(guild.channels, name="welcome")
    if not welcome_channel:
        # Create the channel
        welcome_channel = await guild.create_text_channel(
            "welcome",
            topic="Welcome to HackUTD2025! Please verify to gain access to the server.",
            reason="Verification system setup"
        )
        
        # Set welcome channel permissions
        await welcome_channel.set_permissions(
            guild.default_role, 
            view_channel=True, 
            send_messages=False,
            reason="Welcome channel setup"
        )
        await welcome_channel.set_permissions(
            unverified_role, 
            view_channel=True, 
            send_messages=False,
            reason="Welcome channel setup"
        )
        await welcome_channel.set_permissions(
            verified_role, 
            view_channel=False,
            reason="Welcome channel setup"
        )
        print("Created welcome channel with permissions")
    
    # Clear any existing messages and send welcome message
    await welcome_channel.purge(limit=100)
    await send_welcome_message(welcome_channel)
    print("Sent welcome message")
    
    print("Verification system setup complete!")

# Event handler for when someone joins
async def handle_member_join(member):
    """Give new members the Unverified role"""
    unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
    if unverified_role:
        await member.add_roles(unverified_role, reason="New member verification")
        print(f"Gave {member.display_name} the Unverified role")

# Cog class for easier integration
class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await handle_member_join(member)
    
    @commands.command(name="setup_verification")
    @commands.has_permissions(administrator=True)
    async def setup_verification_command(self, ctx):
        """Admin command to manually setup verification system"""
        await setup_verification_system(ctx.guild)
        await ctx.send("✅ Verification system has been set up!")

async def setup(bot):
    """Setup function for loading as a cog"""
    await bot.add_cog(VerificationCog(bot))