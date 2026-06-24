from fastapi import APIRouter
from app.schemas import EvalRequest, EvalResponse, EvalResult
from app.services.llm_client import call_claude
from app.services.evaluator import evaluate_response

router = APIRouter()

@router.post("/run", response_model=EvalResponse)
async def run_eval(request: EvalRequest):
    results = []

    for model in request.models:
        if "claude" in model:
            result = call_claude(request.prompt, model)
            score = evaluate_response(request.prompt, result["response"])
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
async def get_history():
    return {"history": []}