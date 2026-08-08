"""
Portfolio and Watchlist Manager for Touchgrass Trader.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional


class PortfolioManager:
    """Manages user stock watchlist, current holdings, stop-loss, and target prices."""

    def __init__(self, filepath: Optional[str] = None):
        if not filepath:
            filepath = Path(__file__).resolve().parents[1] / "config" / "watchlist.json"
        self.filepath = Path(filepath)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.filepath.exists():
            # Check for example fallback template
            example_file = self.filepath.parent / "watchlist.example.json"
            if example_file.exists():
                try:
                    with open(example_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    # Initialize user watchlist.json from template
                    self.data = data
                    self.save()
                    return data
                except Exception as e:
                    print(f"[PortfolioManager] Error loading example fallback {example_file}: {e}")

            return {"watchlist": [], "portfolio": []}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[PortfolioManager] Error loading {self.filepath}: {e}")
            return {"watchlist": [], "portfolio": []}

    def save(self) -> bool:
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            print(f"[PortfolioManager] Error saving {self.filepath}: {e}")
            return False

    def get_watchlist(self) -> List[Dict[str, Any]]:
        return self.data.get("watchlist", [])

    def get_portfolio(self) -> List[Dict[str, Any]]:
        return self.data.get("portfolio", [])

    def add_to_watchlist(self, symbol: str, name: str = "", sector: str = "", notes: str = "", target_entry: float = 0.0) -> bool:
        symbol_upper = symbol.upper()
        for item in self.data["watchlist"]:
            if item["symbol"] == symbol_upper:
                item["notes"] = notes or item.get("notes", "")
                if target_entry > 0:
                    item["target_entry"] = target_entry
                return self.save()

        new_item = {
            "symbol": symbol_upper,
            "name": name or symbol_upper,
            "sector": sector or "General",
            "added_date": "2026-08-07",
            "target_entry": target_entry,
            "stop_loss": round(target_entry * 0.92, 2) if target_entry > 0 else 0.0,
            "take_profit": round(target_entry * 1.20, 2) if target_entry > 0 else 0.0,
            "notes": notes or "Auto-discovered candidate"
        }
        self.data["watchlist"].append(new_item)
        return self.save()

    def remove_from_watchlist(self, symbol: str) -> bool:
        symbol_upper = symbol.upper()
        initial_len = len(self.data["watchlist"])
        self.data["watchlist"] = [item for item in self.data["watchlist"] if item["symbol"] != symbol_upper]
        if len(self.data["watchlist"]) < initial_len:
            return self.save()
        return False

    def update_holding(self, symbol: str, shares: float, avg_price: float) -> bool:
        symbol_upper = symbol.upper()
        for item in self.data["portfolio"]:
            if item["symbol"] == symbol_upper:
                item["shares"] = shares
                item["avg_price"] = avg_price
                item["current_value"] = round(shares * avg_price, 2)
                return self.save()

        self.data["portfolio"].append({
            "symbol": symbol_upper,
            "shares": shares,
            "avg_price": avg_price,
            "current_value": round(shares * avg_price, 2),
            "entry_date": "2026-08-07"
        })
        return self.save()
