import streamlit as st
import requests
import plotly.graph_objects as go

# ======================================================
# CONFIG
# ======================================================
# API_BASE = "http://127.0.0.1:8000"

API_BASE = "https://ai-career-risk-analyzer.onrender.com"

st.set_page_config(
    page_title="AI Career Risk Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>
.advice-card {
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    border-left: 5px solid;
}
.low-risk { border-left-color: #28a745; background-color: #1a2e1a; }
.medium-risk { border-left-color: #ffa500; background-color: #2e2a1a; }
.high-risk { border-left-color: #ff4b4b; background-color: #2e1a1a; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.title("🎯 Career Parameters")

    job_title = st.text_input("Job Title", "Software Engineer")
    experience = st.slider("Experience (Years)", 0, 30, 5)
    ai_impact = st.selectbox("AI Integration Level", ["Low", "Moderate", "High"])
    projected_openings = st.number_input(
        "Projected Openings (2030)",
        min_value=0,
        max_value=100000,
        value=15000,
        step=1000
    )
    remote_ratio = st.slider("Remote Work Ratio (%)", 0, 100, 75)

    analyze_btn = st.button("🔥 Analyze Career Risk", width="stretch")

# ======================================================
# HELPERS
# ======================================================
def backend_health_check() -> bool:
    """Check if backend is awake without loading model."""
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def demo_result():
    """Fallback demo result during cold start."""
    return {
        "automation_risk_percent": 42,
        "risk_category": "Medium"
    }

# ======================================================
# MAIN UI
# ======================================================
st.title("🎯 AI Career Risk & Job Market Intelligence")
st.markdown("### Future-proof your career against AI automation")

if analyze_btn:
    payload = {
        "job_title": job_title,
        "experience_required_years": experience,
        "ai_impact_level": ai_impact,
        "projected_openings_2030": projected_openings,
        "remote_work_ratio_percent": remote_ratio
    }

    with st.spinner("🤖 Checking backend status..."):
        if not backend_health_check():
            st.warning("⚠️ Backend cold-start detected. Showing demo results.")
            result = demo_result()
            st.write("Demo Result:")
            st.json(result)

        else:
            try:
                response = requests.post(
                    f"{API_BASE}/analyze-career/",
                    json=payload,
                    timeout=30
                )

                # 🔍 SHOW RAW RESPONSE INFO
                st.write("🔍 Response status code:", response.status_code)
                st.write("🔍 Response headers:", response.headers)

                # response.raise_for_status()

                result = response.json()

                # 🔍 SHOW ACTUAL BACKEND RESULT
                st.success("✅ Backend response received")
                st.write("📦 Backend Result:")
                st.json(result)

            except Exception as e:
                st.error("❌ Exception occurred while calling backend")
                st.exception(e)

                st.warning("⚠️ Backend waking up. Showing demo results.")
                result = demo_result()
                st.write("Demo Result:")
                st.json(result)


    # with st.spinner("🤖 Checking backend status..."):
    #     if not backend_health_check():
    #         st.warning("⚠️ Backend cold-start detected. Showing demo results.")
    #         result = demo_result()
    #     else:
    #         try:
    #             response = requests.post(
    #                 f"{API_BASE}/analyze-career/",
    #                 json=payload,
    #                 timeout=30
    #             )

    #             response.raise_for_status()
    #             print(response)
    #             result = response.json()
    #             print(result)
    #         except Exception:
    #             st.warning("⚠️ Backend waking up. Showing demo results.")
    #             result = demo_result()

    risk_score = result["automation_risk_percent"]
    risk_cat = result["risk_category"]

    col1, col2 = st.columns([1, 2])

    # ==================================================
    # GAUGE
    # ==================================================
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Automation Risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": "#28a745"
                    if risk_score < 30
                    else "#ffa500"
                    if risk_score < 60
                    else "#ff4b4b"
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )
        st.plotly_chart(fig, width="stretch")

    # ==================================================
    # ADVICE
    # ==================================================
    with col2:
        style = (
            "low-risk"
            if risk_cat == "Low"
            else "medium-risk"
            if risk_cat == "Medium"
            else "high-risk"
        )

        advice = {
            "Low": "Your role is resilient. Focus on deep expertise and AI-assisted productivity.",
            "Medium": "Upskill in human-AI collaboration, leadership, and domain specialization.",
            "High": "Consider reskilling into strategic, creative, or AI-oversight roles."
        }

        st.markdown(f"""
        <div class="advice-card {style}">
            <h4>Recommendation for {job_title}</h4>
            <p>{advice[risk_cat]}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("👈 Enter details in the sidebar and click **Analyze Career Risk**.")
    c1, c2, c3 = st.columns(3)
    c1.markdown("### 🔍 Smart Scoring\nML-based automation risk analysis")
    c2.markdown("### 📊 Industry Context\nRisk benchmarking insights")
    c3.markdown("### 🛡️ Future-Proofing\nActionable AI career advice")
