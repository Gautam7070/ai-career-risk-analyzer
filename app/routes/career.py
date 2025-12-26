from fastapi import APIRouter
from ..schemas.career import CareerInput, CareerOutput
from ..ml.predictor import predict_risk


router = APIRouter(prefix="/analyze-career", tags=["Career Analyzer"])

def risk_category(risk: float) -> str:
    if risk < 30:
        return "Low"
    elif risk < 60:
        return "Medium"
    else:
        return "High"

@router.post("/", response_model=CareerOutput)
def analyze_career(data: CareerInput):
    risk = predict_risk(data.dict())
    category = risk_category(risk)

    return {
        "automation_risk_percent": risk,
        "risk_category": category
    }
