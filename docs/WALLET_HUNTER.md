# Wallet Hunter Design

## Goal

Find wallets that repeatedly enter emerging opportunities early, especially in memecoins and new launches.

## Discovery sources

Potential sources:
- DEX trade data
- launchpad activity
- token creation
- liquidity pool creation
- known smart-money providers
- wallet clusters
- historical signal outcomes

## Candidate selection

A wallet becomes a candidate when it repeatedly satisfies several conditions:

1. enters before major attention/price expansion
2. exits profitably or participates in multiple successful events
3. operates with sufficient sample size
4. is not simply following a late liquidity event
5. is not obviously a bot or wash trader unless that behavior is itself relevant
6. has reproducible on-chain evidence

## Required metrics

- first observed entry
- average entry lead time
- median lead time
- number of qualifying trades
- realized/unrealized PnL where available
- win rate
- median return
- max drawdown
- liquidity at entry
- position size where observable
- holding time
- chain
- launchpad/DEX interaction
- wallet cluster
- counterparty patterns

## Wallet states

candidate → probation → watched → high-signal → degraded → archived

The state must be reversible.

## Anti-overfitting

Do not promote a wallet after one trade.

Minimum sample thresholds should be configurable.

The system must store the exact transactions behind every wallet score.
