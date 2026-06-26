from pydantic import BaseModel
from typing import Optional, List

class EvalRequest(BaseModel):
    prompt: str
    models: List[str]
    task_type: Optional[str] = "general"

class BatchEvalRequest(BaseModel):
    prompts: List[str]
    models: List[str]
    task_type: Optional[str] = "general"

class EvalResult(BaseModel):
    model_name: str
    response: str
    score: Optional[float] = None          # LLM Judge 점수 (하위 호환)
    llm_score: Optional[float] = None
    rouge1: Optional[float] = None
    rouge2: Optional[float] = None
    rougeL: Optional[float] = None
    latency_ms: Optional[float] = None

class EvalResponse(BaseModel):
    prompt: str
    results: List[EvalResult]

class BatchEvalResponse(BaseModel):
    total: int
    results: List[EvalResponse]