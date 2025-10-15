import streamlit as st
from name_predictor import process_name_input
from image_predictor import process_image_input
from utils import TITLE_EMOJI, setup_page
setup_page()
def main():
   col1, col2 = st.columns([1, 3])
   
   with col1:
       st.image("https://cdn.mos.cms.futurecdn.net/4jAWtqUCUWKk2bBkmKfiRS-1200-80.jpg", width="stretch")
   
   with col2:
       st.title(f"{TITLE_EMOJI} AI Gender & Ethnicity Analyzer")
       st.markdown("**⚡ Instant predictions • 🎯 High accuracy • 🚀 Fast processing**")
   
   st.markdown("---")
   
   # دکمه‌های رادیویی با هایلایت قرمز واضح
   st.markdown("### 🔘 Select Analysis Method")
   input_type = st.radio(
       "",
       ["Name Analysis", "Image Analysis"],
       horizontal=True,
       help="Choose between name-based or image-based analysis"
   )
   
   st.markdown("---")
   
   if input_type == "Name Analysis":
       process_name_input()
   else:
       process_image_input()
if __name__ == "__main__":
   main()
