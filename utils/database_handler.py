import sqlite3
import logging
from utils.logging_system import LoggingSystem

class DatabaseHandler:
    """Handles database interactions for player data, factions, quests, and game states."""
    
    def __init__(self, db_name="aetherpunk.db"):
        self.db_name = db_name
        self.logger = LoggingSystem()  # Initialize logging
        self.conn = None
        self.cursor = None
        self.connect_db()
        self.setup_database()

    def connect_db(self):
        """Establishes a database connection."""
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.logger.log_event("Connected to database successfully.")
        except sqlite3.Error as e:
            self.logger.log_error(f"Database connection error: {e}")

    def setup_database(self):
        """Creates necessary tables if they do not exist."""
        try:
            with self.conn:
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
            self.logger.log_event("Database tables ensured.")
        except sqlite3.Error as e:
            self.logger.log_error(f"Error setting up database tables: {e}")

    def add_player(self, name, reputation=0, credits=1000):
        """Adds a new player to the database."""
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO players (name, reputation, credits) VALUES (?, ?, ?)", 
                                    (name, reputation, credits))
            self.logger.log_event(f"Player {name} added to database.")
        except sqlite3.IntegrityError:
            self.logger.log_error(f"Failed to add player {name}: Player already exists.")
        except sqlite3.Error as e:
            self.logger.log_error(f"Database error while adding player: {e}")

    def update_player_reputation(self, name, change):
        """Updates player reputation."""
        try:
            with self.conn:
                self.cursor.execute("UPDATE players SET reputation = reputation + ? WHERE name = ?", 
                                    (change, name))
            self.logger.log_event(f"Updated reputation for {name} by {change}.")
        except sqlite3.Error as e:
            self.logger.log_error(f"Error updating player reputation: {e}")

    def update_faction_influence(self, faction_name, change):
        """Modifies faction influence dynamically."""
        try:
            with self.conn:
                self.cursor.execute("UPDATE factions SET influence = influence + ? WHERE name = ?", 
                                    (change, faction_name))
            self.logger.log_event(f"Updated influence for {faction_name} by {change}.")
        except sqlite3.Error as e:
            self.logger.log_error(f"Error updating faction influence: {e}")

    def add_quest(self, player_id, quest_name, status="Active"):
        """Logs a new quest for a player."""
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO quests (player_id, quest_name, status) VALUES (?, ?, ?)", 
                                    (player_id, quest_name, status))
            self.logger.log_event(f"Quest '{quest_name}' assigned to player ID {player_id}.")
        except sqlite3.Error as e:
            self.logger.log_error(f"Error adding quest: {e}")

    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            self.logger.log_event("Database connection closed.")

if __name__ == "__main__":
    db = DatabaseHandler()
    db.add_player("CyberMerc")
    db.update_player_reputation("CyberMerc", 10)
    db.update_faction_influence("Syndicate X", -5)
    db.add_quest(1, "Steal Corporate Data")
    db.close_connection()
