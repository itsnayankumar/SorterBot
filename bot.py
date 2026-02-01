import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from web.server import start_web_server  # Import the server

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
        print("✅ Bot Started on Telegram!")

    async def stop(self, *args):
        await super().stop()
        print("❌ Bot Stopped.")

async def main():
    # 1. Start Bot
    bot = SorterBot()
    await bot.start()

    # 2. Start Web Server
    await start_web_server()

    # 3. Keep running
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
