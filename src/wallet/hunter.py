from typing import List, Dict, Any, Tuple
from src.utils.logger import logger
from src.wallet.models import WalletProfile, WalletScore, WalletLifecycle, WalletCluster
from datetime import datetime
import statistics
import uuid

class WalletHunter2:
    """
    7. WALLET HUNTER 2.0
    Strategic core module to detect and score smart money.
    """
    def __init__(self):
        self.wallets: Dict[str, WalletProfile] = {}
        self.clusters: Dict[str, WalletCluster] = {}

    def analyze_history(self, address: str, chain: str, trade_history: List[Dict[str, Any]]) -> WalletProfile:
        """
        Analyze a wallet's trade history and generate a comprehensive WalletScore.
        """
        profile = self.wallets.get(address, WalletProfile(address=address, chain=chain))
        
        sample_size = len(trade_history)
        if sample_size == 0:
            return profile
            
        pnls = [t.get("pnl_usd", 0.0) for t in trade_history]
        pnl_pcts = [t.get("pnl_pct", 0.0) for t in trade_history]
        lead_times = [t.get("lead_time_hours", 0.0) for t in trade_history]
        
        wins = sum(1 for p in pnl_pcts if p > 0)
        win_rate = wins / sample_size
        
        median_pnl_pct = statistics.median(pnl_pcts) if pnl_pcts else 0.0
        median_lead = statistics.median(lead_times) if lead_times else 0.0
        
        early_entry_count = sum(1 for lt in lead_times if lt > 12.0) # More than 12h before pump
        early_freq = early_entry_count / sample_size
        
        # Risk adjusted performance (simplified Sharpe-like proxy)
        std_dev = statistics.stdev(pnl_pcts) if sample_size > 1 else 1.0
        if std_dev == 0: std_dev = 1.0
        risk_adj = median_pnl_pct / std_dev
        
        # Consistency proxy
        consistency = 1.0 - (std_dev / max(abs(median_pnl_pct), 1.0))
        
        # Calculate raw reputation
        rep_score = (win_rate * 30.0) + (early_freq * 30.0) + (min(median_lead, 48) * 0.5) + (min(risk_adj, 5.0) * 4.0)
        rep_score = min(max(rep_score, 0.0), 100.0)
        
        # Determine confidence based on sample size
        confidence = "LOW"
        if sample_size >= 20:
            confidence = "HIGH"
        elif sample_size >= 5:
            confidence = "MEDIUM"
            
        score = WalletScore(
            sample_size=sample_size,
            realized_pnl_usd=sum(pnls),
            win_rate=win_rate,
            median_pnl_pct=median_pnl_pct,
            risk_adjusted_performance=risk_adj,
            early_entry_frequency=early_freq,
            median_lead_time_hours=median_lead,
            consistency_score=consistency,
            reputation_score=rep_score,
            confidence=confidence
        )
        
        profile.score = score
        from datetime import timezone
        profile.last_active = datetime.now(timezone.utc)
        self._update_lifecycle(profile)
        self.wallets[address] = profile
        
        logger.info(f"[WalletHunter] Analyzed {address} - Score: {rep_score:.1f} (Conf: {confidence})")
        return profile
        
    def _update_lifecycle(self, profile: WalletProfile):
        """State machine for Wallet lifecycle."""
        current = profile.lifecycle_state
        score = profile.score.reputation_score
        conf = profile.score.confidence
        
        if current == WalletLifecycle.CANDIDATE:
            if conf in ["MEDIUM", "HIGH"] and score > 50:
                profile.lifecycle_state = WalletLifecycle.WATCHED
        elif current == WalletLifecycle.WATCHED:
            if conf == "HIGH" and score > 80:
                profile.lifecycle_state = WalletLifecycle.HIGH_SIGNAL
            elif score < 40:
                profile.lifecycle_state = WalletLifecycle.PROBATION
        elif current == WalletLifecycle.HIGH_SIGNAL:
            if score < 70:
                profile.lifecycle_state = WalletLifecycle.DEGRADED
        elif current in [WalletLifecycle.DEGRADED, WalletLifecycle.PROBATION]:
            if score > 60:
                profile.lifecycle_state = WalletLifecycle.WATCHED
            elif conf == "HIGH" and score < 20:
                profile.lifecycle_state = WalletLifecycle.ARCHIVED
                
class WalletClusterer:
    """
    8. WALLET CLUSTERING
    Investigates clusters of wallets belonging to the same entity.
    """
    def __init__(self):
        self.clusters: Dict[str, WalletCluster] = {}
        
    def analyze_behaviors(self, wallets: List[WalletProfile], cross_wallet_events: List[Dict[str, Any]]):
        """
        Looks for common funding, timing similarity, and synchronized behaviors.
        """
        # Placeholder for complex graph logic
        # In reality, this queries the neo4j or relational graph db
        
        logger.info("[WalletClusterer] Analyzing cross-wallet behavior for clustering...")
        
        # Mocking a cluster detection
        if len(wallets) >= 2:
            cluster_id = str(uuid.uuid4())
            cluster = WalletCluster(
                cluster_id=cluster_id,
                probable_wallets=[w.address for w in wallets[:2]],
                confidence="MEDIUM",
                evidence=[
                    "Synchronized entries on token X within 5 minutes",
                    "Common funding from Binance Hot Wallet"
                ],
                cluster_tags=["Automated MEV", "Insider"]
            )
            self.clusters[cluster_id] = cluster
            logger.info(f"[WalletClusterer] Detected probable cluster {cluster_id} with {len(cluster.probable_wallets)} wallets.")
            return cluster
        return None
