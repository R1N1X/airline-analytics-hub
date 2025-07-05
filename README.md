# Airline Analytics Hub

A full-stack airline market analytics dashboard built using **Streamlit** (frontend) and **FastAPI** (backend), enhanced with **OpenAI GPT** for smart insights and **AviationStack API** for real-time flight data.

---

## Features

- Live flight data via AviationStack API  
- Interactive analytics dashboard built in Streamlit  
- AI-powered market insights with OpenAI GPT  
- Route and airline visualizations with charts and KPIs  
- Flight-level intelligence and insights  
- Export filtered data to CSV  
- Auto-refresh mode (30-second interval)  
- Clean, responsive UI using custom HTML/CSS within Streamlit  

---

## Tech Stack

| Layer       | Tool/Service             |
|-------------|--------------------------|
| Frontend    | [Streamlit](https://streamlit.io) |
| Backend     | [FastAPI](https://fastapi.tiangolo.com) |
| AI Engine   | [OpenAI GPT-3.5](https://platform.openai.com) |
| Flight Data | [AviationStack API](https://aviationstack.com/) |
| Styling     | HTML + CSS inside Streamlit |
| Deployment  | [Render](https://render.com), [Streamlit Cloud](https://streamlit.io/cloud) |

----

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/R1N1X/airline-analytics-hub.git
cd airline-analytics-hub
```

### 2️. Setup Environment Variables:
*Create a .env file in the root directory*:
API_KEY=your_aviationstack_api_key
OPENAI_API_KEY=your_openai_api_key

-----

### 3️. Create & Activate Virtual Environment:
*Windows OS*

```bash
python -m venv .venv
.venv\Scripts\activate
```
*Mac OS*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

###  4️. Install Requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5️. Run the Application:
*Run both backend and frontend in parallel*:

```bash
# Terminal 1: Run FastAPI backend
uvicorn backend.main:app --reload
# Access backend docs: http://127.0.0.1:8000/docs


# Terminal 2: Run Streamlit frontend
streamlit run frontend/dashboard.py
# Access frontend dashboard: http://localhost:8501

```

### Made by @R1N1X
