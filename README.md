# ✈️ Airline Analytics Hub

A full-stack airline market analytics dashboard built using **Streamlit** (frontend) and **FastAPI** (backend), enhanced with **OpenAI GPT** for smart insights and **AviationStack API** for real-time flight data.



---

## 📊 Features

- **Live Flight Data** — from AviationStack API
- **Interactive Analytics Dashboard** — built with Streamlit
- **AI-Powered Market Insights** — via OpenAI GPT
- **Route & Airline Visualizations** — KPIs, charts, route heatmaps
- **Flight-level Intelligence** — individual flight summaries
- **Export to CSV** — with filterable, sortable tables
- **Auto-Refresh Mode** — auto-updates every 30 seconds
- **Clean UI** — with HTML + CSS styling


---

## 🧱 Tech Stack

| Layer       | Tool/Service         |
|-------------|----------------------|
| Frontend    | [Streamlit](https://streamlit.io) |
| Backend     | [FastAPI](https://fastapi.tiangolo.com) |
| AI Engine   | [OpenAI GPT-3.5](https://platform.openai.com/) |
| Flight Data | [AviationStack API](https://aviationstack.com/) |
| Styling     | HTML + CSS in Streamlit |
| Deployment  | [Render](https://render.com) + [Streamlit Cloud](https://streamlit.io/cloud) |

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
# ▶️ Start FastAPI backend
uvicorn backend.main:app --reload  # http://127.0.0.1:8000

# ▶️ Start Streamlit frontend
streamlit run frontend/dashboard.py  # http://localhost:8501

```

### Made by @R1N1X
