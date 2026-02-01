from aiohttp import web
from utils.db import db
from config import PORT

async def handle_home(request):
    # Get live stats from Database
    data = db.data
    dump_ch = data.get("dump_channel", "Not Set")
    users = len(data.get("auth_users", []))
    files = data.get("total_files", 0)
    stickers = sum(1 for v in data['stickers'].values() if v)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SorterBot Status</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; background: #111; color: #fff; text-align: center; padding: 40px; }}
            .box {{ background: #222; padding: 20px; border-radius: 10px; margin: 10px auto; max-width: 300px; }}
            h1 {{ color: #4CAF50; }}
            .num {{ font-size: 24px; font-weight: bold; color: #2196F3; }}
        </style>
    </head>
    <body>
        <h1>🤖 Bot is Online</h1>
        <div class="box">
            <div class="num">{files}</div>
            <div>Files Sorted</div>
        </div>
        <div class="box">
            <div class="num">{users}</div>
            <div>Auth Users</div>
        </div>
        <p>Dump Channel: {dump_ch}</p>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_home)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌍 Web Server running on Port {PORT}")
