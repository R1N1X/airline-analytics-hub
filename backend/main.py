from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data_fetcher import fetch_flight_data
from insights_api import generate_insights

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

# HEALTH ENDPOINTS
@app.get("/", tags=["Health"])
def root():
    return {"message": "🚀 Airline Demand API is running"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

# FLIGHT DATA
@app.get("/flights", tags=["Flights"])
def get_flights(limit: int = 50):
    flights = fetch_flight_data(limit=limit)
    if not flights:
        return {"flights": [], "message": "❌ No flight data available. Please check your API connection."}
    return {"flights": flights}

@app.get("/flights/{flight_number}", tags=["Flights"])
def get_flight_by_number(flight_number: str):
    flights = fetch_flight_data(limit=100)
    flight = next((f for f in flights if f['flight_number'] == flight_number), None)
    if flight:
        return {"flight": flight}
    raise HTTPException(status_code=404, detail="Flight not found")

# AI INSIGHTS
@app.get("/insights", tags=["Insights"])
def get_insights(limit: int = 30):
    flights = fetch_flight_data(limit=limit)
    result = generate_insights(flights)
    return result

@app.get("/insights/{flight_number}", tags=["Insights"])
def get_insights_by_flight(flight_number: str):
    flights = fetch_flight_data(limit=50)
    flight_data = next((f for f in flights if f['flight_number'] == flight_number), None)

    if not flight_data:
        raise HTTPException(status_code=404, detail="Flight not found")

    result = generate_insights([flight_data])
    result["flight_number"] = flight_number
    return result

# REDIRECT TO SWAGGER DOCS (OPTIONAL)
@app.get("/docs", include_in_schema=False)
def get_docs():
    return {"message": "API documentation is available at /docs"}
@app.get("/redoc", include_in_schema=False)
def get_redoc():
    return {"message": "API documentation is available at /redoc"}
