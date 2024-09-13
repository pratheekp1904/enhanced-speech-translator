#!/bin/bash
cd /home/ubuntu/speech-translator
python3 -m venv venv
source venv/bin/activate
pip install streamlit SpeechRecognition googletrans==4.0.0-rc1 pyttsx3 pyaudio
