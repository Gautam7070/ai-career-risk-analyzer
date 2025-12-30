from pathlib import Path
import joblib
import requests
import pandas as pd
from functools import lru_cache

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Local model storage
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "automation_risk_model.pkl"

# Hugging Face direct download URL
MODEL_URL = "https://huggingface.co/gautam7070/automation-risk-model/resolve/main/automation_risk_model.pkl"

def download_model():
    MODEL_DIR.mkdir(exist_ok=True)

    if not MODEL_PATH.exists():
        print("📥 Downloading ML model from Hugging Face...")
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()

        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("✅ Model downloaded successfully")

ai_impact_mapping = {"Low": 1, "Moderate": 2, "High": 3}

@lru_cache(maxsize=1)
def get_model():
    download_model()
    return joblib.load(MODEL_PATH)

def predict_risk(data: dict) -> float:
    model = get_model()
    
    # Convert input to DataFrame as expected by the model
    df = pd.DataFrame([{
        "experience_required_years": data["experience_required_years"],
        "ai_impact_level": ai_impact_mapping.get(data["ai_impact_level"], 1),
        "projected_openings_2030": data["projected_openings_2030"],
        "remote_work_ratio_percent": data["remote_work_ratio_percent"]
    }])
    
    prediction = model.predict(df)[0]
    return float(prediction)
