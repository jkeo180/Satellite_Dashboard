import streamlit as st
import pandas as pd
from skyfield.api import load, wgs84, EarthSatellite
import requests

st.title("🛰️ Live Satellite Tracker")

@st.cache_resource(ttl=3600)
def fetch_satellites():
    # Using the Active satellites group URL from your collision script
    tle_url = "https://celestrak.org"
    try:
        response = requests.get(tle_url)
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

# 1. Load Data
ts = load.timescale()
t_now = ts.now()
satellites = fetch_satellites()
sat_data = []

# 2. Compute Positions
for sat in satellites[:100]:  # Limiting to first 100 to keep map rendering fast
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

# 3. Display
df = pd.DataFrame(sat_data)
if not df.empty:
    st.map(df, latitude="lat", longitude="lon")
    st.dataframe(df)
else:
    st.error("No satellite data available.")
