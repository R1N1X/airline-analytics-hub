from typing import List
from collections import Counter
import pandas as pd

class FlightAnalytics:
    def generate_comprehensive_analytics(self, flights: List[dict]) -> dict:
        df = pd.DataFrame(flights)
        summary = {}
        if 'airline' in df.columns:
            summary["flights_by_airline"] = df["airline"].value_counts().to_dict()
        if 'origin' in df.columns and 'destination' in df.columns:
            df["route"] = df["origin"] + " → " + df["destination"]
            summary["popular_routes"] = df["route"].value_counts().head(10).to_dict()
        if 'price' in df.columns and df['price'].notna().any():
            summary["price_stats"] = {
                "average": round(df["price"].mean(), 2),
                "min": round(df["price"].min(), 2),
                "max": round(df["price"].max(), 2)
            }
        return summary

    def analyze_routes(self, flights: List[dict]) -> dict:
        df = pd.DataFrame(flights)
        if 'origin' in df.columns and 'destination' in df.columns:
            df["route"] = df["origin"] + " → " + df["destination"]
            return df["route"].value_counts().to_dict()
        return {}

    def analyze_airlines(self, flights: List[dict]) -> dict:
        df = pd.DataFrame(flights)
        if 'airline' in df.columns:
            return df["airline"].value_counts().to_dict()
        return {}
    def analyze_demand_trends(self, flights: List[dict]) -> dict:
        df = pd.DataFrame(flights)
        if 'departure_time' in df.columns:
            df['departure_time'] = pd.to_datetime(df['departure_time'])
            df.set_index('departure_time', inplace=True)
            demand_trends = df.resample('M').size().to_dict()
            return {str(k): v for k, v in demand_trends.items()}
        return {}
    def analyze_pricing_patterns(self, flights: List[dict]) -> dict:
        df = pd.DataFrame(flights)
        if 'price' in df.columns and df['price'].notna().any():
            price_stats = {
                "average": round(df["price"].mean(), 2),
                "min": round(df["price"].min(), 2),
                "max": round(df["price"].max(), 2)
            }
            return price_stats
        return {}
    def analyze_flight_durations(self, flights: List[dict]) -> dict:    
        df = pd.DataFrame(flights)
        if 'departure_time' in df.columns and 'arrival_time' in df.columns:
            df['departure_time'] = pd.to_datetime(df['departure_time'])
            df['arrival_time'] = pd.to_datetime(df['arrival_time'])
            df['duration'] = (df['arrival_time'] - df['departure_time']).dt.total_seconds() / 3600
            return {
                "average": round(df["duration"].mean(), 2),
                "min": round(df["duration"].min(), 2),
                "max": round(df["duration"].max(), 2)
            }
        return {}
    def analyze_aircraft_types(self, flights: List[dict]) -> dict:
        df = pd.DataFrame(flights)
        if 'aircraft_type' in df.columns:
            return df["aircraft_type"].value_counts().to_dict()
        return {}
    def generate_analytics(self, flights: List[dict]) -> dict:
        analytics = {
            "flights_by_airline": self.analyze_airlines(flights),
            "popular_routes": self.analyze_routes(flights),
            "demand_trends": self.analyze_demand_trends(flights),
            "pricing_patterns": self.analyze_pricing_patterns(flights),
            "flight_durations": self.analyze_flight_durations(flights),
            "aircraft_types": self.analyze_aircraft_types(flights)
        }
        return analytics
def generate_flight_analytics(flights: List[dict]) -> dict:
    analytics = FlightAnalytics()
    return analytics.generate_analytics(flights)
def generate_comprehensive_analytics(flights: List[dict]) -> dict:
    analytics = FlightAnalytics()
    return analytics.generate_comprehensive_analytics(flights)