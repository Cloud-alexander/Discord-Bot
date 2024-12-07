import discord
from discord.ext import commands
from ec2_metadata import ec2_metadata
import os

# Intents setup (required for some events like member joins)
intents = discord.Intents.default()
intents.messages = True  # For reading messages
intents.message_content = True  # To access message content

# Bot Setup
bot = commands.Bot(command_prefix="!", intents=intents))

# Event: Bot ready
@client.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    print("Bot is ready and listening for commands.")

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Event: On message
@client.event
async def on_message(message):
    if message.author == client.user:
        return 
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

# Run the bot
bot.run("YOUR_DISCORD_BOT_TOKEN")
