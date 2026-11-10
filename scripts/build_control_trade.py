"""Pierwszy chronologiczny sygnał: kontrolne porównanie pierwszego altcoina z BTC."""

import csv
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 40


def load_csv(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    protocol_path = ROOT / "config/trade_protocol_v1.json"
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    universe = load_csv("data/processed/event_universe.csv")
    chosen = min(universe, key=lambda row: (row["signal_date_utc"], int(row["eligible_position"])))
    assert chosen["asset_id"] == "ethereum"
    signal = date.fromisoformat(chosen["signal_date_utc"])
    entry = signal + timedelta(days=1)
    exit_day = entry + timedelta(days=protocol["primary_holding_days"])
    prices = load_csv("data/processed/market_prices_daily.csv")
    source_hashes = json.loads((ROOT / "data/metadata/event_prices_raw_sha256.json").read_text(encoding="utf-8"))
    lookup = {(row["asset_id"], row["venue"], row["date_utc"]): row for row in prices}
    coverage = next(row for row in load_csv("data/processed/price_coverage.csv")
                    if row["event_id"] == chosen["event_id"] and row["asset_id"] == chosen["asset_id"])
    venue = coverage["price_venue"]
    assert venue == coverage["benchmark_venue"] == "binance"
    costs = {key: Decimal(str(value)) for key, value in protocol["base_costs"].items()}
    budget = Decimal("1000")
    results = []
    for asset_id, symbol in [(chosen["asset_id"], chosen["symbol_at_event"]), ("bitcoin", "BTC")]:
        buy = lookup[(asset_id, venue, entry.isoformat())]
        sell = lookup[(asset_id, venue, exit_day.isoformat())]
        for row in (buy, sell):
            assert row["quote_currency"] == "USDT"
            assert row["known_partial_day"] == "False"
            source_bytes = (ROOT / row["source_file"]).read_bytes()
            assert hashlib.sha256(source_bytes).hexdigest() == source_hashes[row["source_file"]]
            payload = json.loads(source_bytes)
            original = payload["result"][int(row["source_row"]) - 1]
            assert Decimal(original[1]) == Decimal(row["open"])
            assert datetime.fromtimestamp(original[0] / 1000, timezone.utc).date().isoformat() == row["date_utc"]
        p_in, p_out = Decimal(buy["open"]), Decimal(sell["open"])
        buy_execution = p_in * (1 + costs["adverse_buy_slippage"])
        sell_execution = p_out * (1 - costs["adverse_sell_slippage"])
        cost_per_unit = buy_execution * (1 + costs["buy_fee_rate"])
        proceeds_per_unit = sell_execution * (1 - costs["sell_fee_rate"])
        gross = p_out / p_in - 1
        net = proceeds_per_unit / cost_per_unit - 1
        units = budget / cost_per_unit
        final_cash = units * proceeds_per_unit
        assert abs((final_cash - budget) / budget - net) < Decimal("1e-35")
        assert net <= gross
        results.append({"event_id": chosen["event_id"], "symbol": symbol, "asset_id": asset_id, "venue": venue,
                        "signal_date": signal.isoformat(), "ranking_date": chosen["ranking_snapshot_date"],
                        "entry_rule": "A", "entry_date": entry.isoformat(), "exit_date": exit_day.isoformat(),
                        "holding_days": protocol["primary_holding_days"], "entry_reference_open_usdt": str(p_in),
                        "exit_reference_open_usdt": str(p_out), "gross_return": str(gross), "net_return": str(net),
                        "hypothetical_initial_usdt": str(budget), "hypothetical_final_usdt": str(final_cash),
                        "entry_source_file": buy["source_file"], "entry_source_row": buy["source_row"],
                        "exit_source_file": sell["source_file"], "exit_source_row": sell["source_row"]})
    alt, btc = results
    gross_adv = (Decimal(alt["gross_return"]) - Decimal(btc["gross_return"])) * 100
    net_adv = (Decimal(alt["net_return"]) - Decimal(btc["net_return"])) * 100
    output = ROOT / "data/processed/control_trade.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    def number(value, places=2):
        return f"{Decimal(value):.{places}f}".replace(".", ",")
    table = "\n".join(f"| {row['symbol']} | {number(row['entry_reference_open_usdt'])} | {number(row['exit_reference_open_usdt'])} | {number(Decimal(row['gross_return']) * 100)}% | {number(Decimal(row['net_return']) * 100)}% |" for row in results)
    report = f"""# Przykład kontrolny na rzeczywistych danych: ETH i BTC

## Zdarzenie i reguła

Pierwszy chronologiczny sygnał BTC w badaniu: **{signal.isoformat()}**. Ranking z **{chosen['ranking_snapshot_date']}** kwalifikował ETH do historycznego top 5. Wybrano pierwszą monetę pierwszego zdarzenia według kolejności danych, bez oceny jej późniejszego wyniku.

Reguła A: zakup na otwarciu **{entry.isoformat()}**, sprzedaż na otwarciu **{exit_day.isoformat()}**, po **{protocol['primary_holding_days']} dniach kalendarzowych**. Ceny referencyjne obu aktywów: Binance Spot, USDT. Protokół reguł zapisano w config/trade_protocol_v1.json przed tym obliczeniem.

## Wynik kontrolny

| Aktywo | Otwarcie przy wejściu, USDT | Otwarcie przy wyjściu, USDT | Stopa brutto | Stopa netto w scenariuszu |
| --- | ---: | ---: | ---: | ---: |
{table}

Różnica ETH minus BTC: **{number(gross_adv)} punktu procentowego brutto** i **{number(net_adv)} punktu procentowego netto**.

Różnice obliczamy przed zaokrągleniem prezentowanych stóp, dlatego mogą minimalnie różnić się od odejmowania wartości widocznych w tabeli.

## Dlaczego koszty są częścią projektu

Pytanie badawcze dotyczy wyniku po kosztach. Scenariusz przyjmuje prowizję 0,10% i niekorzystny poślizg 0,05% przy zakupie oraz przy sprzedaży. Są to parametry modelowe, a nie odtworzone historyczne opłaty i faktyczne ceny realizacji. Obliczenie netto uwzględnia całkowity wydatek przy wejściu i wpływ po kosztach przy wyjściu.

Dla hipotetycznego budżetu 1 000 USDT wynik końcowy w tym modelu to {number(alt['hypothetical_final_usdt'])} USDT dla ETH i {number(btc['hypothetical_final_usdt'])} USDT dla BTC. To symulacja na historycznych cenach, nie opis zrealizowanych zleceń.

## Interpretacja i granice

To jeden przykład sprawdzający powiązanie cen, dat, kosztów i benchmarku. Nie pozwala wnioskować o skuteczności strategii w całym okresie ani wybierać najlepszej reguły wejścia. Właściwa analiza musi objąć wszystkie zdarzenia, monety i ustalone reguły, w tym straty oraz przypadki bez wejścia.

Historyczna godzina publikacji rankingu pozostaje niepotwierdzona. Wykonanie zlecenia po modelowej cenie otwarcia i poślizgu jest założeniem. Nie modelowano zaokrągleń liczby monet, minimalnego zlecenia ani ograniczeń kapitału dla wielu pozycji.

Pochodzenie czterech cen i pełna precyzja obliczeń: data/processed/control_trade.csv. Sposób odtworzenia: python scripts/build_control_trade.py.
"""
    (ROOT / "raport/03_pierwsze_zdarzenie.md").write_text(report, encoding="utf-8")
    metadata = {"calculated_at_utc": datetime.now(timezone.utc).isoformat(), "selection_rule": "First chronological event, first eligible position",
                "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(), "protocol_file": "config/trade_protocol_v1.json",
                "gross_advantage_pp": str(gross_adv), "net_advantage_pp": str(net_adv),
                "checks": ["Same venue and dates", "90 calendar days", "Price cells match immutable source JSON", "Net cash-flow matches return formula"],
                "results": results, "scope": "One control example, not a completed strategy evaluation"}
    (ROOT / "reports/control_trade.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"entry": entry.isoformat(), "exit": exit_day.isoformat(), "results": [
        {"symbol": row["symbol"], "entry": row["entry_reference_open_usdt"], "exit": row["exit_reference_open_usdt"],
         "gross_pct": number(Decimal(row["gross_return"]) * 100), "net_pct": number(Decimal(row["net_return"]) * 100)} for row in results],
        "net_advantage_pp": number(net_adv)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
