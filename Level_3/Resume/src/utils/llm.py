import streamlit as st
from groq import Groq
import json
import re
import os
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)
groq_api_key = os.getenv("Groq_API_Key")
if not groq_api_key:
   st.error("Groq API Key not found")
   client = None
else:
   client = Groq(api_key=groq_api_key)
def extract_json(content):
   if not content:
       return "{}"
   
   content = re.sub(r'```json\s*', '', content)
   content = re.sub(r'```\s*', '', content)
   content = content.replace('`', '')
   
   start_idx = content.find('{')
   end_idx = content.rfind('}')
   
   if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
       json_content = content[start_idx:end_idx+1]
   else:
       json_content = content.strip()
   
   json_content = re.sub(r',\s*}', '}', json_content)
   json_content = re.sub(r',\s*]', ']', json_content)
   
   return json_content
def safe_json_load(content):
   if not content:
       return {}
   
   try:
       return json.loads(content)
   except json.JSONDecodeError as e:
       st.warning(f"JSON decode error: {e}")
       return {}
def call_groq_api(prompt, model="llama-3.1-8b-instant"):
   if client is None:
       return ""
   
   try:
       valid_models = ["llama-3.1-8b-instant", "qwen/qwen3-32b", "openai/gpt-oss-120b"]
       if model not in valid_models:
           model = "llama-3.1-8b-instant"
       
       system_message = """You are an expert resume analyst. Return only valid JSON format.
Always use this structure for reviews:
{
 "section_name": {
   "impact_level": "High/Medium/Low",
   "revised_content": "improved text",
   "revision_suggestion": ["suggestion1", "suggestion2"]
 }
}"""
       
       response = client.chat.completions.create(
           model=model,
           messages=[
               {"role": "system", "content": system_message},
               {"role": "user", "content": prompt}
           ],
           temperature=0.1,
           max_tokens=4000
       )
       return response.choices[0].message.content
       
   except Exception as e:
       st.error(f"API Error: {str(e)}")
       return ""
def parse_resume(resume_text):
   if not resume_text or len(resume_text.strip()) < 50:
       return "{}"
   
   if len(resume_text) > 8000:
       resume_text = resume_text[:8000]
   
   prompt = f"""
Parse this resume into JSON format:
{resume_text}
Return JSON with this exact structure:
{{
 "personal_info": {{
   "name": "value",
   "email": "value",
   "phone": "value",
   "location": "value"
 }},
 "summary": "value",
 "work_experience": [
   {{
     "company": "value",
     "title": "value",
     "start_date": "value",
     "end_date": "value",
     "description": "value"
   }}
 ],
 "education": [
   {{
     "institution": "value",
     "degree": "value",
     "field": "value",
     "year": "value"
   }}
 ],
 "skills": ["skill1", "skill2"],
 "certifications": [
   {{
     "name": "value",
     "issuer": "value",
     "year": "value"
   }}
 ]
}}
Return only JSON.
"""
   response = call_groq_api(prompt, model="llama-3.1-8b-instant")
   return extract_json(response) if response else "{}"
def review_resume(resume_json, job_description=None):
   if not resume_json or resume_json == "{}":
       return "{}"
   
   try:
       resume_data = safe_json_load(resume_json)
       if not resume_data:
           return "{}"
   except:
       return "{}"
   
   base_prompt = f"""
Analyze this resume JSON and provide improvement suggestions in JSON format.
RESUME DATA:
{json.dumps(resume_data, indent=2)}
"""
   if job_description:
       if len(job_description) > 2000:
           job_description = job_description[:2000]
           
       prompt = base_prompt + f"""
JOB DESCRIPTION:
{job_description}
Provide feedback for each section with this JSON structure:
{{
 "section_name": {{
   "impact_level": "High/Medium/Low",
   "revised_content": "improved content here",
   "revision_suggestion": ["specific suggestion 1", "specific suggestion 2"]
 }}
}}
Focus on these sections: summary, work_experience, education, skills.
Return only JSON.
"""
   else:
       prompt = base_prompt + """
Provide general improvement suggestions with this JSON structure:
{
 "section_name": {
   "impact_level": "High/Medium/Low",
   "revised_content": "improved content here",
   "revision_suggestion": ["specific suggestion 1", "specific suggestion 2"]
 }
}
Focus on these sections: summary, work_experience, education, skills.
Return only JSON.
"""
   
   models_to_try = ["llama-3.1-8b-instant", "qwen/qwen3-32b", "openai/gpt-oss-120b"]
   
   for model in models_to_try:
       response = call_groq_api(prompt, model)
       if response:
           json_content = extract_json(response)
           review_data = safe_json_load(json_content)
           if review_data:
               return json_content
   
   return create_fallback_review(resume_data)
def create_fallback_review(resume_data):
   fallback = {}
   
   for section_name in resume_data.keys():
       if section_name == 'personal_info':
           continue
           
       section_content = resume_data[section_name]
       
       if isinstance(section_content, str):
           revised_content = f"Improved {section_name}: {section_content}"
       elif isinstance(section_content, list):
           revised_content = [f"Enhanced: {item}" if isinstance(item, str) else item for item in section_content]
       else:
           revised_content = section_content
       
       fallback[section_name] = {
           "impact_level": "Medium",
           "revised_content": revised_content,
           "revision_suggestion": [
               "Add more specific details and achievements",
               "Use action-oriented language"
           ]
       }
   
   try:
       return json.dumps(fallback, indent=2)
   except:
       return "{}"