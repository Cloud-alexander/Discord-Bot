import os
import logging
from discord.ext import commands
from ec2_metadata import ec2_metadata

# Enable logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the bot token from environment variables
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("Error: TOKEN environment variable not set.")

# Initialize the bot with command prefix
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    logger.info(f"Bot is online as {bot.user}")
    print(f"Bot is online as {bot.user}")

# Command: "hello" (simple greeting)
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello! How can I assist you?')

# Command: "serverinfo" (fetch EC2 metadata)
@bot.command(name='serverinfo')
async def serverinfo(ctx):
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
        logger.error(f"Error fetching EC2 metadata: {e}")
        response = "Unable to retrieve EC2 metadata at the moment."

    await ctx.send(response)

# Command: "ping" (latency test)
@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Latency in milliseconds
    await ctx.send(f"Pong! 🏓 Latency: {latency}ms")

# Command: "uptime" (fetch EC2 uptime)
@bot.command(name='uptime')
async def uptime(ctx):
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
        logger.error(f"Error fetching uptime: {e}")
        response = "Unable to retrieve uptime information at the moment."

    await ctx.send(response)

# Error Handler: Catch command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Try `!hello`, `!serverinfo`, `!ping`, or `!uptime`.")
    else:
        logger.error(f"An error occurred: {error}")
        await ctx.send("An error occurred while processing your request.")

# Run the bot
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f"Critical error starting the bot: {e}")
        print(f"Critical error starting the bot: {e}")
