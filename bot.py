import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from web.server import start_web_server # Import your new server

class SorterBot(Client):
    def __init__(self):
        super().__init__(
            "my_sorter_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("✅ Bot is Online!")

    async def stop(self, *args):
        await super().stop()
        print("❌ Bot Stopped.")

async def main():
    # 1. Start the Bot
    bot = SorterBot()
    await bot.start()

    # 2. Start the Web Server (Render needs this)
    await start_web_server()

    # 3. Keep running until stopped
    await idle()
    await bot.stop()

if __name__ == "__main__":
    # Run the main async loop
    asyncio.run(main())

