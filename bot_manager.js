const mineflayer = require("mineflayer")
const fs = require("fs")

const server = JSON.parse(fs.readFileSync("servers.json"))
const botsConfig = JSON.parse(fs.readFileSync("bots.json"))

function startBot(username){

const bot = mineflayer.createBot({
host: server.host,
port: server.port,
username: username
})

bot.on("login", ()=>{
console.log(username + " joined server")
})

bot.on("spawn", ()=>{

setInterval(()=>{

bot.setControlState("jump", true)

setTimeout(()=>{

bot.setControlState("jump", false)

},500)

},30000)

})

bot.on("chat",(user,msg)=>{

if(user===bot.username) return

fs.writeFileSync("mc_chat.txt",user+": "+msg)

})

bot.on("end",()=>{

console.log(username+" reconnecting")

setTimeout(()=>startBot(username),5000)

})

bot.on("error",console.log)

}

botsConfig.bots.forEach(startBot)