from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RiskCategory(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL" # Indicates a likely honeypot or rug, block the alert!

class RiskProfile(BaseModel):
    category: RiskCategory = RiskCategory.LOW
    flags: List[str] = Field(default_factory=list)
    contract_security_score: float = 100.0 # 0-100, 100 is best
    liquidity_score: float = 100.0
    holder_distribution_score: float = 100.0
    overall_risk_score: float = 0.0 # 0-100, 0 is best (no risk)
    can_sell: bool = True
