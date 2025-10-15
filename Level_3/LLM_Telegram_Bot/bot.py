import os
import telebot
from dotenv import load_dotenv
from loguru import logger
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MARKDOWN")
# حذف این خط و انتقال به main
# BOT_USERNAME = bot.get_me().username
def get_bot_username():
   try:
       return bot.get_me().username
   except Exception as e:
       logger.error(f"Failed to get bot username: {e}")
       return None
BOT_USERNAME = get_bot_username()