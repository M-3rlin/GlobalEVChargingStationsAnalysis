import json
import pandas as pd
import pydeck as pdk
import streamlit as st
from pathlib import Path

STATIONS_CSV = "stations_with_land_only_coords.csv"
US_GEOJSON_URL = (
    "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/"
    "master/data/geojson/us-states.json"
)

TARGET_CITIES = [
    "Houston",
    "San Francisco",
    "Los Angeles",
    "Chicago",
    "New York",
]

st.set_page_config(page_title="EV Charging Stations", layout="wide")

@st.cache_data
def load_stations():
    df = pd.read_csv(STATIONS_CSV)

    required_cols = [
        "Charging Station Location",
        "Charger Type",
        "lat",
        "lon",
    ]

    #missing = [c for c in required_cols if c not in df.columns]
    #if missing:
    #    st.error(f"Missing required columns in CSV: {missing}")
    #    st.stop()

    # Filter to target cities
    df = df[df["Charging Station Location"].isin(TARGET_CITIES)]
    # Drop rows without coords
    df = df.dropna(subset=["lat", "lon"])
    return df


@st.cache_data
def load_us_geojson():
    import requests
    return requests.get(US_GEOJSON_URL).json()


df = load_stations()
us_geojson = load_us_geojson()

st.title("EV Charging Stations in Selected US Cities")

st.sidebar.header("Filters")

select_city_sidebar = st.sidebar.selectbox(
    "Select City",
    options=sorted(df["Charging Station Location"].unique())
)

select_charger_types_sidebar= st.sidebar.multiselect(
    "Select Charger Types",
    options=sorted(df["Charger Type"].unique()),
    default=sorted(df["Charger Type"].unique()),
)

point_size_label_sidebar = st.sidebar.radio(
        "Point Size",
        options=["Very Small", "Small", "Medium", "Large"],
        index=2,  # default = Medium,
        horizontal=True
    )
POINT_SIZE_MAP = {
    "Very Small": 10,
    "Small": 250,
    "Medium": 500,
    "Large": 2000,
}

point_radius = POINT_SIZE_MAP[point_size_label_sidebar]

city_df = df[df["Charging Station Location"] == select_city_sidebar]

if select_charger_types_sidebar:
    df_filtered = city_df[city_df["Charger Type"].isin(select_charger_types_sidebar)].copy()
else:
    #keep map center from city_df if no charger type is selected
    df_filtered = city_df.iloc[0:0].copy()  # empty frame with same columns

with st.container():
    st.subheader("Summary")
    st.metric("Total Charging Stations", len(df_filtered))

# Map
st.subheader("Map of Charging Stations")

# Background is the US polygons
geo_layer = pdk.Layer(
    "GeoJsonLayer",
    data=us_geojson,
    pickable=False,
    stroked=True,
    filled=True,
    get_fill_color="[240, 240, 240, 120]",
    get_line_color="[120, 120, 120, 180]",
    line_width_min_pixels=1,
)

COLOR_MAP = {
    "DC Fast Charger": [220, 53, 69, 180],   # red
    "Level 1": [25, 135, 84, 180],          # green
    "Level 2": [13, 110, 253, 180],         # blue
}

df_filtered["color"] = df_filtered["Charger Type"].apply(
    lambda x: COLOR_MAP.get(x, [160, 160, 160, 180])
)

station_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    get_position="[lon, lat]",
    get_radius=point_radius,
    get_fill_color="color",
    pickable=True,
)

tooltip = {
    "html": """
    <b>{Charging Station Location}</b><br/>
    Charger: {Charger Type}<br/>
    """,
    "style": {"backgroundColor": "rgba(0,0,0,0.8)", "color": "white"},
}

if not city_df.empty:
    center_lat = city_df["lat"].mean()
    center_lon = city_df["lon"].mean()
    zoom = 10  # close zoom for a city
else:
    # Safe fallback (should rarely happen)
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    zoom = 3.4


view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=zoom,
    pitch=0,
)

# keeps GeoJSON visible
deck = pdk.Deck(
    layers=[geo_layer, station_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style=None,
)

st.pydeck_chart(deck, use_container_width=True)

with st.expander("Show station data"):
    st.dataframe(df_filtered, use_container_width=True)
