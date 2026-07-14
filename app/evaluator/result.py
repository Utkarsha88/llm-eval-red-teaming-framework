from typing import Optional
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    """
    Standardized output for a single evaluation run.
    This tracks the model's response and execution metadata.
    """
    test_case_id: str
    category: str
    prompt: str
    expected_behavior: str
    model_name: str
    response: str
    latency_seconds: float
    error: Optional[str] = None