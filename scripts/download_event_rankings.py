"""Pobiera wyłącznie rankingi potrzebne dla zapisanych sygnałów BTC."""

import csv
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/raw/rankings/cryptwatch/2026-11-08_events"
USER_AGENT = os.environ.get("RANKING_USER_AGENT", "")


def main():
    requests = list(csv.DictReader((ROOT / "data/processed/ranking_requests.csv").open(encoding="utf-8-sig", newline="")))
    FOLDER.mkdir(parents=True, exist_ok=True)
    manifest_path = FOLDER / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    saved = {row["snapshot_date"]: row for row in manifest}
    for request_row in requests:
        day = request_row["snapshot_date"]
        path = FOLDER / (day + ".json")
        if day in saved:
            assert hashlib.sha256(path.read_bytes()).hexdigest() == saved[day]["sha256"], "Stored source changed"
            continue
        if path.exists():
            raise RuntimeError("Existing file without manifest: " + str(path))
        if not USER_AGENT:
            raise RuntimeError("Set RANKING_USER_AGENT with project identification and contact before downloading new snapshots.")
        request = urllib.request.Request(request_row["url"], headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=25) as response:
                    raw = response.read()
                    headers = dict(response.headers.items())
                break
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise
                time.sleep(min(30, max(2 ** attempt, int(exc.headers.get("Retry-After", "2")))))
        parsed = json.loads(raw)
        if parsed["data"]["date"] != day:
            raise RuntimeError("Requested date differs from returned date: " + day)
        rows = parsed["data"]["rows"]
        if len(rows) < 15:
            raise RuntimeError("Too few ranked assets: " + day)
        path.write_bytes(raw)
        manifest.append({"snapshot_date": day, "url": request_row["url"], "path": path.relative_to(ROOT).as_posix(),
                         "retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "source_as_of": parsed["as_of"],
                         "source": parsed["source"], "rows": len(rows), "sha256": hashlib.sha256(raw).hexdigest(),
                         "etag": headers.get("ETag", headers.get("Etag")), "last_modified": headers.get("Last-Modified"),
                         "user_agent": USER_AGENT})
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{day}: {len(rows)} assets", flush=True)
        time.sleep(1.4)
    print(f"Downloaded or verified {len(requests)} historical snapshots.")


if __name__ == "__main__":
    main()
