import os
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv("config.env")

# --- CREDENTIALS ---
# We use os.getenv so it works on Render automatically
API_ID = int(os.getenv("API_ID", "12345678")) 
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

# --- WEB CONFIG ---
PORT = int(os.getenv("PORT", "8080"))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

# --- MEMORY STORAGE ---
# We keep this here to prevent "Circular Import" errors.
# This is where the bot remembers who is sorting files.
user_sessions = {}
