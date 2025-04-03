# AFL Premiership Window App

This Streamlit app visualizes the **AFL Premiership Window** using data from the [Squiggle API](https://api.squiggle.com.au). It allows you to explore how AFL teams are performing based on points scored and conceded, either by season or by recent form.

---

## 📊 Features

- **Season Ladder View**: Uses official ladder data normalized per game.
- **Rolling Form View**: Shows average performance over the last X games.
- **Dynamic Quadrant Visualization**:
  - 🟩 Premiership Window (top-right)
  - 🟨 Defensive Grinders (top-left)
  - 🟦 Attacking Risks (bottom-right)
  - 🟥 Rebuilders (bottom-left)
- **Team Logos** with visibility-enhancing white halos
- **Dark Theme** with clean grid and transparency
- **Download Chart as PNG** directly from the app

---

## 🏗️ Project Structure

```
afl-premiership-window/
├── app.py               # Main Streamlit app UI
├── utils.py             # Data fetching and plotting logic
├── requirements.txt     # Python dependencies
├── run_dev.sh           # Dev-mode launcher script
├── deploy.sh            # Deployment launcher script
├── .gitignore           # Ignore common build artifacts
├── .streamlit/
│   └── config.toml      # Streamlit dark theme configuration
├── assets/              # Team logo PNGs (used in visualizations)
```

---

## 🚀 Running the App

### 📦 1. Clone the Repo
```bash
git clone https://github.com/aleksandarmilosev/afl-premiership-window.git
cd afl-premiership-window
```

### 🧪 2. Run in Development Mode
Make the script executable (once only):
```bash
chmod +x run_dev.sh
```
Then run it:
```bash
./run_dev.sh
```
This will:
- Create a virtual environment (if not already present)
- Install required dependencies
- Launch the Streamlit app at `http://localhost:8501`

### ⚙️ 3. Run for Deployment
Make the script executable (once only):
```bash
chmod +x deploy.sh
```
Then run it:
```bash
./deploy.sh
```
This is a minimal version of the above, ideal for CI/CD or hosted deployments.

---

## 🖼️ PNG Export
Once the chart is rendered, click the **"Download Chart as PNG"** button to save the visualization.

---

## 🔧 Requirements
- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- Requests

Install manually with:
```bash
pip install -r requirements.txt
```

---

## ☁️ Future Enhancements
- Add interactive quadrant filtering
- Deploy live via Streamlit Cloud
- Include betting odds / ELO overlays
- Export CSV of ranked team metrics

---

## 👤 Author
Created by [@aleksandarmilosev](mailto:amilosev90@gmail.com).
