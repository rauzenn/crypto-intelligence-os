from typing import Dict, Any, List, Optional
from src.utils.logger import logger
from pydantic import BaseModel
from datetime import datetime, timezone

class Position(BaseModel):
    asset: str
    entry_price: float
    size_usd: float
    amount: float
    entry_time: datetime = datetime.now(timezone.utc)
    status: str = "OPEN" # OPEN, CLOSED

class PaperPortfolio:
    """
    STEP 17 (Rule 32): ACTION ENGINE / PAPER TRADING
    Simulates portfolio management and position sizing based on Risk Engine signals.
    """
    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.positions: List[Position] = []
        
    def _calculate_position_size(self, confidence: float, risk_score: float) -> float:
        """
        Basic position sizing simulator.
        High confidence + Low risk = larger size. (Max 5% of portfolio)
        """
        max_risk_pct = 0.05
        
        # Scale down based on risk
        adjusted_risk = max(0.1, 1.0 - (risk_score / 100.0))
        size_pct = max_risk_pct * (confidence / 100.0) * adjusted_risk
        
        return self.balance * size_pct

    def simulate_buy(self, asset: str, current_price: float, confidence: float, risk_score: float) -> Optional[Position]:
        """
        Executes a paper buy if conditions are met.
        """
        if current_price <= 0:
            return None
            
        size_usd = self._calculate_position_size(confidence, risk_score)
        
        if size_usd < 10.0:
            logger.warning(f"[ActionEngine] Size too small (${size_usd:.2f}) for {asset}. Trade aborted.")
            return None
            
        if size_usd > self.balance:
            size_usd = self.balance
            
        amount = size_usd / current_price
        self.balance -= size_usd
        
        pos = Position(asset=asset, entry_price=current_price, size_usd=size_usd, amount=amount)
        self.positions.append(pos)
        
        logger.info(f"[ActionEngine] PAPER BUY: {amount:.2f} {asset} @ ${current_price:.4f} (Total: ${size_usd:.2f})")
        return pos
        
    def simulate_sell(self, asset: str, current_price: float) -> float:
        """
        Closes an open position and realizes PnL.
        """
        for pos in self.positions:
            if pos.asset == asset and pos.status == "OPEN":
                exit_value = pos.amount * current_price
                pnl = exit_value - pos.size_usd
                pnl_pct = (pnl / pos.size_usd) * 100
                
                pos.status = "CLOSED"
                self.balance += exit_value
                
                logger.info(f"[ActionEngine] PAPER SELL: {asset} @ ${current_price:.4f} | PnL: ${pnl:.2f} ({pnl_pct:.1f}%) | New Balance: ${self.balance:.2f}")
                return pnl
        return 0.0
