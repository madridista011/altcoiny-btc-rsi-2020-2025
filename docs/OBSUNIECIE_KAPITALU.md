# Maksymalne obsunięcie kapitału koszyków

Opisowe rozszerzenie analizy 90-dniowej, dodane po opracowaniu pierwotnych wyników. Nie zmienia sygnałów, doboru monet, dat transakcji ani kosztów. Wcześniejsze 14 tabel wynikowych zachowuje niezmienione sumy SHA-256.

Każdy sygnał i reguła mają osobny hipotetyczny budżet 1 000 USDT. Pięć równych początkowych wydatków po 200 USDT obejmuje koszty zakupu. Liczba jednostek pozostaje stała; nie ma rebalansowania. Benchmark BTC ma pięć równych części dopasowanych do giełd poszczególnych altcoinów. Nie jest zawsze inwestycją w BTC na jednej giełdzie.

Ścieżka obejmuje początkową gotówkę, wartość rynkową bezpośrednio po zakupie, 90 dziennych zamknięć UTC i końcową gotówkę po sprzedaży. Prowizja i poślizg dotyczą wejścia oraz wyjścia; dzienne wyceny nie odejmują hipotetycznych kosztów likwidacji. Każda ścieżka ma 93 obserwacje. Końcowa wartość jest zgodna z wcześniejszym zwrotem netto dla równych udziałów.

DD_t = V_t / max(V_0, …, V_t) − 1. MDD = min(DD_t). Wartości ujemne oznaczają spadek względem wcześniejszego maksimum; −25% oznacza utratę jednej czwartej wartości od szczytu. Definicja szczyt–dołek: [QuantConnect](https://www.quantconnect.com/docs/v2/cloud-platform/optimization/objectives). W tej pracy zastosowano ujemny znak obsunięcia.

## Pliki i kolumny

| Plik | Jednostka obserwacji i zawartość |
| --- | --- |
| basket_capital_path_90d.csv | 5 580 wierszy: zdarzenie, reguła i obserwacja ścieżki; observation_index określa kolejność również w tej samej dacie. |
| basket_capital_risk_90d.csv | 60 wierszy: zdarzenie i reguła; MDD, daty oraz etapy szczytu i dołka, ich kwoty i końcowy kapitał. |
| summary_basket_capital_risk_90d.csv | 3 wiersze: reguły A/B/C; mediana, średnia i najgłębsze MDD, sygnał najgłębszej obserwacji oraz liczba płytszych obsunięć koszyka niż BTC. |

Prefiksy alt i btc oznaczają cały koszyk oraz cały dopasowany benchmark. Pola capital_usdt i running_peak_usdt są kwotami; drawdown oraz mdd są ułamkami (−0.25 oznacza −25%). Daty są w UTC. stage przyjmuje initial_cash, entry_mark, daily_close lub exit_cash. Pole peak_observation_index wskazuje indeks wcześniejszego szczytu danej serii. Przy równych szczytach zachowano pierwszy; przy równych najgłębszych obsunięciach pierwsze wystąpienie. Flaga alt_less_severe_mdd jest prawdziwa, gdy alt_mdd > btc_mdd.

## Odtworzenie i granice

Obliczenia: python scripts/analyze_basket_drawdown.py. Kontrole: python -m unittest discover -s tests -p test_basket_drawdown.py -v. Cztery testy obejmują znaną ścieżkę szczyt–dołek, koszty przy stałej cenie, niesynchroniczne ruchy składników i niezależne odtworzenie wszystkich 60 ścieżek z cen i przepływów. Raport pochodzenia i sumy kontrolne: reports/basket_capital_risk_90d.json.

Dzienne ceny nie odtwarzają dokładnych śróddziennych obsunięć. Nie wolno średniej MDD monet nazywać MDD koszyka. Nie wolno skrajnego MDD z 20 osobnych okien nazywać obsunięciem jednego konta za lata 2020–2025. Taki portfel wymagałby osobnego modelu finansowania nakładających się sygnałów.

Nowa miara jest dostępna w pełnym raporcie, na stronie projektu i w CSV. Dotychczasowy skoroszyt Tableau i ośmioslajdowa prezentacja zachowują wcześniejszy zakres; wykres ryzyka pozycji w tych materiałach przedstawia cenowe MAE pojedynczych monet.
