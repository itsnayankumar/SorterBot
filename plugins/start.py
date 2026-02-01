from pyrogram import Client, filters
from config import OWNER_ID, user_sessions  # <--- FIXED IMPORT
from utils.db import db

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("👋 **Sorter Bot Online.**\n\nCommands:\n/settings - Configure Bot\n/startbatch - Start Sorting")

@Client.on_message(filters.command("startbatch") & filters.private)
async def batch_handler(client, message):
    user_id = message.from_user.id
    
    # Check Database for Auth
    auth_list = db.get("auth_users") or []
    if user_id != OWNER_ID and user_id not in auth_list:
        return await message.reply("🔒 **Access Denied.**")
    
    # Initialize Session
    user_sessions[user_id] = {"files": [], "map": {}}
    await message.reply_text("📥 **Batch Active!** Forward your files now.")
