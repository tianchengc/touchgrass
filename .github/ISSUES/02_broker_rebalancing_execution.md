# Issue: Automated Broker Integration for Direct Position Rebalancing Execution

## Description
Touchgrass Trader currently evaluates portfolio health and outputs position rebalancing recommendations (e.g. `BUY`, `SELL / AVOID`, `HOLD`). To enable zero-touch portfolio management, we need an optional broker execution layer.

## Proposed Architecture
- Interface with popular open APIs: **Alpaca Trading API** (US stocks) and **Interactive Brokers API (ib_insync)**.
- Guard executions with strict risk controls (max position sizing limits, stop-loss order attachment, manual approval confirmation flag).

## Tasks
- [ ] Create `touchgrass/src/broker/` interface module.
- [ ] Implement `AlpacaBroker` adapter for order placement and position querying.
- [ ] Add explicit dry-run mode (`--dry-run`) to preview trades before sending to broker.
- [ ] Provide user configuration flag `EXECUTE_AUTOMATED_TRADES=true`.
