from typing import Any, Dict, List
from src.normalization.events import NormalizedEvent
from src.risk.models import RiskProfile, RiskCategory

class RiskGate:
    """
    14. RISK ENGINE 2.0
    Evaluates if an alpha signal is actually a trap/honeypot.
    """
    def evaluate(self, event: NormalizedEvent, contract_analysis: Dict[str, Any]) -> RiskProfile:
        profile = RiskProfile()
        
        # 1. Contract Security
        if contract_analysis.get("is_honeypot", False) or not contract_analysis.get("can_sell", True):
            profile.flags.append("CRITICAL: Honeypot or Cannot Sell detected.")
            profile.can_sell = False
            profile.contract_security_score = 0.0
            profile.category = RiskCategory.CRITICAL
            
        if contract_analysis.get("is_mintable", False):
            profile.flags.append("Mintable token (Inflation risk)")
            profile.contract_security_score -= 30.0
            
        if contract_analysis.get("is_pausable", False):
            profile.flags.append("Pausable contract (Trading block risk)")
            profile.contract_security_score -= 40.0
            
        if contract_analysis.get("is_proxy", False):
            profile.flags.append("Proxy contract (Implementation can change)")
            profile.contract_security_score -= 20.0
            
        # 2. Liquidity Quality
        liquidity = float(event.metadata.get("liquidityUsd", 0) or 0)
        is_locked = contract_analysis.get("liquidity_locked", False)
        
        if liquidity < 10000:
            profile.flags.append("CRITICAL: Micro liquidity (<$10k)")
            profile.liquidity_score = 0.0
            if profile.category != RiskCategory.CRITICAL:
                profile.category = RiskCategory.HIGH
        elif liquidity < 50000:
            profile.flags.append("Low liquidity (<$50k)")
            profile.liquidity_score -= 50.0
            
        if not is_locked and liquidity > 0:
            profile.flags.append("Liquidity is NOT locked (Rug pull risk)")
            profile.liquidity_score -= 50.0
            
        # 3. Holder Distribution
        top_10 = contract_analysis.get("top_10_holders_pct", 0)
        if top_10 > 80.0:
            profile.flags.append("CRITICAL: Extreme holder concentration (>80%)")
            profile.holder_distribution_score = 0.0
            if profile.category != RiskCategory.CRITICAL:
                profile.category = RiskCategory.CRITICAL
        elif top_10 > 50.0:
            profile.flags.append("High holder concentration (>50%)")
            profile.holder_distribution_score -= 40.0
            
        # Overall Risk Calculation (0 is safest, 100 is max risk)
        profile.contract_security_score = max(0.0, profile.contract_security_score)
        profile.liquidity_score = max(0.0, profile.liquidity_score)
        profile.holder_distribution_score = max(0.0, profile.holder_distribution_score)
        
        avg_score = (profile.contract_security_score + profile.liquidity_score + profile.holder_distribution_score) / 3.0
        profile.overall_risk_score = 100.0 - avg_score
        
        # Adjust category based on overall score if not already CRITICAL
        if profile.category != RiskCategory.CRITICAL:
            if profile.overall_risk_score > 70:
                profile.category = RiskCategory.HIGH
            elif profile.overall_risk_score > 30:
                profile.category = RiskCategory.MEDIUM
            else:
                profile.category = RiskCategory.LOW
                
        return profile
