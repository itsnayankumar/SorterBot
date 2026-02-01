from pyrogram import Client, filters
from utils.session import user_sessions  # <--- UPDATED IMPORT

@Client.on_message((filters.document | filters.video | filters.audio) & filters.private)
async def collect_files(client, message):
    user_id = message.from_user.id
    
    # Only collect if a batch session exists
    if user_id in user_sessions:
        user_sessions[user_id]["files"].append(message)
        
        # Show status update
        total = len(user_sessions[user_id]["files"])
        await message.reply_text(f"✅ **Received:** {total} files so far...", quote=True)
