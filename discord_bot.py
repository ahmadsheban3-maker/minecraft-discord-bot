import discord
import subprocess
import json
import os
from dotenv import load_dotenv
from mcstatus import JavaServer
from bot_manager import startBot, botsConfig

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# Load servers
with open("servers.json") as f:
    servers = json.load(f)

# Ready event
@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")

# ---------------------------
# /join (server dropdown)
# ---------------------------
class ServerSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=s["name"], description=f"{s['host']}:{s['port']}", value=str(i))
            for i, s in enumerate(servers)
        ]
        super().__init__(placeholder="Select a server", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        index = int(self.values[0])
        server = servers[index]
        for username in [b for b in botsConfig["bots"]]:
            startBot(username, server)
        await interaction.response.send_message(f"✅ Bots joining **{server['name']}**!")

class ServerDropdown(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ServerSelect())

@tree.command(name="join", description="Make bots join a server")
async def join(interaction: discord.Interaction):
    view = ServerDropdown()
    await interaction.response.send_message("Select a server for your bots:", view=view)

# ---------------------------
# /leave (stop all bots)
# ---------------------------
@tree.command(name="leave", description="Make all bots leave the server")
async def leave(interaction: discord.Interaction):
    # Kill the bot_manager.js process if it exists
    # (Optional: you can track running bots to stop them individually)
    subprocess.Popen(["pkill", "-f", "node"])  # works on Linux/Railway
    await interaction.response.send_message("🛑 Bots left all servers")

# ---------------------------
# /restart
# ---------------------------
@tree.command(name="restart", description="Restart bots")
async def restart(interaction: discord.Interaction):
    subprocess.Popen(["pkill", "-f", "node"])
    await interaction.response.send_message("🔄 Bots restarted, use /join to select server")

# ---------------------------
# /bots
# ---------------------------
@tree.command(name="bots", description="Show configured bots")
async def bots(interaction: discord.Interaction):
    await interaction.response.send_message("🤖 Configured Bots:\n" + "\n".join(botsConfig["bots"]))

# ---------------------------
# /servers
# ---------------------------
@tree.command(name="servers", description="Show available servers")
async def servers_cmd(interaction: discord.Interaction):
    msg = "\n".join([f"{s['name']}: {s['host']}:{s['port']}" for s in servers])
    await interaction.response.send_message(f"🌍 Available Servers:\n{msg}")

# ---------------------------
# /ping
# ---------------------------
@tree.command(name="ping", description="Check server latency")
async def ping(interaction: discord.Interaction):
    msg_list = []
    for s in servers:
        try:
            server = JavaServer.lookup(f"{s['host']}:{s['port']}")
            status = server.status()
            msg_list.append(f"{s['name']}: 🏓 {round(status.latency)}ms | Players: {status.players.online}/{status.players.max}")
        except:
            msg_list.append(f"{s['name']}: ❌ offline")
    await interaction.response.send_message("\n".join(msg_list))

# ---------------------------
# /status
# ---------------------------
@tree.command(name="status", description="Check server status")
async def status(interaction: discord.Interaction):
    msg_list = []
    for s in servers:
        try:
            server = JavaServer.lookup(f"{s['host']}:{s['port']}")
            status = server.status()
            msg_list.append(f"{s['name']}: 🟢 Online | {status.players.online}/{status.players.max} | Version: {status.version.name}")
        except:
            msg_list.append(f"{s['name']}: 🔴 Offline")
    await interaction.response.send_message("\n".join(msg_list))

bot.run(TOKEN)
