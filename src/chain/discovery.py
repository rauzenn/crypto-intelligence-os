from typing import Dict, List, Any
from src.chain.models import ChainProfile, ChainMetrics, ChainState
from src.utils.logger import logger
from datetime import datetime, timezone

class ChainDiscoveryEngine:
    """
    STEP 7 (Rule 9): DYNAMIC CHAIN DISCOVERY
    Evaluates blockchain activity to determine which networks JARVIS should monitor.
    """
    def __init__(self):
        self.chains: Dict[str, ChainProfile] = {}

    def process_chain_metrics(self, chain_name: str, new_metrics: Dict[str, Any]):
        """
        Ingest new metrics for a chain (e.g. from DeFiLlama or general event bus)
        and update its state.
        """
        profile = self.chains.get(chain_name.lower(), ChainProfile(name=chain_name.lower()))
        
        # Update metrics (Mocking delta application)
        profile.metrics.tvl_usd = new_metrics.get("tvl_usd", profile.metrics.tvl_usd)
        profile.metrics.dex_volume_24h = new_metrics.get("dex_volume_24h", profile.metrics.dex_volume_24h)
        profile.metrics.active_addresses_24h = new_metrics.get("active_addresses_24h", profile.metrics.active_addresses_24h)
        profile.metrics.stablecoin_inflows = new_metrics.get("stablecoin_inflows", profile.metrics.stablecoin_inflows)
        profile.metrics.tvl_acceleration = new_metrics.get("tvl_acceleration", 0.0)

        # Evaluate State
        old_state = profile.state
        new_state = self._evaluate_state(profile.metrics)
        
        if old_state != new_state:
            logger.info(f"[ChainDiscovery] {chain_name} transitioned from {old_state} to {new_state}")
            profile.state = new_state
            
        profile.last_updated = datetime.now(timezone.utc)
        self.chains[chain_name.lower()] = profile

    def _evaluate_state(self, metrics: ChainMetrics) -> ChainState:
        """
        Determines the operational monitoring state based on intensity.
        """
        if metrics.tvl_usd > 1_000_000_000 and metrics.dex_volume_24h > 500_000_000:
            return ChainState.HIGH_INTENSITY
        elif metrics.tvl_acceleration > 20.0 or metrics.stablecoin_inflows > 50_000_000:
            return ChainState.EMERGING
        elif metrics.tvl_usd > 100_000_000:
            return ChainState.ACTIVE
        elif metrics.tvl_usd > 10_000_000:
            return ChainState.WATCH
        else:
            return ChainState.DEGRADED

    def get_chains_to_monitor(self) -> List[str]:
        """
        Returns a list of chain names that the system should actively allocate RPC resources to.
        """
        active_states = [ChainState.EMERGING, ChainState.ACTIVE, ChainState.HIGH_INTENSITY]
        return [name for name, profile in self.chains.items() if profile.state in active_states]
