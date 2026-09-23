# Data Source Plan

## Tier 1 — Start here

### DeFiLlama
Use for:
- chain activity
- TVL
- DEX volume
- fees/revenue
- stablecoins
- unlocks
- protocol discovery

### DEX Screener
Use for:
- token/pair discovery
- price
- volume
- liquidity
- market cap/FDV where available
- pair creation time
- social/project metadata
- boosted/token-profile signals as discovery inputs

### CoinGecko
Use for:
- asset metadata
- market metadata
- broad market coverage
- historical market data where appropriate

## Tier 2 — Real-time on-chain

### Helius
Priority for Solana.
Use for:
- wallet monitoring
- parsed transaction events
- token mints
- DEX swaps
- NFT events
- program/account monitoring
- real-time streams

### Alchemy
Priority for EVM abstraction.
Use for:
- RPC
- token/NFT APIs
- transfers
- webhooks
- multi-chain infrastructure

## Tier 3 — Wallet intelligence

### Nansen
Optional paid provider.
Use for:
- smart-money labels
- wallet profiler
- smart-money netflows
- holdings
- DEX trades
- wallet/entity relationships

## Tier 4 — Social

Telegram and X should be integrated only after:
- source permissions/access are clear
- terms/rate limits are reviewed
- source provenance is preserved

## Discovery source policy

Prefer:
1. primary on-chain data
2. official protocol/project announcements
3. structured market data
4. reputable data providers
5. social posts as early signals, not as proof

## Source provenance

Every event should preserve:
- provider
- endpoint/reference
- timestamp
- raw identifier
- ingestion timestamp
- transformation version
