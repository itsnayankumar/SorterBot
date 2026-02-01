import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from utils.db import db
from config import user_sessions  # <--- Import from config
from utils.parser import get_season_episode

# ... (Rest of the file stays exactly the same) ...
# --- HELPER: Safe Sticker Sender ---
async def safe_send(client, chat_id, key):
    """
    Sends a sticker based on the key (e.g., '1', 'spam', 'end').
    If the specific season sticker is missing, it tries 'default'.
    """
    file_id = db.get_sticker(key)
    
    # Fallback to default if a numeric season sticker is missing
    if not file_id and str(key).isdigit():
        file_id = db.get_sticker("default")
    
    if file_id:
        try:
            await client.send_sticker(chat_id, file_id)
            await asyncio.sleep(0.5) # Visual delay
        except Exception as e:
            print(f"⚠️ Failed to send sticker '{key}': {e}")

# --- COMMAND: /dump ---
@Client.on_message(filters.command("dump") & filters.private)
async def pre_dump(client, message):
    user_id = message.from_user.id
    
    # Check if user has forwarded any files
    if not user_sessions.get(user_id, {}).get("files"):
        return await message.reply("❌ **No files found.**\nPlease forward files first.")

    files = user_sessions[user_id]["files"]
    await message.reply_text(f"⏳ **Analyzing {len(files)} files...**")

    # --- SORTING LOGIC ---
    season_map = {}
    for msg in files:
        # Determine filename from Document, Video, or Caption
        fname = msg.document.file_name if msg.document else (msg.video.file_name or msg.caption or "")
        
        # Parse Season & Episode
        season, episode, _ = get_season_episode(fname)
        
        if season not in season_map: 
            season_map[season] = []
        
        season_map[season].append({'msg': msg, 'ep': episode})

    # Save sorted map to session
    user_sessions[user_id]["map"] = season_map
    
    # Ask for confirmation
    await message.reply(
        f"✅ **Sorted into {len(season_map)} Seasons.**\nReady to dump?",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START DUMP", callback_data="go_dump")]])
    )

# --- CALLBACK: Start Dumping ---
@Client.on_callback_query(filters.regex("go_dump"))
async def start_dumping(client, callback):
    user_id = callback.from_user.id
    season_map = user_sessions[user_id]["map"]
    
    # Get Dump Channel from DB
    dump_ch = db.get("dump_channel")

    if not dump_ch: 
        return await callback.answer("❌ Set Dump Channel first via /settings!", show_alert=True)
    
    await callback.message.edit("🚀 **Dumping Started...**\n(This may take a while)")
    
    sorted_seasons = sorted(season_map.keys())

    # --- MAIN DUMP LOOP ---
    for season in sorted_seasons:
        # 1. HEADER SEQUENCE (Spam -> Season -> Spam)
        await safe_send(client, dump_ch, "spam")
        await safe_send(client, dump_ch, season)
        await safe_send(client, dump_ch, "spam")

        # 2. FILE DUMP SEQUENCE
        episodes = sorted(season_map[season], key=lambda x: x['ep'])
        
        for item in episodes:
            try:
                # .copy(chat_id) forwards the EXACT original file (caption + links included)
                await item['msg'].copy(dump_ch)
                await asyncio.sleep(2.5) # Sleep to avoid FloodWait
                
            except FloodWait as e:
                # If Telegram says "Slow Down", we wait exactly as long as it says
                print(f"⏳ FloodWait: Sleeping {e.value} seconds...")
                await asyncio.sleep(e.value)
                await item['msg'].copy(dump_ch)
            except Exception as e:
                print(f"❌ Error copying file: {e}")

    # 3. FOOTER SEQUENCE (Spam -> End -> Spam)
    # Only if an 'End' sticker is actually set
    if db.get_sticker("end"):
        await safe_send(client, dump_ch, "spam")
        await safe_send(client, dump_ch, "end")
        await safe_send(client, dump_ch, "spam")

    # --- STATS & CLEANUP ---
    total_dumped = sum(len(v) for v in season_map.values())
    
    # Update Web Dashboard Stats
    try:
        db.add_files_count(total_dumped)
    except Exception as e:
        print(f"Stats Error: {e}")

    await client.send_message(user_id, f"✅ **Batch Complete!**\n📈 **Stats:** Added +{total_dumped} files to database.")
    
    # Clear user session to free memory
    user_sessions.pop(user_id, None)

