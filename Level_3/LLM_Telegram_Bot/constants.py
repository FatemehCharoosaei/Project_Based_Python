from pathlib import Path
import os
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
WELCOME_MESSAGE = "👋 Hello! Welcome to Sara Bot! I'm here to help answer your questions."
WAITING_MESSAGE = "⏳ Processing your request..."
MAX_RESPONSE_LENGTH = 4000
LLM_MODEL = "deepseek-r1-distill-llama-70b"
BASE_SYSTEM_PROMPT = """You are a helpful AI assistant in a Telegram group chat.
Key guidelines:
- Provide concise, engaging responses
- Use appropriate emojis and markdown formatting
- Keep answers brief and to the point
- Be friendly and professional
- Use your general knowledge to answer questions
- Do not mention or advertise any specific websites, products, or services
- Focus on providing helpful information based on your training data
- Respond in a natural conversational style
- Use markdown formatting to make responses readable"""
SYSTEM_PROMPT = BASE_SYSTEM_PROMPT
REPLY_SYSTEM_PROMPT = BASE_SYSTEM_PROMPT + "\n\nAdditional response guideline from user: {reply_guideline}\n\nPlease incorporate this guideline in your response to the original message."
LIKE_EMOJI = "👍"
DISLIKE_EMOJI = "👎"
BOT_EMOJI = "🤖"
CRY_EMOJI = "😢"
QUESTION_EMOJI = "❓"
HEART_EMOJI = "❤️"
PILE_OF_POO_EMOJI = "💩"
THINKING_EMOJI = "🤔"
HIGH_VOLTAGE_EMOJI = "⚡"
DONT_ASK_TO_ASK_MESSAGE = "Please ask your specific question directly instead of asking if you can ask.\n\nInstead of: 'Can someone help me with Python?'\nAsk: 'How do I create a function in Python?'\n\nThis helps everyone provide better assistance."
REACTION_TRIGGERS = {
   HIGH_VOLTAGE_EMOJI: "generate_response",
   THINKING_EMOJI: "show_reminder",
   PILE_OF_POO_EMOJI: "delete_message"
}
def verify_configuration():
   essential_items = {
       "LOGS_DIR": LOGS_DIR.exists(),
       "BOT_TOKEN": "BOT_TOKEN" in os.environ
   }
   
   for item, status in essential_items.items():
       if not status:
           print(f"Configuration issue: {item}")
   
   return all(essential_items.values())
if __name__ == "__main__":
   config_status = verify_configuration()
   print(f"Configuration status: {'OK' if config_status else 'ISSUES'}")