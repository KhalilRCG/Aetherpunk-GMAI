const questLog = document.getElementById("quest-log");
const socket = new WebSocket("ws://localhost:8000/ws/quests");

socket.onopen = () => {
    console.log("Connected to quest WebSocket.");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.quest_update) {
        displayQuestUpdate(data.quest_update);
        showNotification("Quest Update", data.quest_update);
    }
};

socket.onclose = () => {
    console.log("Disconnected from quest WebSocket.");
};

function displayQuestUpdate(updateMessage) {
    const logEntry = document.createElement("div");
    logEntry.classList.add("quest-update");
    logEntry.innerText = updateMessage;
    logEntry.style.animation = "fadeIn 0.5s ease-in-out";
    questLog.prepend(logEntry);
}

function showNotification(title, message) {
    if (Notification.permission === "granted") {
        new Notification(title, { body: message });
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                new Notification(title, { body: message });
            }
        });
    }
}

// CSS Animations (to be added in a separate stylesheet or inside a <style> tag)
// @keyframes fadeIn {
//     from { opacity: 0; transform: translateY(-10px); }
//     to { opacity: 1; transform: translateY(0); }
// }
