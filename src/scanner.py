"""
Auto Stock Discovery Engine for Touchgrass Trader.
Focuses on high-probability Swing Trading candidates driven by
Serenity Supply-Chain Bottlenecks, KOL Conviction, and Fundamental Catalysts.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
PARENT_ROOT = TOUCHGRASS_ROOT.parent
for p in [str(PARENT_ROOT), str(TOUCHGRASS_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from scripts.bridges import SerenityBridge
except ImportError:
    from touchgrass.scripts.bridges import SerenityBridge


class AutoStockScanner:
    """Discovers high-conviction swing trading stock candidates."""

    def __init__(self):
        self.serenity_screener = SerenityBridge()

    def discover_stocks(self, max_candidates: int = 5) -> List[Dict[str, Any]]:
        """
        Runs Swing Trading stock discovery based on Supply Chain Monopolies & KOL Conviction.
        Promotes multi-day swing setups (5-20 days hold), not day trading.
        """
        candidates = []

        # Serenity Bottleneck Candidates
        bottlenecks = self.serenity_screener.get_supply_chain_candidates()
        for item in bottlenecks:
            candidates.append({
                "symbol": item["symbol"],
                "name": item["name"],
                "source": "Serenity Supply Chain Monopoly",
                "strategy": "Swing Trade (5-20 Days)",
                "pattern": item["bottleneck_type"],
                "target_price": 0.0,
                "score": item["conviction_score"],
                "notes": item["reason"]
            })

        # Sort by conviction score
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:max_candidates]
