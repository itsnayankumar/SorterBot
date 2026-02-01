from pyrogram import Client, filters
from config import ADMINS

# Global Dictionary to store user files in memory
# Structure: { user_id: { "files": [], "map": {} } }
user_sessions = {}

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("👋 Hello! Use /startbatch to begin sorting files.")

@Client.on_message(filters.command("startbatch") & filters.private)
async def batch_handler(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return await message.reply("🔒 Admin only.")
    
    # Initialize session
    user_sessions[user_id] = {"files": [], "map": {}}
    await message.reply_text("📥 **Batch Active!** Forward your files now.")
