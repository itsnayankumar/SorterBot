# 📂 Telegram Video Sorter Bot

<div align="center">

![Logo](https://via.placeholder.com/150?text=Sorter+Bot)

**The ultimate tool for organizing TV Show uploads on Telegram.**
*Takes a messy, shuffled batch of video files and forwards them to your channel in perfect Season & Episode order.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-Latest-orange?style=for-the-badge&logo=telegram&logoColor=white)](https://docs.pyrogram.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Status](https://img.shields.io/badge/Status-Maintained-green?style=for-the-badge)]()

</div>

---

## 🚀 Features

* **🧠 Smart Sorting:** Automatically detects `S01E01`, `1x01`, or `Episode 5` in filenames and sorts them perfectly.
* **📂 15-Season Support:** Handles massive shows with up to 15 seasons in one batch.
* **🎨 Aesthetic Dividers:** Automatically sends a "Spam/Divider" sticker *between* seasons to make your channel look clean.
* **⚙️ Admin Dashboard:** A full UI panel (`/settings`) to configure channels and stickers without touching code.
* **💾 Database Persistence:** Uses a JSON database so you never lose your settings after a restart.
* **📈 Web Dashboard:** Built-in web server with a status page (great for keeping the bot alive on Render/Heroku).
* **👥 Multi-User:** Authorize friends to use the bot via the dashboard.

---

## 🛠️ Commands

| Command | Description |
| :--- | :--- |
| `/start` | Check if the bot is online. |
| `/settings` | **(Owner Only)** Open the Admin Dashboard to set Channel, Stickers, and Users. |
| `/startbatch` | Start a new sorting session. Forward your files after this. |
| `/dump` | Finish the batch and start sending sorted files to the channel. |
| `/cancel` | Cancel any active setting operation. |

---

## ⚙️ Configuration

You can configure the bot using environment variables or a `.env` file.

### Required Variables
| Variable | Description |
| :--- | :--- |
| `API_ID` | Your Telegram API ID ([Get here](https://my.telegram.org)). |
| `API_HASH` | Your Telegram API Hash. |
| `BOT_TOKEN` | Bot Token from [@BotFather](https://t.me/BotFather). |
| `OWNER_ID` | Your Telegram User ID (The main admin). |

### Optional / Web
| Variable | Description |
| :--- | :--- |
| `BASE_URL` | Your website URL (e.g., `https://my-bot.onrender.com`). |
| `PORT` | Web server port (Default: `8080`). |

---

## 🚀 Deployment Guide

### Option 1: Deploy on Render (Recommended)

1.  **Fork this Repository** to your GitHub.
2.  Create a **New Web Service** on [Render](https://render.com).
3.  Connect your GitHub repo.
4.  **Environment:** Choose `Docker`.
5.  Add your Environment Variables (`API_ID`, `BOT_TOKEN`, etc.).
6.  Click **Deploy**.

### Option 2: Deploy on VPS (Docker)

The easiest way to run on a VPS is using Docker.

1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/YourUsername/SorterBot.git](https://github.com/YourUsername/SorterBot.git)
    cd SorterBot
    ```

2.  **Setup Config:**
    Rename `sample_config.env` to `.env` and fill in your details.
    ```bash
    mv sample_config.env .env
    nano .env
    ```

3.  **Build & Run:**
    ```bash
    docker build -t sorterbot .
    docker run -d --env-file .env -p 8080:8080 --name my_bot sorterbot
    ```

### Option 3: Local / VPS (Python)

1.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the Bot:
    ```bash
    python bot.py
    ```

---

## 📸 How It Works

1.  **Setup:** Send `/settings` to set your **Dump Channel** (e.g., `-100xxxx`) and add **Season Stickers**.
2.  **Start:** Send `/startbatch`.
3.  **Forward:** Forward 50+ mixed files (e.g., S1, S5, S2 files all shuffled).
4.  **Dump:** Send `/dump`.
5.  **Result:** The bot will analyze them, group them by season, and send them to your channel in this order:
    > [Spam Sticker]
    > [Season 1 Sticker]
    > [Spam Sticker]
    > *...Sorted Episode Files...*
    > [Spam Sticker]
    > [Season 2 Sticker]
    > ...

---

## 📂 Project Structure

```text
SorterBot/
├── bot.py               # Main Entry Point
├── config.py            # Configuration Manager
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker Setup
├── plugins/
│   ├── dumper.py        # Sorting Logic
│   ├── settings_ui.py   # Admin Dashboard
│   └── ...
└── utils/
    ├── db.py            # JSON Database
    └── parser.py        # File Name Analysis
    
