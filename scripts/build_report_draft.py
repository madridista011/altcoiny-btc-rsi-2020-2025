"""Składa roboczy tekst pracy i opis danych na podstawie zapisanych materiałów."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from redakcja_raportu import redaguj

ROOT = Path(__file__).resolve().parents[1]


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def number(value):
    return f"{value:,}".replace(",", " ")


def main():
    config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
    events = read_csv("data/processed/signal_events.csv")
    universe = read_csv("data/processed/event_universe.csv")
    prices = read_csv("data/processed/market_prices_daily.csv")
    coverage = read_csv("data/processed/price_coverage.csv")
    manifest = json.loads((ROOT / "data/raw/rankings/cryptwatch/2026-11-08_events/manifest.json").read_text(encoding="utf-8"))
    counts = Counter(row["event_id"] for row in universe)
    assert set(counts) == {row["event_id"] for row in events}
    assert all(value == 5 for value in counts.values())
    assert all(row["coverage_complete"] == "True" for row in coverage)
    assert all(row["quote_currency"] == "USDT" for row in prices)
    for source in manifest:
        assert hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() == source["sha256"]
    symbols = sorted({row["symbol_at_event"] for row in universe})
    ages = [int(row["ranking_age_days"]) for row in events]
    chapter = f"""# Dane i źródła

## Źródła wykorzystane w badaniu

W badaniu połączono dwa rodzaje danych: dzienne notowania kryptowalut oraz historyczne rankingi kapitalizacji. Rankingi służyły do wyboru monet dla poszczególnych sygnałów, natomiast dane cenowe służą do wyznaczenia sygnałów BTC i obliczenia wyników inwestycji.

| Źródło | Zakres wykorzystania |
| --- | --- |
| Binance Spot | Dzienne ceny BTC oraz większości wybranych altcoinów, wyrażone w USDT. |
| KuCoin Spot | Historyczne ceny BSV i TON oraz ceny BTC potrzebne do porównań na tej samej giełdzie. |
| CryptWatch, na podstawie CoinMarketCap | Historyczne zestawienia kapitalizacji do wyboru pięciu kwalifikujących się altcoinów przed każdym sygnałem. |

Dane pobrano 8 listopada 2026 r. Ceny Binance pozyskano przez publiczny interfejs danych rynkowych, a ceny KuCoin przez publiczne API świec. Z archiwum CryptWatch pobrano {len(manifest)} zestawień potrzebnych do badanych zdarzeń. Oryginalne odpowiedzi, parametry zapytań i informacje o pobraniu zachowano w plikach projektu.

Opis dostępnych pól cenowych zawierają [dokumentacja Binance](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market) i [dokumentacja KuCoin](https://www.kucoin.com/docs-new/rest/spot-trading/market-data/get-klines). Pochodzenie rankingów oraz warunki dostępu opisuje [CryptWatch](https://cryptwat.ch/api). Wymagane oznaczenie źródła rankingów: Data: CryptWatch, based on CoinMarketCap. Szczegółowy rejestr źródeł i warunków wykorzystania znajduje się w dokumentacji projektu.

## Zakres czasowy i waluta danych

Badany okres obejmuje daty sygnałów od {config['study_start']} do {config['study_end']}. Do rozpoczęcia obliczeń RSI wykorzystano dodatkowo historię BTC od {config['btc_warmup_start']}. Zgromadzono również ceny po zakończeniu 2025 r., maksymalnie do {config['data_end']}, aby umożliwić obserwację późniejszych wyjść z pozycji. Dodatkowe daty nie rozszerzają okresu generowania sygnałów.

Zastosowano dzienny interwał i kalendarz UTC. Wszystkie ceny wykorzystywane do obliczania stóp zwrotu są wyrażone w USDT. Kapitalizacja w rankingach jest podana w USD i służy doborowi aktywów, a nie przeliczaniu wyników. Wynik w USDT nie jest utożsamiany z wynikiem w USD.

## Struktura przygotowanego zbioru

| Element zbioru | Liczba |
| --- | ---: |
| Sygnały BTC w latach 2020–2025 | {len(events)} |
| Historyczne rankingi wykorzystane do doboru | {len(manifest)} |
| Pary zdarzenie–moneta | {len(universe)} |
| Różne altcoiny wybrane przez regułę top 5 | {len(symbols)} |
| Dzienne świece w połączonej tabeli cen wybranych aktywów i BTC | {number(len(prices))} |

Wybrane w różnych zdarzeniach altcoiny to: {', '.join(symbols)}. Nie jest to stała lista obowiązująca przez całe badanie: każda moneta musiała zakwalifikować się na podstawie rankingu dla danego zdarzenia.

Jeden wiersz tabeli cen odpowiada dziennej świecy konkretnego aktywa na konkretnej giełdzie. Zawiera cenę otwarcia, najwyższą, najniższą i zamknięcia, wolumen oraz informacje pozwalające odnaleźć oryginalny rekord źródłowy. Osobne tabele opisują sygnały BTC, skład koszyków i uzasadnienia wykluczeń.

Liczba {len(universe)} oznacza wybory monet dla zdarzeń. Nie jest liczbą niezależnych prób ani liczbą zrealizowanych transakcji we wszystkich wariantach wejścia. Pięć monet wybranych dla tego samego sygnału jest powiązanych wspólnym zdarzeniem, a okresy obserwacji kolejnych sygnałów mogą się nakładać.

## Przygotowanie i kontrola jakości

Sprawdzono formaty i kolejność dat, duplikaty, kompletność potrzebnych kalendarzy, dodatniość cen i zgodność cen najwyższej oraz najniższej z cenami otwarcia i zamknięcia. Zweryfikowano również sposób obliczenia RSI i wpływ długości historii początkowej. Zachowano pliki źródłowe oraz sumy SHA-256, które pozwalają wykrywać późniejsze zmiany lokalnych plików.

Dla wszystkich {len(universe)} par zdarzenie–moneta dostępne są świece altcoina i BTC z tej samej giełdy w pełnych potencjalnych oknach obserwacji. Pokrycie sprawdzono dla okresu od pierwszego dnia po sygnale do 211. dnia po sygnale, uwzględniając przygotowanie danych do opóźnionych wejść i ewentualnego rozszerzenia horyzontu. W podstawowej analizie obowiązuje nadal 90 dni. Nie uzupełniano brakujących cen zerami, interpolacją ani przenoszeniem poprzednich notowań.

Ujednolicono identyfikatory monet i sprawdzono zmiany nazw. Przykładowo historyczny TON występuje w pobranych odpowiedziach pod późniejszą nazwą GRAM. Zachowano symbol źródłowy i osobno zapisano symbol właściwy dla daty badania. BSV i TON pozostały w koszykach mimo braku odpowiednich ówczesnych cen na Binance; ich dane uzupełniono z KuCoin.

## Ograniczenia danych

Najważniejsze ograniczenie dotyczy częstotliwości i dostępności rankingów. Część starszego archiwum zawiera zestawienia tygodniowe. Dla badanych sygnałów użyte rankingi są wcześniejsze o {min(ages)}–{max(ages)} dni. Odtworzony skład może zatem różnić się od rankingu dokładnie z dnia sygnału.

Źródło nie potwierdza historycznych godzin publikacji. Dostępność wcześniejszego zestawienia w chwili potwierdzenia sygnału jest jawnym założeniem, a nie zweryfikowanym faktem. Ograniczenie to należy zachować przy interpretacji wyników.

Drugim ograniczeniem są różnice między giełdami, w tym płynność i przebieg notowań. Wynik każdej monety porównano z wynikiem BTC z tej samej giełdy oraz z identycznych dat wejścia i wyjścia. Obecność dziennej świecy nie dowodzi jednak możliwości realizacji zlecenia o dokładnie wskazanej cenie i bez poślizgu.

Kontrole techniczne nie wykluczają wszystkich możliwych błędów dostawców ani późniejszych korekt ich baz. Przy udostępnianiu danych i raportu należy uwzględnić warunki każdego dostawcy zapisane w rejestrze źródeł.
"""
    chapter = redaguj(chapter)
    (ROOT / "raport/04_dane_i_zrodla.md").write_text(chapter, encoding="utf-8")
    intro = (ROOT / "raport/01_problem_i_cel.md").read_text(encoding="utf-8")
    title_part, body = intro.split("## Cel — wersja po redakcji wypowiedzi autora", 1)
    title = title_part.split("## Roboczy tytuł", 1)[1].strip().strip('„”.')
    body = "## Cel pracy" + body
    methodology = (ROOT / "raport/05_metodologia.md").read_text(encoding="utf-8")
    results = (ROOT / "raport/06_wyniki.md").read_text(encoding="utf-8")
    discussion = (ROOT / "raport/07_dyskusja_i_wnioski.md").read_text(encoding="utf-8")
    abstract = (ROOT / "raport/00_streszczenie.md").read_text(encoding="utf-8")
    reproduction = (ROOT / "raport/08_odtworzenie_i_zrodla.md").read_text(encoding="utf-8")
    consolidated = (f"# {title}\n\nStudium przypadku w ramach kursu Google Data Analytics. Autor: Mateusz Gromski.\n\n"
                    + abstract.strip() + "\n\n"
                    + "# 1. Problem, cel i zakres pracy\n\n" + body.strip()
                    + "\n\n" + chapter.replace("# Dane i źródła", "# 2. Dane i źródła", 1)
                    + "\n\n" + methodology.replace("# Metodologia analizy", "# 3. Metodologia analizy", 1)
                    + "\n\n" + results.replace("# Wyniki analizy 90-dniowej", "# 4. Wyniki analizy 90-dniowej", 1)
                    + "\n\n" + discussion.replace("# Dyskusja i wnioski", "# 5. Dyskusja i wnioski", 1)
                    + "\n\n" + reproduction.replace("# Odtworzenie analizy i źródła", "# 6. Odtworzenie analizy i źródła", 1)
                    + "\n---\n\nStatus: zredagowana wersja robocza analizy 90-dniowej obejmuje streszczenie, sześć rozdziałów i pięć wykresów, w tym uzupełnienie o obsunięcie kapitału koszyków. Horyzonty 30 i 180 dni pozostają niewykonanym rozszerzeniem.\n")
    consolidated = redaguj(consolidated)
    (ROOT / "raport/RAPORT.md").write_text(consolidated, encoding="utf-8")
    print(json.dumps({"main_report": "raport/RAPORT.md", "data_chapter": "raport/04_dane_i_zrodla.md",
                      "methodology_chapter": "raport/05_metodologia.md",
                      "results_chapter": "raport/06_wyniki.md",
                      "discussion_chapter": "raport/07_dyskusja_i_wnioski.md",
                      "abstract": "raport/00_streszczenie.md", "reproduction_chapter": "raport/08_odtworzenie_i_zrodla.md",
                      "events": len(events), "rankings": len(manifest), "event_asset_pairs": len(universe),
                      "altcoins": len(symbols), "price_rows": len(prices), "ranking_age_days": [min(ages), max(ages)]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
