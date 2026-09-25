import asyncio
import httpx
from src.db.schema import init_db, async_session, EventModel
from src.normalization.events import NormalizedEvent, Alert
from src.utils.logger import logger

async def fetch_coingecko():
    logger.info("Fetching data from CoinGecko (Public API)...")
    async with httpx.AsyncClient() as client:
        # Simple public endpoint
        response = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd")
        response.raise_for_status()
        return response.json()

async def persist_event(data):
    logger.info("Persisting normalized event...")
    from src.normalization.events import Provenance
    event = NormalizedEvent(
        event_type="market_price",
        chain="multiple",
        asset="BTC/ETH/SOL",
        provenance=Provenance(
            source_id="coingecko",
            source_type="market",
            raw_reference=f"cg_price_{asyncio.get_event_loop().time()}"
        ),
        metadata=data
    )
    
    async with async_session() as session:
        db_event = EventModel(
            event_type=event.event_type,
            chain=event.chain,
            asset=event.asset,
            timestamp=event.provenance.timestamp.replace(tzinfo=None),
            source=event.provenance.source_id,
            raw_reference=event.provenance.raw_reference,
            metadata_json=event.metadata
        )
        session.add(db_event)
        await session.commit()
        logger.info(f"Event {db_event.raw_reference} saved to DB.")

async def generate_test_alert():
    logger.info("Generating test alert...")
    alert = Alert(
        title="Test Alpha Signal",
        asset="SOL",
        chain="Solana",
        what_changed="System initialized successfully.",
        why_now="P0 foundation completed.",
        evidence=["Database running", "API tested", "Models validated"],
        earlyness="Day 1",
        risk_flags=["Development environment"],
        sources=["System"],
        next_to_watch="Data ingestion pipelines"
    )
    logger.info(f"Generated Alert:\\n{alert.format_telegram()}")
    return alert

async def main():
    logger.info("--- Starting P0 Test Run ---")
    await init_db()
    
    try:
        data = await fetch_coingecko()
        await persist_event(data)
        await generate_test_alert()
        logger.info("--- P0 Test Run Completed Successfully ---")
    except Exception as e:
        logger.error(f"P0 Test Run Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
