import asyncio
from src.utils.logger import logger
from src.sources.registry import registry
from src.db.schema import init_db, async_session, EventModel
from src.bot.telegram_service import send_alert
from src.intelligence.alpha_radar import AlphaRadar
from typing import Dict, Any

radar = AlphaRadar()

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
                        timestamp=event.timestamp.replace(tzinfo=None),
                        source=event.source,
                        raw_reference=event.raw_reference,
                        metadata_json=event.metadata
                    )
                    session.add(db_event)
                    
                    # Run Intelligence Engine (Alpha Radar) on the event
                    # Mock context data for now (in a real scenario, fetch historical stats from DB)
                    context = {
                        "avg_volume_24h": float(event.metadata.get("volume24h", 0) or 0) * 0.2, # Hack to simulate anomaly
                        "social_mentions": 50,
                        "supporting_events": []
                    }
                    
                    alert = await radar.process_event(event, context)
                    if alert:
                        logger.info(f"ALPHA ALERT GENERATED: {alert.title}")
                        await send_alert(alert.format_telegram())

                await session.commit()
                logger.info(f"Persisted and analyzed {len(events)} events from {adapter.name}")
                
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

async def shutdown(ctx: Dict[str, Any]):
    logger.info("Worker shutting down. Cleaning up...")
    await registry.close_all()
