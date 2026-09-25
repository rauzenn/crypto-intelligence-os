from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.normalization.events import Provenance

class SignalTaxonomy(str, Enum):
    MARKET = "MARKET"
    ONCHAIN = "ONCHAIN"
    WALLET = "WALLET"
    NARRATIVE = "NARRATIVE"
    SOCIAL = "SOCIAL"
    NEWS = "NEWS"
    LIQUIDITY = "LIQUIDITY"
    CHAIN = "CHAIN"
    PROTOCOL = "PROTOCOL"
    TOKEN = "TOKEN"
    SECURITY = "SECURITY"
    GOVERNANCE = "GOVERNANCE"
    CAPITAL_FLOW = "CAPITAL_FLOW"

class EarlynessStage(str, Enum):
    T0 = "T0_FIRST_MEASURABLE_SIGNAL"
    T1 = "T1_CROSS_SOURCE_CONFIRMATION"
    T2 = "T2_NARRATIVE_ACCELERATION"
    T3 = "T3_MAJOR_MARKET_REACTION"
    T4 = "T4_MAINSTREAM_VISIBILITY"

class CompositeScore(BaseModel):
    earlyness: float = 0.0
    onchain_strength: float = 0.0
    market_confirmation: float = 0.0
    wallet_quality: float = 0.0
    narrative_velocity: float = 0.0
    source_quality: float = 0.0
    catalyst_strength: float = 0.0
    liquidity_quality: float = 0.0
    risk_penalty: float = 0.0
    cross_source_independence: float = 1.0
    
    raw_score: float = 0.0
    calibrated_score: float = 0.0
    confidence: str = "LOW" # LOW, MEDIUM, HIGH

class AlphaSignal(BaseModel):
    """
    Internal intelligence object produced by Detection Engine.
    Not yet a final Alert.
    """
    signal_id: str
    asset: str
    chain: str
    taxonomy_categories: List[SignalTaxonomy]
    earlyness_stage: EarlynessStage
    score: CompositeScore
    evidence_graph: List[Dict[str, Any]] = Field(default_factory=list)
    provenance_chain: List[Provenance] = Field(default_factory=list)
    created_at: datetime
