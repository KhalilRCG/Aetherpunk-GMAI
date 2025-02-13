const questLog = document.getElementById("quest-log");
const mapContainer = document.getElementById("quest-map");
const socket = new WebSocket("ws://localhost:8000/ws/quests");

socket.onopen = () => {
    console.log("Connected to quest WebSocket.");
    showNotification("Connected", "You are now receiving quest updates.");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.quest_update) {
        displayQuestUpdate(data.quest_update);
        showNotification("Quest Update", data.quest_update);
        updateQuestProgress(data.quest_progress);
        updateMapLocation(data.quest_location);
    }
    if (data.quest_choices) {
        displayQuestChoices(data.quest_choices, data.npc_reactions, data.npc_persuasion);
    }
};

socket.onclose = () => {
    console.log("Disconnected from quest WebSocket.");
    showNotification("Disconnected", "WebSocket connection lost.", true);
};

function displayQuestUpdate(updateMessage) {
    const logEntry = document.createElement("div");
    logEntry.classList.add("quest-update");
    logEntry.innerText = updateMessage;
    logEntry.style.animation = "fadeIn 0.5s ease-in-out";
    questLog.prepend(logEntry);
}

function showNotification(title, message, error = false) {
    const notification = document.createElement("div");
    notification.classList.add("notification");
    if (error) {
        notification.classList.add("error");
    }
    notification.innerText = `${title}: ${message}`;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

function updateQuestProgress(progressData) {
    let progressBar = document.getElementById("quest-progress");
    if (!progressBar) {
        progressBar = document.createElement("div");
        progressBar.id = "quest-progress";
        progressBar.style.width = "100%";
        progressBar.style.background = "#444";
        progressBar.style.borderRadius = "5px";
        progressBar.style.marginTop = "10px";
        let innerBar = document.createElement("div");
        innerBar.id = "progress-inner";
        innerBar.style.height = "10px";
        innerBar.style.width = "0%";
        innerBar.style.background = "#00ff00";
        innerBar.style.borderRadius = "5px";
        progressBar.appendChild(innerBar);
        document.body.appendChild(progressBar);
    }
    
    document.getElementById("progress-inner").style.width = progressData + "%";
}

function updateMapLocation(locationData) {
    if (!mapContainer) return;
    mapContainer.innerHTML = `<p>Current Quest Location: ${locationData}</p>`;
}
