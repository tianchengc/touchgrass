"""
Touchgrass Trader Command Line Interface (CLI).
"""

import sys
import argparse
from pathlib import Path

TOUCHGRASS_ROOT = Path(__file__).resolve().parents[1]
PARENT_ROOT = TOUCHGRASS_ROOT.parent
for p in [str(PARENT_ROOT), str(TOUCHGRASS_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from touchgrass.src.engine import TouchgrassEngine
    from touchgrass.src.portfolio import PortfolioManager
    from touchgrass.src.scanner import AutoStockScanner
    from touchgrass.src.analyzer import StockAnalyzer
except ImportError:
    from src.engine import TouchgrassEngine
    from src.portfolio import PortfolioManager
    from src.scanner import AutoStockScanner
    from src.analyzer import StockAnalyzer


def main():
    parser = argparse.ArgumentParser(
        prog="touchgrass",
        description="🌿 Touchgrass Trader — Swing Trading decision engine for humans who'd rather touch grass than stare at candle charts all day."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available Touchgrass commands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run a full swing trading market evaluation round")
    run_parser.add_argument("--type", choices=["morning", "afternoon", "scheduled"], default="scheduled", help="Market run type")
    run_parser.add_argument("--no-auto-add", action="store_true", help="Disable auto-adding discovered stocks to watchlist")

    # Command: scan
    scan_parser = subparsers.add_parser("scan", help="Run swing trade stock discovery (Supply-chain monopolies & KOL conviction)")
    scan_parser.add_argument("--max", type=int, default=5, help="Max candidates to return")

    # Command: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Run 360-degree swing trade evaluation on a stock symbol")
    analyze_parser.add_argument("symbol", type=str, help="Stock symbol (e.g. NVDA, AAPL, PLTR)")

    # Command: watchlist
    wl_parser = subparsers.add_parser("watchlist", help="View current swing watchlist and portfolio holdings")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a stock symbol to swing watchlist")
    add_parser.add_argument("symbol", type=str, help="Stock symbol")
    add_parser.add_argument("--target", type=float, default=0.0, help="Target entry price")
    add_parser.add_argument("--notes", type=str, default="", help="Notes")

    # Command: remove
    rm_parser = subparsers.add_parser("remove", help="Remove a stock symbol from watchlist")
    rm_parser.add_argument("symbol", type=str, help="Stock symbol")

    # Command: hold
    hold_parser = subparsers.add_parser("hold", help="Add or update an active portfolio holding")
    hold_parser.add_argument("symbol", type=str, help="Stock symbol")
    hold_parser.add_argument("--shares", type=float, required=True, help="Number of shares owned")
    hold_parser.add_argument("--price", type=float, required=True, help="Average purchase price")

    args = parser.parse_args()

    if not args.command or args.command == "run":
        engine = TouchgrassEngine()
        run_type = getattr(args, "type", "scheduled")
        auto_add = not getattr(args, "no_auto_add", False)
        engine.run_market_round(run_type=run_type, auto_add_scanned=auto_add)

    elif args.command == "scan":
        scanner = AutoStockScanner()
        results = scanner.discover_stocks(max_candidates=args.max)
        print(f"\n🔍 Discovered Top {len(results)} Swing Trading Candidates:")
        for idx, item in enumerate(results, 1):
            print(f"{idx}. [{item['symbol']}] {item['name']} - Score: {item['score']} | Strategy: {item['strategy']} | Monopoly: {item['pattern']}")

    elif args.command == "analyze":
        analyzer = StockAnalyzer()
        res = analyzer.analyze_stock(args.symbol)
        print(f"\n📊 Swing Trade Analysis for {res['symbol']} ({res['name']}):")
        print(f"Current Price: ${res['current_price']} ({res['change_pct']:+}%)")
        print(f"Touchgrass Score: {res['touchgrass_score']}/100")
        print(f"Recommended Swing Action: {res['recommended_action']}")
        print(f"Kronos 5-Day Trend Prediction: {res['kronos_prediction']['direction']} (Conf: {res['kronos_prediction']['confidence']*100:.0f}%)")
        print(f"65 Investor Panel Verdict: {res['investor_panel']['verdict']}")
        print(f"Trap Security Status: {res['trap_security']['risk_level']}")

    elif args.command == "watchlist":
        pm = PortfolioManager()
        wl = pm.get_watchlist()
        pf = pm.get_portfolio()
        print("\n📋 Current Swing Watchlist:")
        for item in wl:
            print(f"• {item['symbol']} - {item['name']} (Sector: {item.get('sector')}) | Target Entry: ${item.get('target_entry')} | Notes: {item.get('notes')}")
        print("\n💼 Current Portfolio Holdings:")
        for item in pf:
            print(f"• {item['symbol']}: {item['shares']} shares @ ${item['avg_price']} (Total: ${item['current_value']})")

    elif args.command == "add":
        pm = PortfolioManager()
        success = pm.add_to_watchlist(args.symbol, notes=args.notes, target_entry=args.target)
        if success:
            print(f"✅ Added {args.symbol.upper()} to swing watchlist.")

    elif args.command == "remove":
        pm = PortfolioManager()
        success = pm.remove_from_watchlist(args.symbol)
        if success:
            print(f"✅ Removed {args.symbol.upper()} from swing watchlist.")
        else:
            print(f"⚠️ Symbol {args.symbol.upper()} not found in watchlist.")

    elif args.command == "hold":
        pm = PortfolioManager()
        success = pm.update_holding(args.symbol, shares=args.shares, avg_price=args.price)
        if success:
            print(f"✅ Updated portfolio holding: {args.symbol.upper()} ({args.shares} shares @ ${args.price}).")


if __name__ == "__main__":
    main()
