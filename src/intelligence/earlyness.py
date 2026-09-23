from typing import Any, Dict
from src.models.events import NormalizedEvent

class EarlynessCalculator:
    def calculate(self, event: NormalizedEvent, social_mentions: int) -> str:
        # A very basic proxy for earlyness based on social mentions
        if social_mentions < 10:
            return "Extreme Early (Pre-social)"
        elif social_mentions < 100:
            return "Early (Initial social pickup)"
        elif social_mentions < 1000:
            return "Mid (Consensus forming)"
        else:
            return "Late (Crowded)"
