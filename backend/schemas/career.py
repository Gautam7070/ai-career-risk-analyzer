from pydantic import BaseModel

class CareerInput(BaseModel):
    job_title: str
    experience_required_years: int
    ai_impact_level: str
    projected_openings_2030: int
    remote_work_ratio_percent: float


class CareerOutput(BaseModel):
    automation_risk_percent: float
    risk_category: str
