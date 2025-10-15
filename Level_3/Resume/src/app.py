import streamlit as st
import json
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from utils.pdf import extract_text_from_pdf
from utils.llm import parse_resume, review_resume, safe_json_load
from resume_formatter import format_resume
def init_session_state():
   if 'resume_data' not in st.session_state:
       st.session_state.resume_data = None
   if 'review_data' not in st.session_state:
       st.session_state.review_data = None
   if 'revised_content' not in st.session_state:
       st.session_state.revised_content = {}
   if 'processing_complete' not in st.session_state:
       st.session_state.processing_complete = False
def setup_page():
   st.set_page_config(
       page_title="Resume Parser & Reviewer",
       page_icon="📄",
       layout="wide"
   )
def render_sidebar():
   st.sidebar.title("📄 ResumeAI")
   
   uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type="pdf")
   job_description = st.sidebar.text_area("Job Description (Optional)", height=100)
   
   if st.sidebar.button("🚀 Analyze Resume", type="primary", use_container_width=True):
       if uploaded_file is not None:
           process_resume(uploaded_file, job_description.strip() if job_description else None)
       else:
           st.sidebar.error("Please upload a PDF resume")
def render_main_content():
   if st.session_state.processing_complete and st.session_state.resume_data:
       show_analysis_results()
   else:
       show_welcome_screen()
def show_welcome_screen():
   st.title("📄 AI Resume Analyzer")
   st.info("👈 Upload your PDF resume to begin analysis")
def process_resume(uploaded_file, job_description):
   try:
       st.session_state.processing_complete = False
       
       with st.spinner("📖 Extracting text from PDF..."):
           resume_text = extract_text_from_pdf(uploaded_file)
           if not resume_text or len(resume_text.strip()) < 100:
               st.error("❌ No text could be extracted")
               return
       
       with st.spinner("🤖 Analyzing resume structure..."):
           resume_json = parse_resume(resume_text)
           resume_data = safe_json_load(resume_json)
           
           if not resume_data:
               st.error("❌ Failed to parse resume")
               return
       
       with st.spinner("💡 Generating improvement suggestions..."):
           review_json = review_resume(resume_json, job_description)
           review_data = safe_json_load(review_json)
           
           if not review_data:
               st.warning("⚠️ Using basic suggestions")
               review_data = create_basic_review(resume_data)
       
       st.session_state.revised_content = {}
       
       for section_name in resume_data.keys():
           if section_name == 'personal_info':
               continue
           
           section_review = review_data.get(section_name, {})
           original_content = resume_data[section_name]
           
           revised_content = section_review.get('revised_content', original_content)
           
           if isinstance(revised_content, (dict, list)):
               formatted_content = format_resume({section_name: revised_content})
           else:
               formatted_content = str(revised_content)
           
           st.session_state.revised_content[section_name] = formatted_content
       
       st.session_state.resume_data = resume_data
       st.session_state.review_data = review_data
       st.session_state.processing_complete = True
       
       st.success("🎉 Analysis completed!")
       
   except Exception as e:
       st.error(f"❌ Error: {str(e)}")
def create_basic_review(resume_data):
   basic_review = {}
   for section_name, content in resume_data.items():
       if section_name != 'personal_info':
           basic_review[section_name] = {
               "impact_level": "Medium",
               "revised_content": content,
               "revision_suggestion": ["Add more specific details", "Use action verbs"]
           }
   return basic_review
def show_analysis_results():
   st.title("📊 Analysis Results")
   
   resume_data = st.session_state.resume_data
   review_data = st.session_state.review_data
   
   for section_name in resume_data.keys():
       if section_name != 'personal_info':
           display_section(section_name, resume_data, review_data)
def display_section(section_name, resume_data, review_data):
   section_title = section_name.replace('_', ' ').title()
   
   with st.expander(f"📋 {section_title}", expanded=True):
       col1, col2 = st.columns(2)
       
       with col1:
           st.subheader("Original")
           original_content = format_resume({section_name: resume_data[section_name]})
           st.text_area("Original", original_content, height=150, key=f"orig_{section_name}", disabled=True)
       
       with col2:
           st.subheader("Improved")
           
           section_review = review_data.get(section_name, {})
           impact = section_review.get('impact_level', 'Low')
           
           if impact == "High":
               st.error("High Impact")
           elif impact == "Medium":
               st.warning("Medium Impact")
           else:
               st.success("Low Impact")
           
           current_content = st.session_state.revised_content.get(section_name, "")
           edited = st.text_area("Improved", current_content, height=120, key=f"imp_{section_name}")
           
           if edited != current_content:
               st.session_state.revised_content[section_name] = edited
           
           suggestions = section_review.get('revision_suggestion', [])
           if suggestions:
               st.markdown("**Suggestions:**")
               for suggestion in suggestions:
                   st.markdown(f"- {suggestion}")
def main():
   setup_page()
   init_session_state()
   render_sidebar()
   render_main_content()
if __name__ == "__main__":
   main()