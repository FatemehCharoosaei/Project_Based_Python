from groq import Groq
import os
def call_llm(prompt, model="llama-3.1-8b-instant"):
   try:
       api_key = os.getenv("GROQ_API_KEY")
       
       if not api_key:
           return "Error: GROQ_API_KEY environment variable is not set"
       
       client = Groq(api_key=api_key)
       
       response = client.chat.completions.create(
           model=model,
           messages=[
               {"role": "system", "content": "You are a fact-checking assistant. Analyze news and determine if they're fake or real based on available information."},
               {"role": "user", "content": prompt}
           ],
           temperature=0.1,
           max_tokens=1024
       )
       return response.choices[0].message.content
   except Exception as e:
       return f"Error: {str(e)}"
 
