# System Architecture v0.1

## High-level

                    TELEGRAM / FUTURE WEB
                              |
                       Intelligence API
                              |
                      Agent Orchestrator
                              |
        +----------+----------+----------+----------+
        |          |          |          |          |
     Scout      Market     On-chain    Social     News
        |       Analyst     Analyst    Analyst    Analyst
        +----------+----------+----------+----------+
                              |
                       Evidence Fusion
                              |
                    Alpha / Risk Scoring
                              |
                        Alert Engine
                              |
                       Historical DB
                              |
                       Learning Loop

## Services

### 1. Collectors
- market collectors
- DEX collectors
- chain collectors
- wallet collectors
- social collectors
- news collectors
- protocol/event collectors

### 2. Normalization
Convert heterogeneous sources into common event objects.

Example:

```json
{
  "event_type": "wallet_trade",
  "chain": "solana",
  "wallet": "ADDRESS",
  "asset": "TOKEN",
  "timestamp": "ISO-8601",
  "source": "onchain",
  "raw_reference": "TX_SIGNATURE"
}
```

### 3. Event Bus / Queue
Use Redis initially. Move to a dedicated stream system only when volume requires it.

### 4. Intelligence Agents

- Scout Agent
- Market Agent
- On-chain Agent
- Wallet Hunter Agent
- Narrative Agent
- Social Agent
- News/Catalyst Agent
- Risk Agent
- Bear/Counter-Evidence Agent
- Synthesizer Agent

### 5. Scoring Engine

Initial evidence dimensions:

- Earlyness
- On-chain strength
- Market confirmation
- Liquidity quality
- Wallet quality
- Narrative velocity
- Source quality
- Catalyst strength
- Risk
- Cross-source independence

Do not treat an LLM's subjective confidence as the score.

### 6. Storage

PostgreSQL:

- assets
- chains
- protocols
- wallets
- wallet_events
- token_events
- social_events
- news_events
- narratives
- alerts
- alert_outcomes
- source_profiles
- chain_metrics
- raw_event_refs

Redis:

- queues
- short-lived cache
- deduplication
- rate limiting
- live state

Object storage:

- raw snapshots when needed
- research artifacts

## Agent responsibilities

### Scout
Find abnormal activity.

### Wallet Hunter
Discover and monitor high-performing early wallets.

### Market Analyst
Validate price, volume, liquidity and market structure.

### On-chain Analyst
Validate transfers, swaps, liquidity, holders, contracts and flows.

### Narrative Analyst
Detect emerging themes and cross-project propagation.

### Social Analyst
Measure social velocity and source clusters.

### News/Catalyst Analyst
Find external events and primary-source evidence.

### Risk Agent
Look for contract, liquidity, concentration, unlock, exploit and scam risks.

### Bear Agent
Actively search for evidence against the signal.

### Synthesizer
Produce one evidence-backed alert.

## Security

Never store:

- seed phrases
- private keys
- withdrawal credentials

Secrets live in environment variables / secret manager.

Research API keys must be read-only where possible.

## Deployment

Development:
- macOS
- Antigravity
- local Docker

Production:
- cloud server
- PostgreSQL
- Redis
- worker processes
- scheduler
- Telegram bot

The Mac is not the 24/7 production host.
