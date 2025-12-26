import joblib
import pandas as pd

# Load model once
model = joblib.load("models/automation_risk_model.pkl")

ai_impact_mapping = {
    "Low": 0,
    "Moderate": 1,
    "High": 2
}

def predict_risk(data: dict) -> float:
    df = pd.DataFrame([{
        "experience_required_years": data["experience_required_years"],
        "ai_impact_level": ai_impact_mapping.get(data["ai_impact_level"], 1),
        "projected_openings_2030": data["projected_openings_2030"],
        "remote_work_ratio_percent": data["remote_work_ratio_percent"]
    }])

    prediction = model.predict(df)[0]
    return round(float(prediction), 2)
