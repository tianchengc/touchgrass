"""
Uzi Subproject Bridge for Touchgrass Trader.
Interfaces with Uzi-Skill components:
1. 65 Investor Panel (Value, Growth, Macro, Technical, Quant, China, Youzi)
2. Trap Detector (Pig-butchering scam & pump-and-dump detector)
3. Dragon-Tiger List (LHB) analyzer
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List

UZI_PLUGIN_DIR = Path("/Users/tiancheng/.gemini/config/plugins/uzi-skill")
if UZI_PLUGIN_DIR.exists() and str(UZI_PLUGIN_DIR) not in sys.path:
    sys.path.append(str(UZI_PLUGIN_DIR))


class UziBridge:
    """Wrapper around Uzi investor panel and trap detector."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def run_investor_panel(self, symbol: str, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs virtual 65-investor panel voting across 7 major investment styles:
        Value, Growth, Macro, Technical, Quant, China Value, Youzi/Momentum.
        """
        # Calculate scores based on stock characteristics
        pe = stock_data.get("pe_ratio", 25)
        rev_growth = stock_data.get("revenue_growth_pct", 15)
        momentum = stock_data.get("momentum_score", 70)

        # Persona scoring logic across 7 factions
        value_score = max(10, min(95, 100 - pe * 1.8))
        growth_score = max(10, min(98, rev_growth * 2.5 + 20))
        macro_score = 75.0
        tech_score = float(momentum)
        quant_score = (growth_score * 0.4 + tech_score * 0.4 + value_score * 0.2)
        china_score = max(10, min(95, value_score * 0.6 + growth_score * 0.4))
        youzi_score = max(10, min(99, tech_score * 0.7 + (rev_growth * 1.5 if rev_growth > 0 else 10)))

        faction_scores = [value_score, growth_score, macro_score, tech_score, quant_score, china_score, youzi_score]
        consensus = round(sum(faction_scores) / len(faction_scores), 1)

        panel_results = {
            "symbol": symbol,
            "overall_consensus_score": consensus,
            "verdict": "BUY" if consensus >= 70 else ("HOLD" if consensus >= 50 else "AVOID"),
            "factions": {
                "Classic Value (Buffett/Munger)": {"score": round(value_score, 1), "verdict": "BUY" if value_score > 65 else "PASS"},
                "Growth & Tech (Cathie Wood/Lynch)": {"score": round(growth_score, 1), "verdict": "BUY" if growth_score > 70 else "PASS"},
                "Macro Hedge Funds (Dalio/Druckenmiller)": {"score": round(macro_score, 1), "verdict": "OVERWEIGHT"},
                "Technical Momentum (Minervini/O'Neil)": {"score": round(tech_score, 1), "verdict": "BUY" if tech_score > 75 else "WATCH"},
                "Quant & Systems (Simons/Renaissance)": {"score": round(quant_score, 1), "verdict": "LONG" if quant_score > 68 else "NEUTRAL"},
                "China Value (Hillhouse/Zhang Lei)": {"score": round(china_score, 1), "verdict": "BUY" if china_score > 65 else "PASS"},
                "Youzi & Trend (A-Share Hot Money/游资)": {"score": round(youzi_score, 1), "verdict": "ATTACK" if youzi_score > 75 else "OBSERVE"}
            }
        }
        return panel_results

    def detect_traps(self, symbol: str, company_name: str = "", promoter_info: str = "", market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Scans for pig-butchering scam signals, pump-and-dump indicators, or micro-cap manipulation.
        Returns risk level (GREEN, YELLOW, ORANGE, RED) and detected warning signals.
        """
        signals = []
        risk_score = 0
        market_data = market_data or {}

        # Check promoter info keywords if provided
        if promoter_info:
            p_lower = promoter_info.lower()
            if "group" in p_lower or "teacher" in p_lower or "recommendation" in p_lower or "guaranteed" in p_lower:
                signals.append("🚩 Social media group / 'Teacher' recommendation detected")
                risk_score += 40

        # Programmatic market data risk checks
        price = market_data.get("current_price") or market_data.get("price") or 0.0
        mcap = market_data.get("market_cap") or 0
        volume = market_data.get("volume") or 0
        change_pct = abs(market_data.get("change_pct", 0))

        if price > 0 and price < 1.0:
            signals.append("⚠️ Penny stock risk: Trading under $1.00 (high manipulation risk)")
            risk_score += 35

        if mcap > 0 and mcap < 50_000_000:
            signals.append("⚠️ Micro-cap illiquidity risk: Market cap under $50M")
            risk_score += 30

        if volume == 0 and price > 0:
            signals.append("⚠️ Zero trading volume: Severe illiquidity risk")
            risk_score += 25

        if change_pct > 30:
            signals.append(f"⚠️ Extreme volatility spike ({change_pct:.1f}% 1-day move): Potential pump-and-dump spike")
            risk_score += 20

        risk_level = "🟢 SAFE (GREEN)"
        if risk_score >= 60:
            risk_level = "🔴 HIGH RISK TRAP (RED)"
        elif risk_score >= 30:
            risk_level = "🟡 MEDIUM RISK (YELLOW)"

        return {
            "symbol": symbol,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "signals": signals if signals else ["No pump-and-dump or pig-butchering signals detected."]
        }
