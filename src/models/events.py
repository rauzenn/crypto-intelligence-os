from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

def get_utc_now():
    return datetime.now(timezone.utc)

class NormalizedEvent(BaseModel):
    event_type: str
    chain: str
    wallet: Optional[str] = None
    asset: Optional[str] = None
    timestamp: datetime = Field(default_factory=get_utc_now)
    source: str
    raw_reference: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Alert(BaseModel):
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
    
    def format_telegram(self) -> str:
        evidence_str = "\\n- ".join([""] + self.evidence) if self.evidence else "None"
        risk_str = "\\n- ".join([""] + self.risk_flags) if self.risk_flags else "None"
        sources_str = ", ".join(self.sources)
        
        return f"""*[ALPHA] {self.title}*
Asset: {self.asset or 'N/A'}
Chain: {self.chain or 'N/A'}

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
