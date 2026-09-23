# Chain Monitoring Strategy — 2026-09-22

## Principle

Do not permanently rank chains.

The system should dynamically adjust monitoring intensity using measurable activity.

## Initial seed coverage

Start with:

- Ethereum
- Solana
- Base
- BNB Chain
- Tron
- Arbitrum
- Hyperliquid ecosystem
- Monad
- Sui
- Avalanche

Then add/remove monitoring intensity based on live metrics.

## Why these are in the seed set

Current DeFiLlama chain data exposes TVL, DEX volume, active addresses, stablecoin market cap, fees, protocol counts and changes over multiple time windows. On the current page, Ethereum, Solana, Base, BSC, Tron, Bitcoin and Arbitrum all appear with substantial measured activity; Hyperliquid, Monad, Sui and Avalanche also show material ecosystem metrics. These are operational observations, not a permanent ranking. The system should re-evaluate them continuously.

Important current measurements from the live page are stored only as a starting reference; production decisions must query the live source.

## Dynamic chain score

Example:

chain_activity_score =
  TVL momentum
+ DEX volume momentum
+ active-address momentum
+ stablecoin flow
+ protocol growth
+ new token/contract activity
+ bridge inflow
+ social velocity
+ developer/ecosystem signals

Use rolling z-scores / percentiles rather than raw values where possible.

## Data providers

DeFiLlama is useful for cross-chain TVL, DEX volume, fees, revenue, stablecoins, unlocks and ecosystem-level metrics.

Alchemy provides broad multi-chain infrastructure and currently documents support for Ethereum, Solana, Base, Arbitrum, BNB, Sui, Hyperliquid/HypereVM and many other chains.

## Future discovery

A chain can be promoted into higher-frequency monitoring when it shows:
- accelerating liquidity
- accelerating DEX activity
- rapidly increasing active users
- new protocol launches
- new token launches
- bridge inflows
- narrative/social acceleration

A chain can be demoted when activity decays for a sustained period.

## Source notes

- DeFiLlama Chains: https://defillama.com/chains
- DeFiLlama DEXs: https://defillama.com/dexs
- Alchemy supported chains: https://www.alchemy.com/docs/reference/node-supported-chains
