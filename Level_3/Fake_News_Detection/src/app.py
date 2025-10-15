import streamlit as st
from web_scraper import search_google
from text_processor import prepare_context
from llm_interface import call_llm
from constants import groq_models
from dotenv import load_dotenv
import os
load_dotenv()
st.image("src/images/banner.png")
st.title("Fake News Detector")
st.sidebar.header("About")
st.sidebar.info("This app uses web scraping and AI to analyze whether a given news headline or claim might be fake news.")
model = st.sidebar.selectbox("Select a model", groq_models)
query = st.text_input("Enter a news headline or claim:")
if st.button("Check"):
   if query:
       with st.spinner("Searching and analyzing..."):
           links = search_google(query)
           context = prepare_context(links)
           prompt = f"""
Analyze the following news claim and determine if it's likely to be fake news or not.
NEWS CLAIM: {query}
CONTEXT FROM SEARCH: {context}
Please provide:
1. Your analysis based on the available information
2. Likelihood of being fake news (Low/Medium/High)
3. Key reasons for your assessment
4. Any inconsistencies found
Keep response concise and factual.
"""
           result = call_llm(prompt, model=model)
           st.subheader("Result:")
           st.write(result)
   else:
       st.warning("Please enter a query.")
