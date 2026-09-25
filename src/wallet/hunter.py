from typing import List, Dict, Any, Tuple
from src.utils.logger import logger
from datetime import datetime

class WalletHunter:
    def __init__(self):
        self.watchlist = {} # wallet -> score
        self.min_win_rate = 0.60
        self.min_trades = 5
        self.early_entry_threshold_seconds = 3600 * 24 # 1 day before pump

    def discover_candidates(self, recent_profitable_trades: List[Dict[str, Any]]) -> List[str]:
        """
        Scan a list of profitable trades. If a wallet keeps showing up early, it becomes a candidate.
        """
        candidates = set()
        for trade in recent_profitable_trades:
            wallet = trade.get("wallet")
            entry_time = trade.get("entry_time")
            pump_time = trade.get("pump_time")
            
            if wallet and entry_time and pump_time:
                # Calculate lead time
                lead_time = pump_time - entry_time
                if lead_time > self.early_entry_threshold_seconds:
                    candidates.add(wallet)
                    
        logger.info(f"WalletHunter discovered {len(candidates)} early-entry candidates.")
        return list(candidates)

    def score_wallet(self, wallet_address: str, trade_history: List[Dict[str, Any]]) -> float:
        """
        Score a wallet based on its historical performance.
        Returns a score from 0.0 to 100.0.
        """
        if not trade_history:
            return 0.0
            
        wins = sum(1 for t in trade_history if t.get("pnl_pct", 0) > 0)
        win_rate = wins / len(trade_history)
        
        if len(trade_history) < self.min_trades:
            logger.debug(f"Wallet {wallet_address} ignored (too few trades).")
            return 0.0 # Low confidence due to small sample size
            
        if win_rate < self.min_win_rate:
            return 0.0
            
        # Calculate average earlyness (lead time in hours)
        avg_lead_time_hrs = sum((t.get("pump_time", 0) - t.get("entry_time", 0)) / 3600 for t in trade_history) / len(trade_history)
        
        # Base score on win rate
        score = win_rate * 50.0 
        
        # Bonus for extreme early entries (e.g., avg > 48h)
        if avg_lead_time_hrs > 48:
            score += 30.0
        elif avg_lead_time_hrs > 24:
            score += 15.0
            
        # Bonus for consistency (number of trades)
        score += min(len(trade_history), 20)
        
        final_score = min(score, 100.0)
        logger.info(f"Wallet {wallet_address} scored {final_score:.1f} (WinRate: {win_rate:.2f}, AvgLead: {avg_lead_time_hrs:.1f}h)")
        return final_score

    def update_watchlist(self, wallet_address: str, score: float):
        if score > 60.0:
            self.watchlist[wallet_address] = score
            logger.info(f"Added/Updated {wallet_address} on watchlist with score {score:.1f}.")
        elif wallet_address in self.watchlist and score < 40.0:
            # Demotion
            del self.watchlist[wallet_address]
            logger.info(f"Demoted {wallet_address} from watchlist.")
