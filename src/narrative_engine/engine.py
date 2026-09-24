import re
from typing import List, Dict, Any, Tuple
from src.utils.logger import logger
from datetime import datetime

class NarrativeEngine:
    def __init__(self):
        # Known keywords for narratives
        self.narrative_keywords = {
            "AI": ["ai", "artificial intelligence", "llm", "agent", "agents", "machine learning"],
            "DePIN": ["depin", "compute", "gpu", "storage", "decentralized physical"],
            "RWA": ["rwa", "real world assets", "tokenized", "treasuries"],
            "L2/L3": ["l2", "l3", "rollup", "optimistic", "zk", "layer 2"],
            "Meme": ["meme", "doge", "wif", "pepe", "cat", "dog"],
            "Restaking": ["restaking", "eigen", "avs", "symbiotic", "karak"]
        }

    def _match_topic(self, text: str) -> List[str]:
        text_lower = text.lower()
        matched = []
        for topic, keywords in self.narrative_keywords.items():
            if any(re.search(rf"\b{kw}\b", text_lower) for kw in keywords):
                matched.append(topic)
        return matched

    def extract_topics(self, social_posts: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Extract mentions of narratives from a batch of social posts.
        """
        topics = {}
        for post in social_posts:
            text = post.get("text", "")
            matches = self._match_topic(text)
            for m in matches:
                topics[m] = topics.get(m, 0) + 1
                
        logger.info(f"Extracted narrative mentions: {topics}")
        return topics
        
    def detect_narrative_acceleration(self, topics_current: Dict[str, int], topics_historical: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Detect narratives that are growing faster than their historical baseline.
        Returns a list of dicts with topic and growth rate.
        """
        accelerating = []
        for topic, count in topics_current.items():
            hist_count = topics_historical.get(topic, 0)
            
            # Baseline buffer to avoid division by zero or noisy small numbers
            if count > 5: 
                growth_rate = count / max(hist_count, 1)
                
                if growth_rate > 2.0: # 100% growth
                    accelerating.append({
                        "topic": topic,
                        "current_mentions": count,
                        "historical_mentions": hist_count,
                        "growth_rate": growth_rate
                    })
                    
        # Sort by growth rate descending
        accelerating.sort(key=lambda x: x["growth_rate"], reverse=True)
        
        if accelerating:
            logger.info(f"Narrative acceleration detected: {accelerating}")
            
        return accelerating
