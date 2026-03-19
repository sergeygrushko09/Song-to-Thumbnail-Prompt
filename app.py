import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="UA Thumbnail Architect", layout="wide")

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #3b82f6; color: white; }
    .stTextInput>div>div>input { background-color: #1e1e1e; color: white; }
    </style>
    """, unsafe_allow_file_with_html=True)

# --- SIDEBAR: SETTINGS & UPLOAD ---
with st.sidebar:
    st.title("🧙🏾‍♂️ Synapse Architect")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    uploaded_file = st.file_uploader("Upload Ukrainian Audio", type=['mp3', 'wav', 'aac'])
    
    if api_key:
        genai.configure(api_key=api_key)

# --- APP LOGIC ---
if uploaded_file and api_key:
    model = genai.GenerativeModel("gemini-1.5-flash") # Or gemini-1.5-pro

    # Stage 1: Processing Audio
    if st.button("🚀 Analyze Song"):
        with st.status("Analyzing audio and generating lyrics...", expanded=True) as status:
            # Upload file to Gemini API
            temp_file = "temp_audio.mp3"
            with open(temp_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            audio_data = genai.upload_file(path=temp_file)
            
            # Step 1-3 Prompt
            prompt_init = """Follow these steps:
            Step 1 - provide transcription of Ukrainian lyrics only.
            Step 2 - provide song summary and content description (5 sentences in English).
            Step 3 - Create 5 TITLES and 5 SUBTITLES in Ukrainian (UPPERCASE)."""
            
            response = model.generate_content([prompt_init, audio_data])
            st.session_state['initial_analysis'] = response.text
            status.update(label="Analysis Complete!", state="complete")

    # Display Results for Steps 1-3
    if 'initial_analysis' in st.session_state:
        st.subheader("📝 Song Analysis & Metadata")
        st.markdown(st.session_state['initial_analysis'])
        
        st.divider()

        # Step 4: Interactive Input
        st.subheader("🎯 Step 4: Selection")
        col1, col2 = st.columns(2)
        with col1:
            final_title = st.text_input("Enter chosen TITLE (UPPERCASE)")
        with col2:
            final_subtitle = st.text_input("Enter chosen SUBTITLE (UPPERCASE)")

        # Step 5 & 6: Prompt Generation
        if final_title and final_subtitle:
            if st.button("🎨 Generate 6 High-CTR Thumbnail Prompts"):
                prompt_final = f"""Based on the previous analysis, create 6 high-CTR thumbnail prompts using TITLE: {final_title} and SUBTITLE: {final_subtitle}. 
                Follow the specific constraints: 2 facial close-ups, 2 medium shots, 2 cowboy shots. 
                Include the technical suffix and Step 6 Key Elements for each."""
                
                final_response = model.generate_content(prompt_final)
                st.subheader("🖼️ Final Prompt Architectures")
                st.markdown(final_response.text)

else:
    st.info("Please enter your API Key and upload an audio file in the sidebar to begin.")
