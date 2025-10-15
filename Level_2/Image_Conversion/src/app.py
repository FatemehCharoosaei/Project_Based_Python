from io import BytesIO
import streamlit as st
from PIL import Image
from utils import convert_image_type, resize_image
# ==================== PAGE CONFIG ====================
st.set_page_config(
   page_title="ImageMagic Pro",
   page_icon="🖼️",
   layout="wide",
   initial_sidebar_state="expanded"
)
# ==================== CUSTOM STYLING ====================
st.markdown("""
<style>
   .main-title {
       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
       -webkit-background-clip: text;
       -webkit-text-fill-color: transparent;
       font-size: 4rem;
       font-weight: 800;
       text-align: center;
       margin: 2rem 0;
   }
   .feature-card {
       background: white;
       padding: 2rem;
       border-radius: 15px;
       box-shadow: 0 10px 30px rgba(0,0,0,0.1);
       border-left: 5px solid #667eea;
       margin: 1rem 0;
       transition: transform 0.3s ease;
   }
   .feature-card:hover {
       transform: translateY(-5px);
   }
   .upload-area {
       border: 3px dashed #667eea;
       border-radius: 15px;
       padding: 3rem;
       text-align: center;
       background: #f8f9ff;
       margin: 2rem 0;
   }
   .success-box {
       background: linear-gradient(135deg, #4CAF50, #45a049);
       color: white;
       padding: 1rem;
       border-radius: 10px;
       margin: 1rem 0;
   }
   .info-box {
       background: linear-gradient(135deg, #2196F3, #1976D2);
       color: white;
       padding: 1rem;
       border-radius: 10px;
       margin: 1rem 0;
   }
   .stButton button {
       background: linear-gradient(135deg, #667eea, #764ba2);
       color: white;
       border: none;
       padding: 0.7rem 2rem;
       border-radius: 25px;
       font-weight: 600;
       transition: all 0.3s ease;
   }
   .stButton button:hover {
       transform: scale(1.05);
       box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
   }
   .metric-card {
       background: white;
       padding: 1.5rem;
       border-radius: 10px;
       box-shadow: 0 5px 15px rgba(0,0,0,0.1);
       text-align: center;
   }
</style>
""", unsafe_allow_html=True)
def main():
   # ==================== HERO SECTION ====================
   col1, col2, col3 = st.columns([1, 2, 1])
   with col2:
       st.markdown('<h1 class="main-title">🖼️ ImageMagic Pro</h1>', unsafe_allow_html=True)
       st.markdown("### Professional Image Processing • Instant Results • Studio Quality")
   # ==================== FEATURES OVERVIEW ====================
   with st.container():
       st.markdown("---")
       col1, col2, col3 = st.columns(3)
       
       with col1:
           st.markdown("""
           <div class="feature-card">
               <h3>🎯 Smart Resizing</h3>
               <p>Intelligent aspect ratio preservation • Batch processing • Quality optimization</p>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           st.markdown("""
           <div class="feature-card">
               <h3>🔄 Format Master</h3>
               <p>Seamless format conversion • Quality preservation • Metadata handling</p>
           </div>
           """, unsafe_allow_html=True)
       
       with col3:
           st.markdown("""
           <div class="feature-card">
               <h3>⚡ Instant Delivery</h3>
               <p>Real-time processing • One-click downloads • Cloud-ready outputs</p>
           </div>
           """, unsafe_allow_html=True)
   # ==================== UPLOAD SECTION ====================
   st.markdown("---")
   st.markdown("## 📤 Upload Your Image")
   
   with st.container():
       col1, col2 = st.columns([2, 1])
       
       with col1:
           uploaded_file = st.file_uploader(
               " ",
               type=["jpg", "jpeg", "png", "webp"],
               help="Supported formats: JPG, JPEG, PNG, WEBP • Max size: 200MB"
           )
       with col2:
           st.markdown("""
           <div style='text-align: center; padding: 1rem;'>
               <h4>📁 Supported Formats</h4>
               <p>JPG • PNG • WEBP • JPEG</p>
           </div>
           """, unsafe_allow_html=True)
   if not uploaded_file:
       st.markdown("""
       <div class="upload-area">
           <h3>🚀 Ready to Transform Your Images?</h3>
           <p>Drag and drop your image file above or click to browse</p>
           <p><small>High-quality processing • Fast results • Professional outputs</small></p>
       </div>
       """, unsafe_allow_html=True)
       return
   # ==================== IMAGE PROCESSING ====================
   try:
       image = Image.open(uploaded_file)
       
       # Image Info Dashboard
       col1, col2, col3, col4 = st.columns(4)
       with col1:
           st.markdown(f"""
           <div class="metric-card">
               <h4>📏 Dimensions</h4>
               <h3>{image.width} × {image.height}</h3>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           st.markdown(f"""
           <div class="metric-card">
               <h4>📊 Format</h4>
               <h3>{image.format}</h3>
           </div>
           """, unsafe_allow_html=True)
       
       with col3:
           st.markdown(f"""
           <div class="metric-card">
               <h4>🎨 Mode</h4>
               <h3>{image.mode}</h3>
           </div>
           """, unsafe_allow_html=True)
       
       with col4:
           file_size = len(uploaded_file.getvalue()) / 1024
           st.markdown(f"""
           <div class="metric-card">
               <h4>💾 Size</h4>
               <h3>{file_size:.1f} KB</h3>
           </div>
           """, unsafe_allow_html=True)
       # Image Preview
       col1, col2 = st.columns(2)
       with col1:
           st.markdown("### 📸 Original Preview")
           st.image(image, use_column_width=True)
       # ==================== PROCESSING OPTIONS ====================
       st.markdown("---")
       st.markdown("## ⚙️ Processing Options")
       
       process_type = st.radio(
           "Select your processing method:",
           ["Resize", "Type Conversion"],
           horizontal=True,
           label_visibility="collapsed"
       )
       if process_type == "Resize":
           # Enhanced Resize Section
           col1, col2 = st.columns([2, 1])
           
           with col1:
               st.markdown("### 📏 Resize Configuration")
               
               col_a, col_b = st.columns(2)
               with col_a:
                   keep_aspect_ratio = st.toggle(
                       "🔒 Maintain Aspect Ratio",
                       value=True,
                       help="Automatically calculate proportional dimensions"
                   )
               
               with col_b:
                   if keep_aspect_ratio:
                       width = st.slider(
                           "Target Width (px)",
                           min_value=50,
                           max_value=4000,
                           value=min(1200, image.width),
                           step=10
                       )
                       aspect_ratio = image.width / image.height
                       height = int(width / aspect_ratio)
                       
                       st.markdown(f"""
                       <div class="info-box">
                           <strong>Auto-calculated Height:</strong> {height}px
                       </div>
                       """, unsafe_allow_html=True)
                   else:
                       width = st.slider("Width (px)", 50, 4000, min(800, image.width), 10)
                       height = st.slider("Height (px)", 50, 4000, min(600, image.height), 10)
           with col2:
               st.markdown("### 🎯 Quick Presets")
               preset_col1, preset_col2 = st.columns(2)
               
               with preset_col1:
                   if st.button("HD (1280×720)", use_container_width=True):
                       width, height = 1280, 720
                   if st.button("Social (1080×1080)", use_container_width=True):
                       width, height = 1080, 1080
               
               with preset_col2:
                   if st.button("4K (3840×2160)", use_container_width=True):
                       width, height = 3840, 2160
                   if st.button("Mobile (750×1334)", use_container_width=True):
                       width, height = 750, 1334
           # Process Button
           if st.button("🚀 Process Resizing", use_container_width=True, type="primary"):
               with st.spinner("🔄 Processing your image with premium quality..."):
                   resized_image = resize_image(image, width, height, keep_aspect_ratio)
                   
                   # Results Display
                   col1, col2 = st.columns(2)
                   with col1:
                       st.markdown("### 📸 Original")
                       st.image(image, use_column_width=True)
                   
                   with col2:
                       st.markdown("### ✨ Resized")
                       st.image(resized_image, use_column_width=True)
                   
                   # Download Section
                   st.markdown("---")
                   col1, col2 = st.columns([3, 1])
                   
                   with col1:
                       st.markdown("### 📥 Download Result")
                       result_buffer = BytesIO()
                       resized_image.save(result_buffer, format="PNG", quality=95)
                       
                       st.download_button(
                           label="💾 Download High-Quality PNG",
                           data=result_buffer.getvalue(),
                           file_name="professional_resized.png",
                           mime="image/png",
                           use_container_width=True
                       )
                   
                   with col2:
                       st.markdown(f"""
                       <div class="success-box">
                           <h4>✅ Success!</h4>
                           <p>New size: {width}×{height}</p>
                       </div>
                       """, unsafe_allow_html=True)
       else:  # Type Conversion
           col1, col2 = st.columns([2, 1])
           
           with col1:
               st.markdown("### 🔄 Format Conversion")
               
               output_format = st.selectbox(
                   "Convert to format:",
                   ["JPEG", "PNG", "WEBP"],
                   help="Select your desired output format"
               )
               
               # Quality settings
               if output_format in ["JPEG", "WEBP"]:
                   quality = st.slider("Output Quality", 50, 100, 90)
               
               format_details = {
                   "JPEG": "Best for photographs • Smaller file size • Lossy compression",
                   "PNG": "Lossless quality • Supports transparency • Larger file size",
                   "WEBP": "Modern format • Excellent compression • Best of both worlds"
               }
               
               st.markdown(f"""
               <div class="info-box">
                   <strong>Format Info:</strong> {format_details[output_format]}
               </div>
               """, unsafe_allow_html=True)
           with col2:
               st.markdown("### ⚡ Quick Actions")
               if st.button("🔄 Convert Now", use_container_width=True, type="primary"):
                   with st.spinner("Converting with maximum quality preservation..."):
                       converted_buffer = convert_image_type(image, output_format)
                       
                       if output_format in ["JPEG", "WEBP"]:
                           # Re-convert with quality settings
                           quality_buffer = BytesIO()
                           image.save(quality_buffer, format=output_format, quality=quality)
                           converted_buffer = quality_buffer
                       # Results
                       col1, col2 = st.columns(2)
                       with col1:
                           st.markdown("### 📸 Original")
                           st.image(image, use_column_width=True)
                       
                       with col2:
                           st.markdown(f"### ✨ {output_format} Converted")
                           st.image(converted_buffer.getvalue(), use_column_width=True)
                       # Download
                       st.markdown("---")
                       mime_type = f"image/{output_format.lower()}"
                       file_ext = output_format.lower()
                       
                       st.download_button(
                           label=f"💾 Download {output_format}",
                           data=converted_buffer.getvalue(),
                           file_name=f"converted_image.{file_ext}",
                           mime=mime_type,
                           use_container_width=True
                       )
                       
                       st.markdown(f"""
                       <div class="success-box">
                           <h4>✅ Conversion Complete!</h4>
                           <p>Format: {output_format} • Quality: {quality if output_format in ['JPEG', 'WEBP'] else 'Lossless'}</p>
                       </div>
                       """, unsafe_allow_html=True)
   except Exception as e:
       st.error(f"❌ Processing Error: {str(e)}")
   # ==================== FOOTER ====================
   st.markdown("---")
   col1, col2, col3 = st.columns(3)
   with col2:
       st.markdown("""
       <div style='text-align: center; color: #666; margin-top: 3rem;'>
           <h4>ImageMagic Pro 🚀</h4>
           <p>Professional Image Processing • Built with Streamlit</p>
       </div>
       """, unsafe_allow_html=True)
if __name__ == "__main__":
   main()
