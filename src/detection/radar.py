from typing import Any, Dict, List, Optional
from src.normalization.events import NormalizedEvent, Alert
from src.detection.signal import AlphaSignal, SignalTaxonomy, EarlynessStage, CompositeScore
from src.detection.earlyness import EarlynessEngine
from src.scoring.composite import ScoringEngine
from src.fusion.fusion import EvidenceFusion
from src.risk.risk import RiskGate
from src.event_bus.dedup import AlertDeduplicator
from src.utils.logger import logger
from datetime import datetime, timezone
import uuid

class AlphaRadar:
    """
    11. ALPHA RADAR 2.0
    Signal taxonomy and multi-category detection.
    """
    def __init__(self):
        self.earlyness = EarlynessEngine()
        self.fusion = EvidenceFusion()
        self.scoring = ScoringEngine()
        self.risk = RiskGate()
        self.dedup = AlertDeduplicator()

    async def process_event(self, event: NormalizedEvent, context_data: Dict[str, Any]) -> Optional[Alert]:
        # Determine Taxonomy Category based on event type
        taxonomy_cats = []
        if event.event_type in ["market_price", "market_snapshot", "dex_pair_snapshot"]:
            taxonomy_cats.append(SignalTaxonomy.MARKET)
        elif event.event_type in ["wallet_transfer", "swap"]:
            taxonomy_cats.append(SignalTaxonomy.WALLET)
        elif event.event_type in ["social_mention", "news"]:
            taxonomy_cats.append(SignalTaxonomy.SOCIAL)
        
        if not taxonomy_cats:
            taxonomy_cats.append(SignalTaxonomy.MARKET)

        # 1. Evaluate Earlyness (T0 - T4)
        has_first = True
        cross_source_count = context_data.get("cross_source_count", 1)
        narr_growth = context_data.get("narrative_growth", 0.0)
        volume_surge = context_data.get("volume_surge", False)
        mentions = context_data.get("social_mentions", 0)
        
        stage = self.earlyness.evaluate_stage(has_first, cross_source_count, narr_growth, volume_surge, mentions)
        
        # 2. Fuse Evidence
        supporting_events = context_data.get("supporting_events", [])
        graph_data = self.fusion.build_evidence_graph(event, supporting_events)
        
        # 3. Evaluate Risk
        contract_analysis = context_data.get("contract_analysis", {})
        risk_profile = self.risk.evaluate(event, contract_analysis)
        
        if risk_profile.category.value == "CRITICAL":
            logger.warning(f"Alert BLOCKED due to CRITICAL risk on {event.asset}: {risk_profile.flags}")
            return None
            
        risk_penalty = risk_profile.overall_risk_score / 100.0 # 0.0 to 1.0 penalty
        
        # 4. Generate Signal Object
        score_comps = CompositeScore(
            earlyness=100.0 if stage == EarlynessStage.T0 else 50.0 if stage == EarlynessStage.T1 else 10.0,
            onchain_strength=context_data.get("onchain_strength", 20.0),
            market_confirmation=context_data.get("market_confirmation", 20.0),
            wallet_quality=context_data.get("wallet_quality", 0.0),
            narrative_velocity=narr_growth,
            catalyst_strength=context_data.get("catalyst_strength", 0.0),
            liquidity_quality=risk_profile.liquidity_score,
            risk_penalty=risk_penalty,
            cross_source_independence=graph_data["cross_source_independence"]
        )
        
        # 5. Calculate Score
        final_score = self.scoring.calculate_composite_score(score_comps)
        
        signal = AlphaSignal(
            signal_id=str(uuid.uuid4()),
            asset=event.asset or "UNKNOWN",
            chain=event.chain or "UNKNOWN",
            taxonomy_categories=taxonomy_cats,
            earlyness_stage=stage,
            score=final_score,
            evidence_graph=graph_data["graph_nodes"],
            provenance_chain=[event.provenance],
            created_at=datetime.now(timezone.utc)
        )
        
        # 6. Check Threshold for Alerting
        if signal.score.calibrated_score > 60.0:
            # Deduplicate
            is_dup = await self.dedup.is_duplicate(signal.asset, signal.chain, "alpha_alert")
            if is_dup:
                logger.info(f"Duplicate alert suppressed for {signal.asset}")
                return None
                
            priority = "P1" if signal.score.calibrated_score > 85.0 else "P2"
            
            # Map graph to evidence string list
            ev_list = [f"[{n['type']}] {n['description']}" for n in signal.evidence_graph]
            
            alert = Alert(
                title=f"Alpha Detection: {signal.asset}",
                asset=signal.asset,
                chain=signal.chain,
                what_changed=f"Taxonomy: {', '.join([c.value for c in signal.taxonomy_categories])}",
                why_now=f"Scored {signal.score.calibrated_score:.1f}/100",
                evidence=ev_list,
                earlyness=signal.earlyness_stage.value,
                risk_flags=risk_profile.flags,
                sources=graph_data["sources"],
                next_to_watch="Monitor network and wallet interactions.",
                composite_score=signal.score.calibrated_score,
                priority=priority
            )
            return alert
            
        return None
