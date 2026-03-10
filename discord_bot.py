import discord
import os
from dotenv import load_dotenv
from mcstatus import JavaServer

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# /status command
@bot.tree.command(name="status", description="Check Minecraft server status")
async def status(interaction: discord.Interaction):

    try:
        server = JavaServer.lookup("play.example.com:25565")
        status = server.status()

        await interaction.response.send_message(
            f"🟢 Server Online\nPlayers: {status.players.online}/{status.players.max}"
        )

    except:
        await interaction.response.send_message("🔴 Server Offline")

# Discord → Minecraft chat
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != CHANNEL:
        return

    with open("dc_chat.txt", "w") as f:
        f.write(message.content)

bot.run(TOKEN)
