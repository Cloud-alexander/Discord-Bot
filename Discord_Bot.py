import discord
import os
from ec2_metadata import ec2_metadata

# Get the bot token from environment variables
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("Error: TOKEN environment variable not set.")

# Configure Discord intents to listen for messages
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Event: Bot is ready
@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

# Function: Handle commands
async def handle_commands(message):
    command = message.content.lower()

    # Command: "hello"
    if command == 'hello':
        await message.channel.send('Hello! How can I assist you?')

    # Command: "!serverinfo"
    elif command == '!serverinfo':
        await send_ec2_metadata(message)

    # Command: "!ping"
    elif command == '!ping':
        await message.channel.send('Pong!')

    # Command: "!uptime"
    elif command == '!uptime':
        await send_ec2_uptime(message)

    # Unknown command
    else:
        await message.channel.send(
            "Sorry, I didn't understand that command. Try `hello`, `!serverinfo`, `!ping`, or `!uptime`."
        )

# Function: Send EC2 Metadata
async def send_ec2_metadata(message):
    try:
        region = ec2_metadata.region
        availability_zone = ec2_metadata.availability_zone
        public_ipv4 = ec2_metadata.public_ipv4

        response = (
            "**EC2 Instance Metadata:**\n"
            f"Region: {region}\n"
            f"Availability Zone: {availability_zone}\n"
            f"Public IPv4: {public_ipv4}"
        )
    except Exception as e:
        response = f"Error retrieving EC2 metadata: {e}"

    await message.channel.send(response)

# Function: Send EC2 Uptime
async def send_ec2_uptime(message):
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours, remainder = divmod(uptime_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            response = (
                f"**EC2 Uptime:** {int(hours)} hours, "
                f"{int(minutes)} minutes, {int(seconds)} seconds"
            )
    except Exception as e:
        response = f"Error retrieving uptime: {e}"

    await message.channel.send(response)

# Event: On message
@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return

    # Process commands
    await handle_commands(message)

# Run the bot
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Error starting the bot: {e}")
