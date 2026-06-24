from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import EvalRequest, EvalResponse, EvalResult
from app.services.llm_client import call_llm
from app.services.evaluator import evaluate_response
from app.database import get_db
from app import models as db_models

router = APIRouter()

@router.post("/run", response_model=EvalResponse)
async def run_eval(request: EvalRequest, db: Session = Depends(get_db)):
    if not request.prompt.strip():
        return EvalResponse(prompt=request.prompt, results=[])

    results = []

    for model in request.models:
        try:
            result = call_llm(request.prompt, model)
            score = evaluate_response(request.prompt, result["response"])

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
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return EvalResponse(prompt=request.prompt, results=results)

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(db_models.EvalHistory).order_by(
        db_models.EvalHistory.created_at.desc()
    ).limit(20).all()
    return {"history": history}