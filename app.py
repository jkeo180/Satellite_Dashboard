import streamlit as st
import pandas as pd
from skyfield.api import load, wgs84, EarthSatellite
import requests

st.set_page_config(page_title="Live Satellite Tracker", page_icon="🛰️")
st.title("🛰️ Live Satellite Tracker")

@st.cache_resource(ttl=3600)
def fetch_satellites():
    tle_url = "https://celestrak.org"
    try:
        response = requests.get(tle_url, timeout=10)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        
        ts = load.timescale()
        satellites = []
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                name = lines[i].strip()
                line1 = lines[i+1].strip()
                line2 = lines[i+2].strip()
                sat = EarthSatellite(line1, line2, name, ts)
                satellites.append(sat)
        return satellites
    except Exception as e:
        st.error(f"Failed to fetch TLE data: {e}")
        return []

# Load data safely
ts = load.timescale()
t_now = ts.now()
satellites = fetch_satellites()
sat_data = []

# Compute Positions
if satellites:
    for sat in satellites[:100]:  # Limit to 100 entries for optimal performance
        try:
            geocentric = sat.at(t_now) 
            subpoint = wgs84.subpoint(geocentric) 
            sat_data.append({
                "name": sat.name,
                "lat": subpoint.latitude.degrees,
                "lon": subpoint.longitude.degrees,
                "alt_km": round(subpoint.elevation.km, 2)
            })
        except Exception:
            continue

# Display UI Elements
if sat_data:
    df = pd.DataFrame(sat_data)
    st.map(df, latitude="lat", longitude="lon")
    st.dataframe(df)
else:
    st.error("No satellite data available.")

