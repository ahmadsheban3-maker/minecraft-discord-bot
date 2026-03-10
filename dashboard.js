const express=require("express")
const http=require("http")
const {Server}=require("socket.io")

const app=express()
const server=http.createServer(app)
const io=new Server(server)

app.get("/",(req,res)=>{
res.sendFile(__dirname+"/dashboard.html")
})

setInterval(()=>{

const stats={
bots:3,
ping:Math.floor(Math.random()*120),
tps:(18+Math.random()*2).toFixed(2)
}

io.emit("stats",stats)

},3000)

server.listen(3000,()=>{
console.log("Dashboard running")
})