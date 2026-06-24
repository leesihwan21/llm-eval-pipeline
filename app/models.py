from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class EvalHistory(Base):
    __tablename__ = "eval_history"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=False)
    response = Column(Text, nullable=False)
    score = Column(Float, nullable=True)
    latency_ms = Column(Float, nullable=True)
    task_type = Column(String(50), default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())