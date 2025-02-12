// Establish WebSocket connection for multiplayer chat
let ws = new WebSocket("https://aetherpunk-gmai.onrender.com");

ws.onmessage = function(event) {
    document.getElementById("chatOutput").innerText = event.data;
};

function sendMessage() {
    let message = document.getElementById("chatInput").value;
    ws.send(message);
}

// API Calls
function generateCity() {
    fetch("/city/build/player123", { method: "POST" })
        .then(response => response.json())
        .then(data => document.getElementById("cityOutput").innerText = data.city);
}

function generateQuest() {
    fetch("/quest/player123", { method: "POST" })
        .then(response => response.json())
        .then(data => document.getElementById("questOutput").innerText = data.quest);
}

function generateHeist() {
    fetch("/heist/generate/player123", { method: "POST" })
        .then(response => response.json())
        .then(data => document.getElementById("heistOutput").innerText = data.heist);
}

function tradeWeapons() {
    fetch("/black-market/trade/weapons/10", { method: "POST" })
        .then(response => response.json())
        .then(data => document.getElementById("marketOutput").innerText = "Trade Value: " + data.value);
}

function startFactionWar() {
    fetch("/factions/war/Red Talons/Obsidian Circuit", { method: "POST" })
        .then(response => response.json())
        .then(data => document.getElementById("warOutput").innerText = data);
}
