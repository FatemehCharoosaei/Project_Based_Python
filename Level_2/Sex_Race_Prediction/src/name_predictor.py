import streamlit as st
from names_dataset import NameDataset, NameWrapper
from utils import NAME_EMOJI, display_prediction, display_quick_stats
import countryflag
@st.cache_resource(show_spinner=False)
def load_name_dataset():
   return NameDataset()
nd = load_name_dataset()
def predict_sex_and_race_from_name(name):
   try:
       name = name.strip()
       if not name:
           return "Unknown", "Unknown"
           
       result = NameWrapper(nd.search(name)).describe.split(', ')
       sex = result[0] if len(result) > 0 else "Unknown"
       country = result[1] if len(result) > 1 else "Unknown"
       if country != "Unknown":
           try:
               flag = countryflag.getflag([country])
               country = f"{flag} {country}"
           except:
               country = f"🏳️ {country}"
       return sex, country
       
   except Exception as e:
       st.error(f"Error processing name: {str(e)}")
       return "Unknown", "Unknown"
def process_name_input():
   display_quick_stats()
   
   st.subheader(f"{NAME_EMOJI} Name Analysis")
   
   tab1, tab2 = st.tabs(["🔍 Single Name", "📊 Multiple Names"])
   
   with tab1:
       name = st.text_input(
           "Enter a name:",
           placeholder="e.g., John, Maria, Ahmed...",
           help="Enter any name to predict gender and origin"
       )
       
       if name:
           with st.spinner('Analyzing name...'):
               sex, country = predict_sex_and_race_from_name(name)
               display_prediction(sex, country)
   
   with tab2:
       multiple_names = st.text_area(
           "Enter multiple names (one per line):",
           placeholder="John\nMaria\nAhmed\nWei\n...",
           height=100
       )
       
       if multiple_names:
           names_list = [name.strip() for name in multiple_names.split('\n') if name.strip()]
           
           if st.button("🚀 Analyze All", width="stretch"):
               results = []
               progress_bar = st.progress(0)
               
               for i, name in enumerate(names_list):
                   progress_bar.progress((i + 1) / len(names_list))
                   sex, country = predict_sex_and_race_from_name(name)
                   results.append({"Name": name, "Gender": sex, "Origin": country})
               
               progress_bar.empty()
               
               if results:
                   st.subheader("📊 Batch Results")
                   st.dataframe(results, width="stretch")
