from src.detection.signal import CompositeScore

class ScoringEngine:
    """
    N. SCORING / CALIBRATION LAYER
    Calculates the 'magic score' from independent intelligence vectors.
    """
    
    def calculate_composite_score(self, score_components: CompositeScore) -> CompositeScore:
        # Base weightings for different vectors
        weights = {
            "earlyness": 1.5,
            "onchain_strength": 1.2,
            "market_confirmation": 1.0,
            "wallet_quality": 1.3,
            "narrative_velocity": 1.1,
            "catalyst_strength": 0.9,
            "liquidity_quality": 1.0
        }
        
        # Calculate raw sum
        raw_sum = (
            score_components.earlyness * weights["earlyness"] +
            score_components.onchain_strength * weights["onchain_strength"] +
            score_components.market_confirmation * weights["market_confirmation"] +
            score_components.wallet_quality * weights["wallet_quality"] +
            score_components.narrative_velocity * weights["narrative_velocity"] +
            score_components.catalyst_strength * weights["catalyst_strength"] +
            score_components.liquidity_quality * weights["liquidity_quality"]
        )
        
        # Apply independence multiplier and source quality
        multiplied = raw_sum * score_components.cross_source_independence * (score_components.source_quality or 1.0)
        
        # Apply risk penalty (reduction)
        penalized = multiplied * (1.0 - score_components.risk_penalty)
        
        # Normalize roughly out of 100
        # In reality, this requires calibration curves (Step 12)
        final_raw = min(100.0, max(0.0, penalized))
        
        score_components.raw_score = final_raw
        
        # Calibration will be implemented later, for now calibrated = raw
        score_components.calibrated_score = final_raw
        
        # Confidence calculation
        if score_components.cross_source_independence >= 1.5 and final_raw > 70:
            score_components.confidence = "HIGH"
        elif score_components.cross_source_independence > 1.0 and final_raw > 40:
            score_components.confidence = "MEDIUM"
        else:
            score_components.confidence = "LOW"
            
        return score_components
