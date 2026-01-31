from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

class SorterBot(Client):
    def __init__(self):
        super().__init__(
            "my_sorter_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins") # This loads everything in /plugins folder
        )

    async def start(self):
        await super().start()
        print("✅ Bot is Online and Ready to Sort!")

    async def stop(self, *args):
        await super().stop()
        print("❌ Bot Stopped.")

if __name__ == "__main__":
    app = SorterBot()
    app.run()
  
