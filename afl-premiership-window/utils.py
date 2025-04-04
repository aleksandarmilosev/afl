import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from PIL import Image
from io import BytesIO

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE_DIR, "assets")
HEADERS = {'User-Agent': 'AFLPremiershipWindowApp (amilosev90@gmail.com)'}

TEAM_LOGO_MAP = {
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

FINALS_ROUND_MAP = {"QF": 26, "EF": 27, "SF": 28, "PF": 29, "GF": 30}


def fetch_team_form(season, round_start, round_end, include_finals):
    url = f'https://api.squiggle.com.au/?q=games&year={season}'
    games = requests.get(url, headers=HEADERS).json()['games']

    df = pd.DataFrame(games)
    df = df[df['complete'] == 100]
    df['date'] = pd.to_datetime(df['date'])

    def map_round(r):
        if isinstance(r, int):
            return r
        if isinstance(r, str):
            if r.lower().startswith("opening"):
                return 0
            return FINALS_ROUND_MAP.get(r)
        return None

    df['round_mapped'] = df['round'].apply(map_round)
    df = df[df['round_mapped'].between(round_start, round_end, inclusive='both')]

    records = []
    for _, row in df.iterrows():
        records.append({'Team': row['hteam'], 'Date': row['date'], 'PF': row['hscore'], 'PA': row['ascore']})
        records.append({'Team': row['ateam'], 'Date': row['date'], 'PF': row['ascore'], 'PA': row['hscore']})

    df_flat = pd.DataFrame(records)

    if df_flat.empty:
        return pd.DataFrame(columns=["Team", "PF_avg", "PA_avg"])

    df_flat = df_flat.sort_values(['Team', 'Date'], ascending=[True, False])

    summary = (
        df_flat.groupby('Team')
        .agg(PF_avg=('PF', 'mean'), PA_avg=('PA', 'mean'))
        .reset_index()
    )
    return summary


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
        logo_file = TEAM_LOGO_MAP.get(team)
        if logo_file:
            logo_path = os.path.join(LOGO_DIR, logo_file)
            if os.path.exists(logo_path):
                circle = plt.Circle((x, y), 1, color='white', zorder=1)
                ax.add_patch(circle)
                with open(logo_path, 'rb') as f:
                    img = Image.open(BytesIO(f.read()))
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

    return fig
