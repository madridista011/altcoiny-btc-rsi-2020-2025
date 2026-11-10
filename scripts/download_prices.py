"""Ponowne pobranie cen z publicznego Binance Spot API (bez klucza).

Każde uruchomienie tworzy nowy folder. Nie nadpisuje istniejących źródeł.
Nie pobiera rankingów i nie wykonuje analizy strategii.
"""

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://data-api.binance.vision/api/v3/klines"
DAY_MS = 86_400_000


def milliseconds(day):
    return int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000)


def fetch(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Google-DA-educational-case-study/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
            delay = min(30, max(2 ** attempt, int(exc.headers.get("Retry-After", "1"))))
            time.sleep(delay)
        except urllib.error.URLError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("Download failed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
    tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    folder = ROOT / "data/raw/binance" / tag
    folder.mkdir(parents=True, exist_ok=False)
    manifest = []
    try:
        for asset in config["assets"]:
            for segment in asset["segments"]:
                cursor = milliseconds(segment["start"])
                end = milliseconds(segment["end"]) + DAY_MS - 1
                page = 0
                while cursor <= end:
                    page += 1
                    params = {"symbol": segment["symbol"], "interval": "1d", "limit": 1000,
                              "startTime": cursor, "endTime": end, "timeZone": "0"}
                    url = BASE_URL + "?" + urllib.parse.urlencode(params)
                    raw = fetch(url)
                    rows = json.loads(raw)
                    if not isinstance(rows, list):
                        raise ValueError("Expected an array from Binance: " + raw[:200])
                    path = folder / f"{segment['symbol']}_page{page:03d}.json"
                    path.write_text(raw, encoding="utf-8")
                    manifest.append({"source_id": "binance_spot_api", "connector": "direct_http", "url": url,
                                     "request": params, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                                     "path": path.relative_to(ROOT).as_posix(), "rows": len(rows)})
                    print(f"{segment['symbol']}, page {page}: {len(rows)} rows", flush=True)
                    if not rows or len(rows) < params["limit"]:
                        break
                    next_cursor = int(rows[-1][0]) + DAY_MS
                    if next_cursor <= cursor:
                        raise ValueError("Non-advancing API cursor")
                    cursor = next_cursor
                    time.sleep(0.2)
    finally:
        (folder / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Now run: python scripts/prepare_prices.py --manifest " + (folder / "manifest.json").relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
