import requests
from config import API_KEY

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

