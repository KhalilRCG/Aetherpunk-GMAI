import sqlite3

class DatabaseHandler:
    """Handles database interactions for player data, factions, quests, and game states."""
    def __init__(self, db_name="aetherpunk.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        """Creates necessary tables if they do not exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT UNIQUE,
                               reputation INTEGER,
                               credits INTEGER)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS factions (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT UNIQUE,
                               influence INTEGER,
                               reputation INTEGER,
                               economy INTEGER)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS quests (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               player_id INTEGER,
                               quest_name TEXT,
                               status TEXT,
                               FOREIGN KEY(player_id) REFERENCES players(id))''')
        
        self.conn.commit()
    
    def add_player(self, name, reputation=0, credits=1000):
        """Adds a new player to the database."""
        self.cursor.execute("INSERT INTO players (name, reputation, credits) VALUES (?, ?, ?)", (name, reputation, credits))
        self.conn.commit()
    
    def update_player_reputation(self, name, change):
        """Updates player reputation."""
        self.cursor.execute("UPDATE players SET reputation = reputation + ? WHERE name = ?", (change, name))
        self.conn.commit()
    
    def update_faction_influence(self, faction_name, change):
        """Modifies faction influence dynamically."""
        self.cursor.execute("UPDATE factions SET influence = influence + ? WHERE name = ?", (change, faction_name))
        self.conn.commit()
    
    def add_quest(self, player_id, quest_name, status="Active"):
        """Logs a new quest for a player."""
        self.cursor.execute("INSERT INTO quests (player_id, quest_name, status) VALUES (?, ?, ?)", (player_id, quest_name, status))
        self.conn.commit()
    
    def close_connection(self):
        """Closes the database connection."""
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseHandler()
    db.add_player("CyberMerc")
    db.update_player_reputation("CyberMerc", 10)
    db.update_faction_influence("Syndicate X", -5)
    db.add_quest(1, "Steal Corporate Data")
    db.close_connection()
