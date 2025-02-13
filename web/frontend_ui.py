const questLog = document.getElementById("quest-log");
const mapContainer = document.getElementById("quest-map");
const socket = new WebSocket("ws://localhost:8000/ws/quests");

socket.onopen = () => {
    console.log("Connected to quest WebSocket.");
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

function displayQuestChoices(choices, npcReactions, npcPersuasion) {
    const choiceContainer = document.createElement("div");
    choiceContainer.id = "quest-choices";
    choiceContainer.innerHTML = "<h3>Make a Choice:</h3>";
    
    choices.forEach(choice => {
        let choiceButton = document.createElement("button");
        choiceButton.innerText = choice.text;
        choiceButton.onclick = () => sendPlayerChoice(choice.value);
        choiceButton.classList.add("major-choice"); // Highlight major choices visually
        choiceContainer.appendChild(choiceButton);
        
        if (npcReactions && npcReactions[choice.value]) {
            let npcReaction = document.createElement("p");
            npcReaction.innerText = `NPC Reaction: ${npcReactions[choice.value]}`;
            npcReaction.classList.add("npc-reaction");
            choiceContainer.appendChild(npcReaction);
        }
        
        if (npcPersuasion && npcPersuasion[choice.value]) {
            let npcPersuade = document.createElement("p");
            npcPersuade.innerText = `NPC Persuasion: ${npcPersuasion[choice.value]}`;
            npcPersuade.classList.add("npc-persuasion");
            choiceContainer.appendChild(npcPersuade);
        }
    });
    
    document.body.appendChild(choiceContainer);
}

function sendPlayerChoice(choiceValue) {
    socket.send(JSON.stringify({ action: "player_choice", choice: choiceValue }));
}

function updateMapLocation(locationData) {
    if (!mapContainer) return;
    mapContainer.innerHTML = `<p>Current Quest Location: ${locationData}</p>`;
}

// CSS for visual indicators (to be added in a stylesheet or inside a <style> tag)
// .major-choice {
//     background-color: #ffcc00;
//     border: 2px solid #ff9900;
//     font-weight: bold;
//     transition: transform 0.2s ease-in-out;
// }
// .major-choice:hover {
//     transform: scale(1.1);
// }
// .npc-reaction {
//     font-style: italic;
//     color: #ccc;
//     margin-left: 10px;
// }
// .npc-persuasion {
//     font-style: italic;
//     color: #ff6666;
//     font-weight: bold;
//     margin-left: 10px;
// }
