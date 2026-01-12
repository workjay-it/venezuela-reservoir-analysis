import streamlit as st
import duckdb
from pathlib import Path
import plotly.express as px


BASE_DIR = Path(__file__).resolve().parent

# In-memory DuckDB
con = duckdb.connect()

csv_path = BASE_DIR / "data" / "Reservoir_venezuela.csv"

con.execute(f"""
CREATE TABLE IF NOT EXISTS reservoirs_clean AS
SELECT
    Location AS location,
    CASE
        WHEN CAST(Year_Discovered AS VARCHAR) LIKE '%s' THEN
            CAST(SUBSTR(CAST(Year_Discovered AS VARCHAR), 1, 4) AS INTEGER) + 5
        ELSE
            CAST(Year_Discovered AS INTEGER)
    END AS year_discovered,
    CAST(REPLACE(CAST(Proven_Reserves_Billion_Barrels AS VARCHAR), ',', '') AS DOUBLE) AS proven_reserves_bbb,
    CASE
        WHEN CAST(Estimated_Recoverable_Reserves_Billion_Barrels AS VARCHAR) LIKE '%-%' THEN
            (
                CAST(SPLIT_PART(REPLACE(CAST(Estimated_Recoverable_Reserves_Billion_Barrels AS VARCHAR), ',', ''), '-', 1) AS DOUBLE)
                +
                CAST(SPLIT_PART(REPLACE(CAST(Estimated_Recoverable_Reserves_Billion_Barrels AS VARCHAR), ',', ''), '-', 2) AS DOUBLE)
            ) / 2
        ELSE
            CAST(REPLACE(CAST(Estimated_Recoverable_Reserves_Billion_Barrels AS VARCHAR), ',', '') AS DOUBLE)
    END AS recoverable_reserves_bbb,
    CAST(REPLACE(CAST(Production_Capacity_Barrels_Day AS VARCHAR), ',', '') AS BIGINT) AS production_capacity_bpd
FROM read_csv_auto('{csv_path}');
""")

st.set_page_config(page_title="Venezuela Reservoir Analysis", layout="wide")
st.title("🛢️ Venezuela Reservoir Analytics Dashboard")

locations = con.execute(
    "SELECT DISTINCT location FROM reservoirs_clean ORDER BY location"
).df()["location"]

selected_location = st.sidebar.selectbox("Select Location", ["All"] + list(locations))

query = "SELECT * FROM reservoirs_clean"
if selected_location != "All":
    query += f" WHERE location = '{selected_location}'"

df = con.execute(query).df()

c1, c2, c3 = st.columns(3)
c1.metric("Reservoirs", len(df))
c2.metric("Total Proven Reserves (BBB)", round(df.proven_reserves_bbb.sum(), 2))
c3.metric("Total Production (BPD)", int(df.production_capacity_bpd.sum()))

st.markdown("---")
st.subheader("📊 Proven Reserves by Location")

reserves_by_location = (
    df.groupby("location", as_index=False)
      .agg(total_proven_reserves=("proven_reserves_bbb", "sum"))
)

fig_bar = px.bar(
    reserves_by_location,
    x="location",
    y="total_proven_reserves",
    title="Total Proven Reserves by Location",
    labels={
        "total_proven_reserves": "Proven Reserves (Billion Barrels)",
        "location": "Location"
    }
)

st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📈 Production Capacity vs Proven Reserves")

fig_scatter = px.scatter(
    df,
    x="proven_reserves_bbb",
    y="production_capacity_bpd",
    size="recoverable_reserves_bbb",
    color="location",
    title="Production Capacity vs Proven Reserves",
    labels={
        "proven_reserves_bbb": "Proven Reserves (Billion Barrels)",
        "production_capacity_bpd": "Production Capacity (BPD)"
    }
)

st.plotly_chart(fig_scatter, use_container_width=True)


st.subheader("Strategic Ranking")
st.dataframe(
    df.assign(
        strategic_score=
        df.proven_reserves_bbb * 0.4 +
        df.recoverable_reserves_bbb * 0.4 +
        df.production_capacity_bpd / 100000 * 0.2
    ).sort_values("strategic_score", ascending=False)
)
