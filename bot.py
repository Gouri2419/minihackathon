from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is available
if not api_key:
    st.error("API key is missing. Please check your .env file.")
else:
    # Configure API key for Gemini
    genai.configure(api_key=api_key)

    # Load Gemini Pro model
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    chat = model.start_chat(history=[])

    # Function to get Gemini response
    def get_gemini_response(question):
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    # Streamlit app setup
    st.set_page_config(page_title="Job Prep Chatbot", layout="wide")
    st.title("🎯 Job Preparation Mentor Chatbot")
    st.markdown("Ask me anything about job interviews, resumes, skill-building, or career growth!")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Predefined question options
    st.markdown("### Quick Ask:")
    cols = st.columns(3)

    with cols[0]:
        if st.button("How to prepare for interviews?"):
            st.session_state['chat_history'].append(("You", "How should I prepare for a job interview and improve my skills?"))
            response = get_gemini_response("How should I prepare for a job interview and improve my skills?")
            full_response = ""
            if isinstance(response, list):  # Check if response is a list of chunks
                for chunk in response:
                    st.markdown(chunk.text)
                    full_response += chunk.text
            else:
                st.markdown(response)  # If error occurs, show it
            st.session_state['chat_history'].append(("Bot", full_response))

    with cols[1]:
        if st.button("Tips to improve communication"):
            st.session_state['chat_history'].append(("You", "How can I improve my communication skills for the workplace?"))
            response = get_gemini_response("How can I improve my communication skills for the workplace?")
            full_response = ""
            if isinstance(response, list):
                for chunk in response:
                    st.markdown(chunk.text)
                    full_response += chunk.text
            else:
                st.markdown(response)
            st.session_state['chat_history'].append(("Bot", full_response))

    with cols[2]:
        if st.button("Top resume mistakes"):
            st.session_state['chat_history'].append(("You", "What are the most common mistakes to avoid on a resume?"))
            response = get_gemini_response("What are the most common mistakes to avoid on a resume?")
            full_response = ""
            if isinstance(response, list):
                for chunk in response:
                    st.markdown(chunk.text)
                    full_response += chunk.text
            else:
                st.markdown(response)
            st.session_state['chat_history'].append(("Bot", full_response))
