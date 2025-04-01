import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as patches
import os
from io import BytesIO

# --- CONFIGURATION ---
LOGO_DIR = 'afl_logos/'
DEFAULT_YEAR = 2025
DEFAULT_NUM_GAMES = 5

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

headers = {'User-Agent': 'AFLPremiershipWindowApp (amilosev90@gmail.com)'}

def fetch_year_standings(year):
    url = f'https://api.squiggle.com.au/?q=standings&year={year}'
    standings = requests.get(url, headers=headers).json()['standings']
    df = pd.DataFrame([{
        'Team': team['name'],
        'PF': team['for'],
        'PA': team['against'],
        'Played': team['played']
    } for team in standings])
    df['PF_avg'] = df['PF'] / df['Played']
    df['PA_avg'] = df['PA'] / df['Played']
    return df[['Team', 'PF_avg', 'PA_avg']]

def fetch_rolling_form(num_games, current_year):
    years = [current_year, current_year - 1]
    games = []
    for year in years:
        url = f'https://api.squiggle.com.au/?q=games&year={year}'
        games += requests.get(url, headers=headers).json()['games']

    df_games = pd.DataFrame(games)
    df_games = df_games[df_games['complete'] == 100]
    df_games['date'] = pd.to_datetime(df_games['date'])
    df_games = df_games.sort_values('date', ascending=False)

    records = []
    for _, row in df_games.iterrows():
        records.append({'Team': row['hteam'], 'Date': row['date'], 'PF': row['hscore'], 'PA': row['ascore']})
        records.append({'Team': row['ateam'], 'Date': row['date'], 'PF': row['ascore'], 'PA': row['hscore']})

    df_flat = pd.DataFrame(records).sort_values(['Team', 'Date'], ascending=[True, False])
    recent = (
        df_flat.groupby('Team')
        .head(num_games)
        .groupby('Team')
        .agg(PF_avg=('PF', 'mean'), PA_avg=('PA', 'mean'))
        .reset_index()
    )
    return recent

def plot_premiership_matrix(df, title):
    df['PF_rank'] = df['PF_avg'].rank(method='min', ascending=False)
    df['PA_rank'] = df['PA_avg'].rank(method='min', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor((0, 0, 0.025, 0.85))
    ax.set_facecolor((0, 0, 0, 0))

    ax.set_xlim(19.5, 0)
    ax.set_ylim(0, 19.5)
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')

    ax.fill_betweenx(y=[0.5, 6.5], x1=0.5, x2=6.5, color='limegreen', alpha=0.2, zorder=0)
    ax.axvline(6.5, color='white', linewidth=1.5, alpha=0.7)
    ax.axhline(6.5, color='white', linewidth=1.5, alpha=0.7)

    ax.text(0, 0.75, 'Premiership\nWindow', color='white', fontsize=10, ha='center', va='bottom', weight='bold')
    ax.text(19, 0.75, 'Defensive\nGrinders', color='white', fontsize=10, ha='center', va='bottom', weight='bold')
    ax.text(0, 19.25, 'Attacking\nRisks', color='white', fontsize=10, ha='center', va='bottom', weight='bold')
    ax.text(19, 19, 'Rebuilders', color='white', fontsize=10, ha='center', va='bottom', weight='bold')

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

    ax.set_xticks(range(1, 19))
    ax.set_yticks(range(1, 19))
    ax.set_xticklabels(range(1, 19), color='white')
    ax.set_yticklabels(range(1, 19), color='white')
    ax.tick_params(colors='white')

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
    ax.set_title(title, color='white', fontsize=14, weight='bold', pad=20)
    ax.grid(True, linestyle='--', color='white', alpha=0.3)

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

# --- STREAMLIT UI ---
st.title("AFL Premiership Window")
mode = st.radio("Select Mode", ["Season Ladder", "Rolling Form"])

if mode == "Season Ladder":
    year = st.selectbox(label="Select Year", index=0, options=["2025", "2024", "2023", "2022", "2021", "2020"], placeholder="2025")
    df = fetch_year_standings(year)
    plot_premiership_matrix(df, f"{year} AFL Premiership Window (Ranks Normalised Per Game)")
else:
    num_games = st.slider("Number of Recent Games", 3, 15, DEFAULT_NUM_GAMES)
    df = fetch_rolling_form(num_games, DEFAULT_YEAR)
    plot_premiership_matrix(df, f"AFL Premiership Window (Last {num_games} Games)")
