import streamlit as st
from utils import fetch_team_form, plot_premiership_matrix
from io import BytesIO

# Configure Streamlit
st.set_page_config(
    page_title="AFL Premiership Window",
    layout="centered",
    initial_sidebar_state="auto"
)

# Title
st.title("AFL Premiership Window")

# Finals round mapping for extended slider support
MAX_HA_ROUND = 25
MAX_FINAL_ROUND = 30  # Simulate finals as rounds 26–30

# Inputs
season = st.selectbox("Select Season", list(range(2025, 2015, -1)))
include_finals = st.checkbox("Include Finals", value=False)

# Dynamically adjust round range limit
max_round = MAX_FINAL_ROUND if include_finals else MAX_HA_ROUND
round_range = st.slider("Select Round Range", 0, max_round, (0, max_round))

# Fetch data
df = fetch_team_form(
    season=season,
    round_start=round_range[0],
    round_end=round_range[1],
    include_finals=include_finals
)

# Build title
title = f"{season} AFL Premiership Window – R{round_range[0]}–R{round_range[1]}"
if include_finals and round_range[1] > MAX_HA_ROUND:
    title += " + Finals"

# Plot
fig = plot_premiership_matrix(df, title)
st.pyplot(fig)

# PNG export
buf = BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
st.download_button(
    label="Download Chart as PNG",
    data=buf.getvalue(),
    file_name="afl_premiership_window.png",
    mime="image/png"
)
