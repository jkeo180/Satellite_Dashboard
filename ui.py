import streamlit as st
from skyfield.api import load, EarthSatellite, wgs84
import requests
from io import StringIO
import pandas as pd
import time
import datetime
import folium
from streamlit_folium import st_folium
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
from plotly import graph_objs as go 
from sgp4.api import Satrec

st.title("Interactive Folium Map")
class Location:
    latitude = 37.7749
    longitude = -122.4194
    zoom_level = 12
    m = folium.Map(location=[latitude, longitude], zoom_start=zoom_level, tiles='OpenStreetMap') # Use other tiles for satellite view
    map_data = st_folium(m, use_container_width=True, height=400)
    folium.TileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google').add_to(m)
    folium.LayerControl().add_to(m) 

# Add layer control for users to switch layers
# Render the map and capture user interactions in real-time
    map_data = st_folium(m, width=700, height=500)

# You can access data like the last clicked location or current bounds
class Location:
    def __init__(self, name, lat, lng, alt=0):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.alt = alt
m = folium.Map(location=[37.7749, -122.4194], zoom_start=2)
map_data = st_folium(m, key="satellite_map")
if map_data and map_data.get("last_clicked"):
            click = map_data["last_clicked"]
else:
    pv_loc = Location("San Francisco", 37.7749, -122.4194, 0)

# 3. Rest of your UI
st.title("Live Satellite Tracker — Active Satellites")

url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
@st.cache_resource
def load_satellites(ttl=3600, show_spinner="Downloading TLE data..."):
    with st.spinner(show_spinner):
        response = requests.get(url)
        response.raise_for_status() 
        lines = response.text.strip().splitlines()
        ts = load.timescale()
        satellites = []
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                name = lines[i].strip()
                line1 = lines[i+1].strip()
                line2 = lines[i+2].strip()
                
                try: 
                    ts = load.timescale()  
                    sat = EarthSatellite(line1, line2, name, ts)
                    satellites.append((name, sat))
                    if len(satellites) >= 10:  # limit to 10 for speed
                        break
                except ValueError:
                    pass
    return ts, satellites
ts, satellites = load_satellites()

placeholder = st.empty()
status = st.empty()

while True:
    now = ts.now()
    data = []
    for name, sat in satellites:
        geocentric = sat.at(now)
        subpoint = wgs84.subpoint(geocentric)
        data.append({
            "name": name,
            "lat": round(subpoint.latitude.degrees, 4),
            "lon": round(subpoint.longitude.degrees, 4),
            "alt_km": round(subpoint.elevation.km)
        })
        satellite = Satrec.twoline2rv(tle.line1, tle.line2)
        ts = load.timescale()
        location = location("San Francisco", 37.7749, -122.4194, 0)
        date_start = datetime.datetime.utcnow()
        observer = observer(location, satellite)
        overpasses = observer.pass_list(date_start, limit_date= datetime.timedelta(days=1))

# To this (using your pv_loc instance):
    tle = f"{name}\n{sat.model.line1}\n{sat.model.line2}"

    df = pd.DataFrame(data)
    df_display = df.copy()
    df_display["size"] = 100  # Set a fixed size for all markers

    with placeholder.container():
        st.map(df_display, latitude="lat", longitude="lon", size=100, color="#ff0000")
        st.dataframe(df)
    
    thread = threading.Thread(target=my_function_in_thread,args=(pv_loc, satellite))
    add_script_run_ctx(thread) # Add the context to the thread
    thread.start()
    status.write(f"Last update: {now.utc_strftime('%H:%M:%S UTC')} — refreshing in 10s")
    time.sleep(10)
    try:
        pass
    except KeyboardInterrupt:
        print("Exiting live tracker.")
    for overpass in overpasses:
        print(f"* Rise time: {overpass.rise_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}, Max elevation: {overpass.max_elevation_deg:.1f} deg, Set time: {overpass.set_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        break
