<!DOCTYPE html>
<html lang="en">
<head>
    <title>Aetherpunk RPG - Game Master AI</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body {
            background-color: black;
            color: #00FF00;
            font-family: "Courier New", monospace;
            text-align: center;
            padding: 50px;
        }
        h1 {
            font-size: 36px;
        }
        input, button {
            font-size: 20px;
            padding: 10px;
            margin: 10px;
            background-color: black;
            color: #00FF00;
            border: 2px solid #00FF00;
        }
        input {
            width: 50%;
        }
        #response {
            font-size: 22px;
            line-height: 1.5;
            max-width: 75%;
            margin: auto;
        }
    </style>
</head>
<body>
    <h1>Aetherpunk RPG - Game Master AI</h1>
    <input id="playerInput" type="text" placeholder="Type here..." onkeypress="handleKeyPress(event)"/>
    <button onclick="sendAction()">Submit</button>
    <div id="response">🚀 Welcome to the Aetherverse. Type **new game** to begin.</div>

    <script>
        var socket = io("https://aetherpunk-gmai.onrender.com");
        var allowInput = true;

        function sendAction() { 
            if (!allowInput) return;
            allowInput = false;

            var action = document.getElementById("playerInput").value.trim();
            if (action !== "") {
                socket.emit("chat_message", { message: action });
                document.getElementById("playerInput").value = "";
            }

            setTimeout(() => { allowInput = true; }, 1000);
        }

        function handleKeyPress(event) {
            if (event.key === "Enter") {
                sendAction();
            }
        }

        socket.on("game_response", function(data) {
            document.getElementById("response").innerText = data.response;
        });
    </script>
</body>
</html>
