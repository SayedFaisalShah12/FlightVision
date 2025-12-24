import requests
from config import API_KEY

FLIGHTS_URL = "https://api.aviationstack.com/v1/flights"
AIRPORTS_URL = "https://api.aviationstack.com/v1/airports"


def get_live_flights(limit=5):
    """
    Fetch real-time flight data
    """
    params = {
        "access_key": API_KEY,
        "limit": limit
    }

    response = requests.get(FLIGHTS_URL, params=params)
    response.raise_for_status()
    return response.json().get("data", [])


def get_airport_coordinates(iata_code):
    """
    Fetch latitude & longitude of an airport using IATA code
    """
    params = {
        "access_key": API_KEY,
        "iata_code": iata_code
    }

    response = requests.get(AIRPORTS_URL, params=params)
    response.raise_for_status()
    data = response.json().get("data", [])

    if data:
        lat = data[0].get("latitude")
        lon = data[0].get("longitude")

        if lat is not None and lon is not None:
            return float(lat), float(lon)

    return None, None
