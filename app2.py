from dotenv import load_dotenv
load_dotenv()  # load all env variables from .env

import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai 
import time

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    # Add a progress bar for API call
    with st.spinner('Analyzing invoice...'):
        response = model.generate_content([input, image[0], prompt])
        
    return response.text 

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

# Page configuration with custom title and layout
st.set_page_config(
    page_title="Smart Invoice Query Analyzer",
    page_icon="📊",
    layout="wide"
)

# Add custom styling for better visibility
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stImage {
        max-width: 800px;
        margin: auto;
    }
    .upload-text {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Main title with styling
st.title("📊 Smart Invoice Query Analyzer")
st.markdown("---")

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # File uploader with improved styling
    st.markdown('<p class="upload-text">Upload Invoice Image</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
    
    # Image display with improved visibility
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Improve image quality and visibility
        # Resize image while maintaining aspect ratio
        max_width = 800
        ratio = max_width / float(image.size[0])
        height = int((float(image.size[1]) * float(ratio)))
        image = image.resize((max_width, height), Image.Resampling.LANCZOS)
        
        # Enhance image contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # Increase contrast by 20%
        
        st.image(image, caption="Uploaded Invoice", use_container_width=True)

with col2:
    # Input and submit section
    st.markdown('<p class="upload-text">Analysis Options</p>', unsafe_allow_html=True)
    input = st.text_input("What would you like to know about the invoice?", key="input")
    submit = st.button("Analyze Invoice", use_container_width=True)

# Input prompt for the model
input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on uploaded invoice image
"""

# Response section
if submit:
    try:
        if uploaded_file is None:
            st.error("Please upload an invoice image first!")
        else:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input)
            st.markdown("### Analysis Results")
            st.markdown("---")
            st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Powered by Gemini AI 🚀
    </div>
""", unsafe_allow_html=True)