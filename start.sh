#!/bin/bash
echo "Starting Minecraft bots..."
node bot_manager.js &
echo "Starting Discord bot..."
python discord_bot.py
