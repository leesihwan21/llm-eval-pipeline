from fastapi import APIRouter
from app.schemas import EvalRequest, EvalResponse

router = APIRouter()

@router.post("/run", response_model=EvalResponse)
async def run_eval(request: EvalRequest):
    # 추후 evaluator 서비스 연결
    return EvalResponse(
        prompt=request.prompt,
        results=[]
    )

@router.get("/history")
async def get_history():
    # 추후 DB 연결
    return {"history": []}