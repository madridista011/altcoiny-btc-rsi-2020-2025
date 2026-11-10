# Dane projektu

| Warstwa | Zawartość |
| --- | --- |
| `raw/` | Zachowane odpowiedzi cenowe i rankingowe wykorzystane do przygotowania oraz kontroli analizy. |
| `metadata/` | Parametry pobrań, pochodzenie danych i sumy kontrolne. |
| `staging/` | Pomocniczy zasób cen Binance; jego skład nie oznacza składu koszyków. |
| `processed/` | Dzienne ceny, RSI, 20 sygnałów, 100 wyborów monet i kontrola pokrycia. |
| `analysis/` | 17 tabel wynikowych: transakcje, koszyki, porównania, koszty i ryzyko. |

Na początek warto otworzyć:

- [Skład koszyków dla każdego sygnału](processed/event_baskets.csv).
- [Podsumowanie wyników koszyków](analysis/summary_event_means_90d.csv).
- [Wszystkie 300 porównań monet](analysis/trades_90d.csv).
- [Obsunięcie kapitału koszyków](analysis/basket_capital_risk_90d.csv).

CSV: UTF-8 z BOM, przecinek jako separator pól, kropka dziesiętna. Stopy zwrotu są zapisane jako ułamki, np. `0.05 = 5%`. Pola z końcówką `_pp` są wyrażone w punktach procentowych. Definicje pól: [słownik zdarzeń](../docs/SLOWNIK_ZDARZEN.md), [słownik cen](../docs/SLOWNIK_KOLUMN.md) i [obsunięcie kapitału](../docs/OBSUNIECIE_KAPITALU.md).

Ceny: Binance Spot / Binance Vision oraz KuCoin. Rankingi: **Data: CryptWatch, based on CoinMarketCap**. Warunki wykorzystania i ograniczenia znajdują się w [rejestrze źródeł](../docs/ZRODLA_DANYCH.md).
