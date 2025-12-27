from pathlib import Path
import joblib
import requests
from functools import lru_cache

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Local model storage
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "automation_risk_model.pkl"

# Hugging Face direct download URL
MODEL_URL = (
    "https://huggingface.co/gautam7070/automation-risk-model/resolve/main/automation_risk_model.pkl"
    "resolve/main/automation_risk_model.pkl"
)

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

@lru_cache(maxsize=1)
def get_model():
    download_model()
    return joblib.load(MODEL_PATH)

def predict_risk(features):
    model = get_model()
    return model.predict(features)
