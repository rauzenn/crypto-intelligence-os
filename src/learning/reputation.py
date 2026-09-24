from typing import Dict, Any, List
from src.utils.logger import logger

class ReputationSystem:
    def __init__(self):
        self.source_scores = {}
        self.wallet_scores = {}

    def penalize_source(self, source_name: str, penalty_points: float = 5.0):
        current = self.source_scores.get(source_name, 100.0)
        self.source_scores[source_name] = max(0.0, current - penalty_points)
        logger.info(f"Source {source_name} penalized. New reputation: {self.source_scores[source_name]}")

    def reward_source(self, source_name: str, reward_points: float = 2.0):
        current = self.source_scores.get(source_name, 100.0)
        self.source_scores[source_name] = min(100.0, current + reward_points)
        logger.info(f"Source {source_name} rewarded. New reputation: {self.source_scores[source_name]}")
        
    def recalibrate_wallet(self, wallet_address: str, outcome_pnl: float):
        """
        Dynamically adjust wallet reputation based on actual outcomes of following their trades.
        """
        current = self.wallet_scores.get(wallet_address, 50.0)
        
        if outcome_pnl > 20.0:
            # Huge success
            new_score = current + 10.0
        elif outcome_pnl > 0:
            # Minor success
            new_score = current + 2.0
        elif outcome_pnl < -15.0:
            # Rekt / false positive / scam
            new_score = current - 15.0
        else:
            # Neutral / noise
            new_score = current - 1.0
            
        self.wallet_scores[wallet_address] = max(0.0, min(100.0, new_score))
        logger.info(f"Wallet {wallet_address} recalibrated to {self.wallet_scores[wallet_address]:.1f}")
