# backend/data_fetcher.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.aviationstack.com/v1/flights"

def fetch_flight_data(limit=50):
    params = {
        'access_key': API_KEY,
        'limit': limit
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        flights = data.get('data', [])
        cleaned = []

        for flight in flights:
            cleaned.append({
                "airline": flight.get('airline', {}).get('name', 'N/A'),
                "flight_number": flight.get('flight', {}).get('iata', 'N/A'),
                "departure_airport": flight.get('departure', {}).get('airport', 'N/A'),
                "arrival_airport": flight.get('arrival', {}).get('airport', 'N/A'),
                "departure_time": flight.get('departure', {}).get('scheduled', 'N/A'),
                "arrival_time": flight.get('arrival', {}).get('scheduled', 'N/A'),
                "status": flight.get('flight_status', 'N/A')
            })

        return cleaned

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []
