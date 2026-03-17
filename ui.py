import streamlit as st
import pandas as pd
from skyfield.api import EarthSatellite, load, wgs84
import datetime


st.title("🛰️ Live Satellite Tracker")
@st.cache_resource(ttl=3600)
def fetch_satellites():
   url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
   return load.tle_file(url)
# 1. Load Data
ts = load.timescale()
t_now = load.timescale().now()
satellites = fetch_satellites()
sat_data = []
# 2. Compute Positions
for sat in satellites:
    geocentric = sat.at(t_now) 
    subpoint = wgs84.subpoint(geocentric) 
try:
      
        sat_data.append({
            "name": sat.name,
            "lat": subpoint.latitude.degrees,
            "lon": subpoint.longitude.degrees,
            "alt_km": round(subpoint.elevation.km, 2)
        })
        
finally:
     
#except:
        st.warning(f"Could not compute position for {sat.name}. Skipping.")

# 3. Display
df = pd.DataFrame(sat_data)
if not df.empty:
    st.map(df, latitude="lat", longitude="lon")
    st.dataframe(df)
else:
    st.error("No satellite data available.")