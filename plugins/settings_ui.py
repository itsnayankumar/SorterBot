from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID
from utils.db import db

user_states = {}

@Client.on_message(filters.command("settings") & filters.user(OWNER_ID))
async def open_settings(client, message):
    data = db.data
    dump_ch = data.get('dump_channel', 0)
    
    # Count how many are set
    set_count = sum(1 for v in data['stickers'].values() if v)
    
    text = (
        "⚙️ **Bot Settings Dashboard**\n\n"
        f"📢 **Dump Channel:** `{dump_ch}`\n"
        f"🎭 **Stickers Configured:** `{set_count}/18`\n"
        f"🌀 **Spam Mode:** Active"
    )

    buttons = [
        [InlineKeyboardButton("📢 Set Dump Channel", callback_data="set_dump")],
        [InlineKeyboardButton("🎭 Configure Stickers (1-15)", callback_data="menu_stickers")],
        [InlineKeyboardButton("🌀 Set SPAM Sticker", callback_data="set_st_spam")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# --- STICKER MENU (15 SEASONS) ---
@Client.on_callback_query(filters.regex("menu_stickers"))
async def sticker_menu(client, callback):
    # Create a grid of buttons for Seasons 1-15
    buttons = []
    row = []
    for i in range(1, 16):
        # Mark with ✅ if set
        is_set = "✅" if db.get_sticker(i) else ""
        btn_text = f"S{i} {is_set}"
        row.append(InlineKeyboardButton(btn_text, callback_data=f"set_st_{i}"))
        
        # 4 buttons per row
        if len(row) == 4:
            buttons.append(row)
            row = []
    
    if row: buttons.append(row) # Add leftovers

    # Add Default and End buttons at the bottom
    buttons.append([
        InlineKeyboardButton("Default", callback_data="set_st_default"),
        InlineKeyboardButton("End Sticker", callback_data="set_st_end")
    ])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="main_menu")])

    await callback.message.edit("🎭 **Select a Season to Set:**", reply_markup=InlineKeyboardMarkup(buttons))

# --- HANDLE BUTTON CLICKS ---
@Client.on_callback_query()
async def callback_handler(client, callback: CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data == "close":
        await callback.message.delete()
        return
    
    if data == "main_menu":
        await open_settings(client, callback.message)
        return

    # SET DUMP CHANNEL
    if data == "set_dump":
        user_states[user_id] = "waiting_dump"
        await callback.message.edit("📢 **Send Channel ID:**")
        return

    # SET STICKERS (Handles 1-15, default, end, spam)
    if data.startswith("set_st_"):
        key = data.split("_")[2] # "1", "15", "spam"
        user_states[user_id] = f"waiting_sticker_{key}"
        await callback.message.edit(f"🎭 **Send the Sticker for '{key.upper()}'**\n\n(Forward it here)")

