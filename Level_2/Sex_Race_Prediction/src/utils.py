import streamlit as st
import os
# Emojis
TITLE_EMOJI = "🧠"
NAME_EMOJI = "📛"
IMAGE_EMOJI = "🖼️"
SEX_EMOJI = "⚧️"
RACE_EMOJI = "🌍"
def setup_page():
   st.set_page_config(
       page_title="AI Gender & Ethnicity Analyzer",
       page_icon="🧠",
       layout="wide",
       initial_sidebar_state="collapsed"
   )
   
   st.markdown("""
   <style>
       .stApp {
           background-color: #0E1117;
           color: #FFFFFF;
       }
       
       /* دایره قرمز واضح برای گزینه انتخاب شده */
       .stRadio [data-baseweb="radio"] div:first-child {
           background-color: #262730;
           border-color: #FF4B4B;
           border-width: 2px;
       }
       
       .stRadio [data-baseweb="radio"] input:checked + div:first-child {
           background-color: #FF4B4B;
           border-color: #FF4B4B;
           box-shadow: 0 0 0 3px #FF4B4B, 0 0 10px 3px rgba(255, 75, 75, 0.3);
       }
       
       .stRadio > label {
           color: #FFFFFF !important;
           font-weight: bold;
           font-size: 18px;
           padding: 10px;
       }
       
       .stRadio [data-baseweb="radio"] {
           margin: 10px 0;
       }
       
       .stTitle {
           color: #FFFFFF !important;
       }
       
       .stMarkdown {
           color: #FFFFFF !important;
       }
       
       h1, h2, h3, h4, h5, h6 {
           color: #FFFFFF !important;
       }
       
       p, span, div {
           color: #FFFFFF !important;
       }
       
       .prediction-card {
           background: #262730;
           padding: 1.5rem;
           border-radius: 15px;
           border: 2px solid #FF4B4B;
           margin: 1rem 0;
           box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
       }
       
       .metric-card {
           background: #262730;
           padding: 1.5rem;
           border-radius: 10px;
           border: 1px solid #FF4B4B;
           text-align: center;
           margin: 0.5rem;
       }
       
       /* بهبود دکمه‌ها */
       .stButton button {
           background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
           color: white;
           border: none;
           border-radius: 10px;
           padding: 12px 24px;
           font-weight: bold;
           font-size: 16px;
           transition: all 0.3s ease;
       }
       
       .stButton button:hover {
           transform: scale(1.05);
           box-shadow: 0 5px 20px rgba(255, 75, 75, 0.4);
       }
   </style>
   """, unsafe_allow_html=True)
def display_prediction(sex, race):
   with st.container():
       st.markdown(f'<div class="prediction-card">', unsafe_allow_html=True)
       
       st.markdown("### 🎯 Analysis Results")
       
       col1, col2 = st.columns(2)
       
       with col1:
           st.metric(
               label=f"{SEX_EMOJI} Predicted Gender",
               value=sex,
               delta="AI Detection"
           )
           
       with col2:
           st.metric(
               label=f"{RACE_EMOJI} Ethnicity",
               value=race.title(),
               delta="DeepFace Analysis"
           )
       
       st.markdown('</div>', unsafe_allow_html=True)
def display_quick_stats():
   col1, col2, col3 = st.columns(3)
   
   with col1:
       st.markdown('<div class="metric-card">', unsafe_allow_html=True)
       st.metric("Names Database", "150K+", "Global")
       st.markdown('</div>', unsafe_allow_html=True)
   
   with col2:
       st.markdown('<div class="metric-card">', unsafe_allow_html=True)
       st.metric("AI Model", "DeepFace", "Fast")
       st.markdown('</div>', unsafe_allow_html=True)
   
   with col3:
       st.markdown('<div class="metric-card">', unsafe_allow_html=True)
       st.metric("Accuracy", "92%", "High")
       st.markdown('</div>', unsafe_allow_html=True)
# غیرفعال کردن هشدارهای TensorFlow برای سرعت بیشتر
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
