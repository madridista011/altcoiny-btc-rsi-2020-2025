"""Przygotowuje dwa poziomy obserwacji do Tableau bez zmiany wyników analizy."""

import csv
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tableau"


def read(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def flag(value):
    return 1 if value == "True" else 0 if value == "False" else ""


def decimal(value):
    return format(D(value), ".15g") if value != "" else ""


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    audit = json.loads((ROOT / "reports/trade_output_validation.json").read_text(encoding="utf-8"))
    for relative, digest in audit["analysis_csv_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    OUT.mkdir(exist_ok=True)
    trades = read("data/analysis/trades_90d.csv")
    baskets = read("data/analysis/event_mean_returns_90d.csv")
    coins = []
    common_fields = {"EventID": "event_id", "DataSygnalu": "signal_date", "Regula": "entry_rule",
                     "OkresSygnalu": "signal_period", "Wejscie": "entry_date", "Wyjscie": "exit_date", "Status": "status"}
    number_fields = {"WynikAltNetto": "alt_net_return", "WynikBTCNetto": "btc_net_return",
                     "WynikAltBrutto": "alt_gross_return", "WynikBTCBrutto": "btc_gross_return",
                     "PrzewagaPP": "advantage_net_pp", "WynikWzgledny": "relative_net_return",
                     "MAEAlt": "alt_mae", "MAEBTC": "btc_mae", "MDDAlt": "alt_mdd_close", "MDDBTC": "btc_mdd_close"}
    flags = {"Zysk": "success_profit", "LepszyOdBTC": "success_btc", "ObaWarunki": "success_both"}
    for source in trades:
        row = {**{target: source[key] for target, key in common_fields.items()},
               "Moneta": source["symbol"], "Sygnal": source["signal_date"], "Gielda": source["venue"], "RankingData": source["ranking_date"],
               "WiekRankingu": source["ranking_age_days"],
               **{target: decimal(source[key]) for target, key in number_fields.items()},
               **{target: flag(source[key]) for target, key in flags.items()},
               "LiczbaPar": 1, "KompletnaPara": int(source["status"] == "completed")}
        coins.append(row)
    event_rows = []
    for source in baskets:
        row = {**{target: source[key] for target, key in common_fields.items()},
               "Sygnal": source["signal_date"], "SkladKoszyka": source["symbols"].replace("|", " / "), "WagiGieldBTC": source["btc_venue_weights"],
               "WynikAltNetto": decimal(source["event_mean_alt_net_return"]), "WynikBTCNetto": decimal(source["event_mean_btc_net_return"]),
               "PrzewagaPP": decimal(source["advantage_net_pp"]),
               **{target: flag(source[key]) for target, key in flags.items()},
               "LiczbaZdarzen": 1, "KompletnyKoszyk": int(source["status"] == "completed")}
        event_rows.append(row)
    write("monety.csv", coins)
    write("koszyki.csv", event_rows)
    for source, exported in zip(trades, coins):
        for target, key in number_fields.items():
            if source[key] != "":
                assert abs(D(source[key]) - D(exported[target])) < D("1e-10")
    assert len(coins) == 300 and len(event_rows) == 60
    assert len({(row["EventID"], row["Moneta"], row["Regula"]) for row in coins}) == 300
    assert len({(row["EventID"], row["Regula"]) for row in event_rows}) == 60
    result = {"status": "passed", "coin_rows": len(coins), "basket_rows": len(event_rows),
              "input_hashes": audit["analysis_csv_sha256"],
              "csv_format": "UTF-8 BOM, comma separated, dot decimal, ISO dates; parse locale en_US, display locale pl_PL",
              "fractions": ["WynikAltNetto", "WynikBTCNetto", "MAEAlt", "MAEBTC", "MDDAlt", "MDDBTC"],
              "percentage_points": ["PrzewagaPP"],
              "grain_warning": "Do not physically join the 60 basket rows onto the 300 coin rows. A coin filter must not redefine the original five-coin basket.",
              "output_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in (OUT / "monety.csv", OUT / "koszyki.csv")}}
    (ROOT / "reports/tableau_data_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "coin_rows", "basket_rows")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
