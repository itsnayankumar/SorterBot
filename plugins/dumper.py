import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from utils.db import db
from config import user_sessions  # <--- FIXED IMPORT
from utils.parser import get_season_episode

# ... (Keep your safe_send function here) ...
async def safe_send(client, chat_id, key):
    file_id = db.get_sticker(key)
    if not file_id and str(key).isdigit():
        file_id = db.get_sticker("default")
    if file_id:
        try:
            await client.send_sticker(chat_id, file_id)
            await asyncio.sleep(0.5)
        except: pass

@Client.on_message(filters.command("dump") & filters.private)
async def pre_dump(client, message):
    user_id = message.from_user.id
    if not user_sessions.get(user_id, {}).get("files"):
        return await message.reply("❌ No files found.")

    files = user_sessions[user_id]["files"]
    await message.reply_text(f"⏳ Analyzing {len(files)} files...")

    season_map = {}
    for msg in files:
        fname = msg.document.file_name if msg.document else (msg.video.file_name or msg.caption or "")
        season, episode, _ = get_season_episode(fname)
        if season not in season_map: season_map[season] = []
        season_map[season].append({'msg': msg, 'ep': episode})

    user_sessions[user_id]["map"] = season_map
    await message.reply(
        f"✅ Sorted {len(season_map)} Seasons.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START DUMP", callback_data="go_dump")]])
    )

@Client.on_callback_query(filters.regex("go_dump"))
async def start_dumping(client, callback):
    user_id = callback.from_user.id
    season_map = user_sessions[user_id]["map"]
    dump_ch = db.get("dump_channel")

    if not dump_ch: return await callback.answer("❌ Set Dump Channel first!", show_alert=True)
    
    await callback.message.edit("🚀 **Dumping Original Files...**")
    
    sorted_seasons = sorted(season_map.keys())

    for season in sorted_seasons:
        # Headers
        await safe_send(client, dump_ch, "spam")
        await safe_send(client, dump_ch, season)
        await safe_send(client, dump_ch, "spam")

        # Files
        episodes = sorted(season_map[season], key=lambda x: x['ep'])
        for item in episodes:
            try:
                # COPY EXACT FILE
                await item['msg'].copy(dump_ch)
                await asyncio.sleep(2.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await item['msg'].copy(dump_ch)

    # Footers
    if db.get_sticker("end"):
        await safe_send(client, dump_ch, "spam")
        await safe_send(client, dump_ch, "end")
        await safe_send(client, dump_ch, "spam")

    # Update Stats
    try:
        total = sum(len(v) for v in season_map.values())
        # Manual DB update for stats if you haven't added the helper method yet
        db.data["total_files"] = db.data.get("total_files", 0) + total
        db.save()
    except: pass

    await client.send_message(user_id, "✅ **Batch Complete!**")
    user_sessions.pop(user_id, None)
