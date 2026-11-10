# Sygnały i historyczne koszyki — protokół przygotowania

Data: 2026-11-08. Zakres sygnałów: 2020-01-01–2025-12-31. Na tym etapie nie oceniano rentowności.

## RSI(14) BTC

Użyto dziennych cen zamknięcia BTC/USDT z Binance, w UTC. Pierwsze średnie wzrostów i spadków to zwykłe średnie z 14 zmian ceny, czyli potrzebne jest 15 cen zamknięcia. Dalej stosujemy wygładzanie Wildera: poprzednia średnia razy 13, plus bieżąca zmiana danego rodzaju, podzielone przez 14. RSI = 100 × średni wzrost / (średni wzrost + średni spadek). Gdy obie wartości wynoszą zero, przyjmujemy neutralne 50; przy wyłącznie wzrostach 100, przy wyłącznie spadkach 0.

Wzory zweryfikowano w [dokumentacji eSignal](https://download.esignal.com/products/workstation/help/charts/studies/rsi.htm). Znaczenie rozgrzewki opisuje również [StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi).

Rozpoczęto obliczenia od 2019-01-01. Porównanie własnej pętli z pandas EWM, z jawną identyczną inicjalizacją, dało maksymalną różnicę około 5 × 10^-14 punktu RSI. Kontrolne fikcyjne ciągi rosnące, malejące i stałe dały odpowiednio 100, 0 i 50. Alternatywna rozgrzewka od 2019-07-01 zmieniła wartości w badanym okresie maksymalnie o około 0,00002975 punktu i nie zmieniła żadnej daty sygnału. Kontrola pandas sprawdza implementację rekurencji; wybór inicjalizacji sprawdzono osobno względem wzorów.

Sygnał to przejście: RSI dzisiaj < 30 oraz RSI wczoraj >= 30. Kolejne dni poniżej 30 nie tworzą nowych sygnałów. Użyto pełnej precyzji obliczeń, bez zaokrąglania przed porównaniem z progiem.

Znaleziono 20 sygnałów: 2020 — 1, 2021 — 2, 2022 — 9, 2023 — 2, 2024 — 3, 2025 — 3. Sygnał datowany dniem D jest znany po zakończeniu doby D, czyli na granicy D/D+1. Najwcześniejsze planowane wejście to otwarcie D+1; ceny otwarcia D nie można wykorzystać do realizacji takiego sygnału. Model wykonania i koszty nadal wymagają ustalenia.

## Rankingi i dostępność informacji

Dla każdego sygnału wybrano najnowszą zapisaną datę rankingu ściśle wcześniejszą od dnia sygnału. Pobrano i sprawdzono 19 potrzebnych odpowiedzi CryptWatch; jeden ranking służy dwóm zdarzeniom. Data odpowiedzi musi zgadzać się z żądaną datą. Sprawdzono ciągłość pozycji rankingu, brak duplikatów i SHA-256.

**Założenie wymagające jawnego ujawnienia:** wcześniejszy ranking był dostępny najpóźniej w momencie potwierdzenia sygnału. Źródło nie podaje historycznej chwili publikacji, więc nie jest to fakt potwierdzony znacznikami publikacji. Każdy wiersz ma status publication_time_unverified. Zestawienia użyte dla rzeczywistych sygnałów są starsze o 1–5 dni; część starszego archiwum jest tygodniowa. To historyczny zmienny dobór na podstawie wcześniejszego zestawienia, z ograniczoną dokładnością względem rankingu dokładnie w chwili wejścia. Nie wolno przedstawiać tego jako rekonstrukcji rankingów śróddziennych lub gwarancji dostępności w czasie rzeczywistym.

Nie korzystamy z bieżących statusów aktywności i tagów do usuwania dawnych projektów. Wykluczamy BTC i stablecoiny USDT, USDC oraz BUSD, które wystąpiły przed pozycją odcięcia w tych rankingach. Żaden token opakowany nie wystąpił przed piątym kwalifikującym się aktywem. Nieznana klasyfikacja przed odcięciem zatrzymuje skrypt, zamiast być domyślnie pomijana. Wybór dokumentuje eligibility_audit.csv; przyszła zmiana dat rankingów wymaga ponowienia klasyfikacji, jeśli pojawią się nowe aktywa.

Przy każdym zdarzeniu wybieramy pięć różnych kwalifikujących się aktywów w kolejności źródłowego rankingu. Skład pozostaje zamrożony pomiędzy trzema regułami wejścia. W kolejnym zdarzeniu wybieramy od nowa. Otrzymano 100 par zdarzenie–moneta i 6 różnych zestawów aktywów; zmiana samej kolejności wewnątrz zestawu daje 11 uporządkowanych list.

## Tożsamość TON i zachowanie BSV

W historycznych odpowiedziach z 2024 r. dostawca zwraca późniejszą nazwę GRAM. Zapisane dane szczegółowe identyfikują CMC id 11419 oraz alias TON ważny dla wybranych dat. W tabeli wynikowej symbol historyczny to TON; surowy symbol GRAM pozostaje w osobnej kolumnie. [Bitfinex](https://support.bitfinex.com/hc/en-us/articles/17019918187801-Gram-GRAM) potwierdza późniejszą zmianę nazwy w 2026 r. Samo mapowanie nazwy nie służy do wyboru monety na podstawie późniejszych cen.

BSV pozostaje w koszyku z 2020 r. mimo braku jego cen na Binance. TON występuje w trzech koszykach z 2024 r., także przed [listingiem na Binance 8 sierpnia 2024 r.](https://www.binance.com/en/support/announcement/detail/abba626aa0974b828f91c166bdc12afd). Dostępność ceny na jednej giełdzie nie zmieniła składu top 5.

## Ceny i porównywalność

Dozbierano BNB, ADA, DOGE i TRX z Binance. Dla BSV i TON pozyskano publiczne dane spot KuCoin w USDT. KuCoin przechowuje historyczny TON pod obecną nazwą pary GRAM-USDT; oryginalna odpowiedź i mapowanie zostały zachowane. Dawne zapytanie TON-USDT zwróciło błąd i nie stanowi danych cenowych.

Dla BSV i TON pozyskano także BTC/USDT z KuCoin na te same okresy. W przyszłym porównaniu każda transakcja altcoina użyje BTC z tej samej giełdy i z identycznymi datami. Źródło sygnału RSI pozostaje wspólne — Binance BTC/USDT. Zróżnicowanie giełd i płynności będzie ograniczeniem interpretacji; nie łączymy notowań w jeden arbitralny kurs aktywa.

Sprawdzono wszystkie dni od D+1 do D+211 dla każdej z 100 par zdarzenie–moneta i dla jej BTC. Okno pokrywa do 31 dni oczekiwania na wejście i do 180 dni utrzymywania. Wszystkie wymagane świece są obecne; nie uzupełniano cen. Obecność świecy nie dowodzi realizacji zlecenia o dokładnej cenie bez poślizgu. Podstawowe badanie nadal ma horyzont 90 dni.

## Zależność zdarzeń

Żadnego sygnału nie usunięto. Dodano konserwatywne grupy połączonych potencjalnych okien od sygnału do D+121 (maksymalnie 31 dni do wejścia i 90 dni utrzymywania). Otrzymano 7 takich grup. To pomocnicza etykieta zależności, nie dowód siedmiu niezależnych obserwacji. Nie należy traktować 100 par zdarzenie–moneta jako 100 niezależnych prób ani sumować ich wyników jako zysku jednego portfela.

## Przed analizą stóp zwrotu

Do ustalenia pozostają koszty i poślizg, dokładna konwencja siedmiodniowego opóźnienia, ceny i terminy wyjścia, obsługa braku wejścia w regule powrotu RSI, sposób porównania wspólnych zdarzeń oraz podział czasowy do oceny stabilności. Ewentualne sprawdzenie wrażliwości na dodatkowe opóźnienie rankingu należy określić przed oglądaniem zysków. Nie obliczono jeszcze żadnych wyników strategii.

Aktualizacja etapu: przed pierwszym przykładem kontrolnym zapisano robocze konwencje i scenariusze w config/trade_protocol_v1.json. Obliczono wyłącznie pierwszy chronologiczny przypadek ETH i BTC, reguła A, 90 dni. Przykład w raport/03_pierwsze_zdarzenie.md nie jest pełną analizą strategii ani uzasadnieniem wyboru najlepszej reguły. Niepewność publikacji rankingów pozostaje jawna.
