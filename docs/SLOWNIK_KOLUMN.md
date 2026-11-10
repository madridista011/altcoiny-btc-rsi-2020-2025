# Słownik tabeli `prices_daily.csv`

Jeden wiersz oznacza jedną źródłową świecę dzienną jednego aktywa na Binance Spot. Ceny są zapisane z precyzją zwróconą przez dostawcę. Tabela jest przygotowana do dalszej kontroli i obliczeń; nie zawiera sygnałów ani transakcji.

| Kolumna | Znaczenie i jednostka |
| --- | --- |
| `date_utc` | Data świecy według kalendarza UTC, `RRRR-MM-DD`. |
| `asset_id` | Własny, stabilny identyfikator projektu. `eos_vaulta` obejmuje EOS i jego następcę A po wymianie 1:1. |
| `cache_group` | Historia pobrania cen: `benchmark` — BTC, `initial_download` — pierwsze pobranie, `requested_download` — później pobrane SOL. Ta kolumna nie oznacza przynależności do historycznego top 5 w żadnym zdarzeniu. |
| `source_symbol` | Para u dostawcy: BTCUSDT, ETHUSDT, XRPUSDT, BCHUSDT, LTCUSDT, EOSUSDT, AUSDT lub SOLUSDT. |
| `venue` | Giełda cen w tej tabeli pomocniczej: binance. Łączona tabela market_prices_daily.csv zawiera również kucoin. |
| `quote_currency` | Waluta wyceny: USDT. Nie dokonano konwersji na USD. |
| `source_open_time_utc` | Początek przedziału świecy zapisany przez źródło; ISO 8601, UTC. Nie musi być czasem pierwszej transakcji. |
| `source_close_time_utc` | Koniec przedziału świecy według źródła; ISO 8601, UTC. Ostatnia świeca EOS kończy się wcześniej niż pełna doba. |
| `open` | Cena pierwszej transakcji w świecy; USDT za jednostkę aktywa. |
| `high` | Najwyższa cena transakcji w świecy; USDT za jednostkę aktywa. |
| `low` | Najniższa cena transakcji w świecy; USDT za jednostkę aktywa. |
| `close` | Cena ostatniej transakcji w świecy; USDT za jednostkę aktywa. |
| `volume_base` | Suma wolumenu w jednostkach aktywa, np. BTC. |
| `volume_quote` | Suma wolumenu w USDT. |
| `trade_count` | Liczba transakcji giełdowych w świecy; to nie jest liczba transakcji badanej strategii. |
| `data_phase` | `warmup`: historia BTC przed 2020 r.; `study`: 2020–2025; `followup`: dane po 2025 r. potrzebne do obserwacji późniejszych wyjść. |
| `known_partial_day` | `True`, gdy udokumentowano niepełny dzień handlu podczas migracji albo pierwszego notowania pary. |
| `known_non_midnight_open` | `True` dla A w 2025-05-28 (otwarcie 08:00 UTC) i SOL w 2020-08-11 (06:00 UTC): `open` nie jest ceną dostępną o północy. |
| `known_early_trading_stop` | `True` dla EOS w 2025-05-26: ostatnie notowanie do 03:00 UTC, a nie koniec pełnej doby. |
| `source_file` | Względna ścieżka do niezmienianego JSON źródłowego. |
| `source_row` | Pozycja świecy w tablicy danych w danym JSON, liczona od 1; nie numer linii tekstu pliku. |

`False` w flagach znanych niepełnych sesji oznacza brak takiego oznaczenia w naszej dokumentacji. Nie dowodzi braku wszelkich krótkich przerw giełdowych.

Na dzień 2025-05-27 nie utworzono wiersza EOS/Vaulta. Ten brak jest w oddzielnej tabeli `missing_days.csv`. Nie zastąpiono go zerem, poprzednią ceną ani interpolacją.

`inventory.csv`: `rows` to liczba świec, `study_rows` liczba świec z lat 2020–2025, `missing_days` liczba brakujących dni w oczekiwanym kalendarzu, `known_partial_days` liczba udokumentowanych niepełnych dni. `first_date` i `last_date` określają faktyczny zakres aktywa.

W tabeli inwentarza `calendar_start` oznacza początek oczekiwanego kalendarza źródła dla danego aktywa. `pre_listing_days` oznacza dni od początku badania przed uruchomieniem wybranej pary (223 dla SOL/USDT); nie są one uznawane za nieudokumentowane luki źródła. Ich zakres znajduje się w `availability_exclusions` raportu jakości. Nie przypisuje się im cen ani zerowych stóp zwrotu.

Po doborze historycznych koszyków dodano również pary BNBUSDT, ADAUSDT, DOGEUSDT i TRXUSDT. Ich cache_group to ranking_selected_download — pochodzenie pobrania na podstawie wyznaczonych potrzeb danych, nie osobna kategoria wyników. Właściwy skład dla każdego zdarzenia znajduje się w event_universe.csv; słownik tego pliku i połączonych cen jest w SLOWNIK_ZDARZEN.md.
