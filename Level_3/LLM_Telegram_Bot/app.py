import argparse
import sys
import os
import emoji
from loguru import logger
from bot import BOT_USERNAME, bot
from config import ADMINS_USERNAME
from constants import (
   DONT_ASK_TO_ASK_MESSAGE,
   HIGH_VOLTAGE_EMOJI,
   LLM_MODEL,
   PILE_OF_POO_EMOJI,
   REPLY_SYSTEM_PROMPT,
   SYSTEM_PROMPT,
   THINKING_EMOJI,
   WAITING_MESSAGE,
   WELCOME_MESSAGE,
)
from llm import call_llm
from telegram_utils import (
   get_message_content,
   is_bot_mentioned,
   send_telegram_message,
)
def configure_logger(verbose):
   log_level = "DEBUG" if verbose else "INFO"
   logger.remove()
   logger.add(sys.stderr, level=log_level)
   logger.add("logs/bot.log", rotation="100 MB", level="DEBUG")
   logger.info(f"Log level set to {log_level}")
def is_message_from_admins(message):
   if hasattr(message, "from_user"):
       username = message.from_user.username.lower()
   else:
       username = message.user.username.lower()
   return username in ADMINS_USERNAME
def is_message_reply_to_message(message):
   return message.reply_to_message is not None
def should_process_message(message):
   conditions = [
       is_bot_mentioned(message, BOT_USERNAME),
       is_message_reply_to_message(message),
       is_message_from_admins(message),
   ]
   logger.debug(f"Conditions: {conditions}")
   return all(conditions)
def should_process_reaction(message):
   conditions = [
       is_message_from_admins(message),
   ]
   logger.debug(f"Conditions: {conditions}")
   return all(conditions)
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
   send_telegram_message(
       bot, message.chat.id, WELCOME_MESSAGE, reply_to_message_id=message.id,
   )
@bot.message_handler(func=lambda message: True)
@bot.edited_message_handler(func=lambda message: True)
def handle_message(message):
   if should_process_message(message):
       process_message(message)
@bot.message_reaction_handler(func=lambda message: message.new_reaction)
def handle_reaction(message):
   if should_process_reaction(message):
       process_reaction(message)
def process_message(message):
   reply_to_message = message.reply_to_message
   message_text = get_message_content(message.chat.id, reply_to_message.message_id)
   waiting_message = send_telegram_message(
       bot, message.chat.id, WAITING_MESSAGE, reply_to_message_id=message.id,
   )
   reply_guideline = message.text.replace(f"@{BOT_USERNAME}", "")
   response = call_llm(
       message_text,
       LLM_MODEL,
       REPLY_SYSTEM_PROMPT.format(reply_guideline=reply_guideline),
   )
   send_llm_response(waiting_message, response)
def process_reaction(message):
   if not hasattr(message.new_reaction[-1], "emoji"):
       return
   reaction = emoji.demojize(message.new_reaction[-1].emoji)
   logger.debug(f"Reaction: {reaction}")
   if reaction in [HIGH_VOLTAGE_EMOJI]:
       message_text = get_message_content(message.chat.id, message.message_id)
       waiting_message = send_telegram_message(
           bot,
           message.chat.id,
           WAITING_MESSAGE,
           reply_to_message_id=message.message_id,
       )
       response = call_llm(message_text, LLM_MODEL, SYSTEM_PROMPT)
       send_llm_response(waiting_message, response)
   elif reaction in [THINKING_EMOJI]:
       send_telegram_message(
           bot,
           message.chat.id,
           DONT_ASK_TO_ASK_MESSAGE,
           reply_to_message_id=message.message_id,
       )
   elif reaction in [PILE_OF_POO_EMOJI]:
       bot.delete_message(message.chat.id, message.message_id)
def send_llm_response(message, response):
   send_telegram_message(bot, message.chat.id, response, edit_message_id=message.id)
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Telegram Bot")
   parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
   args = parser.parse_args()
   configure_logger(args.verbose)
   try:
       logger.info("Starting the bot...")
       bot.infinity_polling(
           allowed_updates=[
               "message",
               "message_reaction",
               "callback_query",
               "edited_message",
           ],
           skip_pending=True
       )
   except Exception as e:
       logger.exception(f"An error occurred: {e}")