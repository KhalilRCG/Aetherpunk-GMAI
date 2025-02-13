# Aetherpunk GMAI

Aetherpunk GMAI is a **dynamic Game Master AI** designed for an immersive cyberpunk RPG experience. It integrates **real-time storytelling, faction diplomacy, player-driven quests, and adaptive AI responses** within the Aetherverse.

## Features

- **Real-time Quest Management**
  - Procedural quest generation based on player choices.
  - Dynamic event tracking with WebSocket support.
  
- **Faction System**
  - Reputation tracking with multiple factions.
  - Power struggles, alliances, betrayals, and takeovers.
  - Economic influence and territorial control.

- **NPC Interactions**
  - Dynamic dialogue and reaction systems.
  - NPC persuasion, alliances, and betrayals.

- **Database & Logging**
  - Persistent SQLite database for player, faction, and quest data.
  - Advanced logging for debugging and tracking game events.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/KhalilRCG/Aetherpunk-GMAI.git
   cd Aetherpunk-GMAI
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the AI Game Master:
   ```sh
   python main.py
   ```

## File Structure
```
Aetherpunk-GMAI/
│── gameplay/
│   ├── quest_manager.py
│   ├── faction_manager.py
│   ├── npc_manager.py
│── core/
│   ├── chatbot_ai.py
│   ├── time_manager.py
│── utils/
│   ├── database_handler.py
│   ├── logging_system.py
│── web/
│   ├── frontend_ui.py
│   ├── api_routes.py
│── tests/
│   ├── test_quest_manager.py
│   ├── test_faction_manager.py
│── README.md
│── requirements.txt
│── config.py
│── main.py
```

## API Endpoints

- **WebSocket Connection for Real-Time Updates**
  - `ws://localhost:8000/ws/quests` → Listens for quest updates.

- **Faction Management**
  - `GET /api/factions` → Retrieves faction data.
  - `POST /api/factions/update` → Modifies faction influence.

## Contributing

Pull requests are welcome! If you want to contribute, follow the standard **fork & PR process**.

## License

MIT License. See `LICENSE` for details.

## Contact

For inquiries or collaboration:
- GitHub: [@KhalilRCG](https://github.com/KhalilRCG)

