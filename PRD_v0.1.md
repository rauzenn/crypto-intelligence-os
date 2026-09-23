# Product Requirements Document — Crypto Intelligence OS v0.1

## 1. User

Han is a crypto-native, degen-style market participant seeking early information rather than conventional market commentary.

Primary need:

> Find under-discovered opportunities and meaningful changes as early as possible, verify them quickly, and deliver the evidence in Telegram.

## 2. Definition of Alpha

For this project, alpha is not simply a price increase.

An alpha candidate is an event, asset, wallet behavior, narrative, protocol development, liquidity movement, or information cluster that:

- is not yet broadly discovered,
- has measurable evidence,
- may have meaningful downstream market impact,
- can be detected early enough to matter,
- and survives a minimum verification/risk gate.

The system must explicitly distinguish:

- Early signal
- Confirmed signal
- Late/consensus signal
- Noise
- Scam/risk event
- Unknown

## 3. Scope

### Assets
- Large-cap crypto
- Mid-cap crypto
- Small-cap crypto
- Newly launched tokens
- Memecoins
- Stablecoins
- Governance tokens
- NFT-related assets

### Ecosystems
- Major L1s
- L2s
- Appchains
- emerging chains
- bridges
- interoperability

### Protocols
- DEX
- lending
- restaking
- liquid staking
- yield
- perps infrastructure (research only; user does not trade perps)
- prediction markets
- RWA
- DePIN
- AI/agents
- gaming
- social
- NFT infrastructure
- launchpads

### Events
- Token launches
- liquidity creation
- unusual volume
- unusual wallet activity
- whale accumulation/distribution
- smart-money activity
- new pools
- exchange listings
- protocol launches
- partnerships
- funding
- governance
- upgrades
- unlocks
- hacks/exploits
- bridge flows
- narrative acceleration
- social acceleration

## 4. Alpha Radar

The radar must continuously look for:

### A. Market anomalies
- volume acceleration
- price acceleration
- liquidity changes
- unusual transaction count
- unusual DEX activity

### B. On-chain anomalies
- new wallets
- wallet clustering
- repeated profitable traders
- smart-money accumulation
- token flows
- new liquidity
- bridge inflows/outflows
- protocol usage acceleration

### C. Social anomalies
- mention velocity
- new account clusters
- repeated mentions across independent sources
- influential-source activity
- narrative migration between chains

### D. Fundamental/catalyst anomalies
- new launch
- partnership
- funding
- upgrade
- governance proposal
- token unlock
- exchange listing
- security event

## 5. Wallet Hunter

This is a first-class subsystem.

Goal:

> Identify wallets that repeatedly appear early in major memecoin/trend moves, then monitor them.

### Wallet discovery signals

- early entry before major price expansion
- repeated profitable early entries
- multiple independent successful calls
- concentration in emerging launches
- recurring interaction with launchpads/DEXs
- interaction with tokens before social acceleration
- clustering with other high-performing wallets

### Wallet lifecycle

DISCOVER → SCORE → WATCHLIST → MONITOR → RE-EVALUATE → PROMOTE/DEMOTE

The system must not assume a wallet is "smart money" merely because it made one profitable trade.

## 6. Chain Discovery Engine

The system must not hard-code a permanent chain list.

It periodically measures:

- DeFi TVL
- DEX volume
- active addresses
- protocol count
- stablecoin activity
- new token/contract creation
- liquidity growth
- bridge flows
- social velocity
- developer/ecosystem activity

It produces a dynamic:

- Tier A: high-priority monitoring
- Tier B: opportunistic monitoring
- Tier C: discovery-only monitoring

These are operational monitoring tiers, not quality rankings of chains.

Initial seed coverage should be broad enough to avoid blind spots; the discovery engine decides where monitoring intensity increases.

## 7. Telegram

Telegram is the first user interface.

Commands:

- /radar
- /scan
- /coin <symbol/address>
- /research <asset/project>
- /wallet <address>
- /watchlist
- /narratives
- /chains
- /alerts
- /why <asset>
- /risk <asset>
- /sources
- /status

## 8. Alert format

Every high-priority alert should contain:

- What happened
- Why it matters
- How early the signal is
- Evidence
- Cross-source confirmation
- Risk flags
- Relevant links
- Timestamp
- Confidence / evidence grade
- What would invalidate the signal

Example:

ALPHA RADAR — EARLY SIGNAL

Asset:
Chain:
Detected:
Why now:
On-chain evidence:
Market evidence:
Social evidence:
Catalyst:
Risk flags:
Earlyness:
Evidence grade:
Sources:
Next thing to watch:

The system must never present an alert as a guaranteed profit opportunity.

## 9. Alert quality

Primary objective:

- ≥10 useful alerts/day target

Secondary objectives:

- minimize duplicate alerts
- minimize social-only noise
- maximize lead time
- maximize evidence density
- track false positives
- track missed opportunities
- calibrate scoring

## 10. Learning loop

Every alert becomes a historical event.

Store:

- detection timestamp
- detection price/liquidity
- evidence
- score
- source set
- wallet set
- narrative
- subsequent price/volume/liquidity behavior
- 1h / 6h / 24h / 3d / 7d outcome
- false-positive label
- post-mortem

This creates the project's proprietary historical intelligence layer.
