import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize global variables
isTranslateOn = False
translator = Translator()  # Initialize the translator
pygame.mixer.init()  # Initialize the mixer module

# Create a mapping between language names and language codes (lowercase for consistency)
language_mapping = {name.lower(): code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    """Return the language code for a given language name."""
    return language_mapping.get(language_name.lower(), None)

def translator_function(spoken_text, from_language, to_language):
    """Translate spoken text from the source language to the target language."""
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    """Convert text to speech and play it."""
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")  # Save to a file
    audio = pygame.mixer.Sound("cache_file.mp3")  # Load a sound
    audio.play()  # Play the sound
    os.remove("cache_file.mp3")  # Clean up audio file

def detect_language(audio):
    """Detect the language spoken in the audio input."""
    rec = sr.Recognizer()
    try:
        spoken_text = rec.recognize_google(audio)  # Convert audio to text
        detected_lang = translator.detect(spoken_text).lang  # Detect language of the text
        return detected_lang
    except Exception as e:
        print(e)
        return None

def main_process(output_placeholder, from_language, to_language):
    """Main translation process that listens for audio and translates."""
    global isTranslateOn
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        while isTranslateOn:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
            try:
                output_placeholder.text("Processing...")
                spoken_text = rec.recognize_google(audio, language=from_language)
                output_placeholder.text(f"Recognized Text: {spoken_text}")

                output_placeholder.text("Translating...")
                translated_text = translator_function(spoken_text, from_language, to_language)

                text_to_voice(translated_text.text, to_language)

            except Exception as e:
                output_placeholder.text(f"Error: {e}")
                print(e)

# UI layout
st.title("Language Translator with Detection")

# Placeholder for output messages
output_placeholder = st.empty()

# Initialize session state for languages
if "from_language" not in st.session_state:
    st.session_state.from_language = None

if "to_language" not in st.session_state:
    st.session_state.to_language = None

# Step 1: Detect Language
if st.button("Detect Language"):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        output_placeholder.text("Please say something to detect the language...")
        audio = rec.listen(source, phrase_time_limit=5)
        
    detected_language = detect_language(audio)
    
    if detected_language:
        st.session_state.from_language = detected_language
        output_placeholder.text(f"Detected Input Language: {LANGUAGES.get(detected_language, 'Unknown')}")
    else:
        output_placeholder.text("Could not detect the language. Please try again.")

# Display the input language after detection
if st.session_state.from_language:
    output_placeholder.text(f"Detected Input Language: {LANGUAGES.get(st.session_state.from_language, 'Unknown')}")

# Step 2: Select target language
to_language_name = st.selectbox("Select Output Language:", list(LANGUAGES.values()))

# Update the session state only when a new selection is made
if to_language_name:
    st.session_state.to_language = get_language_code(to_language_name)

# Step 3: Show output language only after it has been selected
if st.session_state.to_language:
    output_placeholder.text(f"Input Language: {LANGUAGES.get(st.session_state.from_language, 'Unknown')}")

# Step 4: Start translation
start_button = st.button("Start")
stop_button = st.button("Stop")

if start_button:
    if not isTranslateOn and st.session_state.from_language:
        isTranslateOn = True
        main_process(output_placeholder, st.session_state .from_language, st.session_state.to_language)
    else:
        output_placeholder.text("Please detect the input language first.")

if stop_button:
    isTranslateOn = False
    output_placeholder.text("Translation stopped.")