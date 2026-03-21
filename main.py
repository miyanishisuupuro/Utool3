import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading
import requests
import time

from utils.data_manager import DataManager
from commands import reminder

# nest_asyncio.apply()  <-- 削除
load_dotenv()
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 10000))
SELF_URL = os.getenv("SELF_URL")
DATA_CHANNEL_ID = int(os.getenv("DATA_CHANNEL_ID", 0))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route("/")
def health(): 
    return "Bot is alive!"

def run_flask(): 
    app.run(host="0.0.0.0", port=PORT)

def keep_alive():
    """Renderのサーバーをスリープさせないためのセルフピン"""
    while True:
        try:
            if SELF_URL: 
                requests.get(SELF_URL)
        except: 
            pass
        time.sleep(300)

data_manager = DataManager(bot, DATA_CHANNEL_ID)

@bot.event
async def on_ready():
    await data_manager.load_files()
    
    # リマインダーコマンドとループの登録
    reminder.register_reminder_commands(bot, data_manager)

    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    # Flaskを別スレッドで起動 (RenderのPORT開放用)
    threading.Thread(target=run_flask, daemon=True).start()
    
    # セルフピンを別スレッドで起動
    if SELF_URL:
        threading.Thread(target=keep_alive, daemon=True).start()
    
    # メインスレッドでDiscord Botを起動
    bot.run(TOKEN)