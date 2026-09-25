import asyncio
from src.utils.logger import logger
from src.ingestion.registry import registry
from src.db.schema import init_db, async_session, EventModel
from src.interface.telegram_service import send_alert
from typing import Dict, Any

async def run_ingestion_cycle(ctx: Dict[str, Any]):
    """
    Periodic task to fetch data from all active sources and persist normalized events.
    """
    logger.info("Starting scheduled ingestion cycle...")
    
    adapters = registry.get_all_active()
    if not adapters:
        logger.warning("No active adapters found for ingestion.")
        return
        
    for adapter in adapters:
        try:
            logger.info(f"Worker fetching from {adapter.name}...")
            raw_data = await adapter.fetch_data()
            events = adapter.normalize_events(raw_data)
            
            if not events:
                continue
                
            async with async_session() as session:
                for event in events:
                    # Persist event
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
                    
                    # C. EVENT BUS: Publish the normalized event to the stream
                    from src.event_bus.bus import bus
                    await bus.publish("events.normalized", event.to_dict())

                await session.commit()
                logger.info(f"Persisted and published {len(events)} events from {adapter.name}")
                
        except Exception as e:
            logger.error(f"Error in ingestion cycle for {adapter.name}: {e}")

async def run_wallet_hunter_cycle(ctx: Dict[str, Any]):
    """
    Periodic task to analyze profitable wallets and update the watchlist.
    """
    logger.info("Starting Wallet Hunter cycle... (Placeholder)")
    # Logic to query recent trades, identify smart money, score, and persist

async def startup(ctx: Dict[str, Any]):
    logger.info("Worker starting up. Initializing DB and resources...")
    await init_db()
    from src.detection.listener import setup_detection_listeners
    setup_detection_listeners()
    from src.wallet.listener import setup_wallet_listeners
    setup_wallet_listeners()

async def shutdown(ctx: Dict[str, Any]):
    logger.info("Worker shutting down. Cleaning up...")
    await registry.close_all()
    from src.event_bus.bus import bus
    await bus.close()
