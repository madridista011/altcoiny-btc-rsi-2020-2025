# Słownik tabel zdarzeń i cen

## signal_events.csv — jeden wiersz na sygnał BTC

| Kolumna | Znaczenie |
| --- | --- |
| event_id | Stały identyfikator zdarzenia, zawierający datę sygnału. |
| signal_date_utc | Dzień świecy, której zamknięcie potwierdziło sygnał. |
| signal_confirmed_at_utc | Granica kolejnej doby UTC; najwcześniejszy moment znajomości pełnej świecy sygnału. |
| previous_rsi, signal_rsi | RSI poprzedniego dnia i dnia sygnału; wartości bez zaokrąglenia. |
| ranking_snapshot_date | Faktyczna data użytego historycznego rankingu. |
| ranking_age_days | Liczba dni od rankingu do dnia sygnału. |
| ranking_availability_status | Znacznik wcześniejszej daty i braku dowodu historycznej godziny publikacji. |
| earliest_entry_date_rule_A | Dzień następnej świecy po sygnale. Nie jest dowodem wykonania transakcji. |
| potential_overlap_group_90d | Konserwatywna grupa potencjalnie nakładających się okien. |
| potential_observation_end_90d | D+121, górny koniec okna przy maksymalnym oczekiwaniu i 90 dniach utrzymywania. |

btc_rsi_daily.csv zawiera dodatkowo dzienne zamknięcie BTC w USDT, RSI, flagę przejścia poniżej 30, flagę przynależności do okresu badania i pochodzenie ceny. Puste pierwsze 14 wartości RSI wynikają z inicjalizacji.

## event_universe.csv — jeden wiersz na wybraną monetę w zdarzeniu

Daty i identyfikator mają znaczenie jak wyżej. eligible_position to miejsce 1–5 po wykluczeniach, source_rank — oryginalne miejsce w globalnym rankingu. asset_id jest własnym stabilnym identyfikatorem. symbol_at_event to symbol historyczny, a source_slug i source_symbol_as_returned zachowują nazewnictwo dostawcy przy pobraniu. source_market_cap_usd jest kapitalizacją źródłową w USD i nie jest ceną wejścia ani walutą stopy zwrotu. ranking_source_file wskazuje zachowany JSON. basket_locked_across_entry_rules oznacza wspólny dobór dla wariantów wejścia.

event_baskets.csv jest skróconą tabelą do czytania: jeden wiersz na zdarzenie, lista pięciu symboli w kolumnie basket. eligibility_audit.csv dokumentuje każdą sprawdzoną pozycję do uzyskania piątej monety, łącznie z odrzuconymi BTC i stablecoinami.

asset_requirements.csv podaje liczbę zdarzeń dla monety, potrzebne granice cen, giełdę i walutę. To plan pokrycia danych; liczba zdarzeń nie oznacza niezależnych transakcji.

## market_prices_daily.csv — jedna świeca aktywa na danej giełdzie

Klucz to (asset_id, venue, date_utc). venue to binance albo kucoin. source_symbol zachowuje rzeczywistą parę API, również GRAM-USDT dla historycznego TON. quote_currency to zawsze USDT. open/high/low/close oznaczają ceny pierwszą/najwyższą/najniższą/ostatnią, w USDT za jednostkę aktywa. volume_base jest wolumenem aktywa, volume_quote wolumenem USDT. Puste trade_count dla KuCoin oznacza brak tego pola w źródle, nie zero transakcji.

known_partial_day, known_non_midnight_open i known_early_trading_stop oznaczają udokumentowane ograniczenia sesji; brak flagi nie dowodzi braku wszystkich przerw. source_file i source_row pozwalają odnaleźć źródłową świecę. Pozycja source_row jest liczona od 1 w oryginalnej tablicy, także gdy API zwracało dni od najnowszego.

price_coverage.csv dokumentuje obecność wszystkich potencjalnie potrzebnych dni altcoina i jego BTC na tej samej giełdzie. coverage_complete nie oznacza zakończenia analizy transakcji ani potwierdzonej możliwości realizacji bez kosztów.

## data/analysis/trades_90d.csv — wynik monety, zdarzenia i reguły

Klucz: event_id, asset_id, entry_rule. W obecnym zbiorze 300 wierszy, po 100 na regułę. Daty są w UTC; entry_date i exit_date to rzeczywiste daty danej reguły, holding_days wynosi 90. waiting_days_after_signal_confirmation liczy pełne dni oczekiwania od granicy D/D+1; w A to 0, w B 6. recovery_date występuje dla C. signal_period grupuje według daty sygnału, a outcome_known_before_2023 według daty wyjścia, nie sygnału.

status = completed pozwala obliczyć wynik; no_entry oznacza brak wymaganego powrotu RSI, a inne statusy opisują problem obserwacji lub wykonania. Puste wyniki nie są zerami. common_sample_three_rules oznacza kompletność wszystkich trzech reguł dla tej samej pary zdarzenie–moneta.

Prefiksy alt_ i btc_ oznaczają monetę oraz dopasowane BTC. entry_open i exit_open to referencyjne ceny przed kosztami. gross_return i net_return są ułamkami: 0.05 to 5%. advantage_net_pp jest już w punktach procentowych: 5 oznacza 5 p.p. relative_net_return jest ułamkiem względnej zmiany wartości. mae i mdd_close są oddzielnymi ujemnymi lub zerowymi miarami cenowymi, bez kosztów. success_profit, success_btc i success_both są flagami trzech kryteriów wyniku, odrębnymi od liter reguł wejścia. Pola source i source_row wskazują źródłowe punkty wejścia i wyjścia.

## Zestawienia wyników pojedynczych monet

summary_by_rule_90d.csv, summary_by_coin_rule_90d.csv, summary_by_period_90d.csv i summary_by_event_rule_90d.csv używają tej samej definicji. candidate_rows obejmuje także braki; completed_trades jest mianownikiem odsetków sukcesu. qualified_events i completed_events liczą różne zdarzenia, a nie monety. mean_* i median_* odnoszą się do kompletnych par. Sukcesy są liczone ze ścisłym >, bez zaliczania remisów. Mediana advantage_net_pp jest medianą dopasowanych różnic, nie różnicą median.

summary_common_sample_90d.csv ogranicza zestawienie do par z kompletnymi A/B/C. paired_rule_comparisons_90d.csv i paired_rule_summary_90d.csv liczą różnicę prawej względem lewej reguły w oznaczeniu right_minus_left. net_return_delta_pp i mae_delta_pp są w p.p.; entry_shift_days wskazuje również przesunięcie wyjścia. Wartość dodatnia mae_delta_pp oznacza mniej ujemne MAE. cost_scenarios_90d.csv zawiera te same kandydatury w trzech scenariuszach; nie są to dodatkowe niezależne transakcje.

## Średnie pięciu monet

event_mean_returns_90d.csv zawiera 60 wierszy: 20 zdarzeń × 3 reguły. event_mean_alt_net_return i event_mean_btc_net_return to średnie pięciu dopasowanych stóp. Status completed wymaga kompletu pięciu monet; nie zmniejsza się mianownika do liczby dostępnych składników. btc_venue_weights pokazuje udział każdej giełdy w dopasowanym porównaniu BTC. To opisowe równe początkowe udziały po 20%, bez łączenia kapitału między zdarzeniami.

summary_event_means_90d.csv i summary_event_means_by_period_90d.csv mają mianownik completed_events, czyli 20 w całym okresie dla każdej reguły. median_event_mean_alt_net_return oznacza medianę 20 średnich pięciu monet, a nie medianę 100 pojedynczych wyników. Uzupełnienie dodano na etapie raportowania po wynikach indywidualnych. Nie zawiera ryzyka koszyka obliczonego ze średniej indywidualnych MAE lub MDD.
