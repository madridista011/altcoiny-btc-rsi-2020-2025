"""RSI Wildera i sygnały BTC; bez liczenia rentowności transakcji."""

import bisect
import csv
import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rsi_wilder(prices, period=14):
    if period < 2:
        raise ValueError("Period must be at least 2")
    result = [None] * len(prices)
    if len(prices) <= period:
        return result
    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [max(change, 0.0) for change in changes]
    losses = [max(-change, 0.0) for change in changes]
    gain = sum(gains[:period]) / period
    loss = sum(losses[:period]) / period
    result[period] = 100 * gain / (gain + loss) if gain + loss else 50.0
    for position in range(period + 1, len(prices)):
        gain = (gain * (period - 1) + gains[position - 1]) / period
        loss = (loss * (period - 1) + losses[position - 1]) / period
        result[position] = 100 * gain / (gain + loss) if gain + loss else 50.0
    return result


def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def validate_rsi(prices, values, days):
    import pandas as pd

    period = 14
    deltas = pd.Series(prices).diff().iloc[1:]
    gains = deltas.clip(lower=0)
    losses = -deltas.clip(upper=0)
    gain_series = pd.concat([pd.Series([gains.iloc[:period].mean()]), gains.iloc[period:]], ignore_index=True)
    loss_series = pd.concat([pd.Series([losses.iloc[:period].mean()]), losses.iloc[period:]], ignore_index=True)
    mean_gain = gain_series.ewm(alpha=1 / period, adjust=False).mean()
    mean_loss = loss_series.ewm(alpha=1 / period, adjust=False).mean()
    independent = (100 * mean_gain / (mean_gain + mean_loss)).fillna(50).tolist()
    error = max(abs(left - right) for left, right in zip(values[period:], independent))
    assert error < 1e-10, error
    assert rsi_wilder(list(range(1, 30)))[14] == 100
    assert rsi_wilder(list(range(30, 1, -1)))[14] == 0
    assert rsi_wilder([10] * 30)[14] == 50
    assert all(value is None for value in values[:period])
    assert all(0 <= value <= 100 for value in values[period:])
    shorter_start = days.index("2019-07-01")
    shorter = rsi_wilder(prices[shorter_start:])
    differences = [abs(values[i] - shorter[i - shorter_start]) for i in range(shorter_start + period, len(days))
                   if "2020-01-01" <= days[i] <= "2025-12-31"]
    def crossings(vals, offset=0):
        return {days[i + offset] for i in range(1, len(vals))
                if vals[i - 1] is not None and vals[i] < 30 <= vals[i - 1]
                and "2020-01-01" <= days[i + offset] <= "2025-12-31"}
    assert crossings(values) == crossings(shorter, shorter_start), "Warmup changes study signals"
    return {"period": period, "seed": "Simple mean of first 14 price changes; first RSI needs 15 closes.",
            "flat_prices_policy": "50 when both smoothed gain and loss are zero",
            "independent_check": "pandas EWM, alpha=1/14, adjust=False, explicit 14-change seed",
            "pandas_version": pd.__version__, "max_difference_from_pandas": error,
            "warmup_sensitivity": {"primary_start": days[0], "alternative_start": "2019-07-01",
                                   "max_difference_in_study": max(differences), "same_study_signal_dates": True},
            "synthetic_edge_cases": "Increasing, decreasing and constant fictional prices passed.",
            "formula_source": "https://download.esignal.com/products/workstation/help/charts/studies/rsi.htm"}


def main():
    config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
    with (ROOT / "data/staging/prices_daily.csv").open(encoding="utf-8-sig", newline="") as stream:
        btc = sorted([row for row in csv.DictReader(stream) if row["asset_id"] == "bitcoin"], key=lambda row: row["date_utc"])
    days = [row["date_utc"] for row in btc]
    assert len(days) == len(set(days))
    assert all((date.fromisoformat(right) - date.fromisoformat(left)).days == 1 for left, right in zip(days, days[1:]))
    prices = [float(row["close"]) for row in btc]
    values = rsi_wilder(prices)
    validation = validate_rsi(prices, values, days)
    index = json.loads((ROOT / "data/raw/rankings/cryptwatch/2026-11-08/snapshots_response.json").read_text(encoding="utf-8"))
    snapshot_days = sorted(row["date"] for row in index["data"])
    indicator = []
    events = []
    cluster = 0
    cluster_end = None
    for i, row in enumerate(btc):
        current = values[i]
        previous = values[i - 1] if i else None
        is_signal = previous is not None and current < 30 <= previous
        in_study = config["study_start"] <= days[i] <= config["study_end"]
        indicator.append({"date_utc": days[i], "btc_close_usdt": row["close"],
                          "rsi_14_wilder": "" if current is None else current,
                          "cross_below_30": is_signal, "in_study": in_study,
                          "source_file": row["source_file"], "source_row": row["source_row"]})
        if not (is_signal and in_study):
            continue
        signal_day = date.fromisoformat(days[i])
        earlier = bisect.bisect_left(snapshot_days, days[i]) - 1
        if earlier < 0:
            raise ValueError("No earlier ranking for " + days[i])
        snapshot_day = snapshot_days[earlier]
        if cluster_end is None or signal_day > cluster_end:
            cluster += 1
        # Conservative connected groups: all 90-day windows with up to 31 days of entry delay may overlap.
        cluster_end = max(cluster_end or signal_day, signal_day + timedelta(days=121))
        events.append({"event_id": "BTC_RSI14_" + days[i].replace("-", ""), "signal_date_utc": days[i],
                       "signal_confirmed_at_utc": (signal_day + timedelta(days=1)).isoformat() + "T00:00:00Z",
                       "previous_rsi": previous, "signal_rsi": current,
                       "ranking_snapshot_date": snapshot_day,
                       "ranking_age_days": (signal_day - date.fromisoformat(snapshot_day)).days,
                       "ranking_availability_status": "date_precedes_signal; publication_time_unverified",
                       "earliest_entry_date_rule_A": (signal_day + timedelta(days=1)).isoformat(),
                       "potential_overlap_group_90d": f"G{cluster:02d}",
                       "potential_observation_end_90d": (signal_day + timedelta(days=121)).isoformat()})
    assert events
    write_csv(ROOT / "data/processed/btc_rsi_daily.csv", indicator)
    write_csv(ROOT / "data/processed/signal_events.csv", events)
    needed = [{"snapshot_date": day, "events_using_snapshot": sum(row["ranking_snapshot_date"] == day for row in events),
               "url": f"https://cryptwat.ch/api/v1/snapshots/{day}?top=30"}
              for day in sorted({row["ranking_snapshot_date"] for row in events})]
    write_csv(ROOT / "data/processed/ranking_requests.csv", needed)
    validation.update({"study_signal_count": len(events), "signals_by_year": dict(Counter(row["signal_date_utc"][:4] for row in events)),
                       "required_snapshots": len(needed), "maximum_ranking_age_days": max(row["ranking_age_days"] for row in events),
                       "potential_overlap_groups_90d": cluster,
                       "grouping_caution": "Connected overlapping potential windows; groups are not proven independent observations.",
                       "no_strategy_returns_computed": True})
    (ROOT / "reports/rsi_validation.json").write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(validation, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
