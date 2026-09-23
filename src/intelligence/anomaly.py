from typing import Any, Dict, List
from src.models.events import NormalizedEvent
from src.utils.logger import logger

class AnomalyDetector:
    def __init__(self):
        self.threshold_volume_multiplier = 3.0
        self.threshold_price_change_pct = 10.0

    def detect_market_anomaly(self, event: NormalizedEvent, historical_context: Dict[str, Any]) -> bool:
        if event.event_type != "dex_pair_snapshot":
            return False
            
        try:
            current_volume = float(event.metadata.get("volume24h", 0) or 0)
            avg_volume = float(historical_context.get("avg_volume_24h", current_volume) or current_volume)
            
            if avg_volume > 0 and current_volume > (avg_volume * self.threshold_volume_multiplier):
                logger.info(f"Anomaly detected for {event.asset}: Volume spike")
                return True
                
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing metrics for anomaly detection: {e}")
            
        return False
