#!/bin/bash
cd /home/ubuntu/speech-translator
source venv/bin/activate
pkill -f streamlit
nohup streamlit run /home/ubuntu/speech-translator/app.py --server.port 80 &
