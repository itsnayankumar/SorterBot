import os
from dotenv import load_dotenv

load_dotenv("config.env")

# --- CREDENTIALS ---
API_ID = int(os.getenv("API_ID", "12345678"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

# --- WEB CONFIG ---
PORT = int(os.getenv("PORT", "8080"))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

# --- MEMORY STORAGE (Add this at the bottom) ---
# This fixes the import errors by keeping memory here
user_sessions = {}
