import streamlit as st
import os
from google import genai

st.set_page_config(page_title="Tamil Voice Summarizer", page_icon="🎙️", layout="centered")

st.title("🎙️ Tamil Voice Note Summarizer")
st.write("Upload any Tamil voice note, and Gemini AI will analyze, transcribe, and summarize it into English!")

# Streamlit Cloud securely manages secrets. We look for the key there first.
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing Gemini API Key! Please configure GEMINI_API_KEY in your Streamlit Secrets.")
else:
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a", "ogg", "amr"])

    if st.button("Process & Summarize", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Gemini is analyzing your audio file... please wait."):
                temp_file_path = f"temp_{uploaded_file.name}"
                
                try:
                    # Save the uploaded file to a temporary local buffer path
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Upload the file directly via the Gemini client
                    audio_file = client.files.upload(file=temp_file_path)
                    
                    prompt = """
                    You are an expert audio translator and summarizer. Process the provided Tamil audio file and return the response exactly in this format:

                    ### English Summary
                    [Provide a clear, cohesive, and concise summary of the audio content in English here]

                    ---

                    ### Original Tamil Transcription
                    [Provide the accurate text transcription of the spoken Tamil text here]
                    """
                    
                    # Generate translation & summary execution
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[audio_file, prompt]
                    )
                    
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")
                    
                finally:
                    # Clean up the temporary local file execution safely
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
        else:
            st.warning("Please upload an audio file first.")