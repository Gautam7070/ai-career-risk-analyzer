from fastapi import FastAPI
from .routes.career import router as career_router


app = FastAPI(
    title="AI Career Risk & Job Market Impact Analyzer",
    description="Predicts automation risk and career insights using ML",
    version="1.0"
)

app.include_router(career_router)
