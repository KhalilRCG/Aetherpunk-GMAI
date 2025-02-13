import logging
import os

class LoggingSystem:
    """Handles logging of game events, errors, and faction activities."""
    def __init__(self, log_file="aetherpunk.log"):
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        """Configures the logging system."""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Logging system initialized.")

    def log_event(self, message):
        """Logs a general game event."""
        logging.info(message)
    
    def log_error(self, message):
        """Logs an error message."""
        logging.error(message)
    
    def log_faction_activity(self, faction, activity):
        """Logs a faction-related event."""
        logging.info(f"Faction {faction}: {activity}")

    def display_logs(self):
        """Reads and returns the last 20 log entries."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                logs = file.readlines()
                return logs[-20:]
        return ["No logs available."]

if __name__ == "__main__":
    logger = LoggingSystem()
    logger.log_event("Player joined Syndicate X.")
    logger.log_faction_activity("Volthari Council", "Declared war on Pyronax Senate.")
    logger.log_error("Database connection lost.")
    print("\n".join(logger.display_logs()))
