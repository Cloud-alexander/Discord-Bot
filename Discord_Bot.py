import discord
import os
from ec2_metadata import ec2_metadata

# Get the bot token from environment variables
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("Error: Discord bot token not found in environment variables.")

# Configure intents to enable message listening
intents = discord.Intents.default()
intents.message_content = True  # Explicitly enable message content intent
client = discord.Client(intents=intents)

# Event: Bot is ready
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

# Centralized command handler
async def handle_command(command):
    """Handles known commands and returns the appropriate response."""
    if command == "hello":
        return "Hello! How can I assist you?"

    elif command == "!serverinfo":
        try:
            return (
                "**EC2 Instance Metadata:**\n"
                f"Region: {ec2_metadata.region}\n"
                f"Availability Zone: {ec2_metadata.availability_zone}\n"
                f"Public IPv4: {ec2_metadata.public_ipv4}"
            )
        except Exception as e:
            return f"An error occurred while retrieving EC2 metadata: {e}"

    elif command == "!ping":
        return "Pong!"

    elif command == "!uptime":
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"EC2 Uptime: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
        except Exception as e:
            return f"An error occurred while retrieving uptime: {e}"

    return "Sorry, I didn't understand that command. Try `hello`, `!serverinfo`, `!ping`, or `!uptime`."

# Event: Handle messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    response = await handle_command(message.content.lower())
    await message.channel.send(response)

# Run the bot
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Error starting the bot: {e}")
