from pydantic import BaseModel
from typing import Optional, List

class EvalRequest(BaseModel):
    prompt: str
    models: List[str]
    task_type: Optional[str] = "general"

class EvalResult(BaseModel):
    model_name: str
    response: str
    score: Optional[float] = None
    latency_ms: Optional[float] = None

class EvalResponse(BaseModel):
    prompt: str
    results: List[EvalResult]