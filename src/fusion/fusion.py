from typing import List, Dict, Any
from src.normalization.events import NormalizedEvent
from src.utils.logger import logger

class EvidenceFusion:
    """
    13. EVIDENCE FUSION
    Constructs an evidence graph for an alert.
    Requires events from independent sources to boost confidence.
    """
    def build_evidence_graph(self, anchor_event: NormalizedEvent, supporting_events: List[NormalizedEvent]) -> Dict[str, Any]:
        """
        Combines multiple events into a structured graph.
        Returns the graph and independence calculation.
        """
        graph_nodes = []
        unique_sources = set()
        
        # Add Anchor
        unique_sources.add(anchor_event.provenance.source_id)
        graph_nodes.append({
            "type": "anchor",
            "source_type": anchor_event.provenance.source_type,
            "description": f"{anchor_event.event_type} on {anchor_event.asset}"
        })
        
        # Add Supporting
        for ev in supporting_events:
            unique_sources.add(ev.provenance.source_id)
            graph_nodes.append({
                "type": "support",
                "source_type": ev.provenance.source_type,
                "description": f"{ev.event_type} confirmed by {ev.provenance.source_id}"
            })
            
        cross_source_independence = 1.0 + (len(unique_sources) * 0.2) # Bonus for multiple unique sources
        
        return {
            "graph_nodes": graph_nodes,
            "unique_source_count": len(unique_sources),
            "cross_source_independence": cross_source_independence,
            "sources": list(unique_sources)
        }
