from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import eval, models
from app.database import engine
from app import models as db_models

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LLM Eval Pipeline",
    description="LLM 응답 품질 자동 평가 파이프라인",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eval.router, prefix="/api/eval", tags=["eval"])
app.include_router(models.router, prefix="/api/models", tags=["models"])

@app.get("/")
def root():
    return {"message": "LLM Eval Pipeline API"}