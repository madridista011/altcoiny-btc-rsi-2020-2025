"""Kontrola końcowej tabeli inną ścieżką: przepływy budżetu i grupowanie pandas."""

import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    trades = pd.read_csv(ROOT / "data/analysis/trades_90d.csv")
    prices = pd.read_csv(ROOT / "data/processed/market_prices_daily.csv")
    rsi = pd.read_csv(ROOT / "data/processed/btc_rsi_daily.csv").set_index("date_utc")["rsi_14_wilder"]
    protocol = json.loads((ROOT / "config/trade_protocol_v1.json").read_text(encoding="utf-8"))
    assert not trades.duplicated(["event_id", "asset_id", "entry_rule"]).any()
    assert trades.groupby(["event_id", "entry_rule"]).size().eq(5).all()
    assert trades["status"].eq("completed").all(), "Current-data audit expects 300 completed rows; review if data change."
    dates = {key: pd.to_datetime(trades[key]) for key in ("signal_date", "entry_date", "exit_date")}
    assert (dates["exit_date"] - dates["entry_date"]).dt.days.eq(90).all()
    shifts = (dates["entry_date"] - dates["signal_date"]).dt.days
    assert shifts[trades.entry_rule.eq("A")].eq(1).all()
    assert shifts[trades.entry_rule.eq("B")].eq(7).all()
    plans = trades.drop_duplicates(["event_id", "entry_rule"])
    for row in plans[plans.entry_rule.eq("C")].itertuples():
        recovery = pd.Timestamp(row.recovery_date)
        signal = pd.Timestamp(row.signal_date)
        assert 1 <= (recovery - signal).days <= 30
        assert pd.Timestamp(row.entry_date) == recovery + pd.Timedelta(days=1)
        assert rsi.loc[recovery.strftime("%Y-%m-%d")] >= 30
        earlier = pd.date_range(signal + pd.Timedelta(days=1), recovery - pd.Timedelta(days=1))
        assert all(rsi.loc[day.strftime("%Y-%m-%d")] < 30 for day in earlier)
    costs = protocol["base_costs"]
    cashflow_errors = []
    risk_errors = []
    for prefix in ("alt", "btc"):
        quantity = 1000 / (trades[prefix + "_entry_open"] * (1 + costs["adverse_buy_slippage"]) * (1 + costs["buy_fee_rate"]))
        proceeds = quantity * trades[prefix + "_exit_open"] * (1 - costs["adverse_sell_slippage"]) * (1 - costs["sell_fee_rate"])
        cashflow_errors.append(float(((proceeds - 1000) / 1000 - trades[prefix + "_net_return"]).abs().max()))
    price_groups = {(asset, venue): group.set_index("date_utc").sort_index()
                    for (asset, venue), group in prices.groupby(["asset_id", "venue"])}
    for row in trades.to_dict("records"):
        for prefix, asset in (("alt", row["asset_id"]), ("btc", "bitcoin")):
            series = price_groups[(asset, row["venue"])]
            assert series.loc[row["entry_date"], "open"] == row[prefix + "_entry_open"]
            assert series.loc[row["exit_date"], "open"] == row[prefix + "_exit_open"]
            last_held = (pd.Timestamp(row["exit_date"]) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            held = series.loc[row["entry_date"]:last_held]
            assert len(held) == 90
            start, end = row[prefix + "_entry_open"], row[prefix + "_exit_open"]
            mae = min(start, end, held.low.min()) / start - 1
            path = pd.Series([start, *held.close.tolist(), end])
            mdd = (path / path.cummax() - 1).min()
            risk_errors.extend([abs(mae - row[prefix + "_mae"]), abs(mdd - row[prefix + "_mdd_close"])])
    advantage_error = float(((trades.alt_net_return - trades.btc_net_return) * 100 - trades.advantage_net_pp).abs().max())
    assert max(cashflow_errors + risk_errors + [advantage_error]) < 1e-10
    summaries = pd.read_csv(ROOT / "data/analysis/summary_by_rule_90d.csv").set_index("entry_rule")
    for rule, group in trades.groupby("entry_rule"):
        stored = summaries.loc[rule]
        assert stored.completed_trades == len(group)
        assert stored.success_profit_count == (group.alt_net_return > 0).sum()
        assert stored.success_btc_count == (group.alt_net_return > group.btc_net_return).sum()
        assert abs(stored.median_alt_net_return - group.alt_net_return.median()) < 1e-12
    event_means = pd.read_csv(ROOT / "data/analysis/event_mean_returns_90d.csv").set_index(["event_id", "entry_rule"])
    actual = trades.groupby(["event_id", "entry_rule"])[["alt_net_return", "btc_net_return"]].mean()
    assert ((actual.alt_net_return - event_means.event_mean_alt_net_return).abs() < 1e-12).all()
    assert ((actual.btc_net_return - event_means.event_mean_btc_net_return).abs() < 1e-12).all()
    assert ((trades.venue.eq("kucoin") & trades.symbol.isin(["BSV", "TON"])) | trades.venue.eq("binance")).all()
    files = sorted((ROOT / "data/analysis").glob("*.csv"))
    result = {"status": "passed", "trade_rows_checked": len(trades), "event_rule_rows_checked": len(event_means),
              "entry_plans_checked": len(plans), "independent_cashflow_budget_usdt": 1000,
              "max_cashflow_return_error": max(cashflow_errors), "max_risk_error": max(risk_errors),
              "max_advantage_pp_error": advantage_error,
              "checks": ["Unique event-asset-rule keys and five assets per event-rule", "Calendar dates A/B/C including earliest RSI recovery and 90-day exits",
                         "Independent 1000-USDT cash flow versus stored net returns", "Entry and exit prices versus processed price candles",
                         "Pandas low minima and cumulative-maximum drawdowns versus Decimal results", "Success denominators and medians",
                         "Event means preserve all five weights; paired BTC uses those same weights"],
              "analysis_csv_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}}
    (ROOT / "reports/trade_output_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "analysis_csv_sha256"}, indent=2))


if __name__ == "__main__":
    main()
