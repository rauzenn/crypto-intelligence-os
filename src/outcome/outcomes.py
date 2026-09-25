from typing import Dict, Any, List
from src.utils.logger import logger
from src.db.schema import async_session, AlertOutcomeModel
from datetime import datetime, timezone

class SignalOutcomeTracker:
    def __init__(self):
        # 1h, 6h, 24h, 3d, 7d
        self.intervals = [3600, 21600, 86400, 259200, 604800] 
        self.false_positive_threshold = -15.0 # If it drops 15% quickly, it might be a false positive trap
        self.success_threshold = 20.0 # 20% gain is a successful alpha signal

    async def record_snapshot(self, alert_id: int, snapshot_label: str, entry_price: float, current_price: float):
        """
        Record the outcome of a past alert at a specific snapshot interval.
        """
        pnl_pct = ((current_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
        
        is_false_positive = "false"
        if pnl_pct < self.false_positive_threshold:
            is_false_positive = "true"
            logger.warning(f"Alert {alert_id} flagged as False Positive! PnL: {pnl_pct:.1f}%")
            
        async with async_session() as session:
            outcome = AlertOutcomeModel(
                alert_id=alert_id,
                snapshot_time=snapshot_label,
                price_at_alert=str(entry_price),
                price_at_snapshot=str(current_price),
                pnl_pct=str(pnl_pct),
                is_false_positive=is_false_positive
            )
            session.add(outcome)
            await session.commit()
            logger.info(f"Recorded {snapshot_label} outcome for Alert {alert_id}. PnL: {pnl_pct:.1f}%")

    def evaluate_system_health(self, recent_outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Review recent false positives and calibrate scoring.
        """
        total = len(recent_outcomes)
        if total == 0:
            return {"status": "insufficient_data"}
            
        false_positives = sum(1 for o in recent_outcomes if o.get("is_false_positive") == "true")
        fp_rate = (false_positives / total) * 100
        
        logger.info(f"System Health: {fp_rate:.1f}% False Positive Rate over last {total} outcomes.")
        
        if fp_rate > 40.0:
            logger.warning("HIGH FALSE POSITIVE RATE. Recommend tightening Risk Engine thresholds.")
            
        return {
            "false_positive_rate": fp_rate,
            "total_evaluated": total,
            "recommendation": "tighten_risk" if fp_rate > 40 else "stable"
        }
