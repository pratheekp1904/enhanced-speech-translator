import streamlit as st
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
import pyttsx3

# Function to translate text
def translate_text(text, dest_language='en'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        st.error(f"An error occurred while translating text: {e}")
        return "Translation Error"

# Function to speak text
def speak_text(text, lang_code=None):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        voice_id = None

        # Select the female voice if specified in settings
        if st.session_state.settings['voice'] == 'female_voice_id':
            for voice in voices:
                if 'zira' in voice.id.lower():
                    voice_id = voice.id
                    break
        else:
            for voice in voices:
                if 'david' in voice.id.lower():
                    voice_id = voice.id
                    break

        engine.setProperty('voice', voice_id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"An error occurred while speaking text: {e}")

# Streamlit app
st.title("Enhanced Speech Translator - v2.0")

# Default settings
if 'settings' not in st.session_state:
    st.session_state.settings = {'language': 'english', 'voice': 'male_voice_id'}

st.sidebar.header("Navigation")
page = st.sidebar.radio("Navigate", ["Home", "Translate", "Settings"], key="navigation")

if page == "Home":
    st.header("Welcome to the Enhanced Speech Translator App")
    st.write("Capture speech, transcribe, translate, and hear the translation.")

elif page == "Translate":
    st.header("Translation Page")

    transcription = st.empty()
    translation = st.empty()

    lang_name = st.selectbox("Select Language", list(LANGUAGES.values()), key="language_selector")
    language_code = [code for code, name in LANGUAGES.items() if name == lang_name][0]

    if st.button("Capture Audio", key="capture_audio_button"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            st.write("Listening...")
            audio_data = recognizer.listen(source, timeout=5)
            st.write("Audio captured")
        try:
            text = recognizer.recognize_google(audio_data)
            transcription.text(f"Transcription: {text}")
            st.session_state.transcription = text
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            st.error(f"An error occurred while capturing audio: {e}")

    input_text = st.text_input("Type text here for translation...", key="input_text")
    if st.button("Translate Text", key="translate_text_button"):
        transcription.text(f"Transcription: {input_text}")
        translated_text = translate_text(input_text, language_code)
        translation.text(f"Translation: {translated_text}")
        speak_text(translated_text, language_code)

    if "transcription" in st.session_state:
        if st.button("Translate and Speak", key="translate_speak_button"):
            text = st.session_state.transcription
            translated_text = translate_text(text, language_code)
            translation.text(f"Translation: {translated_text}")
            speak_text(translated_text, language_code)

elif page == "Settings":
    st.header("Settings")
    st.write("Customize your experience.")

    default_language = st.selectbox(
        "Default Language", 
        list(LANGUAGES.values()), 
        index=list(LANGUAGES.values()).index(st.session_state.settings.get('language', 'english'))
    )
    default_voice = st.selectbox("Voice", ["Male", "Female"], index=1 if st.session_state.settings.get('voice', 'female_voice_id') == 'female_voice_id' else 0)

    if st.button("Save Settings", key="save_settings_button"):
        st.session_state.settings['language'] = default_language
        st.session_state.settings['voice'] = 'female_voice_id' if default_voice == "Female" else 'male_voice_id'
        st.success("Settings saved")
        st.experimental_rerun()
