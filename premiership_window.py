import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# --- CONFIGURATION ---
LOGO_DIR = 'afl_logos/'  # directory where team logos are stored
YEAR = 2025  # year for which to fetch the standings

# Map team names to logo filenames
team_logo_map = {
    "Adelaide": "adelaide.png",
    "Brisbane Lions": "brisbane.png",
    "Carlton": "carlton.png",
    "Collingwood": "collingwood.png",
    "Essendon": "essendon.png",
    "Fremantle": "fremantle.png",
    "Geelong": "geelong.png",
    "Gold Coast": "suns.png",
    "Greater Western Sydney": "giants.png",
    "Hawthorn": "hawthorn.png",
    "Melbourne": "melbourne.png",
    "North Melbourne": "north-melbourne.png",
    "Port Adelaide": "port-adelaide.png",
    "Richmond": "richmond.png",
    "St Kilda": "st-kilda.png",
    "Sydney": "sydney.png",
    "West Coast": "west-coast.png",
    "Western Bulldogs": "western-bulldogs.png"
}

# --- FETCH LADDER DATA FROM SQUIGGLE API ---
headers = {
    'User-Agent': 'AFLPremiershipWindowAnalysis (amilosev90@gmail.com)'
}

url = f'https://api.squiggle.com.au/?q=standings&year={YEAR}'
response = requests.get(url, headers=headers)
standings = response.json()['standings']

# --- PROCESS DATA ---
df = pd.DataFrame([{
    'Team': team['name'],
    'PF': team['for'],
    'PA': team['against'],
    'Played': team['played']
} for team in standings])

# Per-game averages
df['PF_per_game'] = df['PF'] / df['Played']
df['PA_per_game'] = df['PA'] / df['Played']

# Rank teams by per-game PF (descending) and PA (ascending)
df['PF_rank'] = df['PF_per_game'].rank(method='min', ascending=False)
df['PA_rank'] = df['PA_per_game'].rank(method='min', ascending=True)
#df['In_Premiership_Window'] = (df['PF_rank'] <= 6) & (df['PA_rank'] <= 6)

"""# Bounding box for the premiership window
window_df = df[df['In_Premiership_Window']]
pf_min, pf_max = window_df['PF_per_game'].min(), window_df['PF_per_game'].max()
pa_min, pa_max = window_df['PA_per_game'].min(), window_df['PA_per_game'].max()"""

# --- PLOT SETUP ---
fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor((0, 0, 0.025, 0.85))    # figure background
ax.set_facecolor((0, 0, 0, 0))              # axis background

ax.set_xlim(19.5, 0)
ax.set_ylim(0, 19.5)
ax.invert_yaxis()

ax.set_aspect('equal', adjustable='box')

# Shade the Premiership Window (top-right 6x6)
ax.fill_betweenx(
    y=[0.5, 6.5],
    x1=0.5, x2=6.5,
    color='limegreen',
    alpha=0.2,
    zorder=0
)

# Add white lines through PF rank = 6.5 and PA rank = 6.5
ax.axvline(6.5, color='white', linewidth=1.5, alpha=0.7, linestyle='-')
ax.axhline(6.5, color='white', linewidth=1.5, alpha=0.7, linestyle='-')

ax.text(0, 0.75, 'Premiership\nWindow', color='white', fontsize=10, ha='center', va='bottom', weight='bold')
ax.text(19, 0.75, 'Defensive\nGrinders', color='white', fontsize=10, ha='center', va='bottom', weight='bold')
ax.text(0, 19.25, 'Attacking\nRisks', color='white', fontsize=10, ha='center', va='bottom', weight='bold')
ax.text(19, 19, 'Rebuilders', color='white', fontsize=10, ha='center', va='bottom', weight='bold')

# --- PLOT TEAM LOGOS WITH WHITE HALO CIRCLES ---
for _, row in df.iterrows():
    x, y = row['PF_rank'], row['PA_rank']
    team = row['Team']
    logo_file = team_logo_map.get(team)

    if logo_file:
        logo_path = os.path.join(LOGO_DIR, logo_file)
        if os.path.exists(logo_path):
            circle = plt.Circle((x, y), 0.8, color='white', zorder=1)
            ax.add_patch(circle)
            img = plt.imread(logo_path)
            imagebox = OffsetImage(img, zoom=0.07)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False, zorder=2)
            ax.add_artist(ab)
        else:
            ax.text(x, y, team, fontsize=8, ha='center', color='white', zorder=2)
    else:
        ax.text(x, y, team, fontsize=8, ha='center', color='white', zorder=2)

# --- STYLING ---
ax.set_xticks(range(1, 19))
ax.set_yticks(range(1, 19))
ax.set_xticklabels(range(1, 19), color='white')
ax.set_yticklabels(range(1, 19), color='white')
ax.tick_params(colors='white')

# Make ticks match grid alpha
for tick in ax.xaxis.get_major_ticks():
    tick.tick1line.set_color('white')
    tick.tick1line.set_alpha(0.3)
    tick.tick2line.set_color('white')
    tick.tick2line.set_alpha(0.3)

for tick in ax.yaxis.get_major_ticks():
    tick.tick1line.set_color('white')
    tick.tick1line.set_alpha(0.3)
    tick.tick2line.set_color('white')
    tick.tick2line.set_alpha(0.3)

ax.set_xlabel("Most Points For (PF) Rank (Best Offense →)", color='white', fontsize=12)
ax.set_ylabel("Least Points Against (PA) Rank (Best Defense →)", color='white', fontsize=12)

ax.set_title(
    f"{YEAR} AFL Premiership Window (Ranks Normalised Per Game)",
    color='white',
    fontsize=14,
    weight='bold',
    pad=20
)

ax.grid(True, linestyle='--', color='white', alpha=0.3)

for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.show()
