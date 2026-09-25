from typing import List, Dict, Any
from src.normalization.events import NormalizedEvent
from src.utils.logger import logger

class EvidenceFusion:
    def fuse_signals(self, anchor_event: NormalizedEvent, supporting_events: List[NormalizedEvent]) -> Dict[str, Any]:
        """
        Combines multiple events into a single strong evidence profile.
        Requires events from independent sources to boost confidence.
        """
        sources = set([anchor_event.source])
        evidence = [f"Anchor ({anchor_event.source}): {anchor_event.raw_reference}"]
        
        for ev in supporting_events:
            sources.add(ev.source)
            evidence.append(f"Support ({ev.source}): {ev.raw_reference}")
            
        confidence = "High" if len(sources) >= 3 else "Medium" if len(sources) == 2 else "Low"
        
        return {
            "is_fused": len(sources) > 1,
            "unique_sources": list(sources),
            "evidence_list": evidence,
            "confidence": confidence
        }
