from typing import List, Dict, Any
from src.utils.logger import logger

class ChainDiscoveryEngine:
    def __init__(self):
        pass

    def calculate_acceleration(self, chain_metrics_history: List[Dict[str, Any]]) -> Dict[str, str]:
        # Determine monitoring tiers based on activity acceleration
        tiers = {}
        for chain_data in chain_metrics_history:
            chain = chain_data.get("chain")
            tvl_growth = chain_data.get("tvl_growth_pct", 0)
            
            if tvl_growth > 20:
                tiers[chain] = "Tier A"
            elif tvl_growth > 5:
                tiers[chain] = "Tier B"
            else:
                tiers[chain] = "Tier C"
                
        logger.info(f"Chain tiers updated: {tiers}")
        return tiers
