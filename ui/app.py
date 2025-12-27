import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Career Risk Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .advice-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        border-left: 5px solid #ff4b4b;
    }
    .low-risk { border-left-color: #28a745; background-color: #1a2e1a; }
    .medium-risk { border-left-color: #ffa500; background-color: #2e2a1a; }
    .high-risk { border-left-color: #ff4b4b; background-color: #2e1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("🎯 Parameters")
    st.markdown("Adjust your career details to see the AI impact.")
    
    job_title = st.text_input("Job Title", "Software Engineer")
    
    industry = st.selectbox(
        "Industry",
        ["IT", "Finance", "Healthcare", "Manufacturing", "Education", "Retail", "Entertainment", "Transportation"]
    )
    
    experience = st.slider(
        "Experience (Years)",
        min_value=0,
        max_value=30,
        value=5
    )
    
    ai_impact = st.selectbox(
        "Current AI Integration Level",
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

# --- MAIN DISPLAY ---
st.title("🎯 AI Career Risk & Job Market Intelligence")
st.markdown("### Interactive Dashboard for Professional Future-Proofing")

if analyze_btn:
    payload = {
        "job_title": job_title,
        "experience_required_years": experience,
        "ai_impact_level": ai_impact,
        "projected_openings_2030": projected_openings,
        "remote_work_ratio_percent": remote_ratio
    }

    try:
        with st.spinner("🤖 Calculating AI Impact..."):
            response = requests.post(
                "https://ai-career-risk-analyzer.onrender.com/",
                json=payload
            )

        if response.status_code == 200:
            result = response.json()
            risk_score = result['automation_risk_percent']
            risk_cat = result['risk_category']

            # --- METRICS & CHARTS ---
            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader("📊 Key Metrics")
                st.metric("Automation Risk", f"{risk_score}%", delta=f"{risk_cat} Risk", delta_color="inverse")
                
                # Gauge Chart
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = risk_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Risk Level", 'font': {'size': 24}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#ff4b4b" if risk_score > 60 else "#ffa500" if risk_score > 30 else "#28a745"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(40, 167, 69, 0.3)'},
                            {'range': [30, 60], 'color': 'rgba(255, 165, 0, 0.3)'},
                            {'range': [60, 100], 'color': 'rgba(255, 75, 75, 0.3)'}
                        ],
                    }
                ))
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"})
                st.plotly_chart(fig_gauge, use_container_width=True)

            with col2:
                st.subheader("📈 Future Outlook")
                
                # Mock Industry Benchmark Data (In a real app, this would come from the dataset)
                industry_benchmarks = {
                    "IT": 45, "Finance": 55, "Healthcare": 25, "Manufacturing": 75,
                    "Education": 35, "Retail": 80, "Entertainment": 50, "Transportation": 85
                }
                avg_industry_risk = industry_benchmarks.get(industry, 50)

                fig_bench = go.Figure()
                fig_bench.add_trace(go.Bar(
                    x=['Your Role', f'{industry} Average'],
                    y=[risk_score, avg_industry_risk],
                    marker_color=['#ff4b4b', '#1f77b4'],
                    text=[f"{risk_score}%", f"{avg_industry_risk}%"],
                    textposition='auto',
                ))
                fig_bench.update_layout(
                    title=f"Risk vs {industry} Industry Average",
                    yaxis_title="Automation Risk (%)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white"}
                )
                st.plotly_chart(fig_bench, use_container_width=True)

            # --- AI ADVICE SECTION ---
            st.divider()
            st.subheader("💡 AI-Proofing Strategy")
            
            advice_style = "low-risk" if risk_cat == "Low" else "medium-risk" if risk_cat == "Medium" else "high-risk"
            
            advice_content = {
                "Low": "Your role has high human-centric value. Focus on deepening your expertise and staying updated with AI tools that can augment your productivity.",
                "Medium": "AI is increasingly assisting in your field. To stay ahead, focus on 'Soft Skills' (Leadership, Empathy) and 'Human+AI' collaboration techniques.",
                "High": "Significant automation risk detected. Consider upskilling in creative problem-solving, strategic management, or transitioning into high-level AI oversight roles."
            }

            st.markdown(f"""
                <div class="advice-card {advice_style}">
                    <h4>Recommendation for {job_title}</h4>
                    <p>{advice_content[risk_cat]}</p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ API error. Please ensure the FastAPI server (app.main) is running on port 8000.")

    except Exception as e:
        st.error(f"⚠️ Connection Error: {str(e)}")
        st.info("💡 Make sure to start the backend: `python -m uvicorn app.main:app`")

else:
    # Initial State
    st.info("👈 Enter your career details in the sidebar and click 'Analyze' to begin.")
    
    # Showcase some features if no analysis is running
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("### 🔍 Precise Prediction")
        st.write("Using Random Forest models trained on global job market trends.")
    with colB:
        st.markdown("### 📊 Benchmark Analysis")
        st.write("Compare your career trajectory against industry-wide automation averages.")
    with colC:
        st.markdown("### 🛡️ Future Proofing")
        st.write("Get personalized advice on how to remain relevant in the age of AI.")
