"""Łączy ceny wybranych aktywów i sprawdza pokrycie potencjalnych transakcji.

Nie oblicza stóp zwrotu. BSV i TON oraz odpowiadający im BTC pochodzą z KuCoin.
"""

import csv
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from build_signal_events import write_csv

ROOT = Path(__file__).resolve().parents[1]
KUCOIN_SOURCES = [
    {"asset_id": "bitcoin_sv", "symbol": "BSV-USDT", "path": "data/raw/identity_checks/kucoin_bsv_probe.json",
     "startAt": 1584057600, "endAt": 1602374399},
    {"asset_id": "toncoin", "symbol": "GRAM-USDT", "path": "data/raw/identity_checks/kucoin_gram_probe.json",
     "startAt": 1719273600, "endAt": 1741219199},
    {"asset_id": "bitcoin", "symbol": "BTC-USDT", "path": "data/raw/kucoin/2026-11-08/btc_2020.json",
     "startAt": 1584057600, "endAt": 1602374399},
    {"asset_id": "bitcoin", "symbol": "BTC-USDT", "path": "data/raw/kucoin/2026-11-08/btc_2024_2025.json",
     "startAt": 1719273600, "endAt": 1741219199}
]
FIELDS = ["date_utc", "asset_id", "venue", "source_symbol", "quote_currency", "open", "high", "low", "close",
          "volume_base", "volume_quote", "trade_count", "known_partial_day", "known_non_midnight_open",
          "known_early_trading_stop", "source_file", "source_row"]


def read_csv(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    requirements = read_csv("data/processed/asset_requirements.csv")
    selected = {row["asset_id"] for row in requirements} | {"bitcoin"}
    prices = [{key: row[key] for key in FIELDS} for row in read_csv("data/staging/prices_daily.csv") if row["asset_id"] in selected]
    metadata = []
    for source in KUCOIN_SOURCES:
        path = ROOT / source["path"]
        raw = path.read_bytes()
        payload = json.loads(raw)
        assert payload["code"] == "200000", (path, payload)
        rows = payload["data"]
        assert rows
        metadata.append({**source, "url": f"https://api.kucoin.com/api/v1/market/candles?symbol={source['symbol']}&type=1day&startAt={source['startAt']}&endAt={source['endAt']}",
                         "sha256": hashlib.sha256(raw).hexdigest(), "rows": len(rows),
                         "captured_at_utc_from_file_mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()})
        for source_row, raw_row in enumerate(rows, start=1):
            assert len(raw_row) == 7
            timestamp = int(raw_row[0])
            assert timestamp % 86400 == 0
            assert source["startAt"] <= timestamp <= source["endAt"]
            # KuCoin order: time, open, close, high, low, base volume, quote volume.
            op, close, high, low, volume, amount = [Decimal(value) for value in raw_row[1:]]
            assert all(value.is_finite() for value in (op, close, high, low, volume, amount))
            assert min(op, close, high, low) > 0 and min(volume, amount) >= 0
            assert low <= min(op, close) <= max(op, close) <= high
            prices.append({"date_utc": datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat(),
                           "asset_id": source["asset_id"], "venue": "kucoin", "source_symbol": source["symbol"],
                           "quote_currency": "USDT", "open": raw_row[1], "high": raw_row[3], "low": raw_row[4], "close": raw_row[2],
                           "volume_base": raw_row[5], "volume_quote": raw_row[6], "trade_count": "",
                           "known_partial_day": False, "known_non_midnight_open": False, "known_early_trading_stop": False,
                           "source_file": source["path"], "source_row": source_row})
    lock_path = ROOT / "data/metadata/kucoin_event_sources_sha256.json"
    hashes = {row["path"]: row["sha256"] for row in metadata}
    if lock_path.exists():
        assert json.loads(lock_path.read_text(encoding="utf-8")) == hashes, "KuCoin sources changed"
    else:
        lock_path.write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    (ROOT / "data/metadata/kucoin_manifest.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prices.sort(key=lambda row: (row["asset_id"], row["venue"], row["date_utc"]))
    lookup = {(row["asset_id"], row["venue"], row["date_utc"]): row for row in prices}
    assert len(lookup) == len(prices), "Duplicate asset/venue/date"
    venues = {row["asset_id"]: row["preferred_price_venue"] for row in requirements}
    events = read_csv("data/processed/event_universe.csv")
    coverage = []
    missing = []
    for event in events:
        venue = venues[event["asset_id"]]
        signal = date.fromisoformat(event["signal_date_utc"])
        required_days = [(signal + timedelta(days=offset)).isoformat() for offset in range(1, 212)]
        alt_missing = [day for day in required_days if (event["asset_id"], venue, day) not in lookup]
        btc_missing = [day for day in required_days if ("bitcoin", venue, day) not in lookup]
        if alt_missing or btc_missing:
            missing.append({"event_id": event["event_id"], "asset_id": event["asset_id"], "venue": venue,
                            "alt_missing": alt_missing, "btc_missing": btc_missing})
        coverage.append({"event_id": event["event_id"], "asset_id": event["asset_id"], "symbol_at_event": event["symbol_at_event"],
                         "price_venue": venue, "benchmark_venue": venue, "quote_currency": "USDT",
                         "required_start": required_days[0], "required_end": required_days[-1],
                         "required_days": len(required_days), "alt_missing_days": len(alt_missing), "btc_missing_days": len(btc_missing),
                         "coverage_complete": not (alt_missing or btc_missing)})
    report = {"market_price_rows": len(prices), "altcoin_count": len(requirements), "event_asset_pairs": len(events),
              "fully_covered_event_asset_pairs": len(events) - len(missing), "missing_cases": missing,
              "price_venues": sorted(set(row["venue"] for row in prices)), "quote_currency": "USDT",
              "benchmark_policy": "BTC on the same venue and same eventual entry/exit dates; BTC RSI signals always use Binance.",
              "coverage_window": "signal+1 through signal+211, covering up to 31 days before entry plus 180 days holding.",
              "current_api_symbol_ton": "GRAM-USDT; identity is historical Toncoin, not a new asset selected using future information.",
              "no_prices_imputed": True, "no_strategy_returns_computed": True}
    write_csv(ROOT / "data/processed/price_coverage.csv", coverage)
    (ROOT / "reports/event_price_coverage.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit("STOP: unresolved price gaps; see event_price_coverage.json")
    write_csv(ROOT / "data/processed/market_prices_daily.csv", prices, FIELDS)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
