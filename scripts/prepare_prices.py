"""Odtwarza tabelę cen i raport jakości z lokalnych odpowiedzi Binance.

Nie pobiera danych, nie uzupełnia cen i nie oblicza RSI ani wyników strategii.
Uruchomienie: python scripts/prepare_prices.py
"""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY_MS = 86_400_000


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def save_csv(path, rows, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def days_between(start, end):
    current = date.fromisoformat(start)
    last = date.fromisoformat(end)
    while current <= last:
        yield current.isoformat()
        current += timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="data/metadata/event_prices/manifest.json")
    args = parser.parse_args()
    manifest_path = (ROOT / args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
    symbol_map = {
        segment["symbol"]: asset["asset_id"]
        for asset in config["assets"] for segment in asset["segments"]
    }
    cache_groups = {
        asset["asset_id"]: "benchmark" if asset["benchmark"] else asset.get("cache_group", "initial_download")
        for asset in config["assets"]
    }
    partial = {(r["symbol"], r["date"]): r for r in config["known_partial_days"]}
    expected_missing = {(r["asset_id"], r["date"]): r["reason"] for r in config["expected_missing_days"]}
    hashes = {
        entry["path"]: hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest()
        for entry in manifest
    }
    hashes[manifest_path.relative_to(ROOT).as_posix()] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    lock_path = ROOT / "data/metadata" / (manifest_path.parent.name + "_raw_sha256.json")
    if lock_path.exists():
        if json.loads(lock_path.read_text(encoding="utf-8")) != hashes:
            raise SystemExit("STOP: pliki źródłowe lub manifest zmieniły się względem zapisanych SHA-256.")
    else:
        save_json(lock_path, hashes)

    prices = []
    errors = []
    raw_count = 0
    for entry in manifest:
        source_path = entry["path"]
        payload = json.loads((ROOT / source_path).read_text(encoding="utf-8"))
        rows = payload if isinstance(payload, list) else payload["result"]
        if len(rows) != entry["rows"]:
            errors.append({"file": source_path, "error": "manifest_row_count_mismatch"})
        symbol = entry["request"]["symbol"]
        for source_row, row in enumerate(rows, start=1):
            raw_count += 1
            try:
                if len(row) != 12:
                    raise ValueError("wrong_column_count")
                timestamp = int(row[0])
                if timestamp % DAY_MS:
                    raise ValueError("timestamp_not_utc_midnight_or_wrong_unit")
                if not entry["request"]["startTime"] <= timestamp <= entry["request"]["endTime"]:
                    raise ValueError("timestamp_outside_request")
                day = datetime.fromtimestamp(timestamp / 1000, timezone.utc).date().isoformat()
                marker = partial.get((symbol, day), {})
                expected_close = timestamp + DAY_MS - 1
                if marker.get("expected_close_time_utc"):
                    expected_close = int(datetime.fromisoformat(marker["expected_close_time_utc"].replace("Z", "+00:00")).timestamp() * 1000)
                if int(row[6]) != expected_close:
                    raise ValueError("unexpected_close_timestamp")
                op, high, low, close, volume, quote_volume = [Decimal(str(row[i])) for i in (1, 2, 3, 4, 5, 7)]
                if any(not x.is_finite() for x in (op, high, low, close, volume, quote_volume)):
                    raise ValueError("non_finite_number")
                if min(op, high, low, close) <= 0 or min(volume, quote_volume) < 0 or int(row[8]) < 0:
                    raise ValueError("non_positive_price_or_negative_activity")
                if not low <= min(op, close) <= max(op, close) <= high:
                    raise ValueError("inconsistent_ohlc")
                phase = "warmup" if day < config["study_start"] else "study" if day <= config["study_end"] else "followup"
                prices.append({
                    "date_utc": day,
                    "asset_id": symbol_map[symbol],
                    "cache_group": cache_groups[symbol_map[symbol]],
                    "source_symbol": symbol,
                    "venue": "binance",
                    "quote_currency": config["quote_currency"],
                    "source_open_time_utc": datetime.fromtimestamp(timestamp / 1000, timezone.utc).isoformat(timespec="milliseconds"),
                    "source_close_time_utc": datetime.fromtimestamp(int(row[6]) / 1000, timezone.utc).isoformat(timespec="milliseconds"),
                    "open": row[1], "high": row[2], "low": row[3], "close": row[4],
                    "volume_base": row[5], "volume_quote": row[7], "trade_count": row[8],
                    "data_phase": phase,
                    "known_partial_day": bool(marker),
                    "known_non_midnight_open": marker.get("known_non_midnight_open", False),
                    "known_early_trading_stop": marker.get("known_early_trading_stop", False),
                    "source_file": source_path, "source_row": source_row,
                })
            except (ValueError, InvalidOperation, KeyError, IndexError, TypeError) as exc:
                errors.append({"file": source_path, "row": source_row, "error": str(exc)})

    prices.sort(key=lambda r: (r["asset_id"], r["date_utc"]))
    duplicates = [
        {"asset_id": key[0], "date_utc": key[1], "count": count}
        for key, count in Counter((r["asset_id"], r["date_utc"]) for r in prices).items() if count > 1
    ]
    grouped = defaultdict(list)
    for row in prices:
        grouped[row["asset_id"]].append(row)
    missing = []
    inventory = []
    jump_flags = []
    availability_exclusions = []
    for asset in config["assets"]:
        asset_id = asset["asset_id"]
        rows = grouped[asset_id]
        start = config["btc_warmup_start"] if asset["benchmark"] else asset.get("available_from", config["study_start"])
        pre_listing_days = max(0, (date.fromisoformat(start) - date.fromisoformat(config["study_start"])).days)
        if pre_listing_days:
            availability_exclusions.append({"asset_id": asset_id, "from": config["study_start"],
                                           "through": (date.fromisoformat(start) - timedelta(days=1)).isoformat(),
                                           "days": pre_listing_days, "reason": "source_pair_not_yet_listed",
                                           "source": asset["availability_source"]})
        expected = set(days_between(start, config["data_end"]))
        actual = {r["date_utc"] for r in rows}
        absent = sorted(expected - actual)
        extras = sorted(actual - expected)
        for day in absent:
            missing.append({"asset_id": asset_id, "date_utc": day,
                            "documented": (asset_id, day) in expected_missing,
                            "reason": expected_missing.get((asset_id, day), "requires_investigation")})
        if extras:
            errors.append({"asset_id": asset_id, "error": "dates_outside_expected_calendar", "dates": extras})
        inventory.append({"asset_id": asset_id, "cache_group": cache_groups[asset_id],
                          "calendar_start": start, "pre_listing_days": pre_listing_days, "rows": len(rows),
                          "first_date": min(actual) if actual else "", "last_date": max(actual) if actual else "",
                          "study_rows": sum(r["data_phase"] == "study" for r in rows),
                          "missing_days": len(absent), "known_partial_days": sum(r["known_partial_day"] for r in rows)})
        for previous, current in zip(rows, rows[1:]):
            ratio = Decimal(current["close"]) / Decimal(previous["close"])
            if ratio > 5 or ratio < Decimal("0.2"):
                jump_flags.append({"asset_id": asset_id, "date_utc": current["date_utc"],
                                   "previous_date": previous["date_utc"], "close_ratio": str(ratio)})

    unexpected_missing = [r for r in missing if not r["documented"]]
    report = {
        "raw_manifest": manifest_path.relative_to(ROOT).as_posix(),
        "raw_pages": len(manifest), "raw_rows": raw_count, "normalized_rows": len(prices),
        "checks": {"schema_price_timestamp_errors": len(errors), "duplicate_asset_dates": len(duplicates),
                   "unexpected_missing_days": len(unexpected_missing), "documented_missing_days": len(missing) - len(unexpected_missing),
                   "known_partial_days": sum(r["known_partial_day"] for r in prices), "large_close_move_flags": len(jump_flags)},
        "inventory": inventory, "errors": errors, "duplicates": duplicates, "missing_days": missing,
        "availability_exclusions": availability_exclusions,
        "large_close_move_flags": jump_flags,
        "limitations": ["Single venue only; not a consolidated market price.",
                        "Checks do not prove economic accuracy or full intraday tradability.",
                        "A large-move flag is a review trigger, not a reason to delete a price.",
                        "The dataset is not an executable strategy: entry/exit rules and missing-value policies remain to be fixed.",
                        "Cached assets do not define the point-in-time top-five universe; event rankings and additional asset prices remain to be acquired."]
    }
    output = ROOT / "data/staging"
    save_json(ROOT / "reports/data_quality.json", report)
    save_csv(output / "inventory.csv", inventory, list(inventory[0]))
    save_csv(output / "missing_days.csv", missing, ["asset_id", "date_utc", "documented", "reason"])
    if errors or duplicates or unexpected_missing:
        raise SystemExit("STOP: raport jakości zawiera nierozwiązane błędy; tabela cen nie została utworzona.")
    save_csv(output / "prices_daily.csv", prices, list(prices[0]))
    save_csv(output / "prices_base.csv", [r for r in prices if r["cache_group"] in ("benchmark", "initial_download")], list(prices[0]))
    save_csv(output / "prices_ranking_selected.csv", [r for r in prices if r["cache_group"] == "ranking_selected_download"], list(prices[0]))
    extension_rows = [r for r in prices if r["cache_group"] == "requested_download"]
    save_csv(output / "prices_extensions.csv", extension_rows, list(prices[0]))
    extension_sample = []
    for asset_id in sorted({r["asset_id"] for r in extension_rows}):
        extension_sample.extend([r for r in extension_rows if r["asset_id"] == asset_id][:3])
    save_csv(output / "sample_extensions_first_3_days.csv", extension_sample, list(prices[0]))
    sample = [r for r in prices if "2020-01-01" <= r["date_utc"] <= "2020-01-03"]
    save_csv(output / "sample_first_3_days.csv", sample, list(prices[0]))
    print(json.dumps({"rows": len(prices), "checks": report["checks"], "inventory": inventory}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
