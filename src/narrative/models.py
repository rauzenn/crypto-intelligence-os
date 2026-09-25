from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class NarrativeLifecycle(str, Enum):
    BIRTH = "BIRTH"
    EMERGENCE = "EMERGENCE"
    ACCELERATION = "ACCELERATION"
    MAINSTREAM = "MAINSTREAM"
    SATURATION = "SATURATION"
    DECAY = "DECAY"

class NarrativeMetrics(BaseModel):
    mention_velocity: float = 0.0 # Mentions per hour
    unique_sources: int = 0
    unique_accounts: int = 0
    cross_chain_propagation: float = 0.0
    capital_flow_usd: float = 0.0
    token_activity_score: float = 0.0
    developer_activity_score: float = 0.0
    news_catalysts: int = 0

class NarrativeGraphNode(BaseModel):
    name: str
    type: str # "concept", "protocol", "token", "wallet"
    weight: float = 1.0

class NarrativeProfile(BaseModel):
    topic: str
    lifecycle_state: NarrativeLifecycle = NarrativeLifecycle.BIRTH
    metrics: NarrativeMetrics = Field(default_factory=NarrativeMetrics)
    graph_nodes: List[NarrativeGraphNode] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confidence_score: float = 0.0 # How confident are we that this is a real narrative
