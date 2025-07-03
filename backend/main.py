# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.data_fetcher import fetch_flight_data
from backend.insights_api import generate_insights

app = FastAPI(
    title="Airline Demand API",
    description="API for fetching and analyzing airline flight data.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES

@app.get("/", tags=["Health"])
def root():
    return {"message": "🚀 Airline Demand API is running"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

@app.get("/flights", tags=["Flights"])
def get_flights(limit: int = 50):
    flights = fetch_flight_data(limit=limit)
    return {"flights": flights}

@app.get("/flights/{flight_number}", tags=["Flights"])
def get_flight_by_number(flight_number: str):
    flights = fetch_flight_data(limit=50)
    for flight in flights:
        if flight['flight_number'] == flight_number:
            return {"flight": flight}
    raise HTTPException(status_code=404, detail="Flight not found")

@app.get("/insights", tags=["Insights"])
def get_insights(limit: int = 30):
    flights = fetch_flight_data(limit=limit)
    insights = generate_insights(flights)
    return {"insights": insights}

@app.get("/insights/{flight_number}", tags=["Insights"])
def get_insights_by_flight(flight_number: str):
    flights = fetch_flight_data(limit=50)
    flight_data = next((f for f in flights if f['flight_number'] == flight_number), None)

    if not flight_data:
        raise HTTPException(status_code=404, detail="Flight not found")

    insights = generate_insights([flight_data])
    return {"flight_number": flight_number, "insights": insights}
@app.get("/docs", include_in_schema=False)
def get_docs():
    return {"message": "API documentation is available at /docs"}