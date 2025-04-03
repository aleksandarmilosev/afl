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
MAX_FINAL_ROUND = 30

ROUND_LABELS = {
    0: "OR",   # Opening Round
    26: "QF",
    27: "EF",
    28: "SF",
    29: "PF",
    30: "GF"
}
ALL_ROUNDS = list(range(0, 31))
ROUND_DISPLAY = [ROUND_LABELS.get(r, str(r)) for r in ALL_ROUNDS]
label_to_value = {v: k for k, v in ROUND_LABELS.items()}
label_to_value.update({str(i): i for i in range(0, 31)})

# Inputs
season = st.selectbox("Select Season", list(range(2025, 2015, -1)))
include_finals = st.checkbox("Include Finals", value=False)

round_options = ROUND_DISPLAY[:MAX_FINAL_ROUND + 1 if include_finals else MAX_HA_ROUND + 1]
default_rounds = (ROUND_DISPLAY[0], ROUND_DISPLAY[MAX_FINAL_ROUND if include_finals else MAX_HA_ROUND])

round_labels = st.select_slider(
    label="Select Round Range",
    options=round_options,
    value=default_rounds
)

round_range = (label_to_value[round_labels[0]], label_to_value[round_labels[1]])

# Fetch data
df = fetch_team_form(
    season=season,
    round_start=round_range[0],
    round_end=round_range[1],
    include_finals=include_finals
)

# Build title
def format_title_label(label):
    if label.isdigit() and 1 <= int(label) <= 24:
        return f"R{label}"
    return label

title = f"{season} AFL Premiership Window – {format_title_label(round_labels[0])}–{format_title_label(round_labels[1])}"
if include_finals and round_range[1] > MAX_HA_ROUND:
    title += " + Finals"

# Plot or warn
if df.empty:
    st.warning("No games found for the selected season and round range.")
else:
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
