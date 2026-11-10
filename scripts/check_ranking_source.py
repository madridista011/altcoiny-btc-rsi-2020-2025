"""Sprawdza lokalny indeks dat i próbki rankingów; nie wybiera zdarzeń RSI."""

import bisect
import hashlib
import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/raw/rankings/cryptwatch/2026-11-08"


def main():
    index = json.loads((FOLDER / "snapshots_response.json").read_text(encoding="utf-8"))
    dates = sorted(date.fromisoformat(row["date"]) for row in index["data"])
    if len(dates) != len(set(dates)):
        raise SystemExit("Duplicate snapshot dates")
    ages = []
    older_than_seven = []
    missing = []
    day = date(2020, 1, 1)
    while day <= date(2025, 12, 31):
        position = bisect.bisect_left(dates, day) - 1
        if position < 0:
            missing.append(day.isoformat())
        else:
            snapshot = dates[position]
            age = (day - snapshot).days
            ages.append(age)
            if age > 7:
                older_than_seven.append({"potential_signal_date": day.isoformat(),
                                         "previous_snapshot_date": snapshot.isoformat(), "age_days": age})
        day += timedelta(days=1)

    samples = []
    for path in sorted(FOLDER.glob("sample_*_response.json")):
        response = json.loads(path.read_text(encoding="utf-8"))
        snapshot = response["data"]
        requested = path.name.removeprefix("sample_").removesuffix("_response.json")
        if snapshot["date"] != requested:
            raise SystemExit("Sample returned a different snapshot date: " + path.name)
        rows = snapshot["rows"]
        ranks = [row["rank"] for row in rows]
        if len({row["slug"] for row in rows}) != len(rows) or ranks != list(range(1, len(rows) + 1)):
            raise SystemExit("Invalid ranks or duplicate slugs: " + path.name)
        samples.append({"snapshot_date": snapshot["date"], "rows": len(rows),
                        "first_15_symbols_as_returned": [row["symbol"] for row in rows[:15]],
                        "response_as_of": response["as_of"], "source_file": path.relative_to(ROOT).as_posix()})
    reference = ["BTC", "ETH", "XRP", "BCH", "USDT", "BSV", "LTC", "EOS", "BNB", "XTZ", "LINK", "ADA", "XLM", "LEO", "TRX"]
    sample_2020 = next(row for row in samples if row["snapshot_date"] == "2020-03-08")
    if sample_2020["first_15_symbols_as_returned"] != reference:
        raise SystemExit("2020 sample differs from the independently viewed CMC table")
    hashes = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(FOLDER.glob("*.json"))}
    lock = ROOT / "data/metadata/rankings_probe_sha256.json"
    if lock.exists():
        if json.loads(lock.read_text(encoding="utf-8")) != hashes:
            raise SystemExit("Saved ranking responses changed")
    else:
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    report = {
        "verification_date": "2026-11-08", "source": "Data: CryptWatch, based on CoinMarketCap",
        "source_docs": "https://cryptwat.ch/api", "index_snapshot_count": len(dates),
        "first_snapshot": dates[0].isoformat(), "last_snapshot": dates[-1].isoformat(),
        "snapshots_by_study_year": dict(Counter(d.year for d in dates if 2020 <= d.year <= 2025)),
        "calendar_probe": {"method": "Latest stored date strictly before each calendar day; publication time not validated.",
                           "no_earlier_snapshot": missing, "maximum_age_days": max(ages),
                           "older_than_seven_days": older_than_seven},
        "samples": samples,
        "cross_check": {"date": "2020-03-08", "first_15_ranked_symbols_match": True,
                        "source": "https://coinmarketcap.com/historical/20200308/",
                        "method": "Order compared with an independently viewed public CMC table; no full database copied."},
        "raw_files": [{"path": path.relative_to(ROOT).as_posix(),
                       "file_written_at_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                       "sha256": hashes[path.relative_to(ROOT).as_posix()]} for path in sorted(FOLDER.glob("*.json"))],
        "status": "Candidate source verified on three samples and calendar only; full event rankings not acquired.",
        "open_checks": ["Historical publication times and usable lag.",
                        "Date returned by the API may precede the requested date.",
                        "Historical identity and retrospective ticker normalization (e.g. LUNC in an April 2022 response).",
                        "Point-in-time stablecoin and wrapped-token exclusions.",
                        "Price coverage for all coins selected by actual signal dates."]
    }
    output = ROOT / "reports/ranking_source_check.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"snapshots": len(dates), "sample_count": len(samples),
                      "cross_check_match": True, "maximum_snapshot_age_days": max(ages),
                      "days_without_prior_snapshot": len(missing)}, indent=2))


if __name__ == "__main__":
    main()
