import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="Voice Note Summarizer",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Gradient Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff7676 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.15);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.3);
        color: white;
    }
    div.stButton > button:first-child:active {
        transform: translateY(0);
    }
    /* Header Customization */
    .header-container {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
    }
    .subtitle {
        color: #a3a8b4;
        font-size: 1.15rem;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    /* Card Container for Results */
    .result-card {
        background-color: #1e222b;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff4b4b;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.title("🎙️ Tamil Voice Note Summarizer By Jagadeesh")
st.markdown('<p class="subtitle">Convert spoken Tamil audio into clear, organized English insights instantly.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 API Key Missing: Please add your secret key to the Streamlit Advanced Settings panel.")
else:
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader("", type=["mp3", "wav", "m4a", "ogg", "amr"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        st.write("") 

    if st.button("Process & Summarize Voice Note"):
        if uploaded_file is not None:
            with st.spinner("✨ Our AI engine is analyzing your audio file... please wait."):
                temp_file_path = f"temp_{uploaded_file.name}"
                
                try:
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    audio_file = client.files.upload(file=temp_file_path)
                    
                    prompt = """
                    You are an expert audio translator and summarizer. Process the provided Tamil audio file and return the response exactly in this format:

                    ### 📝 English Summary
                    [Provide a clear, cohesive, bulleted, and concise summary of the audio content in English here]

                    ---

                    ### 🗣️ Original Tamil Transcription
                    [Provide the accurate text transcription of the spoken Tamil text here]
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[audio_file, prompt]
                    )
                    
                    st.balloons()
                    st.success("Analysis Complete!")
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"An processing anomaly occurred: {e}")
                    
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
        else:
            st.warning("Please upload a valid voice note file first.")
