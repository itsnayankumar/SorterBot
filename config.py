import os
from dotenv import load_dotenv

# Load variables from config.env (for local testing)
load_dotenv("config.env")

# --- CREDENTIALS ---
# We use os.getenv to read from Render, or use defaults for local
# Replace the "1234..." strings with your actual keys if you want to run locally without a .env file

API_ID = int(os.getenv("API_ID", "12345678"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

# --- WEB CONFIG ---
# Render sets PORT automatically
PORT = int(os.getenv("PORT", "8080"))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
