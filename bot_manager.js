const mineflayer = require("mineflayer");
const fs = require("fs");

const server = JSON.parse(fs.readFileSync("servers.json"));
const botsConfig = JSON.parse(fs.readFileSync("bots.json"));

function startBot(username) {
  const bot = mineflayer.createBot({
    host: server.host,
    port: server.port,
    username: username,
    version: "1.21.11"
  });

  bot.on("login", () => console.log(`${username} joined ${server.host}:${server.port}`));

  // Anti-AFK jump
  bot.on("spawn", () => {
    setInterval(() => {
      bot.setControlState("jump", true);
      setTimeout(() => bot.setControlState("jump", false), 500);
    }, 30000);
  });

  // Minecraft -> Discord chat bridge
  bot.on("chat", (username, message) => {
    if (username === bot.username) return;
    fs.writeFileSync("mc_chat.txt", `[MC] ${username}: ${message}`);
  });

  // Discord -> Minecraft chat
  setInterval(() => {
    if (fs.existsSync("dc_chat.txt")) {
      const msg = fs.readFileSync("dc_chat.txt", "utf-8");
      bot.chat(msg);
      fs.unlinkSync("dc_chat.txt");
    }
  }, 2000);

  // Auto reconnect
  bot.on("end", () => {
    console.log(`${username} disconnected, reconnecting...`);
    setTimeout(() => startBot(username), 5000);
  });

  bot.on("error", (err) => console.log(`${username} error: ${err.message}`));
}

// Start all bots
botsConfig.bots.forEach((b) => startBot(b));
