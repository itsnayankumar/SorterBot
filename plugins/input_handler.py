from pyrogram import Client, filters
from plugins.settings_ui import user_states, open_settings
from utils.db import db
from config import OWNER_ID

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_action(client, message):
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
        await message.reply("❌ Action Cancelled.")
        await open_settings(client, message)

# --- CAPTURE TEXT (For Channel IDs) ---
@Client.on_message(filters.text & filters.private & filters.user(OWNER_ID))
async def handle_text_input(client, message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state: return

    if state == "waiting_dump":
        try:
            ch_id = int(message.text)
            db.set("dump_channel", ch_id)
            await message.reply(f"✅ **Dump Channel Set:** `{ch_id}`")
        except ValueError:
            await message.reply("❌ Invalid ID. It must be a number (e.g., -10012345).")
        
        del user_states[user_id]
        await open_settings(client, message)

# --- CAPTURE STICKERS ---
@Client.on_message(filters.sticker & filters.private & filters.user(OWNER_ID))
async def handle_sticker_input(client, message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state or not state.startswith("waiting_sticker_"): return

    # Extract season key (1, 2, default, etc)
    season_key = state.split("_")[2]
    file_id = message.sticker.file_id

    db.set_sticker(season_key, file_id)
    
    await message.reply(f"✅ **Sticker Saved for:** `{season_key}`")
    
    del user_states[user_id]
    await open_settings(client, message)
