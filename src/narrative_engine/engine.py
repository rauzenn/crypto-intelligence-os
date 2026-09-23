from typing import List, Dict, Any
from src.utils.logger import logger

class NarrativeEngine:
    def __init__(self):
        pass

    def extract_topics(self, social_posts: List[Dict[str, Any]]) -> Dict[str, int]:
        # NLP entity extraction and clustering placeholder
        topics = {}
        for post in social_posts:
            text = post.get("text", "").lower()
            if "ai" in text:
                topics["AI"] = topics.get("AI", 0) + 1
            if "depin" in text:
                topics["DePIN"] = topics.get("DePIN", 0) + 1
                
        logger.info(f"Extracted narratives: {topics}")
        return topics
        
    def detect_narrative_acceleration(self, topics_current: Dict[str, int], topics_historical: Dict[str, int]) -> List[str]:
        accelerating = []
        for topic, count in topics_current.items():
            hist_count = topics_historical.get(topic, 0)
            if hist_count > 0 and count > (hist_count * 2):
                accelerating.append(topic)
                
        return accelerating
