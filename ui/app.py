import streamlit as st
import requests
import plotly.graph_objects as go
import time

# ======================================================
# BACKEND CONFIG
# ======================================================
API_URL = "https://ai-career-risk-analyzer.onrender.com/analyze-career/"
HEALTH_URL = "https://ai-career-risk-analyzer.onrender.com/healthz"

# ------------------------------------------------------
# Wake backend silently (Render cold start fix)
# ------------------------------------------------------
if "backend_warm" not in st.session_state:
    try:
        requests.get(HEALTH_URL, timeout=5)
        st.session_state.backend_warm = True
    except:
        pass


def call_backend(payload):
    """
    Calls backend with retry logic to handle Render cold start.
    Returns (result_json, backend_used: bool)
    """
    for attempt in range(3):  # Increased retries
        try:
            response = requests.post(API_URL, json=payload, timeout=45)
            if response.status_code == 200:
                return response.json(), True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            time.sleep(10)  # Wait longer for cold start
    return None, False


# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Career Risk Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
<style>
.main { background-color: #0e1117; }
.stMetric { background-color: #1e2130; padding: 20px; border-radius: 10px; }
.advice-card { padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 5px solid; }
.low-risk { border-left-color: #28a745; background-color: #1a2e1a; }
.medium-risk { border-left-color: #ffa500; background-color: #2e2a1a; }
.high-risk { border-left-color: #ff4b4b; background-color: #2e1a1a; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR INPUTS
# ======================================================
with st.sidebar:
    st.title("🎯 Career Parameters")
    st.markdown("Adjust details to analyze AI automation risk.")

    job_title = st.text_input("Job Title", "Software Engineer")

    industry = st.selectbox(
        "Industry",
        [
            "IT", "Finance", "Healthcare", "Manufacturing",
            "Education", "Retail", "Entertainment", "Transportation"
        ]
    )

    experience = st.slider(
        "Experience (Years)",
        min_value=0,
        max_value=30,
        value=5
    )

    ai_impact = st.selectbox(
        "AI Integration Level",
        ["Low", "Moderate", "High"]
    )

    projected_openings = st.number_input(
        "Projected Openings (2030)",
        min_value=0,
        max_value=100000,
        value=15000,
        step=1000
    )

    remote_ratio = st.slider(
        "Remote Work Ratio (%)",
        min_value=0,
        max_value=100,
        value=75
    )

    analyze_btn = st.button("🔥 Analyze Career Risk", use_container_width=True)

# ======================================================
# MAIN CONTENT
# ======================================================
st.title("🎯 AI Career Risk & Job Market Intelligence")
st.markdown("### Interactive Dashboard for Future-Proofing Your Career")

if analyze_btn:
    payload = {
        "job_title": job_title,
        "experience_required_years": experience,
        "ai_impact_level": ai_impact,
        "projected_openings_2030": projected_openings,
        "remote_work_ratio_percent": remote_ratio
    }

    with st.spinner("🤖 Analyzing AI Impact..."):
        result, backend_used = call_backend(payload)

    # --------------------------------------------------
    # FALLBACK (Demo Mode)
    # --------------------------------------------------
    if not backend_used:
        result = {
            "automation_risk_percent": 48,
            "risk_category": "Medium"
        }
        st.warning("⚠️ Backend cold-start detected. Showing demo results.")

    risk_score = result["automation_risk_percent"]
    risk_cat = result["risk_category"]

    col1, col2 = st.columns([1, 2])

    # ==================================================
    # METRICS + GAUGE
    # ==================================================
    with col1:
        st.subheader("📊 Risk Score")
        st.metric("Automation Risk", f"{risk_score}%", risk_cat)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Automation Risk Level"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": "#28a745" if risk_score < 30
                    else "#ffa500" if risk_score < 60
                    else "#ff4b4b"
                },
                "steps": [
                    {"range": [0, 30], "color": "rgba(40,167,69,0.3)"},
                    {"range": [30, 60], "color": "rgba(255,165,0,0.3)"},
                    {"range": [60, 100], "color": "rgba(255,75,75,0.3)"}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ==================================================
    # INDUSTRY BENCHMARK
    # ==================================================
    with col2:
        st.subheader("📈 Industry Benchmark")

        industry_avg = {
            "IT": 45, "Finance": 55, "Healthcare": 25,
            "Manufacturing": 75, "Education": 35,
            "Retail": 80, "Entertainment": 50,
            "Transportation": 85
        }.get(industry, 50)

        fig_bar = go.Figure()
        fig_bar.add_bar(
            x=["Your Role", f"{industry} Avg"],
            y=[risk_score, industry_avg],
            marker_color=["#ff4b4b", "#1f77b4"]
        )
        fig_bar.update_layout(
            yaxis_title="Automation Risk (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ==================================================
    # AI ADVICE
    # ==================================================
    st.divider()
    st.subheader("💡 AI-Proofing Strategy")

    advice_style = (
        "low-risk" if risk_cat == "Low"
        else "medium-risk" if risk_cat == "Medium"
        else "high-risk"
    )

    advice_text = {
        "Low": "Your role is resilient. Focus on deep expertise and AI-assisted productivity.",
        "Medium": "Upskill in Human-AI collaboration, leadership, and domain specialization.",
        "High": "Consider reskilling into strategic, creative, or AI-oversight roles."
    }

    st.markdown(f"""
    <div class="advice-card {advice_style}">
        <h4>Recommendation for {job_title}</h4>
        <p>{advice_text[risk_cat]}</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👈 Enter details in the sidebar and click **Analyze Career Risk**.")
    c1, c2, c3 = st.columns(3)
    c1.markdown("### 🔍 Accurate Prediction\nML-based automation risk scoring.")
    c2.markdown("### 📊 Benchmarking\nCompare with industry averages.")
    c3.markdown("### 🛡️ Future-Proofing\nActionable AI career advice.")
