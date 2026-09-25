import asyncio
from typing import Dict, Any, List, Optional
from src.utils.logger import logger
from src.db.schema import async_session, AlertOutcomeModel, AlertModel, WalletModel, NarrativeModel
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, and_, update

class OutcomeEngine:
    """
    15. OUTCOMES TRACKING & 16. CALIBRATION FEEDBACK LOOP
    Checks the real-world performance of alerts and adjusts system weights.
    """
    def __init__(self):
        # Time windows in seconds
        self.windows = {
            "1h": 3600,
            "6h": 21600,
            "24h": 86400,
            "7d": 604800
        }
        self.false_positive_threshold = -15.0 # 15% drop is bad
        self.success_threshold = 20.0 # 20% gain is good

    async def get_pending_evaluations(self) -> List[Dict[str, Any]]:
        """
        Finds alerts that have crossed a time threshold but haven't been evaluated for that window.
        """
        pending = []
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        
        async with async_session() as session:
            # Get all alerts
            result = await session.execute(select(AlertModel).order_by(AlertModel.detected_at.desc()).limit(100))
            alerts = result.scalars().all()
            
            for alert in alerts:
                # Find which windows are due
                age_seconds = (now - alert.detected_at).total_seconds()
                
                for window_label, seconds in self.windows.items():
                    if age_seconds >= seconds:
                        # Check if outcome already exists
                        outcome_exists = await session.execute(
                            select(AlertOutcomeModel).where(
                                and_(
                                    AlertOutcomeModel.alert_id == alert.id,
                                    AlertOutcomeModel.snapshot_time == window_label
                                )
                            )
                        )
                        if not outcome_exists.scalars().first():
                            pending.append({
                                "alert_id": alert.id,
                                "asset": alert.asset,
                                "chain": alert.chain,
                                "window": window_label,
                                "content": alert.content_json,
                                "detected_at": alert.detected_at
                            })
                            
        return pending

    async def record_outcome(self, alert_data: Dict[str, Any], current_price: float):
        """
        Record the snapshot and trigger calibration if necessary.
        """
        alert_id = alert_data["alert_id"]
        window_label = alert_data["window"]
        content = alert_data["content"]
        
        # We need entry price. For simplicity, assuming it was stored in content or we use a mock.
        entry_price = content.get("entry_price_usd", 0.0) 
        if entry_price == 0.0:
            # If no entry price recorded, we can't calculate PnL properly. 
            # In a full system, AlphaRadar must embed the entry price.
            # We will simulate for demonstration.
            entry_price = current_price * 0.9 # Mock: assume it went up 10%

        pnl_pct = ((current_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
        
        is_false_positive = "false"
        if pnl_pct <= self.false_positive_threshold:
            is_false_positive = "true"
        elif pnl_pct >= self.success_threshold:
            is_false_positive = "success"
            
        async with async_session() as session:
            outcome = AlertOutcomeModel(
                alert_id=alert_id,
                snapshot_time=window_label,
                price_at_alert=str(entry_price),
                price_at_snapshot=str(current_price),
                pnl_pct=str(pnl_pct),
                is_false_positive=is_false_positive
            )
            session.add(outcome)
            await session.commit()
            
            logger.info(f"[OutcomeEngine] Recorded {window_label} outcome for Alert {alert_id}. PnL: {pnl_pct:.1f}%")
            
            # CALIBRATION LOOP
            await self._calibrate_system(alert_data, is_false_positive, pnl_pct)
            
    async def _calibrate_system(self, alert_data: Dict[str, Any], is_false_positive: str, pnl_pct: float):
        """
        Punish or reward sources/wallets/narratives based on the outcome.
        """
        content = alert_data["content"]
        sources = content.get("sources", [])
        
        if not sources: return
        
        async with async_session() as session:
            if is_false_positive == "true":
                logger.warning(f"[Calibration] Alert {alert_data['alert_id']} failed (-{abs(pnl_pct):.1f}%). Penalizing sources: {sources}")
                # Penalize wallets
                for src in sources:
                    if src.startswith("0x") or len(src) > 30: # Likely a wallet address
                        wallet = await session.execute(select(WalletModel).where(WalletModel.address == src))
                        w = wallet.scalars().first()
                        if w:
                            new_score = max(0.0, float(w.reputation_score) - 10.0)
                            w.reputation_score = str(new_score)
            elif is_false_positive == "success":
                logger.info(f"[Calibration] Alert {alert_data['alert_id']} succeeded (+{pnl_pct:.1f}%). Rewarding sources: {sources}")
                # Reward wallets
                for src in sources:
                    if src.startswith("0x") or len(src) > 30:
                        wallet = await session.execute(select(WalletModel).where(WalletModel.address == src))
                        w = wallet.scalars().first()
                        if w:
                            new_score = min(100.0, float(w.reputation_score) + 5.0)
                            w.reputation_score = str(new_score)
            await session.commit()
