# ✈️ Airline Analytics Hub

A full-stack airline market analytics dashboard built with **Streamlit** and **FastAPI**, powered by **OpenAI GPT** for intelligent insights and **AviationStack API** for real-time flight data.

---

## 📊 Features

- **Live Flight Data** — from AviationStack
- **Interactive Dashboard** — built in Streamlit
- **AI-Powered Market Insights** — via OpenAI's GPT
- **Route & Airline Analytics** — charts, KPIs, tables
- **Flight-level Deep Dive** — per-flight insights and metrics
- **Export & Filtering** — CSV downloads and multi-filters
- **Auto-Refresh Mode** — real-time updates every 30s

---

## 🧱 Tech Stack

| Layer       | Tool/Service         |
|-------------|----------------------|
| Frontend    | [Streamlit](https://streamlit.io) |
| Backend     | [FastAPI](https://fastapi.tiangolo.com) |
| AI Engine   | [OpenAI GPT-3.5](https://platform.openai.com/) |
| Flight Data | [AviationStack API](https://aviationstack.com/) |
| Styling     | HTML + CSS in Streamlit |
| Deployment  | (Optional) Vercel / Fly.io / Render |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/R1N1X/airline-analytics-hub.git
cd airline-analytics-hub
```
### 2️⃣ Setup Environment Variables
API_KEY=your_aviationstack_api_key
OPENAI_API_KEY=your_openai_api_key

-----

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt

```

###  4️⃣ Run the Application

```bash
▶️ Start the FastAPI backend (port 8000)
uvicorn backend.main:app --reload

▶️ Start the Streamlit frontend (port 8501)
streamlit run dashboard.py

```

