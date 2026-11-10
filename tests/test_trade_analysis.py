import sys
import unittest
from datetime import date, timedelta
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from analyze_trades import entry_plan, path_risk, returns, summarize
from aggregate_event_results import aggregate_events


class TradeAnalysisTests(unittest.TestCase):
    def test_entry_waits_until_after_confirmation_and_deadline(self):
        start = date(2020, 1, 1)
        rsi = {(start + timedelta(days=i)).isoformat(): 29 for i in range(1, 31)}
        self.assertEqual(entry_plan(start.isoformat(), "A", rsi)["entry_date"], "2020-01-02")
        self.assertEqual(entry_plan(start.isoformat(), "B", rsi)["entry_date"], "2020-01-08")
        self.assertEqual(entry_plan(start.isoformat(), "C", rsi)["status"], "no_entry")
        rsi["2020-01-31"] = 30
        self.assertEqual(entry_plan(start.isoformat(), "C", rsi)["entry_date"], "2020-02-01")
        rsi["2020-01-03"] = 30
        self.assertEqual(entry_plan(start.isoformat(), "C", rsi)["entry_date"], "2020-01-04")

    def test_missing_rsi_is_not_no_entry(self):
        self.assertEqual(entry_plan("2020-01-01", "C", {})["status"], "missing_recovery_observation")

    def test_costs_match_known_cash_flow(self):
        costs = {"buy_fee_rate": D("0.01"), "sell_fee_rate": D("0.01"),
                 "adverse_buy_slippage": D(0), "adverse_sell_slippage": D(0)}
        gross, net = returns("100", "100", costs)
        self.assertEqual(gross, 0)
        self.assertAlmostEqual(net, -D(2) / D(101), places=35)

    def test_mae_and_drawdown_are_distinct(self):
        mae, mdd = path_risk("100", "120", [{"low": "100", "close": "150"}, {"low": "120", "close": "130"}])
        self.assertEqual(mae, 0)
        self.assertEqual(mdd, D("-0.2"))
        mae, mdd = path_risk("100", "70", [{"low": "80", "close": "110"}])
        self.assertEqual(mae, D("-0.3"))
        self.assertAlmostEqual(mdd, D(70) / D(110) - 1, places=35)

    def test_no_entry_is_excluded_from_return_denominator_but_counted(self):
        fields = ("alt_gross_return", "alt_net_return", "btc_gross_return", "btc_net_return", "advantage_net_pp",
                  "relative_net_return", "alt_mae", "btc_mae", "alt_mdd_close", "btc_mdd_close")
        complete = {"event_id": "one", "status": "completed", **{field: D("0.1") for field in fields},
                    "success_profit": True, "success_btc": False, "success_both": False}
        result = summarize([complete, {"event_id": "two", "status": "no_entry"}])
        self.assertEqual(result["candidate_rows"], 2)
        self.assertEqual(result["completed_trades"], 1)
        self.assertEqual(result["no_entry_rows"], 1)
        self.assertEqual(result["mean_alt_net_return"], D("0.1"))
        self.assertEqual(result["success_profit_pct"], 100)
        self.assertEqual(result["success_btc_pct"], 0)

    def test_event_average_uses_all_five_budgets_and_preserves_incomplete_basket(self):
        template = {"event_id": "one", "entry_rule": "A", "signal_date": "2020-01-01", "entry_date": "2020-01-02",
                    "exit_date": "2020-04-01", "holding_days": "90", "signal_period": "2020-2022",
                    "potential_overlap_group_90d": "one", "venue": "binance", "status": "completed",
                    "alt_gross_return": "0", "alt_net_return": "0", "btc_gross_return": "0.1", "btc_net_return": "0.1"}
        trades = [{**template, "asset_id": str(i), "symbol": str(i), "alt_net_return": str(value)}
                  for i, value in enumerate(("1", "-0.5", "0", "0", "0"))]
        result = aggregate_events(trades)[0]
        self.assertEqual(result["event_mean_alt_net_return"], D("0.1"))
        self.assertEqual(result["advantage_net_pp"], 0)
        self.assertFalse(result["success_btc"])
        trades[-1]["status"] = "incomplete_observation"
        result = aggregate_events(trades)[0]
        self.assertEqual(result["status"], "incomplete_basket")
        self.assertEqual(result["event_mean_alt_net_return"], "")


if __name__ == "__main__":
    unittest.main()
