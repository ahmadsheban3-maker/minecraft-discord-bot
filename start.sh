#!/bin/bash

echo "Starting Minecraft Bots"
node bot_manager.js &

echo "Starting Dashboard"
node dashboard.js &

echo "Starting Discord Bot"
python discord_bot.py