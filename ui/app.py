import streamlit as st
import requests
import plotly.graph_objects as go

# ===============================
# CONFIG
# ===============================
API_URL = "https://ai-career-risk-analyzer.onrender.com/analyze-career/"
REQUEST_TIMEOUT = 60  # handles Render cold start

st.set_page_config(
    page_title="AI Career Risk Intelligence",
    page_icon="🎯",
    layout="wide"
)

# ===============================
# CUSTOM CSS
# ===============================
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

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.title("🎯 Career Parameters")

    job_title = st.text_input("Job Title", "Software Engineer")
    industry = st.selectbox(
        "Industry",
        ["IT", "Finance", "Healthcare", "Manufacturing", "Education", "Retail", "Entertainment", "Transportation"]
    )
    experience = st.slider("Experience (Years)", 0, 30, 5)
    ai_impact = st.selectbox("AI Integration Level", ["Low", "Moderate", "High"])
    projected_openings = st.number_input("Projected Openings (2030)", 0, 100000, 15000, step=1000)
    remote_ratio = st.slider("Remote Work Ratio (%)", 0, 100, 75)

    analyze_btn = st.button("🔥 Analyze Career Risk", use_container_width=True)

# ===============================
# MAIN
# ===============================
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

    result = None
    backend_used = True

    try:
        with st.spinner("🤖 Analyzing AI Impact..."):
            response = requests.post(API_URL, json=payload, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            result = response.json()
        else:
            backend_used = False

    except Exception:
        backend_used = False

    # ===============================
    # FALLBACK (DEMO MODE)
    # ===============================
    if not backend_used:
        result = {
            "automation_risk_percent": 48,
            "risk_category": "Medium"
        }
        st.warning("⚠️ Backend unavailable (Render sleeping). Showing demo results.")

    risk_score = result["automation_risk_percent"]
    risk_cat = result["risk_category"]

    col1, col2 = st.columns([1, 2])

    # ===============================
    # METRICS
    # ===============================
    with col1:
        st.subheader("📊 Risk Score")
        st.metric("Automation Risk", f"{risk_score}%", risk_cat)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Automation Risk Level"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#28a745" if risk_score < 30 else "#ffa500" if risk_score < 60 else "#ff4b4b"},
            }
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "white"})
        st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # BENCHMARK
    # ===============================
    with col2:
        industry_avg = {
            "IT": 45, "Finance": 55, "Healthcare": 25,
            "Manufacturing": 75, "Education": 35,
            "Retail": 80, "Entertainment": 50,
            "Transportation": 85
        }.get(industry, 50)

        fig_bar = go.Figure()
        fig_bar.add_bar(x=["Your Role", f"{industry} Avg"], y=[risk_score, industry_avg])
        fig_bar.update_layout(
            yaxis_title="Automation Risk (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ===============================
    # ADVICE
    # ===============================
    st.divider()
    advice_style = "low-risk" if risk_cat == "Low" else "medium-risk" if risk_cat == "Medium" else "high-risk"
    advice_text = {
        "Low": "Your role is resilient. Focus on deep expertise and AI-assisted productivity.",
        "Medium": "Upskill in Human-AI collaboration, leadership, and specialization.",
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
