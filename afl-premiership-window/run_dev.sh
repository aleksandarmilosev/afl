#!/bin/zsh

# run_dev.sh - Local developer launcher with setup and friendly output

echo "🧪 Starting AFL Premiership Window (Dev Mode)..."

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv .venv
fi

# Step 2: Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Step 3: Install dependencies if needed
if ! pip show streamlit > /dev/null 2>&1; then
  echo "⬇️ Installing required packages..."
  pip install -r requirements.txt
fi

# Step 4: Run the Streamlit app
echo "🚀 Launching app at http://localhost:8501 ..."
streamlit run app.py
