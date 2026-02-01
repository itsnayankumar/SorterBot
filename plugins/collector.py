from pyrogram import Client, filters
from plugins.start import user_sessions # Import the session dict

@Client.on_message((filters.document | filters.video) & filters.private)
async def collect_files(client, message):
    user_id = message.from_user.id
    
    # Only collect if a session exists
    if user_id in user_sessions:
        user_sessions[user_id]["files"].append(message)
