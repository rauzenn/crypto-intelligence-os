from src.wallet.hunter import WalletHunter2
from src.utils.logger import logger

def run_test():
    hunter = WalletHunter2()
    
    # Mocking some trades for a wallet
    mock_history = [
        {"pnl_pct": 50.0, "pnl_usd": 1500.0, "lead_time_hours": 24.5},
        {"pnl_pct": 120.0, "pnl_usd": 4000.0, "lead_time_hours": 48.0},
        {"pnl_pct": -10.0, "pnl_usd": -200.0, "lead_time_hours": 2.0},
        {"pnl_pct": 30.0, "pnl_usd": 800.0, "lead_time_hours": 14.0},
        {"pnl_pct": -50.0, "pnl_usd": -1000.0, "lead_time_hours": 0.5},
        {"pnl_pct": 200.0, "pnl_usd": 10000.0, "lead_time_hours": 72.0},
    ]
    
    logger.info("Testing WalletHunter2 analysis...")
    profile = hunter.analyze_history("0xABC123", "ethereum", mock_history)
    
    logger.info(f"Final Lifecycle State: {profile.lifecycle_state}")
    logger.info(f"Score: {profile.score.reputation_score:.1f}")
    logger.info(f"Confidence: {profile.score.confidence}")

if __name__ == "__main__":
    run_test()
