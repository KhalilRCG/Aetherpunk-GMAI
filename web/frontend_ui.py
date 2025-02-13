const questLog = document.getElementById("quest-log");
const socket = new WebSocket("ws://localhost:8000/ws/quests");

socket.onopen = () => {
    console.log("Connected to quest WebSocket.");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.quest_update) {
        displayQuestUpdate(data.quest_update);
    }
};

socket.onclose = () => {
    console.log("Disconnected from quest WebSocket.");
};

function displayQuestUpdate(updateMessage) {
    const logEntry = document.createElement("div");
    logEntry.classList.add("quest-update");
    logEntry.innerText = updateMessage;
    questLog.prepend(logEntry);
}
