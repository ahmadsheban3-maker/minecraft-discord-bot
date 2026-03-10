import discord
import subprocess
import json
import os
from dotenv import load_dotenv
from mcstatus import JavaServer

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

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
    print(f"Bot logged in as {bot.user}")


# ---------------------------
# START BOTS
# ---------------------------
@bot.tree.command(name="startbots", description="Start Minecraft bots")
async def startbots(interaction: discord.Interaction):

    if bot.mc_process:
        await interaction.response.send_message("⚠ Bots already running")
        return

    bot.mc_process = subprocess.Popen(["node", "bot_manager.js"])

    await interaction.response.send_message("✅ Minecraft bots started")


# ---------------------------
# STOP BOTS
# ---------------------------
@bot.tree.command(name="stopbots", description="Stop Minecraft bots")
async def stopbots(interaction: discord.Interaction):

    if not bot.mc_process:
        await interaction.response.send_message("⚠ Bots are not running")
        return

    bot.mc_process.kill()
    bot.mc_process = None

    await interaction.response.send_message("🛑 Minecraft bots stopped")


# ---------------------------
# RESTART BOTS
# ---------------------------
@bot.tree.command(name="restart", description="Restart Minecraft bots")
async def restart(interaction: discord.Interaction):

    if bot.mc_process:
        bot.mc_process.kill()

    bot.mc_process = subprocess.Popen(["node", "bot_manager.js"])

    await interaction.response.send_message("🔄 Minecraft bots restarted")


# ---------------------------
# LIST BOTS
# ---------------------------
@bot.tree.command(name="bots", description="Show configured bots")
async def bots(interaction: discord.Interaction):

    with open("bots.json") as f:
        data = json.load(f)

    names = "\n".join(data["bots"])

    await interaction.response.send_message(
        f"🤖 Configured Bots:\n```\n{names}\n```"
    )


# ---------------------------
# SHOW SERVER
# ---------------------------
@bot.tree.command(name="servers", description="Show server information")
async def servers(interaction: discord.Interaction):

    with open("servers.json") as f:
        data = json.load(f)

    msg = f"{data['host']}:{data['port']}"

    await interaction.response.send_message(
        f"🌍 Minecraft Server:\n```\n{msg}\n```"
    )


# ---------------------------
# PING SERVER
# ---------------------------
@bot.tree.command(name="ping", description="Check server latency")
async def ping(interaction: discord.Interaction):

    try:
        with open("servers.json") as f:
            data = json.load(f)

        server = JavaServer.lookup(f"{data['host']}:{data['port']}")
        status = server.status()

        await interaction.response.send_message(
            f"🏓 Ping: {round(status.latency)} ms"
        )

    except:
        await interaction.response.send_message("❌ Server offline")


# ---------------------------
# SERVER STATUS
# ---------------------------
@bot.tree.command(name="status", description="Check Minecraft server status")
async def status(interaction: discord.Interaction):

    try:
        with open("servers.json") as f:
            data = json.load(f)

        server = JavaServer.lookup(f"{data['host']}:{data['port']}")
        status = server.status()

        await interaction.response.send_message(
            f"🟢 Server Online\nPlayers: {status.players.online}/{status.players.max}\nVersion: {status.version.name}"
        )

    except:
        await interaction.response.send_message("🔴 Server Offline")


bot.run(TOKEN)
