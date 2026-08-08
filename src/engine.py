"""
Touchgrass Orchestrator Engine.
Coordinates daily market runs (Morning run at 2h post-open, Afternoon run at 2h pre-close),
watchlist analysis, auto stock discovery, and report generation.
"""

import sys
import os
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
PARENT_ROOT = TOUCHGRASS_ROOT.parent
for p in [str(PARENT_ROOT), str(TOUCHGRASS_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from touchgrass.src.portfolio import PortfolioManager
    from touchgrass.src.scanner import AutoStockScanner
    from touchgrass.src.analyzer import StockAnalyzer
    from touchgrass.src.notifier import Notifier
except ImportError:
    from src.portfolio import PortfolioManager
    from src.scanner import AutoStockScanner
    from src.analyzer import StockAnalyzer
    from src.notifier import Notifier


class TouchgrassEngine:
    """Core execution engine for Touchgrass Trader."""

    def __init__(self, portfolio_file: Optional[str] = None):
        self.portfolio_mgr = PortfolioManager(portfolio_file)
        self.scanner = AutoStockScanner()
        self.analyzer = StockAnalyzer()
        self.notifier = Notifier()

    def run_market_round(self, run_type: str = "scheduled", auto_add_scanned: bool = True) -> Dict[str, Any]:
        """
        Executes one full round of market analysis:
        1. Analyzes existing watchlist stocks
        2. Runs market-wide stock scanner (Breakout + Supply Chain)
        3. Auto-adds top discovered candidate to watchlist
        4. Generates decision report, dispatches notification, and saves report to reports/
        """
        print(f"🌿 Starting Touchgrass Market Round: {run_type.upper()}...")

        # 1. Analyze existing watchlist
        watchlist = self.portfolio_mgr.get_watchlist()
        watchlist_results = []
        for item in watchlist:
            symbol = item["symbol"]
            analysis = self.analyzer.analyze_stock(symbol)
            watchlist_results.append(analysis)

        # 2. Discover new candidates
        candidates = self.scanner.discover_stocks(max_candidates=3)

        # 3. Auto-add top candidate if enabled
        if auto_add_scanned and candidates:
            top_candidate = candidates[0]
            self.portfolio_mgr.add_to_watchlist(
                symbol=top_candidate["symbol"],
                name=top_candidate["name"],
                notes=f"Auto-discovered via {top_candidate['source']}"
            )

        # 4. Generate & dispatch report
        report = self.notifier.format_report_markdown(run_type, watchlist_results, candidates)
        self.notifier.dispatch(report)

        # 5. Save report to reports/ directory (daily_stock_analysis pattern)
        self._save_report(report, run_type=run_type)

        return {
            "run_type": run_type,
            "analyzed_count": len(watchlist_results),
            "discovered_candidates": candidates,
            "report_markdown": report
        }

    def _save_report(self, report_markdown: str, run_type: str = "scheduled"):
        """Saves report markdown to reports/latest.md, reports/report_YYYYMMDD.md, and timestamped reports."""
        try:
            reports_dir = TOUCHGRASS_ROOT / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)

            now = datetime.datetime.now()
            date_str = now.strftime("%Y%m%d")
            time_str = now.strftime("%H%M%S")

            latest_file = reports_dir / "latest.md"
            dated_file = reports_dir / f"report_{date_str}.md"
            timestamped_file = reports_dir / f"report_{date_str}_{time_str}_{run_type}.md"

            for filepath in [latest_file, dated_file, timestamped_file]:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(report_markdown)

            print(f"💾 Report saved to {latest_file}, {dated_file}, and {timestamped_file}")
        except Exception as e:
            print(f"[TouchgrassEngine] Error saving report files: {e}")
