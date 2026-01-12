import streamlit as st
import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
con = duckdb.connect(BASE_DIR / "db" / "reservoir.duckdb")

st.set_page_config(page_title="Venezuela Reservoir Analysis", layout="wide")

st.title("🛢️ Venezuela Reservoir Analytics Dashboard")

# Sidebar filter
locations = con.execute(
    "SELECT DISTINCT location FROM reservoirs_clean ORDER BY location"
).df()["location"]

selected_location = st.sidebar.selectbox(
    "Select Location", ["All"] + list(locations)
)

query = "SELECT * FROM reservoirs_clean"
if selected_location != "All":
    query += f" WHERE location = '{selected_location}'"

df = con.execute(query).df()

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Reservoirs", len(df))
c2.metric("Total Proven Reserves (BBB)", round(df.proven_reserves_bbb.sum(), 2))
c3.metric("Total Production (BPD)", int(df.production_capacity_bpd.sum()))

st.subheader("Strategic Ranking")
st.dataframe(
    df.assign(
        strategic_score=
        df.proven_reserves_bbb * 0.4 +
        df.recoverable_reserves_bbb * 0.4 +
        df.production_capacity_bpd / 100000 * 0.2
    ).sort_values("strategic_score", ascending=False)
)
