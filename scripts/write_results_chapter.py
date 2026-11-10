"""Buduje rozdział wyników wyłącznie z zapisanych, zweryfikowanych obliczeń."""

import hashlib
import json
from decimal import Decimal as D

from analyze_trades import ROOT, read_csv
from write_drawdown_section import section as drawdown_section
from redakcja_raportu import redaguj


def number(value, multiplier=1, digits=2):
    if value == "":
        return "—"
    text = f"{D(value) * multiplier:.{digits}f}"
    if D(text) == 0:
        text = text.lstrip("-")
    return text.replace(".", ",")


def pct(value):
    return number(value, 100) + "%" if value != "" else "—"


def percentage(value):
    return number(value) + "%" if value != "" else "—"


def fraction(row, key, denominator="completed_trades"):
    return f"{row[key + '_count']}/{row[denominator]} ({percentage(row[key + '_pct'])})"


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
                     + ["| " + " | ".join(str(value) for value in row) + " |" for row in rows])


def figure(filename, description):
    path = ROOT / "raport/wykresy" / (filename + ".png")
    assert path.exists(), "Generate figures before writing the report: " + str(path)
    return f"![{description}](<wykresy/{filename}.png>)"


def main():
    validation = json.loads((ROOT / "reports/trade_output_validation.json").read_text(encoding="utf-8"))
    assert validation["status"] == "passed"
    for relative, digest in validation["analysis_csv_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, "Results changed after validation: " + relative
    report = json.loads((ROOT / "reports/backtest_90d.json").read_text(encoding="utf-8"))
    rules = read_csv("data/analysis/summary_by_rule_90d.csv")
    coins = read_csv("data/analysis/summary_by_coin_rule_90d.csv")
    periods = read_csv("data/analysis/summary_by_period_90d.csv")
    pairs = read_csv("data/analysis/paired_rule_summary_90d.csv")
    costs = read_csv("data/analysis/cost_sensitivity_summary_90d.csv")
    event_rules = read_csv("data/analysis/summary_event_means_90d.csv")
    event_periods = read_csv("data/analysis/summary_event_means_by_period_90d.csv")
    event_means = read_csv("data/analysis/event_mean_returns_90d.csv")
    plans = read_csv("data/analysis/entry_plans.csv")
    trades = read_csv("data/analysis/trades_90d.csv")
    events = read_csv("data/processed/signal_events.csv")
    n_events = len(events)
    groups = len({row["potential_overlap_group_90d"] for row in events})
    no_entry_events = sum(row["status"] == "no_entry" for row in plans)
    status_table = table(["Reguła wejścia", "Sygnały", "Kompletne pary altcoin–BTC", "Brak wejścia: pary", "Inne niepełne pary"],
                         [[r["entry_rule"], r["qualified_events"], r["completed_trades"], r["no_entry_rows"], r["other_incomplete_rows"]] for r in rules])
    returns_table = table(["Wejście", "Średni zwrot netto altcoinów", "Mediana zwrotów netto altcoinów", "Średni zwrot netto BTC", "Mediana zwrotów netto BTC", "Mediana różnicy altcoin − BTC (p.p.)"],
                          [[r["entry_rule"], pct(r["mean_alt_net_return"]), pct(r["median_alt_net_return"]), pct(r["mean_btc_net_return"]),
                            pct(r["median_btc_net_return"]), number(r["median_advantage_net_pp"])] for r in rules])
    successes_table = table(["Wejście", "Zysk po kosztach", "Wynik wyższy od BTC", "Zysk i przewaga jednocześnie"],
                           [[r["entry_rule"], fraction(r, "success_profit"), fraction(r, "success_btc"), fraction(r, "success_both")] for r in rules])
    basket_table = table(["Wejście", "Mediana średniej pięciu monet netto", "Mediana dopasowanego BTC netto", "Zysk", "Przewaga nad BTC", "Zysk i przewaga"],
                        [[r["entry_rule"], pct(r["median_event_mean_alt_net_return"]), pct(r["median_event_mean_btc_net_return"]),
                          fraction(r, "success_profit", "completed_events"), fraction(r, "success_btc", "completed_events"),
                          fraction(r, "success_both", "completed_events")] for r in event_rules])
    risk_table = table(["Wejście", "Mediana MAE altcoinów", "Mediana MAE BTC", "Mediana MDD altcoinów z cen zamknięcia", "Mediana MDD BTC z cen zamknięcia"],
                       [[r["entry_rule"], pct(r["median_alt_mae"]), pct(r["median_btc_mae"]), pct(r["median_alt_mdd_close"]), pct(r["median_btc_mdd_close"])] for r in rules])
    pair_table = table(["Zmiana reguły", "Pary / sygnały", "Średnia zmiana wyniku netto (p.p.)", "Mediana zmiany (p.p.)", "Dodatnia zmiana", "Mediana przesunięcia wejścia (dni)"],
                       [[r["comparison"].replace("_minus_", " − "), f"{r['paired_rows']} / {r['events']}", number(r["mean_net_delta_pp"]),
                         number(r["median_net_delta_pp"]), percentage(r["positive_delta_pct"]), number(r["median_entry_shift_days"], digits=1)] for r in pairs])
    coin_sections = []
    for rule in ("A", "B", "C"):
        coin_table = table(["Moneta", "Liczba zdarzeń", "Średnia netto", "Mediana netto", "Zysk", "Przewaga nad BTC", "Mediana różnicy wobec BTC (p.p.)"],
                           [[r["symbol"], r["completed_trades"], pct(r["mean_alt_net_return"]), pct(r["median_alt_net_return"]),
                             fraction(r, "success_profit"), fraction(r, "success_btc"), number(r["median_advantage_net_pp"])] for r in coins if r["entry_rule"] == rule])
        coin_sections.append(f"### Reguła {rule}\n\n{coin_table}")
    period_table = table(["Okres sygnałów", "Wejście", "Sygnały / pary", "Średni zwrot netto altcoinów", "Mediana zwrotów netto altcoinów", "Przewaga pojedynczej monety nad BTC"],
                         [[r["signal_period"], r["entry_rule"], f"{r['completed_events']} / {r['completed_trades']}", pct(r["mean_alt_net_return"]),
                           pct(r["median_alt_net_return"]), fraction(r, "success_btc")] for r in periods])
    event_period_table = table(["Okres sygnałów", "Wejście", "Mediana średniej pięciu monet netto", "Przewaga średniej pięciu monet nad BTC"],
                               [[r["signal_period"], r["entry_rule"], pct(r["median_event_mean_alt_net_return"]),
                                 fraction(r, "success_btc", "completed_events")] for r in event_periods])
    names = {"base": "Podstawowy: 0,05%", "fees_without_slippage": "Bez poślizgu: 0%", "higher_slippage": "Wyższy poślizg: 0,20%"}
    cost_table = table(["Poślizg po każdej stronie", "Wejście", "Średni zwrot netto altcoinów", "Mediana zwrotów netto altcoinów", "Zysk", "Przewaga nad BTC"],
                       [[names[r["scenario"]], r["entry_rule"], pct(r["mean_alt_net_return"]), pct(r["median_alt_net_return"]),
                         fraction(r, "success_profit"), fraction(r, "success_btc")] for r in costs])
    mean_index = {(r["event_id"], r["entry_rule"]): r for r in event_means}
    event_table = table(["Data sygnału UTC", "Monety", "Średnia netto A", "Średnia netto B", "Średnia netto C"],
                        [[event["signal_date_utc"], mean_index[(event["event_id"], "A")]["symbols"].replace("|", ", "),
                          *[pct(mean_index[(event["event_id"], rule)]["event_mean_alt_net_return"]) for rule in ("A", "B", "C")]] for event in events])
    crossing_ids = sorted({row["event_id"] for row in trades if row["signal_period"] == "2020-2022" and row["outcome_known_before_2023"] == "False"})
    crossing_dates = [next(row["signal_date_utc"] for row in events if row["event_id"] == key) for key in crossing_ids]
    coin_text = "\n\n".join(coin_sections)
    chapter = f"""# Wyniki analizy 90-dniowej

## Zakres wykonanych obliczeń

Przeanalizowano {n_events} sygnałów z lat 2020–2025 oraz pięć historycznie dobranych altcoinów dla każdego sygnału. Daje to 100 par zdarzenie–moneta i {report['candidate_rows']} porównań po uwzględnieniu trzech reguł wejścia. Każda transakcja ma dopasowany wynik BTC z tej samej giełdy i tych samych dat. Okres utrzymywania wynosi 90 dni od rzeczywistego wejścia.

A oznacza wejście na otwarciu D+1, B na otwarciu D+7 od daty sygnału, a C wejście następnego dnia po pierwszym powrocie RSI do co najmniej 30 w dozwolonym oknie. Podstawowe koszty wynoszą 0,10% prowizji i 0,05% niekorzystnego poślizgu po każdej stronie. Wszystkie stopy zwrotu wyrażono w USDT.

{status_table}

W regule C wymagany powrót RSI wystąpił dla wszystkich {n_events} sygnałów; liczba przypadków bez wejścia w zestawie planów wyniosła {no_entry_events}. Nie odrzucono żadnej pary z powodu niepełnych danych. Wspólna próba porównania A/B/C obejmuje zatem wszystkie 100 par zdarzenie–moneta. Trzysta wierszy nie oznacza trzystu niezależnych prób: pochodzą z {n_events} sygnałów, a potencjalne nakładające się okna tworzą {groups} konserwatywnych grup.

## Zysk a przewaga nad BTC

{returns_table}

{successes_table}

{figure('01_stopy_zwrotu', 'Średnia i mediana 90-dniowego wyniku netto pojedynczych altcoinów oraz dopasowanego BTC dla reguł A, B i C.')}

**Wykres 1. Średnia i mediana wyniku netto pojedynczych pozycji.** Każda reguła obejmuje 100 par altcoin–BTC z 20 wspólnych sygnałów. D oznacza datę świecy sygnałowej; C oznacza zakup na następnym otwarciu po powrocie RSI do co najmniej 30. BTC jest dopasowany według giełdy i dat. Brak przedziałów ufności: przedstawiono opis próby, a nie niezależnie losowane transakcje.

We wszystkich regułach średnia i mediana wyniku altcoinów były dodatnie, a transakcje z zyskiem były częstsze niż transakcje ze stratą. Jednocześnie średni wynik BTC był wyższy, mediany dopasowanych różnic altcoin–BTC były ujemne, a przewagę nad BTC uzyskało tylko 34–37 ze 100 par w danej regule. Dodatnia stopa zwrotu altcoina nie oznaczała więc zwykle lepszego wyboru niż BTC.

Średnie różnice wyników altcoinów wobec BTC wyniosły odpowiednio {number(rules[0]['mean_advantage_net_pp'])}, {number(rules[1]['mean_advantage_net_pp'])} i {number(rules[2]['mean_advantage_net_pp'])} p.p. dla A, B i C. Medianę różnic obliczono z indywidualnych dopasowanych par; nie jest ona różnicą dwóch osobno wyznaczonych median. Wyniki zagregowane opisują tę próbę historyczną, bez testu istotności i bez twierdzenia o przewadze w przyszłości.

## Średni wynik pięciu monet w jednym zdarzeniu

Uzupełniająco policzono średnią arytmetyczną pięciu stóp zwrotu w każdym zdarzeniu. Taka średnia odpowiada osobnemu hipotetycznemu budżetowi dla sygnału, podzielonemu przy zakupie po 20% między monety, łącznie z kosztami wejścia, bez przywracania wag podczas utrzymywania. To dodatkowe zestawienie opisowe wprowadzone podczas opracowywania wyników; podstawowy protokół ocenia monety oddzielnie. Nie wybrano wag na podstawie zysków.

Porównaniem jest średnia pięciu dopasowanych wyników BTC z tymi samymi wagami. W zdarzeniach z BSV lub TON część tego porównania pochodzi z KuCoin, a reszta z Binance. Nie jest to wtedy jeden kurs BTC z jednej giełdy. Nie łączymy budżetów różnych sygnałów i nie wyliczamy skumulowanego zysku portfela z nakładających się inwestycji.

{basket_table}

{figure('02_zysk_i_przewaga_koszykow', 'Częstość zysku, przewagi nad BTC oraz ich jednoczesnego wystąpienia w 20 koszykach pięciu monet, dla każdej reguły wejścia.')}

**Wykres 2. Zysk i przewaga średniej pięciu monet.** Mianownik wynosi 20 zdarzeń w każdej regule. Początkowy budżet podzielono po 20% na monetę; dopasowany BTC zachowuje te same wagi giełd. Zestawienie opisowe dodano po wynikach indywidualnych. Przedstawione trzy kryteria mogą się nakładać i nie sumują się do 100%.

Mediana średniej pięciu monet wyniosła od 0,68% do 1,76%, a częstość zysku 50–55%. Koszyk o takich równych udziałach pokonał dopasowany BTC w 4–5 z {n_events} zdarzeń. Zysk i przewaga wystąpiły razem w trzech zdarzeniach dla każdej reguły. To inne jednostki podsumowania niż pojedyncze monety, dlatego odsetków z obu tabel nie należy zamieniać miejscami.

## Ryzyko w czasie utrzymywania

{risk_table}

{figure('04_ryzyko_pozycji', 'Mediany największego spadku od wejścia i obsunięcia od szczytu ścieżki zamknięć, oddzielnie dla pojedynczych altcoinów i dopasowanego BTC.')}

**Wykres 3. Mediany cenowych miar ryzyka pojedynczych pozycji.** Wartości bardziej ujemne oznaczają głębszy spadek. MAE wykorzystuje minima dzienne względem wejścia, a MDD ścieżkę zamknięć względem wcześniejszego szczytu. Obie miary zawierają punkty wejścia i wyjścia, pomijają koszty i nie są miarami ryzyka całego koszyka.

We wszystkich trzech regułach mediany obu miar spadku były bardziej ujemne dla altcoinów niż dla ich BTC. Dla A mediana największego spadku od wejścia wyniosła −21,26% dla altcoinów i −18,19% dla BTC. Mediana obsunięcia od wcześniejszego szczytu ścieżki zamknięć wyniosła odpowiednio −32,97% i −20,93%.

MAE opisuje spadek względem ceny wejścia, a MDD względem wcześniejszego maksimum. Są to miary cenowe pojedynczych pozycji, bez kosztów. Nie są ryzykiem koszyka pięciu monet: średnia indywidualnych dołków nie odtwarza wspólnej ścieżki wartości inwestycji. Dzienne zamknięcia nie obejmują całej zmienności śróddziennej.

## Porównanie reguł wejścia na wspólnej próbie

{pair_table}

W tabeli B − A oznacza wynik B pomniejszony o wynik A dla tej samej monety i tego samego sygnału. Reguła B dawała wyższy wynik niż A w 31% par, a reguła C wyższy niż A w 33%. Najwyższą średnią pojedynczych wyników uzyskano w regule A, a najwyższy odsetek przewag nad BTC w regule B. Reguła B zapewniła również najwyższą medianę wyników koszyków pięciu monet. Wskazanie reguły zależy zatem także od wybranej miary.

Oczekiwanie na wejście przesuwało również wyjście, ponieważ każda inwestycja trwała 90 dni od własnej daty zakupu. Ujemna mediana przesunięcia C względem B oznacza, że C wchodziło zwykle wcześniej od B. Różnice nie izolują wpływu samej ceny zakupu. Nie wybrano na podstawie tych wyników uniwersalnie najlepszej reguły ani nie dopasowywano progu RSI.

## Wyniki według monet

Poniższe tabele obejmują każdą monetę, która zakwalifikowała się do historycznego top 5. Liczebność zależy od udziału w rankingach konkretnych zdarzeń, a nie od późniejszego wyniku.

{coin_text}

ETH i XRP występowały w każdym z 20 zdarzeń, SOL w 14, a BCH, BSV i LTC tylko raz. Wynik TRX opiera się na dwóch zdarzeniach, TON na trzech. Odsetek 100% dla TRX nie stanowi mocnego dowodu powtarzalnej przewagi. Mediany różnych monet dotyczą częściowo innych sygnałów, więc nie tworzą porównania na identycznej próbie ani rankingu najlepszych inwestycji.

## Stabilność między okresami

{period_table}

{event_period_table}

{figure('03_przewaga_w_kazdym_zdarzeniu', 'Mapa różnic netto koszyka pięciu monet wobec dopasowanego BTC: wszystkie 20 sygnałów i trzy reguły wejścia, w punktach procentowych.')}

**Wykres 4. Różnica wyników dla każdego sygnału.** Każda komórka oznacza średnią netto pięciu monet minus średnią dopasowanego BTC, w punktach procentowych. Skala barw jest symetryczna wokół zera: niebieski oznacza przewagę koszyka, pomarańczowy przewagę BTC. Linia rozdziela opisowe bloki dat sygnałów. Wiersze są kategoriami zdarzeń; odstępy na wykresie nie przedstawiają upływu czasu ani ścieżki jednego portfela.

W późniejszym okresie średni wynik pojedynczych altcoinów był ujemny we wszystkich trzech regułach, a przewaga nad BTC wystąpiła w 8 z 40 par, czyli 20%. Średnia pięciu monet nie pokonała dopasowanego BTC w żadnym z ośmiu późniejszych zdarzeń. Obserwacja ta ogranicza argument za trwałością przewagi altcoinów w tej próbie.

Podział dotyczy dat sygnałów i ma charakter opisowy. Nie jest testem poza próbą wybranej wcześniej reguły. Sygnał z {', '.join(crossing_dates)} miał wyniki 90-dniowe poznane już po 2023-01-01: łącznie {report['earlier_signal_rows_crossing_2023']} wierszy monet i reguł. Gdyby wcześniejszy okres miał służyć wyborowi reguły przed tą datą, tych wyników nie wolno użyć. W opisowym zestawieniu zachowano wszystkie zdarzenia i nie wybierano reguły do wdrożenia.

## Wrażliwość na modelowane koszty

We wszystkich scenariuszach prowizja wynosi 0,10% po każdej stronie. Zmieniono jedynie niekorzystny poślizg zgodnie z wariantami zapisanymi przed oceną pełnych wyników.

{cost_table}

Wyższe koszty zmniejszają stopy zwrotu i mogą zmienić ocenę zysku. Przy zastosowaniu identycznego dodatniego mnożnika kosztów do altcoina i BTC kolejność ich wyników pozostaje jednak taka sama. Niezmienny odsetek przewag w tabeli wynika z konstrukcji modelu; nie dowodzi odporności na rzeczywiste różnice płynności i prowizji między aktywami. Wynik reguły C, którego średnia netto w scenariuszu podstawowym wynosi tylko 0,25%, wymaga szczególnej ostrożności wobec kosztów.

{drawdown_section()}

## Odpowiedź na pytania badawcze i ograniczenia

Zakup wybranych altcoinów przynosił w tej próbie dodatnie pojedyncze wyniki w 55–62% przypadków zależnie od reguły. Przy równych udziałach pięciu monet częstość dodatniego wyniku zdarzenia wynosiła 50–55%. Nie oznaczało to zwykle przewagi nad zakupem BTC: większość dopasowanych porównań przegrywała z BTC, a średnie i mediany różnic były ujemne.

Termin wejścia zmieniał wyniki, lecz żadna reguła nie dała jednocześnie przewagi altcoinów nad BTC w większości przypadków oraz niższych median badanych miar spadku. Wyniki stanowią opis warunkowej symulacji historycznej. Nie potwierdzają ogólnej skuteczności zakupu altcoinów po wyprzedaniu BTC ani gwarantowanego momentu wejścia.

Siłę wniosków ogranicza {n_events} sygnałów, ich koncentracja w części lat, współzależność monet i nakładanie się okresów. Rankingi poprzedzają sygnały o 1–5 dni, a ich historyczne godziny publikacji pozostają niepotwierdzone. Dostępność rankingu w chwili decyzji jest założeniem. Ceny otwarcia i koszty są modelem wykonania bez rekonstrukcji arkusza zleceń, wielkości zlecenia, zaokrągleń giełdowych i przepływów kapitału między zdarzeniami. Wyniki w USDT nie są wynikami w USD. Te ograniczenia dotyczą również dodatnich wyników.

## Kontrola i możliwość odtworzenia

Sprawdzono sumy SHA-256 {report['source_file_count_verified']} użytych plików źródłowych cen oraz zgodność cen z oryginalnymi rekordami. Pełna tabela odtworzyła wcześniej sprawdzony przypadek kontrolny ETH–BTC. Sześć testów objęło między innymi daty wejścia, brak powrotu RSI, koszty, rozróżnienie MAE/MDD i zachowanie wszystkich pięciu udziałów.

Niezależna kontrola pandas odtworzyła przepływy dla hipotetycznego wydatku 1 000 USDT, daty, miary ryzyka, mianowniki odsetków i średnie zdarzeń. Największa różnica stopy netto między obliczeniami wyniosła mniej niż 0,000000000001; nie wpływa na prezentowane zaokrąglenia. Raporty kontroli nie usuwają ograniczeń jakości historycznego źródła ani założeń wykonania.

Pełne dane: data/analysis/trades_90d.csv; średnie zdarzeń: data/analysis/event_mean_returns_90d.csv; scenariusze kosztów: data/analysis/cost_scenarios_90d.csv. Raporty: reports/backtest_90d.json, reports/event_aggregation_90d.json i reports/trade_output_validation.json. Obliczenia: scripts/analyze_trades.py, scripts/aggregate_event_results.py oraz scripts/validate_trade_outputs.py. Tabele zaokrąglono dopiero przy prezentacji.

## Zestawienie wszystkich sygnałów

Poniższe wartości przedstawiają średnią pięciu stóp zwrotu netto dla danego sygnału i reguły wejścia. Nie sumujemy tych wartości i nie traktujemy ich jako ścieżki jednego portfela. Właściwy skład pochodzi z rankingu przypisanego osobno do każdego zdarzenia.

{event_table}
"""
    chapter = redaguj(chapter)
    (ROOT / "raport/06_wyniki.md").write_text(chapter, encoding="utf-8")
    print(json.dumps({"results_chapter": "raport/06_wyniki.md", "words": len(chapter.split()), "tables": 13,
                      "events": n_events, "trade_rows": len(trades)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
