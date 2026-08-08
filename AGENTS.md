# AGENTS.md — Touchgrass Trader Guidance for AI Assistants

Welcome, AI Agent! You are helping a human manage their stock investments using **Touchgrass Trader**.

## Core Philosophy: Disciplined Swing Trading
1. **Swing Trading Focus (5–20 Days Hold)**: Touchgrass Trader promotes multi-day swing positions in high-conviction companies, **NOT high-frequency day trading or intraday scalp noise**.
2. **Minimum Effort, Maximum Discipline**: Protects non-expert investors from emotional trading, FOMO, and pig-butchering scam traps.
3. **Multi-Factor Intelligence**: Every trade decision is cross-checked against Kronos 5-day AI time-series predictions, Serenity supply chain bottlenecks, Uzi 7-Faction Multi-Investor Panel, and Uzi Trap Detector.
4. **Local & GitHub Automation**: The user can ask you to run rounds locally or rely on GitHub Actions running twice daily during open market hours (11:30 AM ET & 3:30 PM ET).

## Common Agent Operations

### 1. Run Swing Market Digest & Portfolio Analysis
Execute command:
```bash
python main.py run
```

### 2. Auto-Discover Swing Candidates (Supply-Chain Monopolies & KOL Conviction)
Execute command:
```bash
python main.py scan --max 5
```

### 3. Analyze Ticker (Kronos 5-Day Trend + 65 Investor Panel + Trap Security)
Execute command:
```bash
python main.py analyze NVDA
```

### 4. Add/Remove Stock from Swing Watchlist
Execute command:
```bash
python main.py add TICKER --target PRICE --notes "Reasoning"
python main.py remove TICKER
```
