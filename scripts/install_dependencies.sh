#!/bin/bash
cd /home/ubuntu/speech-translator
python3 -m venv venv
source venv/bin/activate
pip install streamlit speechrecognition googletrans==4.0.0-rc1 pyttsx3
