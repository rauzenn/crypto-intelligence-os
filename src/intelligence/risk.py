from typing import Any, Dict, List
from src.models.events import NormalizedEvent

class RiskGate:
    def evaluate(self, event: NormalizedEvent, contract_analysis: Dict[str, Any]) -> List[str]:
        risk_flags = []
        
        # Example rules
        if contract_analysis.get("is_mintable", False):
            risk_flags.append("Mintable token (Inflation risk)")
            
        if contract_analysis.get("top_10_holders_pct", 0) > 50.0:
            risk_flags.append("High holder concentration (>50%)")
            
        liquidity = float(event.metadata.get("liquidityUsd", 100000) or 0)
        if liquidity < 50000:
            risk_flags.append("Low liquidity (<$50k)")
            
        return risk_flags
