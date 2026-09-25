from typing import Any, Dict
from src.normalization.events import NormalizedEvent
from src.detection.signal import EarlynessStage

class EarlynessEngine:
    """
    12. EARLYNESS ENGINE
    Evaluates where the signal is in its lifecycle (T0-T4).
    "Fiyat yükseldi bir alpha değildir. Sistem bunu ne kadar erken fark etti?"
    """
    
    def evaluate_stage(self, 
                       has_first_signal: bool, 
                       cross_source_count: int, 
                       narrative_growth: float, 
                       market_volume_surge: bool,
                       mainstream_mentions: int) -> EarlynessStage:
        """
        Determines the current earlyness stage based on multiple vectors.
        """
        if mainstream_mentions > 100:
            return EarlynessStage.T4
            
        if market_volume_surge and narrative_growth > 50.0:
            return EarlynessStage.T3
            
        if narrative_growth > 20.0:
            return EarlynessStage.T2
            
        if cross_source_count > 1:
            return EarlynessStage.T1
            
        if has_first_signal:
            return EarlynessStage.T0
            
        return EarlynessStage.T0 # Default to earliest if unknown but detected
