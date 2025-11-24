from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Transaction(BaseModel):
    id: str
    date: str
    merchant: str
    amount: float
    category: str
    risk_score: int = 0
    is_anomaly: bool = False
    reason: Optional[str] = None

class AnalysisRequest(BaseModel):
    filename: str

class AnalysisResult(BaseModel):
    job_id: str
    status: str
    total_transactions: int
    high_risk_count: int
    transactions: List[Transaction]
    manager_summary: Optional[str] = None