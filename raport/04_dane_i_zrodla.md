# Dane i źródła

## Źródła wykorzystane w badaniu

W badaniu połączono dwa rodzaje danych: dzienne notowania kryptowalut oraz historyczne rankingi kapitalizacji. Rankingi służyły do wyboru monet dla poszczególnych sygnałów, natomiast dane cenowe wykorzystano do wyznaczenia sygnałów BTC i obliczenia stóp zwrotu.

| Źródło | Zakres wykorzystania |
| --- | --- |
| Binance Spot | Dzienne ceny BTC oraz większości wybranych altcoinów, wyrażone w USDT. |
| KuCoin Spot | Historyczne ceny BSV i TON oraz ceny BTC potrzebne do porównań na tej samej giełdzie. |
| CryptWatch, na podstawie CoinMarketCap | Historyczne zestawienia kapitalizacji do wyboru pięciu kwalifikujących się altcoinów przed każdym sygnałem. |

Dane pobrano 8 listopada 2026 r. Ceny Binance pozyskano przez publiczny interfejs danych rynkowych, a ceny KuCoin przez publiczne API świec. Z archiwum CryptWatch pobrano 19 zestawień potrzebnych do badanych zdarzeń. Oryginalne odpowiedzi, parametry zapytań i informacje o pobraniu zachowano w plikach projektu.

Opis dostępnych pól cenowych zawierają [dokumentacja Binance](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market) i [dokumentacja KuCoin](https://www.kucoin.com/docs-new/rest/spot-trading/market-data/get-klines). Pochodzenie rankingów oraz warunki dostępu opisuje [CryptWatch](https://cryptwat.ch/api). Wymagane oznaczenie źródła rankingów: Data: CryptWatch, based on CoinMarketCap. Szczegółowy rejestr źródeł i warunków wykorzystania znajduje się w dokumentacji projektu.

## Zakres czasowy i waluta danych

Badany okres obejmuje daty sygnałów od 2020-01-01 do 2025-12-31. Do rozpoczęcia obliczeń RSI wykorzystano dodatkowo historię BTC od 2019-01-01. Zgromadzono również ceny po zakończeniu 2025 r., maksymalnie do 2026-07-31, aby umożliwić obserwację późniejszych wyjść z pozycji. Dodatkowe daty nie rozszerzają okresu generowania sygnałów.

Dane cenowe analizowano w postaci dziennych świec według czasu UTC. Wszystkie ceny wykorzystywane do obliczania stóp zwrotu są wyrażone w USDT. Kapitalizacja w rankingach jest podana w USD i służy doborowi aktywów, a nie przeliczaniu wyników. Wynik w USDT nie jest utożsamiany z wynikiem w USD.

## Struktura przygotowanego zbioru

| Element zbioru | Liczba |
| --- | ---: |
| Sygnały BTC w latach 2020–2025 | 20 |
| Historyczne rankingi wykorzystane do doboru | 19 |
| Pary zdarzenie–moneta | 100 |
| Różne altcoiny w koszykach po 5 monet | 11 |
| Dzienne świece w połączonej tabeli cen wybranych aktywów i BTC | 25 114 |

Wybrane w różnych zdarzeniach altcoiny to: ADA, BCH, BNB, BSV, DOGE, ETH, LTC, SOL, TON, TRX, XRP. Nie jest to stała lista obowiązująca przez całe badanie: każda moneta musiała zakwalifikować się na podstawie rankingu dla danego zdarzenia.

Jeden wiersz tabeli cen odpowiada dziennej świecy konkretnego aktywa na konkretnej giełdzie. Zawiera cenę otwarcia, najwyższą, najniższą i zamknięcia, wolumen oraz informacje pozwalające odnaleźć oryginalny rekord źródłowy. Osobne tabele opisują sygnały BTC, skład koszyków i uzasadnienia wykluczeń.

Liczba 100 oznacza wybory monet dla zdarzeń. Nie jest liczbą niezależnych prób ani liczbą zrealizowanych transakcji we wszystkich wariantach wejścia. Pięć monet wybranych dla tego samego sygnału jest powiązanych wspólnym zdarzeniem, a okresy obserwacji kolejnych sygnałów mogą się nakładać.

## Przygotowanie i kontrola jakości

Sprawdzono formaty i kolejność dat, duplikaty, kompletność danych w wymaganych okresach, dodatniość cen i zgodność cen najwyższej oraz najniższej z cenami otwarcia i zamknięcia. Zweryfikowano również sposób obliczenia RSI i wpływ długości historii początkowej. Zachowano pliki źródłowe oraz sumy SHA-256, które pozwalają wykrywać późniejsze zmiany lokalnych plików.

Dla wszystkich 100 par zdarzenie–moneta dostępne są świece altcoina i BTC z tej samej giełdy w pełnych potencjalnych oknach obserwacji. Kompletność danych sprawdzono dla okresu od pierwszego dnia po sygnale do 211. dnia po sygnale, uwzględniając przygotowanie danych do opóźnionych wejść i ewentualnego rozszerzenia horyzontu. W podstawowej analizie obowiązuje nadal 90 dni. Nie uzupełniano brakujących cen zerami, interpolacją ani przenoszeniem poprzednich notowań.

Ujednolicono identyfikatory monet i sprawdzono zmiany nazw. Przykładowo historyczny TON występuje w pobranych odpowiedziach pod późniejszą nazwą GRAM. Zachowano symbol źródłowy i osobno zapisano symbol właściwy dla daty badania. BSV i TON pozostały w koszykach mimo braku odpowiednich ówczesnych cen na Binance; ich dane uzupełniono z KuCoin.

## Ograniczenia danych

Najważniejsze ograniczenie dotyczy częstotliwości i dostępności rankingów. Część starszego archiwum zawiera zestawienia tygodniowe. Dla badanych sygnałów użyte rankingi są wcześniejsze o 1–5 dni. Odtworzony skład może zatem różnić się od rankingu dokładnie z dnia sygnału.

Źródło nie potwierdza historycznych godzin publikacji. Dostępność wcześniejszego zestawienia w chwili potwierdzenia sygnału jest jawnym założeniem, a nie zweryfikowanym faktem. Ograniczenie to należy zachować przy interpretacji wyników.

Drugim ograniczeniem są różnice między giełdami, w tym płynność i przebieg notowań. Wynik każdej monety porównano z wynikiem BTC z tej samej giełdy oraz z identycznych dat wejścia i wyjścia. Obecność dziennej świecy nie dowodzi jednak możliwości realizacji zlecenia o dokładnie wskazanej cenie i bez poślizgu.

Kontrole techniczne nie wykluczają wszystkich możliwych błędów dostawców ani późniejszych korekt ich baz. Przy udostępnianiu danych i raportu należy uwzględnić warunki każdego dostawcy zapisane w rejestrze źródeł.
