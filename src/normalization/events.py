from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import uuid

def get_utc_now():
    return datetime.now(timezone.utc)

class Provenance(BaseModel):
    """Tracks the origin and reliability of an intelligence object."""
    source_id: str
    source_type: str
    timestamp: datetime = Field(default_factory=get_utc_now)
    raw_reference: str
    is_processed: bool = False
    confidence_score: float = 0.0

class NormalizedEvent(BaseModel):
    """
    B. NORMALIZATION LAYER
    Standardized event format for all JARVIS systems.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    chain: str
    wallet: Optional[str] = None
    asset: Optional[str] = None
    provenance: Provenance
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "chain": self.chain,
            "wallet": self.wallet,
            "asset": self.asset,
            "provenance": self.provenance.model_dump(),
            "metadata": self.metadata
        }

class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    asset: Optional[str] = None
    chain: Optional[str] = None
    detected_at: datetime = Field(default_factory=get_utc_now)
    what_changed: str
    why_now: str
    evidence: List[str] = Field(default_factory=list)
    earlyness: str
    risk_flags: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    next_to_watch: str
    composite_score: float = 0.0
    priority: str = "P3" # P0, P1, P2, P3
    
    def format_telegram(self) -> str:
        evidence_str = "\n- ".join([""] + self.evidence) if self.evidence else "None"
        risk_str = "\n- ".join([""] + self.risk_flags) if self.risk_flags else "None"
        sources_str = ", ".join(self.sources)
        
        return f"""*[{self.priority}] {self.title}*
Asset: {self.asset or 'N/A'}
Chain: {self.chain or 'N/A'}
Score: {self.composite_score:.1f}

*What changed:*
{self.what_changed}

*Why now:*
{self.why_now}

*Evidence:* {evidence_str}

*Earlyness:* {self.earlyness}

*Risk flags:* {risk_str}

*Next to watch:* {self.next_to_watch}

*Sources:* {sources_str}
"""
