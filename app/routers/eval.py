from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import EvalRequest, EvalResponse, EvalResult, BatchEvalRequest, BatchEvalResponse
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
            metrics = evaluate_response(request.prompt, result["response"])

            history = db_models.EvalHistory(
                prompt=request.prompt,
                model_name=result["model_name"],
                response=result["response"],
                score=metrics["llm_score"],
                llm_score=metrics["llm_score"],
                rouge1=metrics["rouge1"],
                rouge2=metrics["rouge2"],
                rougeL=metrics["rougeL"],
                latency_ms=result["latency_ms"],
                task_type=request.task_type
            )
            db.add(history)
            db.commit()

            results.append(EvalResult(
                model_name=result["model_name"],
                response=result["response"],
                score=metrics["llm_score"],
                llm_score=metrics["llm_score"],
                rouge1=metrics["rouge1"],
                rouge2=metrics["rouge2"],
                rougeL=metrics["rougeL"],
                latency_ms=result["latency_ms"]
            ))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return EvalResponse(prompt=request.prompt, results=results)


@router.post("/batch", response_model=BatchEvalResponse)
async def run_batch_eval(request: BatchEvalRequest, db: Session = Depends(get_db)):
    """여러 프롬프트를 일괄 평가"""
    if not request.prompts:
        raise HTTPException(status_code=400, detail="프롬프트 목록이 비어있습니다")

    all_results = []

    for prompt in request.prompts:
        if not prompt.strip():
            continue

        prompt_results = []
        for model in request.models:
            try:
                result = call_llm(prompt, model)
                metrics = evaluate_response(prompt, result["response"])

                history = db_models.EvalHistory(
                    prompt=prompt,
                    model_name=result["model_name"],
                    response=result["response"],
                    score=metrics["llm_score"],
                    llm_score=metrics["llm_score"],
                    rouge1=metrics["rouge1"],
                    rouge2=metrics["rouge2"],
                    rougeL=metrics["rougeL"],
                    latency_ms=result["latency_ms"],
                    task_type=request.task_type
                )
                db.add(history)

                prompt_results.append(EvalResult(
                    model_name=result["model_name"],
                    response=result["response"],
                    score=metrics["llm_score"],
                    llm_score=metrics["llm_score"],
                    rouge1=metrics["rouge1"],
                    rouge2=metrics["rouge2"],
                    rougeL=metrics["rougeL"],
                    latency_ms=result["latency_ms"]
                ))
            except ValueError as e:
                continue

        db.commit()
        all_results.append(EvalResponse(prompt=prompt, results=prompt_results))

    return BatchEvalResponse(total=len(all_results), results=all_results)


@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(db_models.EvalHistory).order_by(
        db_models.EvalHistory.created_at.desc()
    ).limit(20).all()
    return {"history": history}