import re
from typing import List, Dict, Any, Tuple, Optional
from src.utils.logger import logger
from datetime import datetime, timezone
from src.narrative.models import NarrativeProfile, NarrativeLifecycle, NarrativeMetrics, NarrativeGraphNode

class NarrativeEngine2:
    """
    10. NARRATIVE ENGINE 2.0
    More than keyword counting. Understands the lifecycle and builds an entity graph.
    Answers: "Is this narrative in an early stage?"
    """
    def __init__(self):
        self.narratives: Dict[str, NarrativeProfile] = {}
        
        # Base ontology for building graphs. 
        # In a real scenario, this is expanded via ML/NLP or an external knowledge graph.
        self.ontology = {
            "AI": {
                "keywords": ["ai", "artificial intelligence", "llm", "agent"],
                "sub_nodes": [
                    {"name": "AI Agents", "type": "concept"},
                    {"name": "Autonomous agents", "type": "concept"}
                ]
            },
            "DePIN": {
                "keywords": ["depin", "compute", "gpu", "storage"],
                "sub_nodes": []
            },
            "RWA": {
                "keywords": ["rwa", "tokenized", "treasuries"],
                "sub_nodes": []
            }
        }

    def _determine_lifecycle(self, metrics: NarrativeMetrics) -> NarrativeLifecycle:
        """
        Determines the stage of a narrative based on complex metrics.
        """
        if metrics.mention_velocity > 500 and metrics.capital_flow_usd > 10_000_000:
            return NarrativeLifecycle.SATURATION
        elif metrics.mention_velocity > 100 and metrics.news_catalysts > 2:
            return NarrativeLifecycle.MAINSTREAM
        elif metrics.mention_velocity > 20 and metrics.capital_flow_usd > 1_000_000:
            return NarrativeLifecycle.ACCELERATION
        elif metrics.mention_velocity > 5 and metrics.unique_sources > 2:
            return NarrativeLifecycle.EMERGENCE
        else:
            return NarrativeLifecycle.BIRTH

    def process_social_event(self, text: str, source_id: str, author_id: str) -> List[str]:
        """
        Processes a single piece of text, updates graphs, and returns detected narratives.
        """
        text_lower = text.lower()
        detected = []
        
        for topic, data in self.ontology.items():
            if any(re.search(rf"\b{kw}\b", text_lower) for kw in data["keywords"]):
                detected.append(topic)
                
                # Create or fetch profile
                profile = self.narratives.get(topic, NarrativeProfile(topic=topic))
                
                # Update basic metrics (Simulated increment for this event)
                profile.metrics.mention_velocity += 0.1 # Will be properly windowed in DB
                profile.metrics.unique_sources += 1 # Rough proxy
                profile.metrics.unique_accounts += 1
                
                # Update Graph Nodes
                existing_node_names = [n.name for n in profile.graph_nodes]
                for sub in data["sub_nodes"]:
                    if sub["name"] not in existing_node_names:
                        profile.graph_nodes.append(NarrativeGraphNode(name=sub["name"], type=sub["type"]))
                        
                # Re-evaluate lifecycle
                new_state = self._determine_lifecycle(profile.metrics)
                if new_state != profile.lifecycle_state:
                    logger.info(f"[NarrativeEngine] {topic} transitioned from {profile.lifecycle_state} to {new_state}")
                    profile.lifecycle_state = new_state
                    
                profile.last_updated = datetime.now(timezone.utc)
                self.narratives[topic] = profile
                
        return detected
        
    def integrate_market_data(self, topic: str, capital_flow: float, token_activity: float):
        """
        Combines market realities (TVL, volume) with the narrative.
        "Is this narrative really growing or just repeated by same accounts?"
        """
        if topic in self.narratives:
            profile = self.narratives[topic]
            profile.metrics.capital_flow_usd += capital_flow
            profile.metrics.token_activity_score += token_activity
            
            # Re-evaluate lifecycle with new hard financial data
            profile.lifecycle_state = self._determine_lifecycle(profile.metrics)
            
            # If financial data is high, confidence in the narrative increases
            if capital_flow > 100_000:
                profile.confidence_score = min(100.0, profile.confidence_score + 10.0)
                
            self.narratives[topic] = profile
            logger.info(f"[NarrativeEngine] Integrated market data for {topic}. Capital Flow: {profile.metrics.capital_flow_usd}")
            
    def get_early_narratives(self) -> List[NarrativeProfile]:
        """Returns narratives that are in BIRTH or EMERGENCE."""
        return [n for n in self.narratives.values() if n.lifecycle_state in [NarrativeLifecycle.BIRTH, NarrativeLifecycle.EMERGENCE, NarrativeLifecycle.ACCELERATION]]
