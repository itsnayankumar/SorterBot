from aiohttp import web
from utils.db import db
import os

# Render gives a PORT env variable. Default to 8080 if not found.
PORT = int(os.environ.get("PORT", 8080))

async def handle_home(request):
    # Get live stats
    data = db.data
    dump_ch = data.get("dump_channel", "Not Set")
    users = len(data.get("auth_users", []))
    files = data.get("total_files", 0)
    stickers = sum(1 for v in data['stickers'].values() if v)

    # Simple HTML Dashboard
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SorterBot Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; background: #1e1e1e; color: #fff; text-align: center; padding: 50px; }}
            .card {{ background: #2d2d2d; padding: 20px; margin: 10px auto; width: 80%; max-width: 400px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
            h1 {{ color: #4CAF50; }}
            .stat {{ font-size: 24px; font-weight: bold; color: #64b5f6; }}
            .label {{ color: #aaa; font-size: 14px; }}
        </style>
    </head>
    <body>
        <h1>🤖 SorterBot is Running</h1>
        <div class="card">
            <div class="stat">{files}</div>
            <div class="label">Total Files Sorted</div>
        </div>
        <div class="card">
            <div class="stat">{users}</div>
            <div class="label">Authorized Users</div>
        </div>
        <div class="card">
            <div class="stat">{stickers}/18</div>
            <div class="label">Stickers Configured</div>
        </div>
        <div class="card">
            <div class="label">Target Channel</div>
            <div style="margin-top:5px; font-family:monospace;">{dump_ch}</div>
        </div>
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
    print(f"🌍 Web Server running on port {PORT}")
