from pyrogram import Client, filters
from config import OWNER_ID  # <--- Changed from ADMINS to OWNER_ID
from utils.db import db

# Global session storage
user_sessions = {}

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("👋 **Sorter Bot Online.**\n\nCommands:\n/settings - Configure Bot\n/startbatch - Start Sorting")

@Client.on_message(filters.command("startbatch") & filters.private)
async def batch_handler(client, message):
    user_id = message.from_user.id
    
    # Logic: Allow if user is the Owner OR is in the Authorized Users list in Database
    auth_list = db.get("auth_users") or []
    
    if user_id != OWNER_ID and user_id not in auth_list:
        return await message.reply("🔒 **Access Denied.** You are not authorized to use this bot.")
    
    # Initialize session
    user_sessions[user_id] = {"files": [], "map": {}}
    await message.reply_text("📥 **Batch Active!** Forward your files now.")
