import discord
from ec2_metadata import ec2_metadata
import os

# Initialize the bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Bot is ready and listening for commands.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    try:
        # Respond to "hello world"
        if message.content.lower() == "hello world":
            await message.channel.send("Hello!")

        # Respond to "tell me about my server!"
        elif message.content.lower() == "tell me about my server!":
            try:
                info = (
                    f"**Server Info:**\n"
                    f"- **Public IP:** {ec2_metadata.public_ipv4 or 'Not Available'}\n"
                    f"- **Region:** {ec2_metadata.region or 'Not Available'}\n"
                    f"- **Availability Zone:** {ec2_metadata.availability_zone or 'Not Available'}"
                )
                await message.channel.send(info)
            except Exception as e:
                await message.channel.send(f"Error fetching server data: {e}")

        # Default response for unknown commands
        else:
            await message.channel.send("Sorry, I don't understand that command.")
    except Exception as general_error:
        await message.channel.send(f"An error occurred: {general_error}")

# Graceful error handling for connection issues
@client.event
async def on_error(event, *args, **kwargs):
    with open("error.log", "a") as log_file:
        log_file.write(f"Error in {event}: {args}\n")

# Token stored securely in an environment variable
token = os.getenv('TOKEN')
if not token:
    print("Error: Discord bot token not found in environment variables.")
else:
    client.run(token)