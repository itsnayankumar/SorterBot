from pyrogram import Client, filters
from config import user_sessions  # <--- FIXED IMPORT

@Client.on_message((filters.document | filters.video | filters.audio) & filters.private)
async def collect_files(client, message):
    user_id = message.from_user.id
    
    # Only collect if session exists
    if user_id in user_sessions:
        user_sessions[user_id]["files"].append(message)
        
        total = len(user_sessions[user_id]["files"])
        # Reply with quote to acknowledge file
        await message.reply_text(f"✅ **Added.** Total: {total}", quote=True)
