from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import EvalRequest, EvalResponse, EvalResult
from app.services.llm_client import call_claude
from app.services.evaluator import evaluate_response
from app.database import get_db
from app import models as db_models

router = APIRouter()

@router.post("/run", response_model=EvalResponse)
async def run_eval(request: EvalRequest, db: Session = Depends(get_db)):
    results = []

    for model in request.models:
        if "claude" in model:
            result = call_claude(request.prompt, model)
            score = evaluate_response(request.prompt, result["response"])

            # DB 저장
            history = db_models.EvalHistory(
                prompt=request.prompt,
                model_name=result["model_name"],
                response=result["response"],
                score=score,
                latency_ms=result["latency_ms"],
                task_type=request.task_type
            )
            db.add(history)
            db.commit()

            results.append(EvalResult(
                model_name=result["model_name"],
                response=result["response"],
                score=score,
                latency_ms=result["latency_ms"]
            ))

    return EvalResponse(
        prompt=request.prompt,
        results=results
    )

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(db_models.EvalHistory).order_by(
        db_models.EvalHistory.created_at.desc()
    ).limit(20).all()
    return {"history": history}