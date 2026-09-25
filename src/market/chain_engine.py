from typing import List, Dict, Any
from src.utils.logger import logger
from datetime import datetime

class ChainDiscoveryEngine:
    def __init__(self):
        self.tvl_threshold_a = 50_000_000 # $50M
        self.tvl_threshold_b = 5_000_000  # $5M

    def calculate_acceleration(self, chain_metrics_history: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Determine monitoring tiers based on activity acceleration, absolute TVL, and volume.
        """
        tiers = {}
        for chain_data in chain_metrics_history:
            chain = chain_data.get("chain", "unknown")
            tvl = chain_data.get("tvl", 0)
            tvl_growth_pct = chain_data.get("tvl_growth_pct", 0)
            vol_growth_pct = chain_data.get("vol_growth_pct", 0)
            
            # Tier logic
            if tvl > self.tvl_threshold_a or tvl_growth_pct > 50 or vol_growth_pct > 100:
                tiers[chain] = "Tier A" # High priority, continuous monitoring
            elif tvl > self.tvl_threshold_b or tvl_growth_pct > 20 or vol_growth_pct > 50:
                tiers[chain] = "Tier B" # Opportunistic monitoring
            else:
                tiers[chain] = "Tier C" # Discovery-only periodic scans
                
        # Count tiers for logging
        counts = {"Tier A": 0, "Tier B": 0, "Tier C": 0}
        for t in tiers.values():
            counts[t] = counts.get(t, 0) + 1
            
        logger.info(f"Chain tiers evaluated. A:{counts['Tier A']} B:{counts['Tier B']} C:{counts['Tier C']}")
        return tiers
