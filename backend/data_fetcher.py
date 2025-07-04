# backend/data_fetcher.py

import os
import requests
import random
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.aviationstack.com/v1/flights"

def calculate_duration(departure_time: str, arrival_time: str) -> str:
    """
    Estimate duration in "Xh Ym" format from ISO timestamps.
    """
    try:
        if not departure_time or not arrival_time:
            return "N/A"

        dep = datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
        arr = datetime.fromisoformat(arrival_time.replace("Z", "+00:00"))
        duration = arr - dep
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes = remainder // 60
        return f"{int(hours)}h {int(minutes)}m"
    except Exception:
        return "N/A"

def fetch_flight_data(limit=50):
    params = {
        'access_key': API_KEY,
        'limit': limit
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # ❗ Check that the response contains expected data
        if not isinstance(data, dict) or 'data' not in data:
            print("❌ API response is invalid or missing 'data' key:", data)
            return []

        flights = data.get('data', [])
        cleaned = []

        for flight in flights:
            departure = flight.get('departure', {}) or {}
            arrival = flight.get('arrival', {}) or {}
            airline = flight.get('airline', {}) or {}
            aircraft = flight.get('aircraft', {}) or {}

            dep_time = departure.get('scheduled')
            arr_time = arrival.get('scheduled')

            cleaned.append({
                "flight_number": flight.get('flight', {}).get('iata', 'N/A'),
                "airline": airline.get('name', 'N/A'),
                "origin": departure.get('airport', 'N/A'),
                "destination": arrival.get('airport', 'N/A'),
                "departure_time": dep_time or "N/A",
                "arrival_time": arr_time or "N/A",
                "status": flight.get('flight_status', 'N/A'),
                "price": round(random.uniform(100, 1000), 2),  # Mock price
                "duration": calculate_duration(dep_time, arr_time),
                "aircraft_type": aircraft.get('iata', 'N/A')
            })

        return cleaned

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []
