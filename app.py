import streamlit as st
import pandas as pd
from datetime import datetime, date

from detector import detect_diseases
from schedule import get_schedule
from food_db import get_food_recommendations
from parser import parse_report_text
from db import save_report, get_history
from utils import extract_text_from_image, extract_text_from_pdf
from ai_explainer import explain_report

# ---------------- STREAMLIT CONFIGURATION ----------------
st.set_page_config(
    page_title="HealthPath AI - Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS INJECTIONS ----------------
def inject_custom_css():
    st.markdown("""
        <style>
        /* Import premium font */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Apply font family globally */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Premium Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: var(--secondary-background-color);
            border-right: 1px solid rgba(128, 128, 128, 0.1);
        }
        
        /* Custom Header Brand logo */
        .logo-container {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            padding: 5px 10px;
        }
        .logo-icon {
            font-size: 2.2rem;
        }
        .logo-text {
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--primary-color), #00b4d8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Glassmorphic Cards */
        .health-card {
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .health-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.06);
            border-color: var(--primary-color);
        }
        
        /* Timeline styling for Daily/Weekly Schedules */
        .timeline-item {
            padding-left: 15px;
            border-left: 3px solid var(--primary-color);
            margin-bottom: 12px;
            margin-top: 4px;
        }
        .timeline-time {
            font-weight: 700;
            color: var(--primary-color);
            font-size: 0.95rem;
        }
        .timeline-text {
            color: var(--text-color);
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        /* Food recommendation tags */
        .food-badge {
            background-color: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
            border: 1px solid rgba(76, 175, 80, 0.2);
            border-radius: 8px;
            padding: 10px 14px;
            text-align: center;
            font-weight: 600;
            font-size: 0.95rem;
            display: inline-block;
            margin: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }
        
        /* Metric block custom styles */
        div[data-testid="stMetricValue"] {
            font-weight: 800;
            font-size: 2.2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ---------------- BRANDING SIDEBAR ----------------
st.sidebar.markdown("""
    <div class="logo-container">
        <span class="logo-icon">🩺</span>
        <span class="logo-text">HealthPath AI</span>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation Menu",
    ["Analyze Report", "Weekly Plan", "Insights", "History"]
)

# Initialize Session State values to persist analysis results across tabs
if "user_diseases" not in st.session_state:
    st.session_state["user_diseases"] = None
if "user_data" not in st.session_state:
    st.session_state["user_data"] = None
if "health_score" not in st.session_state:
    st.session_state["health_score"] = None

# Global Branded Header
st.markdown("""
    <div style="margin-bottom: 15px; border-bottom: 1px solid rgba(128,128,128,0.15); padding-bottom: 15px;">
        <span style="font-size: 2.2rem; font-weight: 800; color: var(--primary-color);">🩺 HealthPath AI</span>
        <span style="font-size: 1.1rem; opacity: 0.7; margin-left: 10px;">| Patient Health Assistant</span>
    </div>
""", unsafe_allow_html=True)

# ---------------- ANALYZE REPORT ----------------
if menu == "Analyze Report":
    st.title("📤 Health Report Analysis")
    st.markdown("Upload medical lab reports (PDF/Images) or enter key metrics manually to generate your daily wellness schedule.")
    
    mode = st.radio("Input Method", ["Upload Report", "Manual Entry"], horizontal=True)
    data = {}

    # -------- Upload Mode --------
    if mode == "Upload Report":
        file = st.file_uploader("Upload Lab Report PDF or Image", type=["png", "jpg", "jpeg", "pdf"])
        
        if file:
            with st.spinner("Extracting text from report..."):
                if file.type == "application/pdf":
                    text = extract_text_from_pdf(file)
                else:
                    text = extract_text_from_image(file)

            st.text_area("Extracted Lab Report Text", text, height=180)
            data = parse_report_text(text)
            
            st.subheader("📊 Parsed Lab Values")
            if data:
                st.json(data)
            else:
                st.warning("⚠️ No matching bio-metrics (sugar, HbA1c, hemoglobin, cholesterol, blood pressure) detected in the text. You can enter them manually.")

    # -------- Manual Entry Mode --------
    else:
        st.markdown("Enter your lab report values below:")
        col1, col2 = st.columns(2)
        with col1:
            data["sugar"] = st.number_input("Fasting Blood Sugar (mg/dL)", min_value=0.0, value=0.0, step=5.0)
            data["hba1c"] = st.number_input("HbA1c (%)", min_value=0.0, value=0.0, step=0.1)
            data["hemoglobin"] = st.number_input("Hemoglobin (g/dL)", min_value=0.0, value=0.0, step=0.5)
        with col2:
            data["cholesterol"] = st.number_input("Total Cholesterol (mg/dL)", min_value=0.0, value=0.0, step=10.0)
            data["bp"] = st.number_input("Blood Pressure (Systolic)", min_value=0.0, value=0.0, step=5.0)

    # -------- Generate Plan Button --------
    if st.button("🚀 Generate Health Plan", type="primary", use_container_width=True):
        if not data or sum(data.values()) == 0:
            st.error("Please provide at least one medical metric before generating the schedule.")
        else:
            with st.spinner("Analyzing parameters..."):
                diseases = detect_diseases(data)
                save_report(data, diseases)
                
                # Wellness Score computation
                health_score = max(0, 100 - len(diseases) * 15)
                
                # Persist details in session state
                st.session_state["user_diseases"] = diseases
                st.session_state["user_data"] = data
                st.session_state["health_score"] = health_score
                
                st.success("🎉 Health plan generated successfully! Switch to other tabs to view your customized schedules.")
                st.rerun()

    # -------- Display active analyzed profile if available --------
    if st.session_state["user_diseases"] is not None:
        diseases = st.session_state["user_diseases"]
        data = st.session_state["user_data"]
        health_score = st.session_state["health_score"]
        
        st.markdown("---")
        st.subheader("📋 Active Health Analysis Summary")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("🌿 Wellness Score", f"{health_score}/100")
        with col_m2:
            if not diseases:
                st.success("🟢 No chronic health issues detected! Maintaining normal levels.")
            else:
                st.warning(f"⚠️ Detected Conditions: {', '.join(diseases)}")
        
        # AI Explanation Section
        st.subheader("🧠 Health Insights & Explanation")
        st.info(explain_report(diseases, data))
        
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("📅 Daily Schedule")
            schedule = get_schedule(diseases)
            for time, activity in schedule.items():
                if time != "NOTE" and time != "Rest":
                    st.markdown(f"""
                        <div class="timeline-item">
                            <div class="timeline-time">{time}</div>
                            <div class="timeline-text">{activity}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
        with col_right:
            st.subheader("🍎 Recommended Foods")
            food_list = get_food_recommendations(diseases)
            if food_list:
                for item in food_list:
                    st.markdown(f'<span class="food-badge">🥗 {item}</span>', unsafe_allow_html=True)
            else:
                st.info("No specific food recommendations.")

# ---------------- WEEKLY PLAN ----------------
elif menu == "Weekly Plan":
    st.title("📅 7-Day Personalized Health Plan")
    
    if st.session_state["user_diseases"] is None:
        st.warning("⚠️ **No Active Health Profile Found**")
        st.info("Please navigate to the **Analyze Report** section first, upload a report or enter your metrics manually, and click **Generate Health Plan** to unlock your customized 7-day schedule.")
        
        # Fallback expansion preview
        with st.expander("👀 View Default Base Schedule (Non-customized)"):
            base_schedule = get_schedule([])
            for time, activity in base_schedule.items():
                if time != "NOTE":
                    st.markdown(f"- **{time}** : {activity}")
    else:
        diseases = st.session_state["user_diseases"]
        custom_schedule = get_schedule(diseases)
        
        st.success(f"🗓️ Customized 7-Day Plan generated based on detected conditions: **{', '.join(diseases) if diseases else 'General Wellness'}**")
        
        week = {
            "Monday": custom_schedule,
            "Tuesday": custom_schedule,
            "Wednesday": custom_schedule,
            "Thursday": custom_schedule,
            "Friday": custom_schedule,
            "Saturday": custom_schedule,
            "Sunday": {"Rest Day": "Light walk, hydration, relaxation and sleep hygiene"}
        }
        
        # Display 7-day plan cards
        for day, plan in week.items():
            with st.container():
                st.markdown(f"### 🗓️ {day}")
                for time, activity in plan.items():
                    if time != "NOTE":
                        st.markdown(f"""
                            <div class="timeline-item">
                                <div class="timeline-time">{time}</div>
                                <div class="timeline-text">{activity}</div>
                            </div>
                        """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

# ---------------- INSIGHTS ----------------
elif menu == "Insights":
    st.title("📌 Health Insights Dashboard")
    
    history = get_history()
    total = len(history)
    st.metric("Total Reports Analyzed", total)
    
    if not history:
        st.info("No reports have been analyzed yet. Go to 'Analyze Report' to begin tracking.")
    else:
        latest = history[0]
        
        st.subheader("🧾 Latest Report Snapshot")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Blood Sugar", f"{latest[2]} mg/dL")
        with col2:
            st.metric("HbA1c", f"{latest[3]} %")
        with col3:
            st.metric("Hemoglobin", f"{latest[4]} g/dL")
        with col4:
            st.metric("Cholesterol", f"{latest[5]} mg/dL")
        with col5:
            st.metric("Systolic BP", f"{latest[6]} mmHg")
            
        st.markdown(f"**Analysis Timestamp:** `{latest[1]}`")
        if latest[7]:
            st.warning(f"**Identified Health Conditions:** {latest[7]}")
        else:
            st.success("🟢 **Wellness Status:** Normal range (No conditions identified)")

# ---------------- HISTORY ----------------
elif menu == "History":
    st.title("📜 Patient Analysis History")
    st.markdown("Track your historical lab reports over time.")
    
    history = get_history()
    
    if not history:
        st.info("No historical records found in database.")
    else:
        # Convert sqlite tuples list into a clean Pandas DataFrame for professional rendering
        df_hist = pd.DataFrame(
            history,
            columns=["ID", "Timestamp", "Blood Sugar (mg/dL)", "HbA1c (%)", "Hemoglobin (g/dL)", "Cholesterol (mg/dL)", "Systolic BP", "Identified Conditions"]
        )
        # Display the formatted inventory
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
        
        # Download data logs option
        csv = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete Health Logs as CSV",
            data=csv,
            file_name="healthpath_history.csv",
            mime="text/csv",
            use_container_width=True
        )
