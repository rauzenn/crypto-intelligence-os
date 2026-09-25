#!/bin/bash
mv src/sources/adapters src/ingestion/
mv src/sources/base.py src/ingestion/
mv src/sources/registry.py src/ingestion/
mv src/models/events.py src/normalization/
mv src/queue/redis_client.py src/event_bus/
mv src/intelligence/anomaly.py src/detection/
mv src/intelligence/earlyness.py src/detection/
mv src/intelligence/fusion.py src/fusion/
mv src/intelligence/risk.py src/risk/
mv src/intelligence/dedup.py src/event_bus/
mv src/intelligence/alpha_radar.py src/detection/radar.py
mv src/intelligence/coin_research.py src/research/
mv src/bot/telegram_service.py src/interface/
mv src/learning/outcomes.py src/outcome/
mv src/wallet_hunter/hunter.py src/wallet/
mv src/chain_discovery/engine.py src/market/chain_engine.py
mv src/narrative_engine/engine.py src/narrative/
# cleanup empty dirs
rm -rf src/sources src/models src/queue src/intelligence src/bot src/wallet_hunter src/chain_discovery src/narrative_engine
