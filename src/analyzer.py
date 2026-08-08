"""
Multi-stage Stock Analysis Engine for Touchgrass Trader.
Combines:
1. Real-time Market Data (DailyStockAnalysis Bridge)
2. Time-Series Predictions (Kronos Bridge)
3. 65 Investor Panel Scoring (Uzi Bridge)
4. Pig-butchering & Pump-and-dump Trap Detection (Uzi Bridge)
5. Serenity KOL Scorecard
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
    from touchgrass.subprojects.daily_stock_analysis.bridge import DailyStockAnalysisBridge
    from touchgrass.subprojects.kronos.bridge import KronosBridge
    from touchgrass.subprojects.uzi.bridge import UziBridge
    from touchgrass.subprojects.serenity.bridge import SerenityBridge
except ImportError:
    from subprojects.daily_stock_analysis.bridge import DailyStockAnalysisBridge
    from subprojects.kronos.bridge import KronosBridge
    from subprojects.uzi.bridge import UziBridge
    from subprojects.serenity.bridge import SerenityBridge


class StockAnalyzer:
    """Evaluates individual stocks or watchlist portfolios."""

    def __init__(self):
        self.dsa_bridge = DailyStockAnalysisBridge()
        self.kronos_bridge = KronosBridge()
        self.uzi_bridge = UziBridge()
        self.serenity_bridge = SerenityBridge()

    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """
        Runs comprehensive 360-degree evaluation on a stock symbol.
        """
        # 1. Fetch data
        market_data = self.dsa_bridge.fetch_market_data(symbol)

        # 2. Kronos prediction
        kronos_pred = self.kronos_bridge.predict_trend(
            symbol,
            market_data.get("historical_prices", [])
        )

        # 3. Uzi 65-Investor Panel
        investor_panel = self.uzi_bridge.run_investor_panel(symbol, market_data)

        # 4. Trap Detector
        trap_check = self.uzi_bridge.detect_traps(symbol, market_data=market_data)

        # 5. Serenity KOL Scorecard
        kol_scorecard = self.serenity_bridge.evaluate_kol_sentiment(symbol)

        # Calculate final Touchgrass Action & Score
        composite_score = round(
            investor_panel["overall_consensus_score"] * 0.40 +
            (85 if kronos_pred["direction"] == "BULLISH" else 55) * 0.30 +
            kol_scorecard["kol_sentiment_score"] * 0.30,
            1
        )

        action = "HOLD"
        if composite_score >= 80 and "SAFE" in trap_check["risk_level"]:
            action = "BUY"
        elif composite_score <= 50 or "HIGH RISK" in trap_check["risk_level"]:
            action = "SELL / AVOID"

        return {
            "symbol": symbol,
            "name": market_data.get("shortName", symbol),
            "current_price": market_data["current_price"],
            "change_pct": market_data["change_pct"],
            "touchgrass_score": composite_score,
            "recommended_action": action,
            "kronos_prediction": kronos_pred,
            "investor_panel": investor_panel,
            "trap_security": trap_check,
            "kol_sentiment": kol_scorecard
        }
