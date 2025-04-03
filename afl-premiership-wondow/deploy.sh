#!/bin/zsh

# deploy.sh - Minimal launcher for production or CI/CD

# Ensure the virtual environment exists
[ -d ".venv" ] || python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies silently
pip install -r requirements.txt --quiet

# Launch the Streamlit app
streamlit run app.py

