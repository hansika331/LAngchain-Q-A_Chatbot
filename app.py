from dotenv import load_dotenv
import streamlit as st
import os
import pyttsx3
import speech_recognition as sr
from chatbot.memory import get_huggingface_response
from chatbot.features import analyze_sentiment, summarize_text , get_voice_input, speak_text
# from chatbot.knowledge import search_wikipedia

# Load environment variables
load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the environment.")

tts_engine = pyttsx3.init()

# Streamlit Configuration
st.set_page_config(page_title="Q&A Chatbot", layout="centered")
st.title("LangChain Q&A Chatbot")

# Input Section
st.sidebar.header("Features")
use_sentiment = st.sidebar.checkbox("Enable Sentiment Analysis")
use_summary = st.sidebar.checkbox("Enable Summarization")
use_voice_input = st.sidebar.checkbox("Enable Voice Input (Microphone)")  # Real-time voice input
use_voice_output = st.sidebar.checkbox("Enable Voice Output")  # Text-to-speech feature

st.header("Ask Your Question")
user_input = ""

# Voice Input: Real-time microphone input
if use_voice_input:
    st.info("Press the 'Start Recording' button to provide input via microphone.")
    if st.button("Start Recording"):
        user_input = get_voice_input()
        if user_input.startswith("Sorry") or user_input.startswith("Could not"):
            st.error(user_input)
            user_input = ""  # Reset user_input if recognition failed
        else:
            st.success(f"Recognized Speech: {user_input}")
             # Display the recognized speech in the input bar
            st.session_state["user_input"] = user_input

# Initialize session state for user input
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""


# Fallback to Text Input
st.session_state["user_input"] = st.text_input(
    "Enter your question:", value=st.session_state["user_input"]
)

submit = st.button("Submit")

# If the submit button is clicked, process the user input
if submit:
    if st.session_state["user_input"]:
        st.success(f"Processing input: {st.session_state['user_input']}")
        # Call your response function here, e.g.:
        # response = process_input(st.session_state["user_input"])
        # st.write(response)
    else:
        st.warning("Please provide an input before submitting!")

# Process Input
# Process Input After Submit
if submit and st.session_state["user_input"]:
    user_input = st.session_state["user_input"]

   # Q&A Response
    response = get_huggingface_response(user_input)
    st.subheader("Chatbot Response")
    st.write(response)
  

    # Voice Input and Output Information
    if use_voice_input and use_voice_output:
        st.info("Voice input and output are both enabled. Speak your query, and the bot will respond aloud.")
    elif use_voice_input:
        st.info("Voice input is enabled. Speak your query.")
    elif use_voice_output:
        st.info("Voice output is enabled. The bot will read responses aloud.")

    # Voice Output: For both input and response
    if use_voice_output:
        st.info("Playing the voice output...")
        if user_input:
            st.info("Reading your input...")
            speak_text(user_input)
        if response:
            st.info("Reading the bot's response...")
            speak_text(response)



    # Sentiment Analysis
    if use_sentiment and response:
        try:
            sentiment = analyze_sentiment(user_input)
            st.subheader("Sentiment Analysis")
            st.write(sentiment)
        except Exception as e:
            st.error(f"Sentiment analysis failed: {e}")


    # Summarization
    if use_summary:
        summary = summarize_text(user_input)
        st.subheader("Summarization")
        st.write(summary)

    
    # # Wikipedia Search
    # if use_wikipedia:
    #     st.subheader("Wikipedia Search Results")
    #     try:
    #         wiki_result = search_wikipedia(user_input)
    #         st.write(wiki_result)
    #     except Exception as e:
    #         st.error(f"An error occurred while searching Wikipedia: {e}")
        

elif submit:
    st.warning("Please provide an input before submitting!")