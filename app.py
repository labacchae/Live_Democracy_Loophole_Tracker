import streamlit as st
import pandas as pd
import altair as alt

# 1. Page config
st.set_page_config(
    page_title="Live Democracy Loophole Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Load data
@st.cache_data
def load_data():
    return pd.read_csv("flagged_bills_classified.csv")

df = load_data()

# 3. Sidebar filters
st.sidebar.header("Filters")
cats = st.sidebar.multiselect(
    "Category", options=df["Category"].unique(), default=df["Category"].unique()
)
states = st.sidebar.multiselect(
    "State", options=df["state"].unique(), default=df["state"].unique()
)
min_threat = st.sidebar.slider("Min Threat Level", 1, 5, 1)

mask = (
    df["Category"].isin(cats)
    & df["state"].isin(states)
    & (df["ThreatLevel"] >= min_threat)
)
df_filt = df[mask]

# 4. Metrics row
total = len(df_filt)
avg_threat = round(df_filt["ThreatLevel"].mean(), 2) if total else 0
top_cat = df_filt["Category"].value_counts().idxmax() if total else None

col1, col2, col3 = st.columns(3, gap="large")
col1.metric("Bills Matching Filters", total)
col2.metric("Avg. Threat Level", avg_threat)
col3.metric("Top Category", top_cat)

# 5. Plots
st.markdown("### Bills by Category")
bar = (
    alt.Chart(df_filt)
    .mark_bar()
    .encode(
        x=alt.X("Category:N", sort="-y", title=""),
        y=alt.Y("count():Q", title="Number of Bills"),
        color="Category:N",
        tooltip=["Category", "count()"]
    )
    .properties(width=800, height=300)
)
st.altair_chart(bar, use_container_width=True)

st.markdown("### Avg. Threat Level by State")
line = (
    alt.Chart(df_filt)
    .mark_circle(size=100)
    .encode(
        x=alt.X("state:N", title="State"),
        y=alt.Y("mean(ThreatLevel):Q", title="Avg. Threat Level"),
        color=alt.Color("mean(ThreatLevel):Q", scale=alt.Scale(scheme="reds")),
        tooltip=["state", "mean(ThreatLevel)"]
    )
    .properties(width=800, height=300)
)
st.altair_chart(line, use_container_width=True)

# 6. Top‑Threat Table
st.markdown("### Top 10 High‑Threat Bills")
st.dataframe(
    df_filt.sort_values("ThreatLevel", ascending=False)
    .head(10)
    [["state", "bill_id", "title", "Category", "ThreatLevel", "Explanation"]],
    use_container_width=True,
)
