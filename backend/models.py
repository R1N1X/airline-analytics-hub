from typing import List, Optional
from pydantic import BaseModel

class Flight(BaseModel):
    airline: Optional[str]
    flight_number: Optional[str]
    origin: Optional[str]
    destination: Optional[str]
    departure_time: Optional[str]
    arrival_time: Optional[str]
    status: Optional[str]
    price: Optional[float] = None
    duration: Optional[str] = None
    aircraft_type: Optional[str] = None

class FlightResponse(BaseModel):
    flights: List[Flight]
    total_count: int
    timestamp: str
    filters_applied: Optional[dict] = {}

class InsightsResponse(BaseModel):
    insights: str
    data_points: Optional[int] = None
    focus_area: Optional[str] = None
    generated_at: str
    confidence: Optional[int] = None

class AnalyticsResponse(BaseModel):
    analytics: dict
    data_points: int
    generated_at: str
