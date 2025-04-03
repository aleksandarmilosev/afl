# AFL Premiership Window App

This Streamlit app visualizes the **AFL Premiership Window** using data from the [Squiggle API](https://api.squiggle.com.au). It enables teams' performance comparison based on **points for** and **points against**, normalized per game, over selected rounds of a given season.

---

## 📊 Features

- **Round-by-Round Analysis**: Select any round range (including Opening Round and Finals)
- **Finals Support**: Optionally include or exclude finals rounds (QF, EF, SF, PF, GF)
- **Custom Titles and Downloadable Charts**: Auto-updating chart labels and PNG export
- **Team Logos + Visual Haloing**: Clear logos with circular white backgrounds
- **Dark Mode Theme**: Clean dark aesthetic with transparent accents

---

## 🏗️ Project Structure

```
afl-premiership-window/
├── app.py               # Main Streamlit app
├── utils.py             # Data fetching + chart logic
├── run_dev.sh           # Local dev launcher
├── deploy.sh            # Production deployment script
├── requirements.txt     # Dependencies
├── .streamlit/
│   └── config.toml      # Theme config (optional)
├── assets/              # Team logo images
```

---

## 🚀 Quick Start

### 1. Clone the Repo
```bash
git clone https://github.com/aleksandarmilosev/afl-premiership-window.git
cd afl-premiership-window
```

### 2. Run Locally (Dev Mode)
```bash
chmod +x run_dev.sh
./run_dev.sh
```

### 3. Deploy Script (Minimal)
```bash
chmod +x deploy.sh
./deploy.sh
```

### 4. View in Browser
```text
http://localhost:8501
```

---

## 🖼️ Download Chart
Use the **Download Chart as PNG** button at the bottom of the app interface.

---

## 🔧 Requirements
- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- Requests

Install manually:
```bash
pip install -r requirements.txt
```

---

## ✅ Round Support
| Type             | Label         | Rank |
|------------------|---------------|------|
| Opening Round    | `0`           | ✅   |
| Home & Away      | `1–25`        | ✅   |
| Finals           | `QF`, `EF`, `SF`, `PF`, `GF` → 26–30 | ✅   |

---

## 💡 Future Ideas
- Hover tooltips with match context
- Multi-season comparison overlay
- Finals-only filtering toggle
- CSV export of ranked metrics

---

## 👤 Author
Created by [@aleksandarmilosev](mailto:amilosev90@gmail.com). Feedback and PRs welcome!
