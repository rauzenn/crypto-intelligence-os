import asyncio
from src.db.schema import init_db, async_session, AlertModel, WalletModel, AlertOutcomeModel
from src.outcome.outcomes import OutcomeEngine
from src.utils.logger import logger
from datetime import datetime, timezone, timedelta
import json
from sqlalchemy import select, delete

async def setup_test_data():
    await init_db()
    async with async_session() as session:
        # Clear old outcomes for this test
        await session.execute(delete(AlertOutcomeModel))
        
        # Insert a test wallet
        wallet = WalletModel(
            address="0xTestWallet123",
            reputation_score="50.0",
            chain="ethereum"
        )
        session.add(wallet)
        
        # Insert an old alert (2 hours ago)
        old_time = datetime.now(timezone.utc) - timedelta(hours=2)
        alert = AlertModel(
            title="Test Alert",
            asset="MEME",
            chain="solana",
            detected_at=old_time.replace(tzinfo=None),
            content_json={
                "entry_price_usd": 100.0,
                "sources": ["0xTestWallet123", "twitter"]
            }
        )
        session.add(alert)
        await session.commit()
        
async def run_eval():
    engine = OutcomeEngine()
    
    logger.info("Running Outcome Evaluation...")
    pending = await engine.get_pending_evaluations()
    logger.info(f"Found {len(pending)} pending evaluations.")
    
    for p in pending:
        # Simulate price drop to $80 (-20%) -> triggers False Positive!
        await engine.record_outcome(p, current_price=80.0)
        
    # Check if wallet reputation was penalized
    async with async_session() as session:
        w = await session.execute(select(WalletModel).where(WalletModel.address == "0xTestWallet123"))
        wallet = w.scalars().first()
        logger.info(f"Wallet reputation is now: {wallet.reputation_score}")
        
async def main():
    await setup_test_data()
    await run_eval()

if __name__ == "__main__":
    asyncio.run(main())
