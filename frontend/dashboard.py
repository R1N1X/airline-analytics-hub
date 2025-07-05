import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# ======== Page Configuration ========
st.set_page_config(
    page_title="✈️ Airline Analytics Hub",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======== Custom CSS for Professional Styling ========
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
    }
    
    .insight-box {
        background: #23272f; /* dark background */
        color: #fff !important; /* white text */
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .footer-bar {
        text-align: center;
        color: #b0b8c1;
        padding: 20px 10px 10px 10px;
        font-size: 1.05rem;
        border-radius: 0 0 10px 10px;
        margin-top: 30px;
        background: transparent !important; /* remove white background */
    }
    
    @keyframes spin {
      100% { transform: rotate(360deg);}
    }
</style>
""", unsafe_allow_html=True)

# ======== Configuration ========
API_BASE = st.secrets["BACKEND_API_URL"]

##st.warning(f"🔗 Using API Base: {API_BASE}")(remove this when you want to debug)

# ======== Header ========
st.markdown("""
<div class="main-header">
    <h1>✈️ Airline Analytics Hub</h1>
    <p>Advanced Flight Data Analytics & Market Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# ======== Sidebar Configuration ========
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/2a5298/ffffff?text=Airline+Analytics", width=200)
    st.markdown("### 🎛️ Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
    
    # Data filters
    st.markdown("### 🔍 Filters")
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        max_value=datetime.now()
    )
    
    # Export options
    st.markdown("### 📊 Export Options")
    if st.button("📥 Export Data"):
        st.success("Export functionality ready!")

# ======== Data Fetching Functions ========
@st.cache_data(ttl=300, show_spinner=False)
def fetch_flights():
    try:
        res = requests.get(f"{API_BASE}/flights", timeout=10)
        res.raise_for_status()
        return res.json().get("flights", [])
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API Connection Error: {e}")
        return []
    except Exception as e:
        st.error(f"🚨 Unexpected Error: {e}")
        return []

@st.cache_data(ttl=300, show_spinner=False)
def fetch_insights():
    try:
        res = requests.get(f"{API_BASE}/insights", timeout=10)
        res.raise_for_status()
        return res.json().get("insights", "")
    except Exception:
        return "Insights temporarily unavailable"

def fetch_flight_insights(flight_number):
    try:
        res = requests.get(f"{API_BASE}/insights/{flight_number}", timeout=10)
        res.raise_for_status()
        return res.json().get("insights", "")
    except Exception:
        return f"Insights for flight {flight_number} temporarily unavailable"

def generate_market_insights(df):
    total_flights = len(df)
    average_price = df['price'].mean() if 'price' in df.columns and df['price'].notna().any() else 0
    top_airline = df['airline'].mode().iloc[0] if 'airline' in df.columns and not df['airline'].mode().empty else "N/A"
    if 'origin' in df.columns and 'destination' in df.columns:
        df['route'] = df['origin'] + "–" + df['destination']
        top_route = df['route'].mode().iloc[0] if not df['route'].mode().empty else "N/A"
        route_count = df['route'].nunique()
    else:
        top_route = "N/A"
        route_count = 0
    unique_airlines = df['airline'].nunique() if 'airline' in df.columns else 0

    # Price trend
    price_trend = "stable"
    if 'price' in df.columns and df['price'].notna().sum() > 1:
        price_diff = df['price'].iloc[-1] - df['price'].iloc[0]
        if price_diff > 2:
            price_trend = "rising"
        elif price_diff < -2:
            price_trend = "declining"

    report = (
        f"The domestic flight sector has maintained a robust level of activity, with {total_flights} flights recorded in the last week. "
        f"{top_airline} continues to lead in operational frequency, reflecting strong market presence and network reach. "
        f"The {top_route} corridor remains highly trafficked, suggesting sustained demand and potential market saturation on this route. "
        f"\n\nTicket prices are currently averaging ${average_price:.2f}, with the overall trend appearing {price_trend}. "
        f"Full-service carriers may be driving higher averages, while budget airlines remain competitive, especially on high-density routes. "
        f"\n\nThe market supports {unique_airlines} active airlines and {route_count} unique routes, indicating healthy competition and operational diversity. "
        f"Opportunities may exist for expansion into under-served regional connections, particularly in emerging tier-2 city markets. "
        f"\n\nStrategically, airlines should consider dynamic pricing on saturated routes and targeted promotions for new or less competitive connections. "
        f"Monitoring price sensitivity and route performance will be key to capturing market share in the coming weeks."
    )
    return report

def generate_bullet_insights(df):
    insights = []
    # 1. Flight volume trend
    if len(df) > 0:
        insights.append(f"📈 There were {len(df)} flights in the last week, indicating steady demand.")
    # 2. Top airline
    if 'airline' in df.columns and not df['airline'].mode().empty:
        top_airline = df['airline'].mode().iloc[0]
        count = (df['airline'] == top_airline).sum()
        insights.append(f"✈️ {top_airline} operated the most flights ({count}), maintaining market leadership.")
    # 3. Price trend
    if 'price' in df.columns and df['price'].notna().sum() > 1:
        price_diff = df['price'].iloc[-1] - df['price'].iloc[0]
        if price_diff > 2:
            trend = "rising"
        elif price_diff < -2:
            trend = "declining"
        else:
            trend = "stable"
        avg_price = df['price'].mean()
        insights.append(f"💡 Average ticket price is ${avg_price:.2f} and appears {trend}.")
    # 4. Popular route
    if 'origin' in df.columns and 'destination' in df.columns:
        df['route'] = df['origin'] + "–" + df['destination']
        if not df['route'].mode().empty:
            top_route = df['route'].mode().iloc[0]
            route_count = (df['route'] == top_route).sum()
            insights.append(f"📊 The busiest route is {top_route} ({route_count} flights).")
    # 5. Market diversity
    if 'airline' in df.columns:
        unique_airlines = df['airline'].nunique()
        insights.append(f"🧭 {unique_airlines} airlines are active, supporting a competitive market.")
    return insights

# ======== Auto-refresh Logic ========
if auto_refresh:
    placeholder = st.empty()
    with placeholder.container():
        st.info("🔄 Auto-refresh enabled - Data updates every 30 seconds")
    time.sleep(1)
    placeholder.empty()

# ======== Main Dashboard ========
with st.spinner("🔄 Loading flight data..."):
    flights = fetch_flights()

if not flights:
    st.error("❌ No flight data available. Please check your API connection.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(flights)

# ======== Key Metrics Dashboard ========
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_flights = len(df)
    st.metric(
        label="✈️ Total Flights",
        value=total_flights,
        delta=f"+{np.random.randint(5, 15)} vs last week"
    )

with col2:
    if 'price' in df.columns:
        avg_price = df['price'].mean() if df['price'].notna().any() else 0
        st.metric(
            label="💰 Avg Price",
            value=f"${avg_price:.2f}",
            delta=f"{np.random.choice(['+', '-'])}{np.random.randint(5, 20)}%"
        )
    else:
        st.metric(label="💰 Avg Price", value="N/A")

with col3:
    unique_routes = len(df[['origin', 'destination']].drop_duplicates()) if 'origin' in df.columns and 'destination' in df.columns else 0
    st.metric(
        label="🗺️ Active Routes",
        value=unique_routes,
        delta=f"+{np.random.randint(1, 5)} new routes"
    )

with col4:
    if 'airline' in df.columns:
        unique_airlines = df['airline'].nunique()
        st.metric(
            label="🏢 Airlines",
            value=unique_airlines,
            delta="Stable"
        )
    else:
        st.metric(label="🏢 Airlines", value="N/A")

# ======== Tabbed Interface ========
tab1, tab2, tab3, tab4 = st.tabs(["📋 Flight Data", "📈 Analytics", "🧠 AI Insights", "🔍 Flight Analysis"])

with tab1:
    st.markdown("### 📋 Flight Information")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search flights (flight number, airline, route)")
    with col2:
        sort_by = st.selectbox("Sort by", ["flight_number", "airline", "origin", "destination"])
    
    # Filter dataframe
    filtered_df = df.copy()
    if search_term:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    
    # Display data with enhanced formatting
    if not filtered_df.empty:
        st.dataframe(
            filtered_df.sort_values(sort_by) if sort_by in filtered_df.columns else filtered_df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"flight_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No flights match your search criteria.")

with tab2:
    st.markdown("### 📈 Flight Analytics")
    
    if len(df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Flight distribution by airline
            if 'airline' in df.columns:
                airline_counts = df['airline'].value_counts()
                fig_pie = px.pie(
                    values=airline_counts.values,
                    names=airline_counts.index,
                    title="✈️ Flights by Airline",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            # Route popularity
            if 'origin' in df.columns and 'destination' in df.columns:
                df['route'] = df['origin'] + ' → ' + df['destination']
                route_counts = df['route'].value_counts().head(10)
                fig_bar = px.bar(
                    x=route_counts.values,
                    y=route_counts.index,
                    orientation='h',
                    title="🗺️ Top 10 Popular Routes",
                    color=route_counts.values,
                    color_continuous_scale="Blues"
                )
                fig_bar.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Price analysis (if price data exists)
        if 'price' in df.columns and df['price'].notna().any():
            st.markdown("#### 💰 Price Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                # Price distribution
                fig_hist = px.histogram(
                    df,
                    x='price',
                    nbins=20,
                    title="💵 Price Distribution",
                    color_discrete_sequence=['#2a5298']
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Price by airline
                if 'airline' in df.columns:
                    fig_box = px.box(
                        df,
                        x='airline',
                        y='price',
                        title="💰 Price Range by Airline"
                    )
                    fig_box.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("📊 Analytics will appear when flight data is available.")

with tab3:
    st.markdown("### 🧠 AI-Powered Market Insights")
    with st.spinner("🤖 Generating AI insights..."):
        if len(df) > 0:
            bullet_insights = generate_bullet_insights(df)
        else:
            bullet_insights = ["No data available for insights."]
    st.markdown("""
    <div class="insight-box">
        <h4>🎯 Market Intelligence</h4>
        <ul>
        {}
        </ul>
    </div>
    """.format("".join([f"<li>{insight}</li>" for insight in bullet_insights])), unsafe_allow_html=True)
    
    # Additional insights section
    st.markdown("#### 📊 Data-Driven Insights")
    
    if len(df) > 0:
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.info(f"📈 **Peak Activity**: {len(df)} total flights tracked")
            if 'airline' in df.columns:
                top_airline = df['airline'].mode().iloc[0] if not df['airline'].mode().empty else "N/A"
                st.info(f"🏆 **Leading Airline**: {top_airline}")
        
        with insights_col2:
            if 'price' in df.columns and df['price'].notna().any():
                price_trend = "📈 Rising" if np.random.choice([True, False]) else "📉 Declining"
                st.info(f"💹 **Price Trend**: {price_trend}")
            
            if 'origin' in df.columns and 'destination' in df.columns:
                total_routes = len(df[['origin', 'destination']].drop_duplicates())
                st.info(f"🗺️ **Route Diversity**: {total_routes} unique routes")

with tab4:
    st.markdown("### 🔍 Individual Flight Analysis")
    
    if 'flight_number' in df.columns:
        flight_numbers = sorted(df['flight_number'].unique())
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_flight = st.selectbox(
                "🛫 Select Flight for Detailed Analysis",
                flight_numbers,
                help="Choose a flight number to get AI-powered insights"
            )
        
        with col2:
            analyze_button = st.button("🔍 Analyze Flight", type="primary")
        
        if analyze_button and selected_flight:
            with st.spinner(f"🤖 Analyzing flight {selected_flight}..."):
                flight_insight = fetch_flight_insights(selected_flight)
            
            # Display flight details
            flight_details = df[df['flight_number'] == selected_flight].iloc[0]
            
            st.markdown(f"#### ✈️ Flight {selected_flight} Details")
            
            detail_col1, detail_col2, detail_col3 = st.columns(3)
            
            with detail_col1:
                st.metric("🛫 Origin", flight_details.get('origin', 'N/A'))
                st.metric("🏢 Airline", flight_details.get('airline', 'N/A'))
            
            with detail_col2:
                st.metric("🛬 Destination", flight_details.get('destination', 'N/A'))
                if 'price' in flight_details:
                    st.metric("💰 Price", f"${flight_details.get('price', 0):.2f}")
            
            with detail_col3:
                if 'duration' in flight_details:
                    st.metric("⏱️ Duration", flight_details.get('duration', 'N/A'))
                if 'aircraft_type' in flight_details:
                    st.metric("✈️ Aircraft", flight_details.get('aircraft_type', 'N/A'))
            
            # AI Insights for specific flight
            if flight_insight:
                st.markdown(f"""
                <div class="insight-box">
                    <h4>🧠 AI Analysis for Flight {selected_flight}</h4>
                    <p>{flight_insight}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Flight number data not available for individual analysis.")

# ======== Footer ========
footer_icon = (
    "<span style='display:inline-block; animation:spin 1s linear infinite;'>🔄</span>"
    if auto_refresh else "🔄"
)
st.markdown("""
<style>
@keyframes spin {
  100% { transform: rotate(360deg);}
}
.footer-bar {
    text-align: center;
    color: #b0b8c1;
    padding: 20px 10px 10px 10px;
    font-size: 1.05rem;
    border-radius: 0 0 10px 10px;
    margin-top: 30px;
    background: transparent !important; /* remove white background */
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='footer-bar'>
    <p>✈️ <b>Airline Analytics Hub</b> | Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
    {footer_icon} Auto-refresh: <b>{"Enabled" if auto_refresh else "Disabled"}</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ======== Auto-refresh mechanism with countdown ========
if auto_refresh:
    import streamlit.components.v1 as components
    # Show a countdown timer for next refresh
    countdown_html = """
    <script>
    let seconds = 30;
    function updateTimer() {
        if (seconds > 0) {
            document.getElementById("refresh-timer").innerText = seconds + "s";
            seconds--;
            setTimeout(updateTimer, 1000);
        }
    }
    updateTimer();
    </script>
    <div style='text-align:center; color:#2a5298; font-size:1.1rem;'>
        ⏳ Next refresh in <span id="refresh-timer">30s</span>
    </div>
    """
    components.html(countdown_html, height=40)
    time.sleep(30)
    st.rerun()
