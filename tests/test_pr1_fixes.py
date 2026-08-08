import unittest
import sys
from pathlib import Path

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
if str(TOUCHGRASS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOUCHGRASS_ROOT))

try:
    from touchgrass.subprojects.uzi.bridge import UziBridge
    from touchgrass.src.analyzer import StockAnalyzer
except ImportError:
    from subprojects.uzi.bridge import UziBridge
    from src.analyzer import StockAnalyzer


class TestPR1Fixes(unittest.TestCase):

    def test_uzi_bridge_7_factions(self):
        bridge = UziBridge()
        res = bridge.run_investor_panel("NVDA", {"pe_ratio": 30, "revenue_growth_pct": 25, "momentum_score": 80})
        self.assertIn("factions", res)
        factions = res["factions"]
        self.assertEqual(len(factions), 7)
        self.assertIn("Classic Value (Buffett/Munger)", factions)
        self.assertIn("Growth & Tech (Cathie Wood/Lynch)", factions)
        self.assertIn("Macro Hedge Funds (Dalio/Druckenmiller)", factions)
        self.assertIn("Technical Momentum (Minervini/O'Neil)", factions)
        self.assertIn("Quant & Systems (Simons/Renaissance)", factions)
        self.assertIn("China Value (Hillhouse/Zhang Lei)", factions)
        self.assertIn("Youzi & Trend (A-Share Hot Money/游资)", factions)

    def test_uzi_bridge_detect_traps_market_data(self):
        bridge = UziBridge()
        # Test penny stock + micro-cap risk
        res = bridge.detect_traps("PENNY", market_data={"price": 0.50, "market_cap": 10_000_000, "volume": 0})
        self.assertGreater(res["risk_score"], 50)
        self.assertIn("HIGH RISK", res["risk_level"])
        self.assertTrue(any("Penny stock" in s for s in res["signals"]))
        self.assertTrue(any("Micro-cap" in s for s in res["signals"]))
        self.assertTrue(any("Zero trading volume" in s for s in res["signals"]))

    def test_analyzer_integration(self):
        analyzer = StockAnalyzer()
        res = analyzer.analyze_stock("NVDA")
        self.assertIn("investor_panel", res)
        self.assertEqual(len(res["investor_panel"]["factions"]), 7)
        self.assertIn("trap_security", res)


if __name__ == "__main__":
    unittest.main()
