from typing import Any, Dict, List
from src.models.events import NormalizedEvent, Alert
from src.intelligence.anomaly import AnomalyDetector
from src.intelligence.earlyness import EarlynessCalculator
from src.intelligence.fusion import EvidenceFusion
from src.intelligence.risk import RiskGate
from src.intelligence.dedup import AlertDeduplicator
from src.utils.logger import logger
from datetime import datetime, timezone

class AlphaRadar:
    def __init__(self):
        self.anomaly = AnomalyDetector()
        self.earlyness = EarlynessCalculator()
        self.fusion = EvidenceFusion()
        self.risk = RiskGate()
        self.dedup = AlertDeduplicator()

    async def process_event(self, event: NormalizedEvent, context_data: Dict[str, Any]) -> Alert | None:
        # 1. Detect Anomaly
        if not self.anomaly.detect_market_anomaly(event, context_data):
            return None
            
        # 2. Deduplicate
        is_dup = await self.dedup.is_duplicate(event.asset, event.chain, "volume_spike")
        if is_dup:
            logger.info(f"Duplicate alert suppressed for {event.asset}")
            return None
            
        # 3. Earlyness
        social_mentions = context_data.get("social_mentions", 0)
        earlyness_score = self.earlyness.calculate(event, social_mentions)
        
        # 4. Fusion
        supporting_events = context_data.get("supporting_events", [])
        fusion_result = self.fusion.fuse_signals(event, supporting_events)
        
        # 5. Risk
        contract_analysis = context_data.get("contract_analysis", {})
        risk_flags = self.risk.evaluate(event, contract_analysis)
        
        # 6. Generate Alert
        alert = Alert(
            title=f"Volume Acceleration: {event.asset}",
            asset=event.asset,
            chain=event.chain,
            what_changed="Significant volume spike detected against historical baseline.",
            why_now="Detected via continuous DEX scanning.",
            evidence=fusion_result["evidence_list"],
            earlyness=earlyness_score,
            risk_flags=risk_flags,
            sources=fusion_result["unique_sources"],
            next_to_watch="Monitor for social velocity increase or smart money wallet entry."
        )
        return alert
