import requests
from config import API_KEY

BASE_URL = "https://api.aviationstack.com/v1/flights"

def get_live_flights(limit=5):
    params = {
        "access_key": API_KEY,
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()["data"]

def get_airport_coordinates(iata_code):
    url = "https://api.aviationstack.com/v1/airports"
    params = {
        "access_key": API_KEY,
        "iata_code": iata_code
    }

    response = requests.get(url)
    data = response.json().get("data", [])

    if data:
        return float(data[0]["latitude"]), float(data[0]["longitude"])

    return None, None
