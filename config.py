import os
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

class Config:
    """Configuration settings for Aetherpunk GMAI."""
    
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aetherpunk.db")
    LOG_FILE = os.getenv("LOG_FILE", "aetherpunk.log")
    WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8000))
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "yes")

if __name__ == "__main__":
    print("Configuration Loaded:")
    print(f"DATABASE_URL: {Config.DATABASE_URL}")
    print(f"LOG_FILE: {Config.LOG_FILE}")
    print(f"WEBSOCKET_PORT: {Config.WEBSOCKET_PORT}")
    print(f"DEBUG_MODE: {Config.DEBUG_MODE}")
