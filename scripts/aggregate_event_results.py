"""Opisowe średnie pięciu monet w zdarzeniu, bez łączenia kapitału między sygnałami."""

import json
import statistics
from collections import defaultdict
from decimal import Decimal as D

from analyze_trades import ROOT, read_csv, save_json, write_csv


def aggregate_events(trades):
    groups = defaultdict(list)
    for row in trades:
        groups[(row["event_id"], row["entry_rule"])].append(row)
    result = []
    for (event_id, rule), group in sorted(groups.items()):
        assert len(group) == 5 and len({row["asset_id"] for row in group}) == 5
        for key in ("signal_date", "entry_date", "exit_date", "holding_days", "signal_period"):
            assert len({row[key] for row in group}) == 1, (event_id, rule, key)
        first = group[0]
        completed = [row for row in group if row["status"] == "completed"]
        no_entry = sum(row["status"] == "no_entry" for row in group)
        status = "completed" if len(completed) == 5 else "no_entry" if no_entry == 5 else "incomplete_basket"
        row = {"event_id": event_id, "entry_rule": rule,
               **{key: first[key] for key in ("signal_date", "entry_date", "exit_date", "holding_days", "signal_period", "potential_overlap_group_90d")},
               "symbols": "|".join(sorted(item["symbol"] for item in group)),
               "btc_venue_weights": "|".join(f"{venue}:{sum(item['venue'] == venue for item in group)}/5" for venue in sorted({item["venue"] for item in group})),
               "selected_assets": 5, "completed_assets": len(completed), "no_entry_assets": no_entry, "status": status,
               **{key: "" for key in ("event_mean_alt_gross_return", "event_mean_alt_net_return", "event_mean_btc_gross_return", "event_mean_btc_net_return",
                                      "advantage_net_pp", "relative_net_return", "success_profit", "success_btc", "success_both")}}
        if status == "completed":
            for field in ("alt_gross_return", "alt_net_return", "btc_gross_return", "btc_net_return"):
                row["event_mean_" + field] = statistics.mean(D(item[field]) for item in group)
            alt, btc = row["event_mean_alt_net_return"], row["event_mean_btc_net_return"]
            row["advantage_net_pp"] = (alt - btc) * 100
            row["relative_net_return"] = (1 + alt) / (1 + btc) - 1
            row["success_profit"], row["success_btc"] = alt > 0, alt > btc
            row["success_both"] = row["success_profit"] and row["success_btc"]
        result.append(row)
    return result


def event_summary(rows, keys):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in keys)].append(row)
    result = []
    for key, group in sorted(groups.items()):
        completed = [row for row in group if row["status"] == "completed"]
        summary = {**dict(zip(keys, key)), "qualified_events": len(group), "completed_events": len(completed),
                   "no_entry_events": sum(row["status"] == "no_entry" for row in group),
                   "incomplete_events": sum(row["status"] not in ("completed", "no_entry") for row in group)}
        for field in ("event_mean_alt_gross_return", "event_mean_alt_net_return", "event_mean_btc_gross_return", "event_mean_btc_net_return", "advantage_net_pp"):
            values = [row[field] for row in completed]
            summary["mean_" + field] = statistics.mean(values) if values else ""
            summary["median_" + field] = statistics.median(values) if values else ""
        for field in ("success_profit", "success_btc", "success_both"):
            count = sum(row[field] for row in completed)
            summary[field + "_count"] = count
            summary[field + "_pct"] = D(100) * count / len(completed) if completed else ""
        result.append(summary)
    return result


def main():
    rows = aggregate_events(read_csv("data/analysis/trades_90d.csv"))
    summary = event_summary(rows, ("entry_rule",))
    by_period = event_summary(rows, ("signal_period", "entry_rule"))
    write_csv("data/analysis/event_mean_returns_90d.csv", rows)
    write_csv("data/analysis/summary_event_means_90d.csv", summary)
    write_csv("data/analysis/summary_event_means_by_period_90d.csv", by_period)
    save_json("reports/event_aggregation_90d.json", {
        "reporting_extension_defined_after_individual_results": True,
        "interpretation": "Arithmetic mean of five returns within the same event and rule. Equal 20% initial total-budget shares, no rebalancing during the holding period. Separate hypothetical budget per signal.",
        "benchmark": "Mean of five venue-matched BTC returns with the same weights. Not always a single-venue BTC return.",
        "no_capital_path_across_overlapping_events": True,
        "no_average_of_asset_MAE_or_MDD_reported_as_basket_risk": True,
        "summary": summary, "summary_by_period": by_period})
    print(json.dumps(summary, ensure_ascii=False, default=str, indent=2))


if __name__ == "__main__":
    main()
