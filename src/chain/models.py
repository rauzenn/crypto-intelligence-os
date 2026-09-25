from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class ChainState(str, Enum):
    EMERGING = "EMERGING"
    WATCH = "WATCH"
    ACTIVE = "ACTIVE"
    HIGH_INTENSITY = "HIGH_INTENSITY"
    DEGRADED = "DEGRADED"

class ChainMetrics(BaseModel):
    tvl_usd: float = 0.0
    tvl_acceleration: float = 0.0
    dex_volume_24h: float = 0.0
    active_addresses_24h: int = 0
    stablecoin_inflows: float = 0.0
    new_contracts_deployed: int = 0
    social_activity_score: float = 0.0

class ChainProfile(BaseModel):
    name: str
    state: ChainState = ChainState.WATCH
    metrics: ChainMetrics = Field(default_factory=ChainMetrics)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_supported: bool = True # Whether our ingestors support this chain yet
