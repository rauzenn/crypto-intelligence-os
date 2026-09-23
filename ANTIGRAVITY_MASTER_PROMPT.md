# Antigravity Master Prompt — Crypto Intelligence OS

You are the engineering team for a project called Crypto Intelligence OS.

Your job is to build the repository according to the project files in this repository.

## Mission

Build a 24/7 crypto intelligence system for a degen-style user whose priority is early discovery.

The system must detect under-discovered crypto opportunities and meaningful ecosystem changes as early as possible, verify them using multiple independent evidence sources, assess risk, and deliver concise evidence-backed alerts through Telegram.

## Non-negotiable rules

1. Do not build autonomous trading in Phase 1.
2. Never request or store seed phrases/private keys.
3. Never commit secrets.
4. Do not create fake data or pretend an API works if it has not been tested.
5. Every external data adapter must have:
   - timeout
   - retry policy
   - rate-limit handling
   - logging
   - test/mocking path
6. Every alert must have evidence references and timestamps.
7. Do not let a single social post trigger a high-priority alpha alert.
8. Do not call a wallet "smart money" based on one successful transaction.
9. Preserve raw references so every derived signal can be audited.
10. Prefer primary/on-chain evidence over social commentary when they conflict.
11. Build modular adapters so providers can be replaced.
12. Keep the chain list dynamic; do not hard-code a permanent "top chains" ranking.
13. Do not optimize for alert count at the expense of information quality.
14. The minimum target is 10 useful alerts/day, not 10 arbitrary alerts/day.

## Build order

Phase 1:
- repository foundation
- configuration
- database
- Redis
- event models
- source adapters
- Telegram
- logging
- tests

Phase 2:
- market anomaly detection
- DEX/token discovery
- Solana wallet monitoring
- Alpha Radar
- Coin Research

Phase 3:
- Wallet Hunter
- Chain Discovery
- Narrative Engine
- Risk Engine

Phase 4:
- historical outcomes
- source reputation
- score calibration
- dashboard

## First engineering task

Before writing a large amount of code:

1. Read README.md
2. Read PRD_v0.1.md
3. Read ARCHITECTURE_v0.1.md
4. Read TASKS_v0.1.md
5. Produce an implementation plan
6. Identify missing API credentials/configuration
7. Implement only the P0 foundation
8. Run tests
9. Report:
   - files created
   - commands run
   - tests passed/failed
   - missing credentials
   - next recommended task

Do not silently skip failures.

## Architecture preference

Use Python for data/intelligence services.

Use PostgreSQL for durable state.

Use Redis for queues/cache/deduplication.

Use Telegram as first interface.

Keep the web dashboard as a later application.

Use async I/O where appropriate.

## Data philosophy

The system should favor:
- real-time event streams
- structured APIs
- on-chain evidence
- historical measurements
- source provenance

Avoid scraping if a documented API exists.

## Wallet Hunter

This is a strategic priority.

The system must discover candidate wallets from observed historical behavior rather than relying only on a provider's label.

Candidate metrics:
- realized PnL where available
- win rate
- average entry lead time
- early-entry frequency
- number of independent successful events
- average liquidity at entry
- concentration
- holding period
- interaction with launchpads
- interaction with newly created pools
- overlap with other successful wallets

A wallet score must include sample size. Small samples should be marked as low-confidence.

## Alert template

Title:
[ALPHA] <asset/event>

Body:
- What changed
- Why now
- Evidence
- Earlyness
- Risk
- What to monitor next
- Sources

## Completion criterion for P0

A local developer should be able to:

1. start the services
2. run migrations
3. run tests
4. start the Telegram bot
5. ingest at least one real/public market data source
6. persist a normalized event
7. generate a test alert
8. inspect logs

After P0, stop and report before expanding scope.
