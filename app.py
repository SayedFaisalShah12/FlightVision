import streamlit as st
import pandas as pd
from api_client import get_live_flights
from utils import haversine
from prediction import predict_landing_time

st.set_page_config(page_title="AI Flight Predictor", layout="wide")

st.title("✈️ AI Flight Landing Prediction System")

# Fetch flights
flights = get_live_flights(limit=3)

rows = []

for flight in flights:
    live = flight.get("live")
    arrival = flight.get("arrival")
    flight_info = flight.get("flight", {})

    # Check live data first (most reliable)
    if live and live.get("latitude") and live.get("longitude"):
        lat1 = live["latitude"]
        lon1 = live["longitude"]
        speed = live.get("speed_horizontal", 0)

        distance = None
        eta = None

        # Arrival latitude/longitude often missing in AviationStack
        if arrival and arrival.get("latitude") and arrival.get("longitude"):
            lat2 = float(arrival["latitude"])
            lon2 = float(arrival["longitude"])

            distance = haversine(lat1, lon1, lat2, lon2)
            eta = predict_landing_time(distance, speed)

        rows.append({
            "Flight": flight_info.get("iata", "N/A"),
            "Latitude": lat1,
            "Longitude": lon1,
            "Speed (km/h)": speed,
            "Distance (km)": round(distance, 2) if distance else None,
            "ETA (minutes)": eta
        })

# Always define columns (important!)
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
st.dataframe(df)

# Graph with safety check
if not df.empty and df["ETA (minutes)"].notna().any():
    st.subheader("📈 ETA Comparison")
    st.bar_chart(
        df.dropna(subset=["ETA (minutes)"]).set_index("Flight")["ETA (minutes)"]
    )
else:
    st.warning("⚠️ ETA prediction not available (arrival coordinates missing).")

# Map visualization
if not df.empty:
    st.subheader("🗺️ Live Aircraft Positions")
    st.map(df[["Latitude", "Longitude"]])
