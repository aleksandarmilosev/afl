#!/bin/zsh

# Set up virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements if needed
if [ ! -d ".venv/lib" ] || ! pip show streamlit &> /dev/null; then
  echo "📦 Installing dependencies..."
  pip install -r requirements.txt
fi

# Launch the Streamlit app
echo "🚀 Launching AFL Premiership Window..."
streamlit run premiership_window_app.py
