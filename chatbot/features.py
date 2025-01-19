from transformers import pipeline
import speech_recognition as sr
import pyttsx3

# Sentiment Analysis
def analyze_sentiment(text: str) -> dict:
    sentiment_analyzer = pipeline("sentiment-analysis")
    return sentiment_analyzer(text)



# Summarization
def summarize_text(text: str) -> str:
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]["summary_text"]



# Voice Input: Converts microphone input to text
def get_voice_input() -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening... Speak now.")
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand your speech."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"An error occurred: {e}"



# Voice Output: Converts text to speech
def speak_text(text: str):
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()

    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"An error occurred during text-to-speech: {e}")
