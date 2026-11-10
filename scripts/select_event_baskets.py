"""Dobiera historyczny top 5 bez filtrowania według dostępności cen."""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from build_signal_events import write_csv

ROOT = Path(__file__).resolve().parents[1]


def main():
    events = list(csv.DictReader((ROOT / "data/processed/signal_events.csv").open(encoding="utf-8-sig", newline="")))
    classification = json.loads((ROOT / "config/asset_classification.json").read_text(encoding="utf-8"))["assets"]
    manifest = json.loads((ROOT / "data/raw/rankings/cryptwatch/2026-11-08_events/manifest.json").read_text(encoding="utf-8"))
    sources = {}
    for entry in manifest:
        path = ROOT / entry["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], entry["path"]
        payload = json.loads(path.read_bytes())
        assert payload["data"]["date"] == entry["snapshot_date"]
        sources[entry["snapshot_date"]] = (payload["data"]["rows"], entry)
    universe = []
    audit = []
    summaries = []
    for event in events:
        snapshot = event["ranking_snapshot_date"]
        assert snapshot < event["signal_date_utc"]
        rows, entry = sources[snapshot]
        selected = []
        ranks = [int(row["rank"]) for row in rows]
        assert ranks == list(range(1, len(rows) + 1))
        assert len({row["slug"] for row in rows}) == len(rows)
        for raw in rows:
            if len(selected) == 5:
                break
            slug = raw["slug"]
            if slug not in classification:
                raise ValueError(f"Unknown classification before cutoff: {event['event_id']} {slug}")
            info = classification[slug]
            if slug == "gram":
                detail = json.loads((ROOT / info["identity_evidence_file"]).read_text(encoding="utf-8"))["data"]["coin"]
                assert detail["id"] == info["cmc_id"]
                assert any(alias["symbol"] == "TON" and alias["valid_from"] <= snapshot < alias["valid_to"] for alias in detail["aliases"])
            audit.append({"event_id": event["event_id"], "ranking_snapshot_date": snapshot,
                          "source_rank": raw["rank"], "source_slug": slug, "source_symbol": raw["symbol"],
                          "asset_id": info["asset_id"], "historical_symbol": info["historical_symbol"],
                          "eligible": info["eligible"], "reason": info["reason"], "ranking_source_file": entry["path"]})
            if not info["eligible"]:
                continue
            record = {"event_id": event["event_id"], "signal_date_utc": event["signal_date_utc"],
                      "ranking_snapshot_date": snapshot, "ranking_age_days": event["ranking_age_days"],
                      "eligible_position": len(selected) + 1, "source_rank": raw["rank"],
                      "asset_id": info["asset_id"], "symbol_at_event": info["historical_symbol"],
                      "source_slug": slug, "source_symbol_as_returned": raw["symbol"],
                      "source_market_cap_usd": raw["market_cap"], "ranking_source_file": entry["path"],
                      "ranking_availability_status": event["ranking_availability_status"],
                      "basket_locked_across_entry_rules": True}
            universe.append(record)
            selected.append(record)
        assert len(selected) == 5
        assert len({row["asset_id"] for row in selected}) == 5
        summaries.append({"event_id": event["event_id"], "signal_date_utc": event["signal_date_utc"],
                          "rsi_14": event["signal_rsi"], "ranking_snapshot_date": snapshot,
                          "ranking_age_days": event["ranking_age_days"],
                          "basket": " / ".join(row["symbol_at_event"] for row in selected),
                          "potential_overlap_group_90d": event["potential_overlap_group_90d"],
                          "ranking_timing": event["ranking_availability_status"]})
    assert len(universe) == len(events) * 5
    # Missing prices must not remove historically selected BSV or TON.
    assert {"bitcoin_sv", "toncoin"}.issubset({row["asset_id"] for row in universe})
    requirements = []
    for asset_id in sorted({row["asset_id"] for row in universe}):
        selections = [row for row in universe if row["asset_id"] == asset_id]
        first = min(date.fromisoformat(row["signal_date_utc"]) + timedelta(days=1) for row in selections)
        last = max(date.fromisoformat(row["signal_date_utc"]) + timedelta(days=211) for row in selections)
        requirements.append({"asset_id": asset_id, "symbol": selections[0]["symbol_at_event"],
                             "selected_events": len(selections), "required_start": first.isoformat(),
                             "required_end": last.isoformat(),
                             "preferred_price_venue": "kucoin" if asset_id in ("bitcoin_sv", "toncoin") else "binance",
                             "quote_currency": "USDT"})
    output = ROOT / "data/processed"
    write_csv(output / "event_universe.csv", universe)
    write_csv(output / "event_baskets.csv", summaries)
    write_csv(output / "eligibility_audit.csv", audit)
    write_csv(output / "asset_requirements.csv", requirements)
    counts = Counter(row["symbol_at_event"] for row in universe)
    report = {"events": len(events), "historical_snapshots": len(sources), "selected_asset_event_rows": len(universe),
              "distinct_altcoins": len(counts), "selected_events_by_coin": dict(counts),
              "distinct_ordered_baskets": len({row["basket"] for row in summaries}),
              "distinct_asset_sets": len({tuple(sorted(row["asset_id"] for row in universe if row["event_id"] == event["event_id"])) for event in events}),
              "all_baskets_have_five_distinct_eligible_assets": True,
              "all_snapshots_precede_signal_day": True,
              "prices_not_used_to_filter_selection": True,
              "source_symbol_normalizations": [{"source_symbol": "GRAM", "symbol_at_event": "TON", "asset_id": "toncoin",
                                                "basis": "CMC id 11419 and date-valid aliases in the saved detail response"}],
              "ranking_publication_time_verified": False, "no_strategy_returns_computed": True}
    (ROOT / "reports/universe_validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
