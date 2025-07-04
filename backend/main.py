from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ✅ Keep these imports assuming you're running from root
from data_fetcher import fetch_flight_data
from insights_api import generate_insights

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Airline Demand API",
    description="API for fetching and analyzing airline flight data.",
    version="1.0.0"
)

# ✅ Enable CORS (for Streamlit frontend to access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health routes
@app.get("/", tags=["Health"])
def root():
    return {"message": "🚀 Airline Demand API is running"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

# ✅ Flights route
@app.get("/flights", tags=["Flights"])
def get_flights(limit: int = 50):
    flights = fetch_flight_data(limit=limit)
    return {"flights": flights}

@app.get("/flights/{flight_number}", tags=["Flights"])
def get_flight_by_number(flight_number: str):
    flights = fetch_flight_data(limit=100)
    for flight in flights:
        if flight.get('flight_number') == flight_number:
            return {"flight": flight}
    raise HTTPException(status_code=404, detail="Flight not found")

# ✅ Insights routes
@app.get("/insights", tags=["Insights"])
def get_insights(limit: int = 30):
    flights = fetch_flight_data(limit=limit)
    insights = generate_insights(flights)
    return {"insights": insights}

@app.get("/insights/{flight_number}", tags=["Insights"])
def get_insights_by_flight(flight_number: str):
    flights = fetch_flight_data(limit=100)
    flight_data = next((f for f in flights if f.get('flight_number') == flight_number), None)

    if not flight_data:
        raise HTTPException(status_code=404, detail="Flight not found")

    insights = generate_insights([flight_data])
    return {"flight_number": flight_number, "insights": insights}

@app.get("/insights/summary", tags=["Insights"])
def get_insights_summary(limit: int = 30):
    flights = fetch_flight_data(limit=limit)
    insights = generate_insights(flights)

    summary = {
        "total_flights": len(flights),
        "average_delay": round(
            sum(f.get('delay', 0) for f in flights) / len(flights), 2
        ) if flights else 0,
        "most_delayed_flight": max(flights, key=lambda x: x.get('delay', 0), default=None)
    }

    return {"summary": summary, "insights": insights}
