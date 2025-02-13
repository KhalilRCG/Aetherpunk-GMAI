import logging
import os
from logging.handlers import RotatingFileHandler

class LoggingSystem:
    """Handles logging of game events, errors, and faction activities."""
    
    def __init__(self, log_file="aetherpunk.log", max_size=5*1024*1024, backup_count=3):
        """Initializes the logging system with log rotation."""
        self.log_file = log_file
        self.max_size = max_size  # Max log file size (5MB default)
        self.backup_count = backup_count  # Number of backup logs to keep
        self.setup_logger()

    def setup_logger(self):
        """Configures the logging system with log rotation."""
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        handler = RotatingFileHandler(self.log_file, maxBytes=self.max_size, backupCount=self.backup_count)
        handler.setFormatter(log_formatter)
        
        logging.basicConfig(level=logging.INFO, handlers=[handler])
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

    def display_logs(self, num_lines=20):
        """Reads and returns the last 'num_lines' log entries."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                logs = file.readlines()
                return logs[-num_lines:]
        return ["No logs available."]

if __name__ == "__main__":
    logger = LoggingSystem()
    logger.log_event("Player joined Syndicate X.")
    logger.log_faction_activity("Volthari Council", "Declared war on Pyronax Senate.")
    logger.log_error("Database connection lost.")
    print("\n".join(logger.display_logs()))
