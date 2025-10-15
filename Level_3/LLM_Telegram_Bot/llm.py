import os
from groq import Groq
from loguru import logger
# Make sure this is your actual Groq API key, not the placeholder
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def call_llm(prompt, model="qwen/qwen3-32b", system_prompt="You are a helpful assistant."):
   try:
       response = client.chat.completions.create(
           model=model,
           messages=[
               {
                   "role": "system",
                   "content": system_prompt
               },
               {
                   "role": "user",
                   "content": prompt
               }
           ],
           temperature=0.7,
           max_tokens=1024,
           top_p=1,
           stream=False
       )
       return response.choices[0].message.content
       
   except Exception as e:
       logger.error(f"Groq API error: {e}")
       return "Sorry, there was an error processing your question. Please try again."
