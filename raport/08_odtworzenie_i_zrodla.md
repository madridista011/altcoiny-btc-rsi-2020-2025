# Odtworzenie analizy i źródła

## Narzędzia i sposób pracy

| Narzędzie lub format | Zastosowanie w wykonanym projekcie |
| --- | --- |
| Python 3.12.14 | Przygotowanie cen, RSI, dobór historycznych monet, obliczenie transakcji i składanie raportu. |
| pandas 3.0.1 | Niezależna kontrola RSI, przepływów pieniężnych, statystyk i miar ryzyka. |
| decimal z biblioteki standardowej Python | Obliczenia stóp zwrotu przy precyzji 40 cyfr znaczących, przed zaokrągleniem prezentacyjnym. |
| Matplotlib 3.10.8 | Pięć wykresów eksportowanych do PNG i SVG, w tym obsunięcie kapitału koszyków. |
| Tableau Public 2026.2 | Interaktywna prezentacja wyników: siedem wykresów i dwa dashboardy z oddzielnymi poziomami monet i koszyków, zapisane lokalnie w TWBX. |
| JSON i CSV | Zachowane odpowiedzi źródeł, parametry, tabele pośrednie i wyniki. |
| SHA-256 | Sprawdzanie integralności lokalnych źródeł i niezmienności tabel wynikowych. |

Obliczenia wykonano w Pythonie. Zachowane dane źródłowe, kod i raporty kontroli pozwalają odtworzyć analizę. Tableau służy do interaktywnego przeglądania oraz agregowania gotowych wyników. Działanie dashboardów sprawdzono w aplikacji Tableau Public.

## Instrukcja odtworzenia z zachowanych źródeł

Pełne odtworzenie wymaga katalogu projektu wraz z danymi źródłowymi. Polecenia uruchamia się w jego katalogu głównym, w środowisku Python z zależnościami wskazanymi w requirements-plots.txt. Instalacja zależności i ich wersje są opisane w README.md; podstawowe obliczenia wymagają requirements.txt. Lokalne środowisko generatora wykresów opisano w README.md.

~~~text
python scripts/prepare_prices.py
python scripts/build_signal_events.py
python scripts/select_event_baskets.py
python scripts/prepare_event_prices.py
python scripts/check_ranking_source.py
python scripts/analyze_trades.py
python scripts/aggregate_event_results.py
python scripts/validate_trade_outputs.py
python scripts/analyze_basket_drawdown.py
python scripts/build_figures.py
python scripts/build_drawdown_figure.py
python scripts/write_results_chapter.py
python scripts/build_report_draft.py
python scripts/validate_report_assets.py
python -m unittest discover -s tests -p test_trade_analysis.py -v
python -m unittest discover -s tests -p test_basket_drawdown.py -v
~~~

Ta ścieżka wykorzystuje zapisane odpowiedzi dostawców. Zmiana konfiguracji lub danych wymaga ponownego przejścia kontroli oraz sprawdzenia, czy tekst nadal opisuje właściwy zakres badania. Protokół v1 zachowuje parametry sprzed pełnych obliczeń. Kontrola skryptu transakcji porównuje jego hash z zapisem sprzed przykładu kontrolnego. Świeże pobranie danych stanowi osobny proces: wymaga kontroli aktualnego dostępu i zgodności z zachowanym archiwum.

Oczekiwany rezultat obejmuje 20 sygnałów, 100 wyborów monet, 300 kompletnych wierszy transakcji i 60 średnich zdarzeń. Raporty walidacji potwierdzają integralność cen, kompletność kluczy, daty, wyniki i zgodność wykresów. Weryfikacja SHA-256 wykrywa zmianę pliku lokalnego, ale nie dowodzi bezbłędności danych dostawcy ani historycznej godziny ich udostępnienia.

## Układ plików

| Katalog lub plik | Zawartość |
| --- | --- |
| config/ | Parametry i klasyfikacja aktywów. |
| data/raw/ | Oryginalne odpowiedzi cenowe i rankingowe. |
| data/metadata/ | Manifesty źródeł, parametry zapytań i sumy kontrolne. |
| data/processed/ | Oczyszczone świece, sygnały, dobór monet i kontrole pokrycia. |
| data/analysis/ | Transakcje 90-dniowe i zestawienia wyników. |
| scripts/ oraz tests/ | Kod przygotowania, analizy, kontroli i raportowania. |
| reports/ | Wyniki kontroli w formacie JSON. |
| raport/PRACA_ROBOCZA.md | Główny dokument, składany z fragmentów raportu. |
| raport/wykresy/ | Pięć wykresów w PNG i SVG; dane pierwszych czterech w dane_do_wykresow.csv, piątego w data/analysis/summary_basket_capital_risk_90d.csv. |
| tableau/Altcoiny_RSI_BTC.twbx oraz tableau/INSTRUKCJA.md | Przenośny pakiet interaktywnych dashboardów i instrukcja filtrów oraz agregacji. |
| docs/ oraz DZIENNIK_PROJEKTU.md | Źródła, słowniki i historia decyzji. |

CSV są zapisane w UTF-8 z BOM, z przecinkiem jako separatorem pól i kropką dziesiętną. Przy przeglądzie w polskim Excelu należy użyć importu „Dane → Z tekstu/CSV”. Stopy zwrotu w tabelach analizy są zwykle ułamkami, np. 0.05 oznacza 5%; pola zakończone _pp są już w punktach procentowych. Szczegóły podaje docs/SLOWNIK_ZDARZEN.md.

Uzupełniająca analiza MDD kapitału obejmuje 60 osobnych ścieżek i 5 580 obserwacji. Definicje kolumn i zakres publikacji opisano w docs/OBSUNIECIE_KAPITALU.md. Interaktywny wykres obsunięć znajduje się na stronie projektu. Dotychczasowe dashboardy Tableau oraz ośmioslajdowa prezentacja zachowują wcześniejszy zakres ryzyka pojedynczych pozycji.

## Literatura metodyczna

Przy opracowaniu terminologii i sposobu prezentacji analizy wykorzystano publikację: Foster Provost, Tom Fawcett, **Analiza danych w biznesie. Sztuka podejmowania skutecznych decyzji**, tłum. Leszek Sielicki, Helion, 2014.

## Źródła danych i definicji

Rejestr wykorzystania źródeł powstał podczas przygotowania projektu 2026-11-08. Pełne zakresy dat, parametry pobrań, ograniczenia dostępu oraz udokumentowane warunki wykorzystania znajdują się w docs/ZRODLA_DANYCH.md i manifestach. Poniższy wykaz dotyczy materiałów wykorzystanych w bieżącym badaniu.

| Źródło | Zastosowanie |
| --- | --- |
| [Binance — dokumentacja danych rynkowych Spot](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market) | Dzienne świece cenowe oraz interpretacja pól API; wspólny sygnał RSI pochodzi z BTC/USDT Binance. |
| [KuCoin — Get Klines](https://www.kucoin.com/docs-new/rest/spot-trading/market-data/get-klines) | Ceny BSV, historycznego TON oraz dopasowanego BTC dla tych pozycji. |
| [CryptWatch — API](https://cryptwat.ch/api) | 19 wcześniejszych rankingów potrzebnych do doboru pięciu monet dla 20 sygnałów. Oznaczenie: Data: CryptWatch, based on CoinMarketCap. |
| [CoinMarketCap — zestawienie 8 marca 2020 r.](https://coinmarketcap.com/historical/20200308/) | Kontrola kolejności pierwszych 15 pozycji jednej próbki rankingowej; nie jest weryfikacją całego archiwum. |
| [eSignal — Relative Strength Index](https://download.esignal.com/products/workstation/help/charts/studies/rsi.htm) oraz [StockCharts — RSI](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi) | Opis inicjalizacji i wygładzania RSI. Implementację sprawdzono oddzielnie na zachowanych cenach. |
| [Binance — notowania TON](https://www.binance.com/en/support/announcement/detail/abba626aa0974b828f91c166bdc12afd) oraz [Bitfinex — Gram](https://support.bitfinex.com/hc/en-us/articles/17019918187801-Gram-GRAM) | Kontrola ograniczeń historycznej dostępności pary oraz późniejszego nazewnictwa aktywa; mapowanie oparto również na zachowanym identyfikatorze i aliasach. |

Oznaczenie danych cenowych: Binance Spot / Binance Vision oraz KuCoin. Oznaczenie rankingów: **Data: CryptWatch, based on CoinMarketCap**. Warunki Binance zapisano z odnośnikiem do [Binance Vision Dataset Terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md), a warunki KuCoin z odnośnikiem do [KuCoin Terms of Use](https://www.kucoin.com/legal/terms-of-use). Dostęp badawczy i zachowanie źródeł nie oznaczają jednolitej otwartej licencji na redystrybucję wszystkich surowych danych. Przed publicznym udostępnieniem bazy trzeba odnieść się do rejestru warunków właściwego dostawcy.
