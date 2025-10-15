import streamlit as st
from deepface import DeepFace
import os
import tempfile
from utils import IMAGE_EMOJI, display_prediction
import cv2
import numpy as np
@st.cache_resource
def load_deepface_model():
   return DeepFace
def predict_gender_and_ethnicity_fast(img_path):
   try:
       analysis = DeepFace.analyze(
           img_path=img_path,
           actions=['gender', 'race'],
           detector_backend='opencv',
           enforce_detection=False,
           silent=True,
           align=False
       )
       
       if analysis and len(analysis) > 0:
           result = analysis[0]
           
           gender = result.get('dominant_gender', 'Unknown')
           if gender == "Man":
               gender = "Male"
           elif gender == "Woman":
               gender = "Female"
           
           ethnicity = result.get('dominant_race', 'Unknown')
           
           return gender, ethnicity
           
       else:
           return "Unknown", "No face detected"
           
   except Exception as e:
       return "Error", str(e)
def process_image_input():
   st.subheader(f"{IMAGE_EMOJI} Image Analysis")
   
   uploaded_file = st.file_uploader(
       "Choose an image...",
       type=["jpg", "jpeg", "png"],
       help="Upload a clear face image for gender and ethnicity detection"
   )
   
   if uploaded_file is not None:
       col1, col2 = st.columns(2)
       
       with col1:
           st.image(uploaded_file, caption="Uploaded Image", width="stretch")
       
       if st.button("🚀 Analyze Image", width="stretch", type="primary"):
           with st.spinner('Analyzing...'):
               with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                   tmp_file.write(uploaded_file.getbuffer())
                   tmp_path = tmp_file.name
               
               try:
                   gender, ethnicity = predict_gender_and_ethnicity_fast(tmp_path)
                   display_prediction(gender, ethnicity)
                       
               except Exception as e:
                   st.error(f"❌ Error: {str(e)}")
               
               finally:
                   if os.path.exists(tmp_path):
                       os.remove(tmp_path)