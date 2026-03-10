import discord
import subprocess
import json
import os
from dotenv import load_dotenv
from mcstatus import JavaServer

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()

class DiscordController(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.mc_process = None

    async def setup_hook(self):
        await self.tree.sync()

bot = DiscordController()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ---------------------------
# /join (start bots)
# ---------------------------
@bot.tree.command(name="join", description="Make Minecraft bots join the server")
async def join(interaction: discord.Interaction):
    if bot.mc_process:
        await interaction.response.send_message("⚠ Bots are already on the server")
        return
    bot.mc_process = subprocess.Popen(["node", "bot_manager.js"])
    await interaction.response.send_message("✅ Bots joined the server")

# ---------------------------
# /leave (stop bots)
# ---------------------------
@bot.tree.command(name="leave", description="Make Minecraft bots leave the server")
async def leave(interaction: discord.Interaction):
    if not bot.mc_process:
        await interaction.response.send_message("⚠ Bots are not on the server")
        return
    bot.mc_process.kill()
    bot.mc_process = None
    await interaction.response.send_message("🛑 Bots left the server")

# ---------------------------
# /restart
# ---------------------------
@bot.tree.command(name="restart", description="Restart Minecraft bots")
async def restart(interaction: discord.Interaction):
    if bot.mc_process:
        bot.mc_process.kill()
    bot.mc_process = subprocess.Popen(["node", "bot_manager.js"])
    await interaction.response.send_message("🔄 Bots restarted")

# ---------------------------
# /bots
# ---------------------------
@bot.tree.command(name="bots", description="Show configured bots")
async def bots(interaction: discord.Interaction):
    with open("bots.json") as f:
        data = json.load(f)
    names = "\n".join(data["bots"])
    await interaction.response.send_message(f"🤖 Configured Bots:\n```\n{names}\n```")

# ---------------------------
# /servers
# ---------------------------
@bot.tree.command(name="servers", description="Show Minecraft servers")
async def servers(interaction: discord.Interaction):
    with open("servers.json") as f:
        data = json.load(f)
    await interaction.response.send_message(f"🌍 Minecraft Server:\n```\n{data['host']}:{data['port']}\n```")

# ---------------------------
# /ping
# ---------------------------
@bot.tree.command(name="ping", description="Check server latency")
async def ping(interaction: discord.Interaction):
    try:
        with open("servers.json") as f:
            data = json.load(f)
        server = JavaServer.lookup(f"{data['host']}:{data['port']}")
        status = server.status()
        await interaction.response.send_message(
            f"🏓 Ping: {round(status.latency)} ms | Players: {status.players.online}/{status.players.max}"
        )
    except:
        await interaction.response.send_message("❌ Server offline")

# ---------------------------
# /status
# ---------------------------
@bot.tree.command(name="status", description="Check server status")
async def status(interaction: discord.Interaction):
    try:
        with open("servers.json") as f:
            data = json.load(f)
        server = JavaServer.lookup(f"{data['host']}:{data['port']}")
        status = server.status()
        await interaction.response.send_message(
            f"🟢 Server Online | Version: {status.version.name}\nPlayers: {status.players.online}/{status.players.max}"
        )
    except:
        await interaction.response.send_message("🔴 Server Offline")

bot.run(TOKEN)
