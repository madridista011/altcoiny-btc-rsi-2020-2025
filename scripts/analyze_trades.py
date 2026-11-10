"""Odtwarzalna analiza 90-dniowych transakcji A/B/C z zachowaniem braków wejścia."""

import csv
import hashlib
import itertools
import json
import statistics
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, getcontext
from pathlib import Path

from build_signal_events import rsi_wilder

ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 40
D = Decimal
RULES = ("A", "B", "C")


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(relative, rows):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_json(relative, value):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def entry_plan(signal_day, rule, rsi_by_day):
    signal = date.fromisoformat(signal_day)
    if rule == "A":
        return {"status": "planned", "entry_date": (signal + timedelta(days=1)).isoformat(), "recovery_date": ""}
    if rule == "B":
        return {"status": "planned", "entry_date": (signal + timedelta(days=7)).isoformat(), "recovery_date": ""}
    if rule != "C":
        raise ValueError("Unknown entry rule")
    for offset in range(1, 31):
        day = (signal + timedelta(days=offset)).isoformat()
        if day not in rsi_by_day or rsi_by_day[day] is None:
            return {"status": "missing_recovery_observation", "entry_date": "", "recovery_date": ""}
        if rsi_by_day[day] >= 30:
            return {"status": "planned", "entry_date": (signal + timedelta(days=offset + 1)).isoformat(), "recovery_date": day}
    return {"status": "no_entry", "entry_date": "", "recovery_date": ""}


def cost_factor(costs):
    return ((1 - costs["adverse_sell_slippage"]) * (1 - costs["sell_fee_rate"]) /
            ((1 + costs["adverse_buy_slippage"]) * (1 + costs["buy_fee_rate"])))


def returns(p_in, p_out, costs):
    p_in, p_out = D(p_in), D(p_out)
    assert p_in > 0 and p_out > 0
    gross = p_out / p_in - 1
    net = (p_out / p_in) * cost_factor(costs) - 1
    return gross, net


def path_risk(p_in, p_out, holding_rows):
    p_in, p_out = D(p_in), D(p_out)
    minimum = min([p_in, p_out] + [D(row["low"]) for row in holding_rows])
    mae = minimum / p_in - 1
    path = [p_in] + [D(row["close"]) for row in holding_rows] + [p_out]
    peak, drawdown = path[0], D(0)
    for value in path:
        peak = max(peak, value)
        drawdown = min(drawdown, value / peak - 1)
    return mae, drawdown


def summarize(rows, keys=()):
    complete = [row for row in rows if row["status"] == "completed"]
    result = {**dict(zip(keys, (rows[0][key] for key in keys))),
              "candidate_rows": len(rows), "qualified_events": len({row["event_id"] for row in rows}),
              "completed_trades": len(complete), "completed_events": len({row["event_id"] for row in complete}),
              "no_entry_rows": sum(row["status"] == "no_entry" for row in rows),
              "other_incomplete_rows": sum(row["status"] not in ("completed", "no_entry") for row in rows)}
    for field in ("alt_gross_return", "alt_net_return", "btc_gross_return", "btc_net_return", "advantage_net_pp",
                  "relative_net_return", "alt_mae", "btc_mae", "alt_mdd_close", "btc_mdd_close"):
        values = [row[field] for row in complete]
        result["mean_" + field] = statistics.mean(values) if values else ""
        result["median_" + field] = statistics.median(values) if values else ""
    for field in ("success_profit", "success_btc", "success_both"):
        count = sum(row[field] for row in complete)
        result[field + "_count"] = count
        result[field + "_pct"] = D(100) * count / len(complete) if complete else ""
    return result


def grouped_summary(rows, keys):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in keys)].append(row)
    return [summarize(values, keys) for _, values in sorted(groups.items())]


def verify_price_sources(prices, config):
    hashes = json.loads((ROOT / "data/metadata/event_prices_raw_sha256.json").read_text(encoding="utf-8"))
    hashes.update(json.loads((ROOT / "data/metadata/kucoin_event_sources_sha256.json").read_text(encoding="utf-8")))
    binance_ids = {seg["symbol"]: asset["asset_id"] for asset in config["assets"] for seg in asset["segments"]}
    kucoin_meta = {row["path"]: row for row in json.loads((ROOT / "data/metadata/kucoin_manifest.json").read_text(encoding="utf-8"))}
    raw_sources = {}
    for source in sorted({row["source_file"] for row in prices}):
        raw = (ROOT / source).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == hashes[source], source
        payload = json.loads(raw)
        raw_sources[source] = payload.get("result", payload.get("data")) if isinstance(payload, dict) else payload
    for row in prices:
        original = raw_sources[row["source_file"]][int(row["source_row"]) - 1]
        assert row["quote_currency"] == "USDT"
        if row["venue"] == "binance":
            indexes, divisor = {"open": 1, "high": 2, "low": 3, "close": 4}, 1000
            assert binance_ids[row["source_symbol"]] == row["asset_id"]
        else:
            indexes, divisor = {"open": 1, "high": 3, "low": 4, "close": 2}, 1
            metadata = kucoin_meta[row["source_file"]]
            assert row["venue"] == "kucoin" and metadata["asset_id"] == row["asset_id"]
            assert metadata["symbol"] == row["source_symbol"]
        assert datetime.fromtimestamp(int(original[0]) / divisor, timezone.utc).date().isoformat() == row["date_utc"]
        for field, index in indexes.items():
            assert D(row[field]) == D(str(original[index])), (row["source_file"], row["source_row"], field)
    return {source: hashes[source] for source in raw_sources}


def build_trades():
    config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
    protocol_bytes = (ROOT / "config/trade_protocol_v1.json").read_bytes()
    protocol = json.loads(protocol_bytes)
    control_metadata = json.loads((ROOT / "reports/control_trade.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(protocol_bytes).hexdigest() == control_metadata["protocol_sha256"], "Protocol changed after the control calculation"
    costs = {key: D(str(value)) for key, value in protocol["base_costs"].items()}
    holding_days = protocol["primary_holding_days"]
    events = read_csv("data/processed/signal_events.csv")
    universe = read_csv("data/processed/event_universe.csv")
    coverage = {(row["event_id"], row["asset_id"]): row for row in read_csv("data/processed/price_coverage.csv")}
    prices = read_csv("data/processed/market_prices_daily.csv")
    source_hashes = verify_price_sources(prices, config)
    lookup = {(row["asset_id"], row["venue"], row["date_utc"]): row for row in prices}
    assert len(lookup) == len(prices)
    bitcoin = sorted([row for row in prices if row["asset_id"] == "bitcoin" and row["venue"] == "binance"], key=lambda row: row["date_utc"])
    rsi = rsi_wilder([float(row["close"]) for row in bitcoin])
    rsi_by_day = {row["date_utc"]: value for row, value in zip(bitcoin, rsi)}
    computed_signals = {bitcoin[i]["date_utc"] for i in range(1, len(bitcoin))
                        if rsi[i - 1] is not None and rsi[i] < 30 <= rsi[i - 1]
                        and config["study_start"] <= bitcoin[i]["date_utc"] <= config["study_end"]}
    assert computed_signals == {event["signal_date_utc"] for event in events}
    event_map = {event["event_id"]: event for event in events}
    plans = []
    plan_map = {}
    for event in events:
        for rule in RULES:
            plan = {"event_id": event["event_id"], "signal_date": event["signal_date_utc"], "entry_rule": rule,
                    **entry_plan(event["signal_date_utc"], rule, rsi_by_day)}
            plan["exit_date"] = (date.fromisoformat(plan["entry_date"]) + timedelta(days=holding_days)).isoformat() if plan["entry_date"] else ""
            plan_map[(event["event_id"], rule)] = plan
            plans.append(plan)
    rows = []
    for selected in universe:
        event = event_map[selected["event_id"]]
        paired = coverage[(selected["event_id"], selected["asset_id"])]
        venue = paired["price_venue"]
        assert paired["benchmark_venue"] == venue
        assert selected["ranking_snapshot_date"] < selected["signal_date_utc"]
        for rule in RULES:
            plan = plan_map[(selected["event_id"], rule)]
            row = {"event_id": selected["event_id"], "signal_date": selected["signal_date_utc"],
                   "ranking_date": selected["ranking_snapshot_date"], "ranking_age_days": selected["ranking_age_days"],
                   "ranking_availability_status": selected["ranking_availability_status"],
                   "asset_id": selected["asset_id"], "symbol": selected["symbol_at_event"], "venue": venue,
                   "entry_rule": rule, "holding_days": holding_days, "recovery_date": plan["recovery_date"],
                   "entry_date": plan["entry_date"], "exit_date": plan["exit_date"],
                   "waiting_days_after_signal_confirmation": (date.fromisoformat(plan["entry_date"]) - date.fromisoformat(selected["signal_date_utc"])).days - 1 if plan["entry_date"] else "",
                   "potential_overlap_group_90d": event["potential_overlap_group_90d"],
                   "signal_period": "2020-2022" if selected["signal_date_utc"] < "2023-01-01" else "2023-2025",
                   "outcome_known_before_2023": bool(plan["exit_date"] and plan["exit_date"] < "2023-01-01"),
                   "status": plan["status"], "status_detail": "",
                   **{field: "" for field in ("alt_entry_open", "alt_exit_open", "btc_entry_open", "btc_exit_open",
                                               "alt_gross_return", "alt_net_return", "btc_gross_return", "btc_net_return",
                                               "advantage_net_pp", "relative_net_return", "alt_mae", "btc_mae", "alt_mdd_close", "btc_mdd_close",
                                               "success_profit", "success_btc", "success_both",
                                               "alt_entry_source", "alt_entry_source_row", "alt_exit_source", "alt_exit_source_row",
                                               "btc_entry_source", "btc_entry_source_row", "btc_exit_source", "btc_exit_source_row")}}
            if plan["status"] != "planned":
                rows.append(row)
                continue
            entry, exit_day = date.fromisoformat(plan["entry_date"]), date.fromisoformat(plan["exit_date"])
            assert entry > date.fromisoformat(row["signal_date"])
            assert (exit_day - entry).days == holding_days
            series = {}
            for prefix, asset in (("alt", row["asset_id"]), ("btc", "bitcoin")):
                first = lookup.get((asset, venue, entry.isoformat()))
                last = lookup.get((asset, venue, exit_day.isoformat()))
                held = [lookup.get((asset, venue, (entry + timedelta(days=offset)).isoformat())) for offset in range(holding_days)]
                if first is None or last is None or any(value is None for value in held):
                    row["status"] = "incomplete_observation"
                    row["status_detail"] = prefix + ": missing required candle"
                    break
                if first["known_non_midnight_open"] == "True" or last["known_non_midnight_open"] == "True":
                    row["status"] = "unavailable_midnight_execution"
                    row["status_detail"] = prefix + ": documented non-midnight open"
                    break
                if any(value["known_partial_day"] == "True" for value in held):
                    row["status"] = "partial_session_requires_review"
                    row["status_detail"] = prefix + ": documented partial session during holding"
                    break
                series[prefix] = (first, last, held)
            if row["status"] != "planned":
                rows.append(row)
                continue
            for prefix, (first, last, held) in series.items():
                row[prefix + "_entry_open"], row[prefix + "_exit_open"] = D(first["open"]), D(last["open"])
                row[prefix + "_gross_return"], row[prefix + "_net_return"] = returns(first["open"], last["open"], costs)
                row[prefix + "_mae"], row[prefix + "_mdd_close"] = path_risk(first["open"], last["open"], held)
                for side, source in (("entry", first), ("exit", last)):
                    row[prefix + "_" + side + "_source"] = source["source_file"]
                    row[prefix + "_" + side + "_source_row"] = source["source_row"]
                assert row[prefix + "_net_return"] <= row[prefix + "_gross_return"]
                assert -1 < row[prefix + "_mae"] <= 0 and -1 < row[prefix + "_mdd_close"] <= 0
            alt, btc = row["alt_net_return"], row["btc_net_return"]
            row["advantage_net_pp"] = (alt - btc) * 100
            row["relative_net_return"] = (1 + alt) / (1 + btc) - 1
            row["success_profit"], row["success_btc"] = alt > 0, alt > btc
            row["success_both"] = row["success_profit"] and row["success_btc"]
            row["status"] = "completed"
            rows.append(row)
    assert len(rows) == len(universe) * 3
    assert len({(row["event_id"], row["asset_id"], row["entry_rule"]) for row in rows}) == len(rows)
    completeness = defaultdict(set)
    for row in rows:
        if row["status"] == "completed":
            completeness[(row["event_id"], row["asset_id"])].add(row["entry_rule"])
    for row in rows:
        row["common_sample_three_rules"] = completeness[(row["event_id"], row["asset_id"])] == set(RULES)
    control = read_csv("data/processed/control_trade.csv")
    for reference in control:
        match = next(row for row in rows if row["event_id"] == reference["event_id"] and row["asset_id"] == "ethereum" and row["entry_rule"] == "A")
        prefix = "alt" if reference["symbol"] == "ETH" else "btc"
        assert abs(match[prefix + "_net_return"] - D(reference["net_return"])) < D("1e-30")
    return rows, plans, protocol, protocol_bytes, source_hashes


def main():
    rows, plans, protocol, protocol_bytes, source_hashes = build_trades()
    common = [row for row in rows if row["common_sample_three_rules"]]
    summaries = grouped_summary(rows, ("entry_rule",))
    common_summaries = grouped_summary(common, ("entry_rule",)) if common else []
    by_coin = grouped_summary(rows, ("symbol", "entry_rule"))
    by_period = grouped_summary(rows, ("signal_period", "entry_rule"))
    event_summaries = grouped_summary(rows, ("event_id", "signal_date", "entry_rule", "potential_overlap_group_90d"))
    rule_pairs = []
    paired = {(row["event_id"], row["asset_id"], row["entry_rule"]): row for row in rows}
    for event_id, asset_id in sorted({(row["event_id"], row["asset_id"]) for row in common}):
        for left, right in itertools.combinations(RULES, 2):
            before, after = paired[(event_id, asset_id, left)], paired[(event_id, asset_id, right)]
            rule_pairs.append({"event_id": event_id, "symbol": before["symbol"], "comparison": right + "_minus_" + left,
                               "left_entry": before["entry_date"], "right_entry": after["entry_date"],
                               "left_exit": before["exit_date"], "right_exit": after["exit_date"],
                               "entry_shift_days": (date.fromisoformat(after["entry_date"]) - date.fromisoformat(before["entry_date"])).days,
                               "net_return_delta_pp": (after["alt_net_return"] - before["alt_net_return"]) * 100,
                               "mae_delta_pp": (after["alt_mae"] - before["alt_mae"]) * 100})
    pair_summary = []
    for comparison in sorted({row["comparison"] for row in rule_pairs}):
        subset = [row for row in rule_pairs if row["comparison"] == comparison]
        pair_summary.append({"comparison": comparison, "paired_rows": len(subset), "events": len({row["event_id"] for row in subset}),
                             "mean_net_delta_pp": statistics.mean(row["net_return_delta_pp"] for row in subset),
                             "median_net_delta_pp": statistics.median(row["net_return_delta_pp"] for row in subset),
                             "positive_delta_pct": D(100) * sum(row["net_return_delta_pp"] > 0 for row in subset) / len(subset),
                             "median_entry_shift_days": statistics.median(row["entry_shift_days"] for row in subset)})
    sensitivity = []
    scenarios = [("base", {key: D(str(value)) for key, value in protocol["base_costs"].items()})]
    for scenario in protocol["cost_sensitivity_before_results"]:
        scenarios.append((scenario["name"], {"buy_fee_rate": D(str(scenario["fee_each_side"])),
                                            "sell_fee_rate": D(str(scenario["fee_each_side"])),
                                            "adverse_buy_slippage": D(str(scenario["slippage_each_side"])),
                                            "adverse_sell_slippage": D(str(scenario["slippage_each_side"]))}))
    for name, costs in scenarios:
        for original in rows:
            row = dict(original)
            row["scenario"] = name
            if row["status"] == "completed":
                factor = cost_factor(costs)
                row["alt_net_return"] = (1 + row["alt_gross_return"]) * factor - 1
                row["btc_net_return"] = (1 + row["btc_gross_return"]) * factor - 1
                row["advantage_net_pp"] = (row["alt_net_return"] - row["btc_net_return"]) * 100
                row["relative_net_return"] = (1 + row["alt_net_return"]) / (1 + row["btc_net_return"]) - 1
                row["success_profit"] = row["alt_net_return"] > 0
                row["success_btc"] = row["alt_net_return"] > row["btc_net_return"]
                row["success_both"] = row["success_profit"] and row["success_btc"]
            sensitivity.append(row)
    sensitivity_summary = grouped_summary(sensitivity, ("scenario", "entry_rule"))
    write_csv("data/analysis/trades_90d.csv", rows)
    write_csv("data/analysis/entry_plans.csv", plans)
    write_csv("data/analysis/summary_by_rule_90d.csv", summaries)
    if common_summaries:
        write_csv("data/analysis/summary_common_sample_90d.csv", common_summaries)
    write_csv("data/analysis/summary_by_coin_rule_90d.csv", by_coin)
    write_csv("data/analysis/summary_by_period_90d.csv", by_period)
    write_csv("data/analysis/summary_by_event_rule_90d.csv", event_summaries)
    if rule_pairs:
        write_csv("data/analysis/paired_rule_comparisons_90d.csv", rule_pairs)
        write_csv("data/analysis/paired_rule_summary_90d.csv", pair_summary)
    write_csv("data/analysis/cost_scenarios_90d.csv", sensitivity)
    write_csv("data/analysis/cost_sensitivity_summary_90d.csv", sensitivity_summary)
    report = {"holding_days": 90, "candidate_rows": len(rows), "status_counts": dict(Counter(row["status"] for row in rows)),
              "events": len({row["event_id"] for row in rows}), "altcoins": len({row["symbol"] for row in rows}),
              "common_sample_event_asset_pairs": len(common) // 3,
              "common_sample_events": len({row["event_id"] for row in common}),
              "summary_by_rule": summaries, "summary_common_sample": common_summaries, "summary_by_period": by_period,
              "paired_rule_summary": pair_summary, "cost_sensitivity": sensitivity_summary,
              "source_file_count_verified": len(source_hashes), "source_sha256": source_hashes,
              "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
              "before_2023_outcome_complete_rows": sum(row["status"] == "completed" and row["signal_period"] == "2020-2022" and row["outcome_known_before_2023"] for row in rows),
              "earlier_signal_rows_crossing_2023": sum(row["status"] == "completed" and row["signal_period"] == "2020-2022" and not row["outcome_known_before_2023"] for row in rows),
              "limitations": ["Historical ranking publication times unverified; earlier-date availability is assumed.",
                              "Twenty signals and overlapping observations; trade rows are not independent.",
                              "Descriptive time split, no rule chosen or tuned on these full-period results.",
                              "Common equal costs cannot test differences in real liquidity, venue fees or execution.",
                              "No portfolio-capital simulation or summation of overlapping returns.",
                              "MAE uses reference-price lows; MDD uses closes plus reference entry and exit, not full intraday path."]}
    save_json("reports/backtest_90d.json", report)
    print(json.dumps({"candidate_rows": len(rows), "status_counts": report["status_counts"],
                      "common_pairs": len(common) // 3, "source_files_verified": len(source_hashes),
                      "summary": [{"rule": row["entry_rule"], "n": row["completed_trades"],
                                   "median_net_pct": row["median_alt_net_return"] * 100 if row["median_alt_net_return"] != "" else "",
                                   "median_advantage_pp": row["median_advantage_net_pp"],
                                   "profit_pct": row["success_profit_pct"], "beat_btc_pct": row["success_btc_pct"]} for row in summaries]}, indent=2, default=str))


if __name__ == "__main__":
    main()
