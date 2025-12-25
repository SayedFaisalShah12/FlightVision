import streamlit as st
import pandas as pd
import math

from airport_coords import AIRPORT_COORDS
from api_client import get_live_flights, get_airport_coordinates
from utils import haversine
from prediction import predict_landing_time

st.set_page_config(
    page_title="FlightVision",
    layout="wide"
)

st.title("✈️ FlightVision")

st.write(
    "This system tracks live aircraft positions and predicts landing time "
    "using real-time aviation data and AI-based estimation."
)

# Fetch live flights
flights = get_live_flights(limit=5)

rows = []

for flight in flights:
    live = flight.get("live")
    arrival = flight.get("arrival")
    flight_info = flight.get("flight", {})

    # Live aircraft position must exist
    if live and live.get("latitude") and live.get("longitude"):
        lat1 = live["latitude"]
        lon1 = live["longitude"]

        speed = live.get("speed_horizontal")

        if not speed or speed <= 0:
            speed = 800  # fallback average aircraft speed (km/h)

        distance = None
        eta = None

        # Try to get arrival airport coordinates
        if arrival:
            lat2 = arrival.get("latitude")
            lon2 = arrival.get("longitude")

            if lat2 is not None and lon2 is not None:
                distance = haversine(lat1, lon1, lat2, lon2)
                eta = predict_landing_time(distance, speed)

        # Fallback: estimate remaining distance if arrival is missing
        if distance is None:
            distance = 500  # fallback remaining distance in km (demo-safe)
            eta = predict_landing_time(distance, speed)


        rows.append({
            "Flight": flight_info.get("iata", "N/A"),
            "Latitude": lat1,
            "Longitude": lon1,
            "Speed (km/h)": speed,
            "Distance (km)": round(distance, 2) if distance else None,
            "ETA (minutes)": eta
        })

# Create DataFrame with fixed columns
df = pd.DataFrame(
    rows,
    columns=[
        "Flight",
        "Latitude",
        "Longitude",
        "Speed (km/h)",
        "Distance (km)",
        "ETA (minutes)"
    ]
)

st.subheader("📊 Live Flight Data")
st.dataframe(df, use_container_width=True)


def calculate_eta_km(lat1, lon1, lat2, lon2, speed_kmh=850):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return int((distance / speed_kmh) * 60)

last_flight = flights[-1] if flights else None
if last_flight:
    arrival = last_flight.get("arrival", {})
    arrival_iata = arrival.get("iata")
    st.write("DEBUG arrival IATA:", arrival_iata)
    if arrival_iata and arrival_iata in AIRPORT_COORDS and last_flight.get("live"):
        dest = AIRPORT_COORDS[arrival_iata]
        lat1 = last_flight["live"].get("latitude")
        lon1 = last_flight["live"].get("longitude")
        if lat1 is not None and lon1 is not None:
            eta = calculate_eta_km(lat1, lon1, dest["lat"], dest["lon"])
            st.success(f"🕒 Estimated Time to Arrival: {eta} minutes")
        else:
            st.warning("⚠️ Live coordinates unavailable for ETA.")
    else:
        st.warning("⚠️ ETA prediction unavailable for this destination.")
else:
    st.warning("No flights available to estimate ETA.")


# Map visualization
st.subheader("🗺️ Live Aircraft Positions")

map_df = df.rename(
    columns={
        "Latitude": "latitude",
        "Longitude": "longitude"
    }
)

if not map_df.empty and "latitude" in map_df.columns and "longitude" in map_df.columns:
    st.map(map_df[["latitude", "longitude"]])
else:
    st.warning("No flight location data available.")




    

