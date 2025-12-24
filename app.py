import streamlit as st
import pandas as pd

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
        if arrival and arrival.get("iata"):
            lat2, lon2 = get_airport_coordinates(arrival["iata"])

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

# ETA Graph
if not df.empty and df["ETA (minutes)"].notna().any():
    st.subheader("📈 Estimated Time of Arrival (ETA)")
    st.bar_chart(
        df.dropna(subset=["ETA (minutes)"])
          .set_index("Flight")["ETA (minutes)"]
    )
else:
    st.warning("⚠️ ETA prediction unavailable for current flights.")

# Map visualization
if not df.empty:
    st.subheader("🗺️ Live Aircraft Positions")
    st.map(df[["Latitude", "Longitude"]])

