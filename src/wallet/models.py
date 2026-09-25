from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class WalletLifecycle(str, Enum):
    CANDIDATE = "CANDIDATE"
    PROBATION = "PROBATION"
    WATCHED = "WATCHED"
    HIGH_SIGNAL = "HIGH_SIGNAL"
    DEGRADED = "DEGRADED"
    ARCHIVED = "ARCHIVED"

class WalletScore(BaseModel):
    sample_size: int = 0
    realized_pnl_usd: float = 0.0
    win_rate: float = 0.0
    median_pnl_pct: float = 0.0
    risk_adjusted_performance: float = 0.0
    early_entry_frequency: float = 0.0
    median_lead_time_hours: float = 0.0
    consistency_score: float = 0.0
    
    # Final values
    reputation_score: float = 0.0
    confidence: str = "LOW" # LOW, MEDIUM, HIGH

class WalletProfile(BaseModel):
    address: str
    chain: str
    lifecycle_state: WalletLifecycle = WalletLifecycle.CANDIDATE
    score: WalletScore = Field(default_factory=WalletScore)
    known_labels: List[str] = Field(default_factory=list)
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WalletCluster(BaseModel):
    cluster_id: str
    probable_wallets: List[str]
    confidence: str = "LOW"
    evidence: List[str]
    cluster_tags: List[str] = Field(default_factory=list)
