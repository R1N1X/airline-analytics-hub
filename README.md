# ✈️ Airline Analytics Hub

A full-stack airline market analytics dashboard built with Streamlit and FastAPI, powered by OpenAI GPT for intelligent insights and **AviationStack API** for real-time flight data.



---

## 📊 Features

- **Live Flight Data** — powered by AviationStack
- **Interactive Dashboard** — Streamlit-based UI
- **AI Market Insights** — OpenAI GPT-driven intelligence
- **Route & Airline Analytics** — charts, KPIs, deep dives
- **Flight-level Analysis** —  individual flight summaries
- **Export & Filters ** — download CSV, filter flights
- **Auto-Refresh Mode ** — real-time updates every 30s

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

### 1️⃣ Clone the Repo:

```bash
git clone https://github.com/R1N1X/airline-analytics-hub.git
cd airline-analytics-hub
```
### 2️⃣ Setup Environment Variables:
*Create a .env file in the root directory*:
API_KEY=your_aviationstack_api_key
OPENAI_API_KEY=your_openai_api_key

-----

### 3️⃣ Create & Activate Virtual Environment:
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

###  4️⃣ Install Requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5️⃣ Run the Application:
*Run both backend and frontend in parallel*:

```bash
# ▶️ Start the FastAPI backend (localhost:8000)

# ▶️ Start the Streamlit frontend (localhost:8501)
streamlit run dashboard.py

```
