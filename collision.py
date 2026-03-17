import requests
import numpy as np
import pandas as pd
from skyfield.api import load, EarthSatellite, wgs84

#loads map
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"


def load_satellites(limit=10):

    response = requests.get(TLE_URL)
    response.raise_for_status()

    lines = response.text.strip().splitlines()

    ts = load.timescale()
    satellites = []

    for i in range(0, len(lines), 3):

        if i + 2 < len(lines):

            name = lines[i]
            line1 = lines[i + 1]
            line2 = lines[i + 2]

            sat = EarthSatellite(line1, line2, name, ts)
            satellites.append((name, sat))

            if len(satellites) >= limit:
                break

    return ts, satellites
#compute positions
def compute_positions(ts, satellites):

    now = ts.now()

    data = []

    for name, sat in satellites:

        geocentric = sat.at(now)
        subpoint = wgs84.subpoint(geocentric)

        data.append({
            "name": name,
            "lat": subpoint.latitude.degrees,
            "lon": subpoint.longitude.degrees,
            "alt_km": subpoint.elevation.km
        })

    return pd.DataFrame(data)
# Closest approach calculation

def closest_approach(ts, satA, satB):

    times = ts.utc(2026, 1, 1, range(0, 3600))

    closest = float("inf")
    closest_time = None

    for t in times:

        posA = satA.at(t).position.km
        posB = satB.at(t).position.km

        distance = np.linalg.norm(posA - posB)

        if distance < closest:
            closest = distance
            closest_time = t

    return closest, closest_time

# Example usage


if __name__ == "__main__":

    ts, satellites = load_satellites()

    df = compute_positions(ts, satellites)

    print(df)

    satA = satellites[0][1]
    satB = satellites[1][1]

    distance, time_of_close = closest_approach(ts, satA, satB)

    print("Closest distance:", distance, "km")
    print("Time:", time_of_close.utc_strftime('%Y-%m-%d %H:%M:%S'))