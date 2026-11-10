# Stopy zwrotu największych altcoinów po sygnałach wyprzedania Bitcoina: porównanie z BTC i analiza momentu wejścia w latach 2020–2025

Studium przypadku w ramach kursu Google Data Analytics.

Autor: **Mateusz Gromski**. Data opracowania: 8 listopada 2026 r.

# Streszczenie

Celem projektu była ocena, czy zakup pięciu altcoinów o najwyższej kapitalizacji spośród monet spełniających kryteria doboru przynosił zysk po kosztach oraz wyższą stopę zwrotu niż zakup BTC w tych samych terminach. Badanie objęło sygnały z lat 2020–2025, wyznaczone przez przejście dziennego RSI(14) BTC/USDT z wartości co najmniej 30 poniżej 30.

Dla każdego sygnału dobierano pięć monet według wcześniejszego historycznego rankingu kapitalizacji, z wyłączeniem BTC, stablecoinów i tokenów opakowanych. Porównano wejścia na otwarciu D+1, na otwarciu D+7 oraz po powrocie RSI do co najmniej 30, gdzie D oznacza datę świecy sygnałowej. Każdą pozycję utrzymywano 90 dni. Uwzględniono modelowe koszty: prowizję 0,10% oraz niekorzystny poślizg 0,05% przy zakupie i sprzedaży.

Zidentyfikowano 20 sygnałów, 100 par zdarzenie–moneta i 300 kompletnych porównań trzech reguł. Mediany stóp zwrotu netto pojedynczych altcoinów wyniosły odpowiednio 3,59%, 2,22% i 3,39%. Zysk wystąpił w 55–62% pojedynczych porównań, lecz przewaga nad dopasowanym BTC tylko w 34–37%. Koszyk pięciu monet o równych początkowych udziałach uzyskał wyższą stopę zwrotu niż dopasowany BTC w 4–5 z 20 zdarzeń. Wartości median badanych miar wskazywały na większe spadki cen altcoinów niż BTC.

Uzupełniająca analiza kapitału całych koszyków wykazała mediany maksymalnego obsunięcia od −26,72% do −26,85%, wobec −20,93% dla BTC. Najgłębsze obsunięcie koszyka w próbie wyniosło −54,76%. Każde zdarzenie ma osobny hipotetyczny budżet; nie odtwarzano wspólnego konta za cały badany okres.

W tej próbie dodatni wynik altcoinów zwykle nie oznaczał przewagi nad BTC. Zakres wnioskowania ograniczają niewielka liczba sygnałów i zależność między obserwacjami, modelowe koszty oraz rankingi wcześniejsze o 1–5 dni, których historyczne godziny publikacji nie są potwierdzone. Wyniki mają charakter opisowy i dotyczą przyjętego horyzontu 90 dni. Stopy zwrotu obliczono na podstawie cen wyrażonych w USDT.

**Słowa kluczowe:** analiza danych, kryptowaluty, RSI, historyczny dobór altcoinów, BTC, stopa zwrotu, ryzyko.

# 1. Problem, cel i zakres pracy

## Cel pracy

Celem projektu była ocena, czy zakup pięciu altcoinów o najwyższej kapitalizacji spośród monet spełniających kryteria doboru przynosił zysk po kosztach oraz wyższą stopę zwrotu niż zakup BTC w tych samych terminach. Badanie obejmowało sygnały wyprzedania wyznaczone przez RSI(14) pary BTC/USDT w latach 2020–2025. Dla każdego sygnału ustalano skład koszyka na podstawie wcześniejszego historycznego rankingu kapitalizacji. Oceniono wyniki poszczególnych monet, a następnie porównano stopy zwrotu i miary ryzyka dla trzech reguł wejścia.

## Problem badawczy

Czy po przejściu RSI(14) BTC z wartości co najmniej 30 do wartości poniżej 30 zakup pięciu największych kwalifikujących się altcoinów, dobranych według wcześniejszego historycznego rankingu, przynosił zysk po kosztach i przewyższał wynik BTC?

Skład jest dobierany osobno dla każdego sygnału. W obrębie jednego zdarzenia porównanie reguł wejścia obejmuje ten sam zestaw monet. BTC, stablecoiny i tokeny opakowane są wykluczone z koszyka altcoinów.

## Pytania badawcze

1. Czy zakup wybranych altcoinów przynosił dodatnią stopę zwrotu po kosztach?
2. Czy wynik był wyższy niż wynik BTC kupowanego i sprzedawanego w tych samych terminach?
3. Jak wejście na otwarciu D+1, na otwarciu D+7 lub po powrocie RSI do co najmniej 30 zmieniało wyniki i ryzyko? D oznacza datę świecy sygnałowej, a terminy są liczone od tej daty.

## Zakres pracy

Badanie obejmuje sygnały z lat 2020–2025, wyznaczane za pomocą RSI(14) BTC/USDT na dziennych danych UTC. Dla każdego sygnału wybieranych jest pięć największych kwalifikujących się altcoinów, z wyłączeniem BTC, stablecoinów i tokenów opakowanych. Podstawowy okres utrzymywania pozycji wynosi 90 dni.

Skład monet jest ustalany osobno dla każdego zdarzenia według wcześniejszego historycznego rankingu kapitalizacji i pozostaje taki sam podczas porównania reguł wejścia w ramach tego zdarzenia. Przyjęto model transakcji na rynku spot, bez dźwigni, z cenami wyrażonymi w USDT. Oddzielnie oceniono dodatnią stopę zwrotu netto, przewagę nad BTC oraz jednoczesne spełnienie obu warunków.

Lata 2020–2025 określają daty sygnałów. Dodatkowa historia BTC przed 2020 r. służy rozpoczęciu obliczeń RSI, a ceny po 2025 r. umożliwiają obserwację pełnego okresu utrzymywania pozycji otwartych po ostatnich sygnałach. Wiek użytych rankingów i niepotwierdzone godziny ich publikacji uwzględniono w ograniczeniach badania.

## Odbiorca i zastosowanie

Odbiorcą jest analityk oceniający historyczne reguły inwestycyjne. Wyniki mogą wesprzeć decyzję, czy którąś regułę warto poddać dalszym testom. Rekruter czytający portfolio będzie mógł ocenić sposób formułowania pytań, przygotowania danych i uzasadniania wniosków.

## Oddzielne kryteria wyniku

- Zysk: stopa zwrotu netto altcoina jest dodatnia.
- Przewaga nad BTC: stopa zwrotu netto altcoina jest wyższa niż stopa zwrotu netto BTC przy tych samych datach zakupu i sprzedaży.
- Zysk i przewaga: spełnione są oba warunki jednocześnie.

Litery A, B i C w dalszej części raportu oznaczają wyłącznie reguły wejścia. Nazwy trzech kryteriów wyniku odpowiadają warunkom ustalonym na początku projektu; zmieniono ich oznaczenie w tekście, aby uniknąć dwuznaczności.

Wartością projektu jest rzetelna odpowiedź, również gdy analiza pokaże stratę, brak przewagi lub zbyt małą liczbę niezależnych obserwacji.

## Założenie dostępności rankingu

Przygotowane rankingi poprzedzają sygnały o 1–5 dni. Źródło nie potwierdza dokładnych historycznych godzin publikacji; dostępność wcześniejszego zestawienia w chwili potwierdzenia sygnału pozostaje jawnym założeniem. Odtworzony dobór może różnić się od rankingu dokładnie z chwili zakupu. Ceny i kwoty kapitału wyrażono w USDT.

# 2. Dane i źródła

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


# 3. Metodologia analizy

## Charakter badania i jednostka obserwacji

Badanie ma charakter historycznej symulacji transakcji spot, bez dźwigni. Punktem wyjścia jest sygnał wyprzedania BTC. Dla każdego zdarzenia wybrano pięć altcoinów spełniających kryteria doboru. Ich stopy zwrotu porównano ze stopami zwrotu BTC dla identycznych dat zakupu i sprzedaży. Ocenie poddano trzy reguły wejścia.

Jednostkę obserwacji w tabeli transakcji określa połączenie zdarzenia, monety, reguły wejścia i okresu utrzymywania pozycji. Pięć monet po jednym sygnale nie oznacza pięciu niezależnych zdarzeń. Podstawowy horyzont wynosi 90 dni. Horyzonty 30 i 180 dni pozostają możliwym rozszerzeniem badania.

Poniższy rozdział opisuje protokół roboczy zapisany przed pełnymi obliczeniami, początkowo sprawdzony na jednym przykładzie kontrolnym ETH–BTC. Pełną analizę 90-dniową wykonano według tych reguł i przedstawiono w kolejnym rozdziale. Odrębnie przedstawiono założenia dotyczące kosztów, dostępności rankingów i realizacji zleceń oraz wyniki uzyskane na podstawie danych.

## Wyznaczanie RSI i sygnału BTC

RSI(14) obliczono metodą Wildera na podstawie dziennych cen zamknięcia BTC/USDT z giełdy Binance, według czasu UTC. Dla każdej pary kolejnych cen wzrost zdefiniowano jako dodatnią zmianę ceny lub zero, a spadek jako wartość bezwzględną ujemnej zmiany lub zero. Pierwsze średnie obejmują 14 zmian, co wymaga 15 cen zamknięcia. W kolejnych dniach każdą ze średnich aktualizowano według wzoru:

**nowa średnia = (poprzednia średnia × 13 + bieżący wzrost lub spadek) / 14**

Następnie:

**RSI = 100 × średni wzrost / (średni wzrost + średni spadek)**

Przy braku spadków RSI wynosi 100, przy braku wzrostów 0, a gdy obie średnie wynoszą zero, przyjęto neutralną wartość 50. Do rozpoczęcia obliczeń wykorzystano dane historyczne z 2019 r., poprzedzające okres badania. Wartości nie są zaokrąglane przed sprawdzeniem progu. Sposób inicjalizacji i wygładzania opisują [eSignal](https://download.esignal.com/products/workstation/help/charts/studies/rsi.htm) i [StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi). Sprawdzenie implementacji i sposobu inicjalizacji zapisano w raporcie walidacji RSI.

Sygnał występuje, gdy **wartość RSI w dniu D jest niższa niż 30, a dzień wcześniej wynosiła co najmniej 30**. Kolejne dni pozostawania poniżej progu nie są nowymi sygnałami. Nowy sygnał może powstać po wcześniejszym powrocie wskaźnika do co najmniej 30.

D oznacza datę świecy sygnałowej. Sygnał jest potwierdzony dopiero po jej zakończeniu, na granicy dni D i D+1. Zakup na podstawie tego sygnału nie jest przypisywany do ceny otwarcia ani zamknięcia dnia D. Najwcześniejsze modelowane wejście przypada na otwarcie kolejnego dnia. To konwencja symulacji dziennej; rzeczywiste opóźnienie decyzji i wykonania zlecenia nie jest odtwarzane.

## Historyczny dobór pięciu altcoinów

Dla każdego sygnału wybrano najnowszy ranking z pobranego archiwum, którego data była ściśle wcześniejsza od dnia D. Kolejność wynika z historycznego rankingu kapitalizacji. Kolejne pozycje rankingu przeglądano do wybrania pięciu różnych monet spełniających kryteria doboru. Pomijano BTC, stablecoiny i tokeny opakowane reprezentujące inne aktywa. Wykluczenia i identyfikatory zapisano w tabeli kontrolnej.

Przy doborze nie uwzględniano obecnego statusu projektu, późniejszych stóp zwrotu ani dostępności notowań na jednej giełdzie. W przypadku BSV i TON potrzebne ceny pozyskano z KuCoin. Historyczne nazwy i identyfikatory aktywów przyporządkowano niezależnie od oznaczeń użytych przez dostawcę danych.

Skład ustalony dla zdarzenia pozostaje taki sam w regułach A, B i C. W następnym zdarzeniu dobór jest wykonywany ponownie. Koszyka nie aktualizowano w czasie oczekiwania na zakup zgodnie z regułą B lub C. Dzięki temu porównanie tych reguł zachowuje ten sam zestaw aktywów.

W badanych zdarzeniach ranking poprzedza sygnał o 1–5 dni. Założenie, że był on dostępny najpóźniej w chwili potwierdzenia sygnału, nie jest potwierdzone historycznymi godzinami publikacji. Zmienny dobór na podstawie wcześniejszych zestawień może różnić się od dokładnego rankingu z dnia sygnału; ograniczenie to pozostaje częścią interpretacji.

## Reguły wejścia

Wszystkie daty oznaczają dni kalendarzowe UTC, a ceny wejścia są cenami otwarcia odpowiednich świec, skorygowanymi następnie o modelowany poślizg.

| Reguła | Warunek i termin wejścia |
| --- | --- |
| A — następna świeca | Zakup na otwarciu dnia D+1. |
| B — opóźnione wejście | Zakup na otwarciu dnia D+7, licząc od daty świecy sygnałowej D. |
| C — powrót RSI | W dniach D+1–D+30 wyszukuje się pierwszą świecę BTC, dla której wartość RSI po zamknięciu wynosi co najmniej 30. Zakup następuje na otwarciu kolejnego dnia. |

W przyjętej konwencji B następuje sześć dni po A; siedem dni jest liczonych od daty D, a nie od wejścia A. W regule C limit 30 dni dotyczy świecy potwierdzającej powrót RSI, dlatego najpóźniejsze wejście przypada na D+31. Te konwencje są zapisane w protokole, aby uniknąć przesunięcia wyników o jeden dzień.

Jeżeli w regule C nie wystąpi wymagany powrót RSI, przypadek otrzymuje status „brak wejścia”. Przypadek pozostaje w zestawieniu zdarzeń i w statystyce częstości wejść. Nie przypisuje się mu zerowej stopy zwrotu, ponieważ nie doszło do modelowanego zakupu.

## Wyjście z pozycji i porównanie z BTC

Wyjście następuje na otwarciu świecy dokładnie 90 dni kalendarzowych po modelowanym zakupie zgodnym z daną regułą. Jeżeli wejście przypada na dzień T, wyjście przypada na T+90. Reguły A, B i C mogą więc mieć różne daty zakończenia inwestycji.

Dla każdej transakcji dotyczącej altcoina obliczono stopę zwrotu BTC z tej samej giełdy, dla identycznych dat zakupu i sprzedaży oraz tego samego scenariusza kosztów. Źródłem wspólnego sygnału RSI pozostaje Binance BTC/USDT. Takie dopasowanie pozwala ocenić wybór aktywa przy ustalonych terminach zakupu i sprzedaży.

Wynik wcześniejszego i późniejszego wejścia obejmuje inną cenę zakupu, czas oczekiwania i przesunięcie daty sprzedaży. Tabele transakcji zawierają te daty i opóźnienia. Różnice opisują pełne reguły wejścia i wyjścia; nie izolują wpływu samej ceny zakupu. Do wyznaczania sygnału zakupu nie wykorzystano przyszłego minimum ceny.

## Stopy zwrotu i scenariusze kosztów

Niech P_we oznacza referencyjną cenę wejścia, a P_wy referencyjną cenę wyjścia. Stopa brutto wynosi:

**r_brutto = P_wy / P_we − 1**

W podstawowym scenariuszu symulacji przyjęto prowizję f = 0,10% oraz niekorzystny poślizg s = 0,05% przy zakupie i przy sprzedaży. Prowizja zakupu jest doliczana do wydatku, a prowizja sprzedaży potrącana z wpływu. Przy utrzymywaniu tej samej liczby jednostek aktywa:

**r_netto = [P_wy × (1 − s) × (1 − f)] / [P_we × (1 + s) × (1 + f)] − 1**

W obliczeniach f = 0,001, a s = 0,0005. Stopę zwrotu zapisaną jako ułamek mnoży się przez 100 w celu przedstawienia jej w procentach. Obliczenia przeprowadzono z pełną precyzją, a zaokrąglenia zastosowano wyłącznie przy prezentacji wyników.

Przyjęte koszty są założeniem symulacji; nie odtwarzają indywidualnych historycznych prowizji ani warunków w arkuszu zleceń. Przed pierwszym przykładem kontrolnym zapisano również dwa scenariusze wrażliwości: tę samą prowizję z poślizgiem 0% oraz z poślizgiem 0,20% po każdej stronie. Wyniki tych wariantów przedstawiono w rozdziale wyników. Wspólne parametry dla BTC i altcoinów ułatwiają porównanie, ale nie oznaczają identycznych rzeczywistych kosztów i płynności.

## Przewaga nad BTC i kryteria sukcesu

Podstawowa różnica wyników jest liczona na stopach netto z dopasowanej pary altcoin–BTC:

**przewaga w punktach procentowych = 100 × (r_alt − r_BTC)**

Wzór zakłada, że r_alt i r_BTC zapisano jako ułamki. Uzupełniająca miara względna wynosi:

**wynik względny = (1 + r_alt) / (1 + r_BTC) − 1**

Pierwsza miara jest różnicą dwóch stóp zwrotu, a druga porównuje końcową wartość jednostki kapitału. Punkty procentowe służą zatem do przedstawiania różnicy stóp zwrotu, a procenty do przedstawiania stopy zwrotu.

Każdą kompletną parę porównywanych inwestycji oceniono według trzech odrębnych kryteriów:

- Zysk: r_alt netto > 0.
- Przewaga nad BTC: r_alt netto > r_BTC netto.
- Zysk i przewaga: oba warunki jednocześnie.

Przy równości z zerem lub BTC ścisły warunek „większy” nie jest spełniony. Zestawienia stosują pełne nazwy kryteriów wyniku. Litery A, B i C oznaczają wyłącznie reguły wejścia.

## Pomiar ryzyka

Główną miarą niekorzystnego ruchu ceny jest największy spadek względem ceny wejścia. Niech L_min oznacza najmniejszą spośród referencyjnej ceny wejścia, dziennych cen minimalnych od dnia wejścia do dnia poprzedzającego wyjście oraz referencyjnej ceny wyjścia. Wtedy:

**największy spadek od wejścia = L_min / P_we − 1**

Uwzględnienie ceny wejścia zapewnia, że miara nie jest dodatnia. Uwzględnienie ceny otwarcia przy wyjściu pozwala ująć ewentualny spadek na tej granicy; nie uwzględnia się minimum z pozostałej części dnia po zamknięciu pozycji. Miara, określana jako niekorzystne odchylenie od wejścia (MAE), jest cenowa i nie zawiera prowizji ani poślizgu. Koszty są odrębnie uwzględnione w stopie netto.

Pomocniczo obliczono maksymalne obsunięcie od wcześniejszego szczytu (MDD). Dla ścieżki złożonej z ceny otwarcia przy wejściu, dziennych zamknięć podczas utrzymywania oraz ceny otwarcia przy wyjściu zastosowano wzór:

**MDD = minimum po t z: [cena_t / najwyższa cena tej ścieżki do chwili t − 1]**

MDD przedstawiono osobno od spadku względem wejścia. Ścieżka dziennych zamknięć nie odtwarza wszystkich szczytów i dołków śróddziennych. W obu miarach wartości ujemne oznaczają spadek, a zero brak spadku w odpowiednio zdefiniowanej ścieżce.

## Braki danych i zależność obserwacji

Brakujących cen nie zastępowano zerem ani poprzednim notowaniem. Rozróżniono brak wejścia, brak danych z przyczyn technicznych, brak notowań i niepełny okres obserwacji. Niekompletne przypadki zachowano z odpowiednimi oznaczeniami i podano ich liczbę; stopy zwrotu dla takich przypadków nie obliczano. Migracje i zmiany nazw wymagają potwierdzenia tożsamości aktywa; zgodność samych symboli giełdowych nie wystarcza do połączenia danych.

Uwzględniono wszystkie sygnały spełniające przyjętą definicję. Do opisu zależności użyto grup utworzonych przez połączenie potencjalnie nakładających się okresów od D do D+121: do 31 dni przed wejściem i 90 dni utrzymywania. Podział na grupy nie przesądza o niezależności statystycznej obserwacji. Wyników pięciu monet przypisanych do jednego sygnału ani wyników inwestycji o nakładających się okresach nie traktowano jako niezależnych obserwacji.

## Zestawienia i ocena stabilności

Wyniki dla horyzontu 90 dni przedstawiono osobno dla monet i reguł wejścia. Dla każdej grupy podano liczbę sygnałów objętych analizą, liczbę kompletnych transakcji oraz liczbę przypadków braku wejścia lub brakujących danych. Dla kompletnych transakcji obliczono średnią, medianę, odsetek dodatnich wyników, odsetek przewag nad BTC i odsetek jednoczesnego spełnienia obu warunków. Mianowniki tych odsetków są jawne i zgodne z liczbą kompletnych dopasowanych par.

Porównanie terminów wejścia oparto również na wspólnym zestawie zdarzeń z kompletnymi wynikami wszystkich porównywanych reguł. Wspólna próba obejmuje wszystkie 100 par zdarzenie–moneta; kompletność danych nie wymagała wykluczenia żadnej z nich. Osobno przedstawiono kompletność i liczbę braków wejścia w C, która wyniosła zero.

Stabilność opisano w częściach 2020–2022 i 2023–2025, według dat sygnałów. Nie dostrajano progu RSI ani parametrów po poznaniu wyników i nie wybierano reguły do wdrożenia. Przed obliczeniami zapisano, że ewentualny wybór na wcześniejszym okresie mógłby korzystać wyłącznie z wyników poznanych przed 2023-01-01. W rozdziale wyników wskazano transakcje przekraczające tę granicę. Zestawienie nie stanowi niezależnego testu wybranej wcześniej reguły.

Małe liczebności, współzależność monet i różnice rynkowe między latami ograniczają siłę wniosków. Historycznie najwyższy wynik nie wyznacza uniwersalnie najlepszego momentu wejścia. Stóp zwrotu z nakładających się transakcji nie sumowano jako zysku jednego portfela; wymagałoby to osobnego modelu kapitału.

## Uzupełnienie: maksymalne obsunięcie kapitału koszyka

Po opracowaniu pierwotnych wyników dodano opisową analizę MDD kapitału całego koszyka. Każde zdarzenie i reguła otrzymują osobny budżet 1 000 USDT; po 200 USDT przeznaczono na każdy altcoin, łącznie z kosztami zakupu. Liczba jednostek jest stała: q_i = 200 / [cena wejścia_i × (1 + poślizg zakupu) × (1 + prowizja zakupu)]. Nie stosowano rebalansowania. Dopasowany punkt odniesienia obejmuje pięć analogicznych części BTC z tych samych giełd i dat co monety koszyka.

Początkowa wartość kapitału wynosi 1 000 USDT. Kolejne obserwacje obejmują wartość rynkową bezpośrednio po zakupie, sumę q_i × dzienna cena zamknięcia_i przez 90 dni oraz wpływ gotówki po końcowej sprzedaży z uwzględnieniem jej kosztów. Daje to 93 uporządkowane obserwacje na zdarzenie i regułę, łącznie 5 580. Prowizji sprzedaży nie odejmuje się przy każdej dziennej wycenie otwartych pozycji.

Dla kapitału V_t obliczono szczyt P_t = max(V_0, …, V_t), następnie DD_t = V_t / P_t − 1 oraz MDD = min(DD_t). W raporcie MDD ma znak ujemny; np. −25% oznacza spadek o 25% od wcześniejszego szczytu. Taka definicja odpowiada spadkowi od szczytu do późniejszego dołka opisanemu w [dokumentacji QuantConnect](https://www.quantconnect.com/docs/v2/cloud-platform/optimization/objectives); w tej pracy zapisano go z przeciwnym znakiem do dodatniej wielkości straty.

MDD oblicza się ze wspólnej ścieżki wartości pięciu składników. Średnia arytmetyczna pięciu indywidualnych wartości MDD nie wyznacza MDD koszyka, ponieważ szczyty i dołki monet mogą wypadać w innych momentach. Raportuje się medianę, najgłębszą obserwację i liczbę zdarzeń z płytszym MDD niż BTC. To uzupełnienie zachowuje pierwotne sygnały, skład, daty i koszty. Nie tworzy jednego portfela finansującego nakładające się sygnały. Dane dzienne nie pozwalają odtworzyć dokładnego śróddziennego obsunięcia kapitału.

## Odtworzenie i status obliczeń

Parametry analizy zapisano w config/trade_protocol_v1.json. Dane źródłowe i pochodzenie wierszy zachowano w manifestach oraz tabelach przygotowania. Procedury przygotowania RSI, koszyków i cen można odtworzyć za pomocą skryptów projektu.

Wykonano pełną tabelę trzech reguł dla 90 dni, pomiary ryzyka, zestawienia stabilności oraz wrażliwości kosztowej. Analiza odtworzyła wcześniej sprawdzony przypadek kontrolny ETH–BTC. Niezależna kontrola przepływów pieniężnych i obliczeń pandas potwierdziła wyniki na prezentowanej dokładności. Odtworzenie: scripts/analyze_trades.py i scripts/validate_trade_outputs.py.

Na etapie opracowania wyników dodano opisową średnią pięciu monet w zdarzeniu, odtwarzaną przez scripts/aggregate_event_results.py. Równe początkowe udziały po 20% oznaczają osobny budżet dla każdego sygnału; porównaniem jest tak samo ważona średnia dopasowanych wyników BTC. Zestawienie jest jawnie oznaczone jako uzupełnienie po obliczeniu indywidualnych wyników. Nie zmienia sygnałów, doboru, reguł ani parametrów kosztowych. Nie rekonstruuje wspólnej ścieżki kapitału między nakładającymi się zdarzeniami.


# 4. Wyniki analizy 90-dniowej

## Zakres wykonanych obliczeń

Przeanalizowano 20 sygnałów z lat 2020–2025 oraz pięć historycznie dobranych altcoinów dla każdego sygnału. Daje to 100 par zdarzenie–moneta i 300 porównań po uwzględnieniu trzech reguł wejścia. Każda transakcja ma dopasowany wynik BTC z tej samej giełdy i tych samych dat. Okres utrzymywania pozycji wynosi 90 dni od modelowanej daty zakupu.

A oznacza wejście na otwarciu D+1, B na otwarciu D+7 od daty sygnału, a C wejście następnego dnia po pierwszym powrocie RSI do co najmniej 30 w dozwolonym oknie. Podstawowe koszty wynoszą 0,10% prowizji i 0,05% niekorzystnego poślizgu po każdej stronie. Wszystkie stopy zwrotu obliczono na podstawie cen wyrażonych w USDT.

| Reguła wejścia | Sygnały | Kompletne pary altcoin–BTC | Brak wejścia: pary | Inne niepełne pary |
| --- | --- | --- | --- | --- |
| A | 20 | 100 | 0 | 0 |
| B | 20 | 100 | 0 | 0 |
| C | 20 | 100 | 0 | 0 |

W regule C wymagany powrót RSI wystąpił dla wszystkich 20 sygnałów; liczba przypadków bez wejścia w zestawie planów wyniosła 0. Nie odrzucono żadnej pary z powodu niepełnych danych. Wspólna próba porównania A/B/C obejmuje zatem wszystkie 100 par zdarzenie–moneta. Trzysta wierszy nie oznacza trzystu niezależnych prób: pochodzą z 20 sygnałów, a potencjalnie nakładające się okresy obserwacji tworzą 7 grup wyodrębnionych z zachowaniem ostrożności.

## Zysk a przewaga nad BTC

| Wejście | Średnia stopa zwrotu netto altcoinów | Mediana stóp zwrotu netto altcoinów | Średnia stopa zwrotu netto BTC | Mediana stóp zwrotu netto BTC | Mediana różnicy altcoin − BTC (p.p.) |
| --- | --- | --- | --- | --- | --- |
| A | 5,96% | 3,59% | 11,51% | 5,56% | -6,00 |
| B | 2,84% | 2,22% | 8,01% | 4,94% | -5,02 |
| C | 0,25% | 3,39% | 6,49% | 5,78% | -6,73 |

| Wejście | Zysk po kosztach | Stopa zwrotu wyższa niż dla BTC | Zysk i przewaga jednocześnie |
| --- | --- | --- | --- |
| A | 62/100 (62,00%) | 34/100 (34,00%) | 30/100 (30,00%) |
| B | 55/100 (55,00%) | 37/100 (37,00%) | 30/100 (30,00%) |
| C | 57/100 (57,00%) | 34/100 (34,00%) | 29/100 (29,00%) |

![Średnia i mediana 90-dniowego wyniku netto pojedynczych altcoinów oraz dopasowanego BTC dla reguł A, B i C.](<wykresy/01_stopy_zwrotu.png>)

**Wykres 1. Średnia i mediana stóp zwrotu netto pojedynczych pozycji.** Każda reguła obejmuje 100 par altcoin–BTC z 20 wspólnych sygnałów. D oznacza datę świecy sygnałowej; C oznacza zakup na następnym otwarciu po powrocie RSI do co najmniej 30. BTC jest dopasowany według giełdy i dat. Brak przedziałów ufności: przedstawiono opis próby, a nie niezależnie losowane transakcje.

We wszystkich regułach średnia i mediana stóp zwrotu altcoinów były dodatnie, a transakcje z zyskiem były częstsze niż transakcje ze stratą. Jednocześnie średni wynik BTC był wyższy, mediany dopasowanych różnic altcoin–BTC były ujemne, a wyższą stopę zwrotu niż BTC uzyskano jedynie w 34–37 ze 100 porównań dla danej reguły. Dodatnia stopa zwrotu altcoina nie oznaczała więc zwykle lepszego wyboru niż BTC.

Średnie różnice wyników altcoinów wobec BTC wyniosły odpowiednio -5,55, -5,16 i -6,24 p.p. dla A, B i C. Medianę różnic obliczono z indywidualnych dopasowanych par; nie jest ona różnicą dwóch osobno wyznaczonych median. Wyniki zagregowane opisują tę próbę historyczną, bez testu istotności i bez twierdzenia o przewadze w przyszłości.

## Stopy zwrotu koszyków pięciu monet

Uzupełniająco obliczono stopę zwrotu koszyka jako średnią arytmetyczną pięciu stóp zwrotu w obrębie każdego zdarzenia. Taka średnia odpowiada osobnemu hipotetycznemu budżetowi dla sygnału, podzielonemu przy zakupie po 20% między monety, łącznie z kosztami wejścia, bez przywracania początkowych wag w okresie utrzymywania pozycji. To dodatkowe zestawienie opisowe wprowadzone podczas opracowywania wyników; podstawowy protokół ocenia monety oddzielnie. Nie wybrano wag na podstawie zysków.

Punkt odniesienia stanowi średnia pięciu stóp zwrotu BTC dopasowanych według giełdy i terminów, z zastosowaniem tych samych wag. W zdarzeniach z BSV lub TON część tego porównania pochodzi z KuCoin, a reszta z Binance. Nie jest to wtedy jeden kurs BTC z jednej giełdy. Dla każdego sygnału przyjęto odrębny budżet. Nie obliczano łącznej stopy zwrotu jednego portfela finansującego nakładające się inwestycje.

| Wejście | Mediana stóp zwrotu netto koszyków | Mediana stóp zwrotu netto dopasowanego BTC | Zysk | Przewaga nad BTC | Zysk i przewaga |
| --- | --- | --- | --- | --- | --- |
| A | 0,68% | 5,56% | 10/20 (50,00%) | 5/20 (25,00%) | 3/20 (15,00%) |
| B | 1,76% | 4,93% | 11/20 (55,00%) | 4/20 (20,00%) | 3/20 (15,00%) |
| C | 1,20% | 5,78% | 11/20 (55,00%) | 5/20 (25,00%) | 3/20 (15,00%) |

![Częstość zysku, przewagi nad BTC oraz ich jednoczesnego wystąpienia w 20 koszykach pięciu monet, dla każdej reguły wejścia.](<wykresy/02_zysk_i_przewaga_koszykow.png>)

**Wykres 2. Zysk koszyka pięciu monet i jego przewaga nad BTC.** Mianownik wynosi 20 zdarzeń w każdej regule. Początkowy budżet podzielono po 20% na monetę; dopasowany BTC zachowuje te same wagi giełd. Zestawienie opisowe dodano po wynikach indywidualnych. Przedstawione trzy kryteria mogą się nakładać i nie sumują się do 100%.

Mediana stóp zwrotu koszyków wyniosła od 0,68% do 1,76%, a częstość zysku 50–55%. Koszyk o takich równych udziałach pokonał dopasowany BTC w 4–5 z 20 zdarzeń. Zysk i przewaga wystąpiły razem w trzech zdarzeniach dla każdej reguły. Zestawienia dotyczą różnych jednostek obserwacji: pojedynczej monety i całego koszyka. Odsetki z obu poziomów analizy wymagają odrębnej interpretacji.

## Ryzyko w czasie utrzymywania

| Wejście | Mediana MAE altcoinów | Mediana MAE BTC | Mediana MDD altcoinów z cen zamknięcia | Mediana MDD BTC z cen zamknięcia |
| --- | --- | --- | --- | --- |
| A | -21,26% | -18,19% | -32,97% | -20,93% |
| B | -23,88% | -15,90% | -32,64% | -20,93% |
| C | -23,50% | -14,99% | -33,02% | -20,93% |

![Mediany największego spadku od wejścia i obsunięcia od szczytu ścieżki zamknięć, oddzielnie dla pojedynczych altcoinów i dopasowanego BTC.](<wykresy/04_ryzyko_pozycji.png>)

**Wykres 3. Mediany cenowych miar ryzyka pojedynczych pozycji.** Wartości bardziej ujemne oznaczają głębszy spadek. MAE wykorzystuje minima dzienne względem wejścia, a MDD wykorzystuje ścieżkę cen zamknięcia względem wcześniejszego szczytu. Obie miary zawierają punkty wejścia i wyjścia, pomijają koszty i nie opisują ryzyko całego koszyka.

We wszystkich trzech regułach mediany obu miar spadku były bardziej ujemne dla altcoinów niż dla dopasowanych inwestycji w BTC. Dla A mediana największego spadku od wejścia wyniosła −21,26% dla altcoinów i −18,19% dla BTC. Mediana obsunięcia od wcześniejszego szczytu ścieżki zamknięć wyniosła odpowiednio −32,97% i −20,93%.

MAE opisuje spadek względem ceny wejścia, a MDD względem wcześniejszego maksimum. Są to miary cenowe pojedynczych pozycji, bez kosztów. Nie opisują ryzyka koszyka pięciu monet: średnia indywidualnych dołków nie odtwarza wspólnej ścieżki wartości inwestycji. Dzienne zamknięcia nie obejmują całej zmienności śróddziennej.

## Porównanie reguł wejścia na wspólnej próbie

| Zmiana reguły | Pary / sygnały | Średnia różnica stóp zwrotu netto (p.p.) | Mediana zmiany (p.p.) | Dodatnia zmiana | Mediana przesunięcia wejścia (dni) |
| --- | --- | --- | --- | --- | --- |
| B − A | 100 / 20 | -3,12 | -5,62 | 31,00% | 6,0 |
| C − A | 100 / 20 | -5,72 | -2,66 | 33,00% | 2,5 |
| C − B | 100 / 20 | -2,60 | 1,10 | 54,00% | -3,5 |

W tabeli B − A oznacza wynik B pomniejszony o wynik A dla tej samej monety i tego samego sygnału. Reguła B dawała wyższy wynik niż A w 31% par, a reguła C wyższy niż A w 33%. Najwyższą średnią pojedynczych wyników uzyskano w regule A, a najwyższy odsetek przewag nad BTC w regule B. Dla reguły B uzyskano również najwyższą medianę stóp zwrotu koszyków pięciu monet. Wskazanie reguły zależy zatem także od wybranej miary.

Oczekiwanie na wejście przesuwało również wyjście, ponieważ każda inwestycja trwała 90 dni od własnej daty zakupu. Ujemna mediana przesunięcia C względem B oznacza, że zakup zgodny z regułą C następował zwykle wcześniej niż zakup zgodny z regułą B. Różnice nie izolują wpływu samej ceny zakupu. Nie wybrano na podstawie tych wyników uniwersalnie najlepszej reguły ani nie dopasowywano progu RSI.

## Wyniki według monet

Poniższe tabele obejmują każdą monetę, która zakwalifikowała się do pięciu najwyżej sklasyfikowanych altcoinów spełniających kryteria doboru. Liczebność zależy od udziału w rankingach konkretnych zdarzeń, a nie od późniejszego wyniku.

### Reguła A

| Moneta | Liczba zdarzeń | Średnia stopa zwrotu netto | Mediana stóp zwrotu netto | Zysk | Przewaga nad BTC | Mediana różnicy wobec BTC (p.p.) |
| --- | --- | --- | --- | --- | --- | --- |
| ADA | 13 | 1,80% | -2,63% | 6/13 (46,15%) | 4/13 (30,77%) | -11,03 |
| BCH | 1 | 77,74% | 77,74% | 1/1 (100,00%) | 0/1 (0,00%) | -27,58 |
| BNB | 19 | 6,13% | 7,83% | 14/19 (73,68%) | 6/19 (31,58%) | -4,91 |
| BSV | 1 | 90,01% | 90,01% | 1/1 (100,00%) | 0/1 (0,00%) | -14,74 |
| DOGE | 6 | 2,43% | 4,08% | 4/6 (66,67%) | 0/6 (0,00%) | -24,52 |
| ETH | 20 | 9,54% | 1,84% | 13/20 (65,00%) | 8/20 (40,00%) | -2,75 |
| LTC | 1 | 55,85% | 55,85% | 1/1 (100,00%) | 0/1 (0,00%) | -49,47 |
| SOL | 14 | -10,49% | -3,29% | 7/14 (50,00%) | 5/14 (35,71%) | -5,53 |
| TON | 3 | -20,02% | -25,25% | 0/3 (0,00%) | 0/3 (0,00%) | -31,96 |
| TRX | 2 | -3,06% | -3,06% | 0/2 (0,00%) | 2/2 (100,00%) | 22,97 |
| XRP | 20 | 12,03% | 17,76% | 15/20 (75,00%) | 9/20 (45,00%) | -1,03 |

### Reguła B

| Moneta | Liczba zdarzeń | Średnia stopa zwrotu netto | Mediana stóp zwrotu netto | Zysk | Przewaga nad BTC | Mediana różnicy wobec BTC (p.p.) |
| --- | --- | --- | --- | --- | --- | --- |
| ADA | 13 | 1,07% | -10,03% | 4/13 (30,77%) | 4/13 (30,77%) | -14,94 |
| BCH | 1 | 28,14% | 28,14% | 1/1 (100,00%) | 0/1 (0,00%) | -47,97 |
| BNB | 19 | 7,20% | 3,75% | 14/19 (73,68%) | 9/19 (47,37%) | -1,68 |
| BSV | 1 | 42,96% | 42,96% | 1/1 (100,00%) | 0/1 (0,00%) | -33,09 |
| DOGE | 6 | -3,02% | -4,52% | 2/6 (33,33%) | 0/6 (0,00%) | -29,82 |
| ETH | 20 | 7,08% | 7,05% | 12/20 (60,00%) | 7/20 (35,00%) | -2,84 |
| LTC | 1 | 26,06% | 26,06% | 1/1 (100,00%) | 0/1 (0,00%) | -50,06 |
| SOL | 14 | -15,34% | -16,23% | 5/14 (35,71%) | 5/14 (35,71%) | -9,09 |
| TON | 3 | -22,53% | -23,44% | 0/3 (0,00%) | 0/3 (0,00%) | -35,68 |
| TRX | 2 | 3,55% | 3,55% | 2/2 (100,00%) | 2/2 (100,00%) | 27,63 |
| XRP | 20 | 9,42% | 7,81% | 13/20 (65,00%) | 10/20 (50,00%) | -0,14 |

### Reguła C

| Moneta | Liczba zdarzeń | Średnia stopa zwrotu netto | Mediana stóp zwrotu netto | Zysk | Przewaga nad BTC | Mediana różnicy wobec BTC (p.p.) |
| --- | --- | --- | --- | --- | --- | --- |
| ADA | 13 | 0,22% | -8,86% | 5/13 (38,46%) | 5/13 (38,46%) | -11,53 |
| BCH | 1 | 8,54% | 8,54% | 1/1 (100,00%) | 0/1 (0,00%) | -44,61 |
| BNB | 19 | 3,20% | 4,70% | 14/19 (73,68%) | 7/19 (36,84%) | -4,89 |
| BSV | 1 | 12,07% | 12,07% | 1/1 (100,00%) | 0/1 (0,00%) | -41,06 |
| DOGE | 6 | -3,57% | -3,24% | 3/6 (50,00%) | 0/6 (0,00%) | -28,50 |
| ETH | 20 | 3,95% | 8,54% | 12/20 (60,00%) | 7/20 (35,00%) | -4,21 |
| LTC | 1 | 12,95% | 12,95% | 1/1 (100,00%) | 0/1 (0,00%) | -40,19 |
| SOL | 14 | -15,68% | -13,21% | 5/14 (35,71%) | 3/14 (21,43%) | -9,39 |
| TON | 3 | -24,13% | -24,90% | 0/3 (0,00%) | 0/3 (0,00%) | -35,23 |
| TRX | 2 | 1,57% | 1,57% | 1/2 (50,00%) | 2/2 (100,00%) | 26,44 |
| XRP | 20 | 7,93% | 11,70% | 14/20 (70,00%) | 10/20 (50,00%) | 0,32 |

ETH i XRP występowały w każdym z 20 zdarzeń, SOL w 14, a BCH, BSV i LTC tylko raz. Wynik TRX opiera się na dwóch zdarzeniach, TON na trzech. Odsetek 100% dla TRX nie stanowi mocnego dowodu powtarzalnej przewagi. Mediany różnych monet dotyczą częściowo innych sygnałów, więc nie tworzą porównania na identycznej próbie ani rankingu najlepszych inwestycji.

## Stabilność między okresami

| Okres sygnałów | Wejście | Sygnały / pary | Średnia stopa zwrotu netto altcoinów | Mediana stóp zwrotu netto altcoinów | Przewaga pojedynczej monety nad BTC |
| --- | --- | --- | --- | --- | --- |
| 2020-2022 | A | 12 / 60 | 10,24% | 7,53% | 26/60 (43,33%) |
| 2020-2022 | B | 12 / 60 | 6,66% | 2,63% | 29/60 (48,33%) |
| 2020-2022 | C | 12 / 60 | 2,86% | 5,53% | 26/60 (43,33%) |
| 2023-2025 | A | 8 / 40 | -0,45% | 2,50% | 8/40 (20,00%) |
| 2023-2025 | B | 8 / 40 | -2,88% | 1,57% | 8/40 (20,00%) |
| 2023-2025 | C | 8 / 40 | -3,68% | -0,50% | 8/40 (20,00%) |

| Okres sygnałów | Wejście | Mediana stóp zwrotu netto koszyków | Przewaga koszyka nad BTC |
| --- | --- | --- | --- |
| 2020-2022 | A | 0,68% | 5/12 (41,67%) |
| 2020-2022 | B | 3,65% | 4/12 (33,33%) |
| 2020-2022 | C | 2,72% | 5/12 (41,67%) |
| 2023-2025 | A | 2,64% | 0/8 (0,00%) |
| 2023-2025 | B | -0,59% | 0/8 (0,00%) |
| 2023-2025 | C | -1,43% | 0/8 (0,00%) |

![Mapa różnic netto koszyka pięciu monet wobec dopasowanego BTC: wszystkie 20 sygnałów i trzy reguły wejścia, w punktach procentowych.](<wykresy/03_przewaga_w_kazdym_zdarzeniu.png>)

**Wykres 4. Różnica wyników dla każdego sygnału.** Każda komórka oznacza średnią netto pięciu monet minus średnią dopasowanego BTC, w punktach procentowych. Skala barw jest symetryczna wokół zera: niebieski oznacza przewagę koszyka, pomarańczowy przewagę BTC. Linia rozdziela opisowe bloki dat sygnałów. Wiersze są kategoriami zdarzeń; odstępy na wykresie nie przedstawiają upływu czasu ani ścieżki jednego portfela.

W późniejszym okresie średnia stopa zwrotu pojedynczych altcoinów był ujemny we wszystkich trzech regułach, a przewaga nad BTC wystąpiła w 8 z 40 par, czyli 20%. Stopa zwrotu koszyka pięciu monet nie przewyższyła stopy zwrotu dopasowanego BTC w żadnym z ośmiu późniejszych zdarzeń. Obserwacja ta ogranicza argument za trwałością przewagi altcoinów w tej próbie.

Podział dotyczy dat sygnałów i ma charakter opisowy. Nie jest testem poza próbą wybranej wcześniej reguły. Sygnał z 2022-11-09 miał wyniki 90-dniowe poznane już po 2023-01-01: łącznie 15 wierszy monet i reguł. Gdyby wcześniejszy okres miał służyć wyborowi reguły przed tą datą, tych wyników nie wolno użyć. W opisowym zestawieniu zachowano wszystkie zdarzenia i nie wybierano reguły do wdrożenia.

## Wrażliwość na modelowane koszty

We wszystkich scenariuszach prowizja wynosi 0,10% po każdej stronie. Zmieniono jedynie niekorzystny poślizg zgodnie z wariantami zapisanymi przed oceną pełnych wyników.

| Poślizg po każdej stronie | Wejście | Średnia stopa zwrotu netto altcoinów | Mediana stóp zwrotu netto altcoinów | Zysk | Przewaga nad BTC |
| --- | --- | --- | --- | --- | --- |
| Podstawowy: 0,05% | A | 5,96% | 3,59% | 62/100 (62,00%) | 34/100 (34,00%) |
| Podstawowy: 0,05% | B | 2,84% | 2,22% | 55/100 (55,00%) | 37/100 (37,00%) |
| Podstawowy: 0,05% | C | 0,25% | 3,39% | 57/100 (57,00%) | 34/100 (34,00%) |
| Bez poślizgu: 0% | A | 6,07% | 3,69% | 62/100 (62,00%) | 34/100 (34,00%) |
| Bez poślizgu: 0% | B | 2,95% | 2,33% | 56/100 (56,00%) | 37/100 (37,00%) |
| Bez poślizgu: 0% | C | 0,35% | 3,49% | 57/100 (57,00%) | 34/100 (34,00%) |
| Wyższy poślizg: 0,20% | A | 5,65% | 3,28% | 62/100 (62,00%) | 34/100 (34,00%) |
| Wyższy poślizg: 0,20% | B | 2,54% | 1,92% | 54/100 (54,00%) | 37/100 (37,00%) |
| Wyższy poślizg: 0,20% | C | -0,05% | 3,08% | 54/100 (54,00%) | 34/100 (34,00%) |

Wyższe koszty zmniejszają stopy zwrotu i mogą zmienić ocenę zysku. Przy zastosowaniu identycznego dodatniego mnożnika kosztów do altcoina i BTC kolejność ich wyników pozostaje jednak taka sama. Niezmienny odsetek przewag w tabeli wynika z konstrukcji modelu; nie dowodzi odporności na rzeczywiste różnice płynności i prowizji między aktywami. Wynik reguły C, którego średnia netto w scenariuszu podstawowym wynosi tylko 0,25%, wymaga szczególnej ostrożności wobec kosztów.

## Maksymalne obsunięcie kapitału koszyka

Uzupełniająco odtworzono wartość każdego pięcioelementowego koszyka oraz dopasowanej inwestycji w BTC w trakcie 90 dni. Dla każdego sygnału i reguły przyjęto osobny budżet 1 000 USDT. Wyniki procentowe nie zależą od tej skali przy proporcjonalnych kosztach i pominięciu zaokrągleń giełdowych. Maksymalne obsunięcie (MDD) opisuje największy spadek od wcześniejszego maksimum wartości kapitału, a nie wyłącznie stratę względem początkowego wydatku.

| Reguła | Mediana MDD koszyka | Mediana MDD BTC | Największe obsunięcie koszyka | Największe obsunięcie BTC | Płytsze MDD koszyka niż BTC |
| --- | --- | --- | --- | --- | --- |
| A | −26,85% | −20,93% | −54,76% | −40,35% | 1/20 |
| B | −26,72% | −20,93% | −45,31% | −40,35% | 2/20 |
| C | −26,80% | −20,93% | −44,89% | −40,35% | 3/20 |

![Mediany i najgłębsze obsunięcia kapitału koszyków oraz dopasowanego BTC dla trzech reguł wejścia.](<wykresy/05_obsuniecie_kapitalu.png>)

**Wykres 5. Maksymalne obsunięcie kapitału.** Mediana obejmuje 20 osobnych zdarzeń w każdej regule. Najgłębsze obsunięcie jest skrajną obserwacją w danej grupie; po stronie altcoinów i BTC może pochodzić z innych sygnałów. Wartości ujemne oznaczają spadek względem wcześniejszego szczytu. Im dalej od zera, tym głębsze obsunięcie.

Mediany MDD koszyków mieściły się w przybliżeniu w przedziale od −26,8% do −26,7%, wobec −20,93% dla BTC. Koszyk miał płytsze obsunięcie niż dopasowany BTC w 1/20 zdarzeń w regule A, 2/20 w B i 3/20 w C. Uzupełnienie wskazuje zatem na głębsze obsunięcia koszyków w większości porównań tej próby.

Największe obsunięcie koszyka wystąpiło w regule A po sygnale z 17 maja 2021 r. i wyniosło −54,76%. Dla reguł B i C najgłębsze obsunięcia wyniosły odpowiednio −45,31% i −44,89%, po sygnale z 21 maja 2021 r. Największe obsunięcie dopasowanego BTC wyniosło −40,35% w każdej regule, po sygnale z 9 maja 2022 r. Są to daty sygnałów; daty szczytu i dołka zapisano oddzielnie w tabeli szczegółowej.

Wyceny uwzględniają początkową gotówkę, wartość rynkową zaraz po zakupie, 90 dziennych zamknięć UTC i końcowy wpływ po sprzedaży. Koszty naliczono przy modelowanym zakupie i sprzedaży; nie odejmowano hipotetycznej prowizji sprzedaży przy każdej wycenie dziennej. Ta miara dotyczy kapitału całego koszyka, w odróżnieniu od wcześniej opisanych cenowych MDD pojedynczych monet. Nie jest średnią ich obsunięć.

Analizę dodano po opracowaniu pierwotnych wyników jako opisowe rozszerzenie. Dzienne wyceny nie odtwarzają obsunięć wewnątrz dnia. Nie połączono nakładających się inwestycji w jedną ścieżkę konta za lata 2020–2025. Dane szczegółowe: data/analysis/basket_capital_risk_90d.csv; pełne ścieżki: data/analysis/basket_capital_path_90d.csv. Końcowe kwoty wszystkich 60 ścieżek są zgodne z wcześniej obliczonymi zwrotami netto koszyków i BTC.



## Odpowiedź na pytania badawcze i ograniczenia

Zakup wybranych altcoinów przynosił w tej próbie dodatnie pojedyncze wyniki w 55–62% przypadków zależnie od reguły. Przy równych udziałach pięciu monet częstość dodatniego wyniku zdarzenia wynosiła 50–55%. Nie oznaczało to zwykle przewagi nad zakupem BTC: większość dopasowanych porównań przegrywała z BTC, a średnie i mediany różnic były ujemne.

Termin wejścia zmieniał wyniki, lecz żadna reguła nie dała jednocześnie przewagi altcoinów nad BTC w większości przypadków oraz niższych median badanych miar spadku. Wyniki stanowią opis warunkowej symulacji historycznej. Nie potwierdzają ogólnej skuteczności zakupu altcoinów po wyprzedaniu BTC ani gwarantowanego momentu wejścia.

Siłę wniosków ogranicza 20 sygnałów, ich koncentracja w części lat, współzależność monet i nakładanie się okresów. Rankingi poprzedzają sygnały o 1–5 dni, a ich historyczne godziny publikacji pozostają niepotwierdzone. Dostępność rankingu w chwili decyzji jest założeniem. Ceny otwarcia i koszty są modelem wykonania bez rekonstrukcji arkusza zleceń, wielkości zlecenia, zaokrągleń giełdowych i przepływów kapitału między zdarzeniami. Wyniki w USDT nie są wynikami w USD. Te ograniczenia dotyczą również dodatnich wyników.

## Kontrola i możliwość odtworzenia

Sprawdzono sumy SHA-256 34 użytych plików źródłowych cen oraz zgodność cen z oryginalnymi rekordami. Pełna tabela odtworzyła wcześniej sprawdzony przypadek kontrolny ETH–BTC. Sześć testów objęło między innymi daty wejścia, brak powrotu RSI, koszty, rozróżnienie MAE/MDD i zachowanie wszystkich pięciu udziałów.

Niezależna kontrola pandas odtworzyła przepływy dla hipotetycznego wydatku 1 000 USDT, daty, miary ryzyka, mianowniki odsetków i średnie zdarzeń. Największa różnica stopy netto między obliczeniami wyniosła mniej niż 0,000000000001; nie wpływa na prezentowane zaokrąglenia. Raporty kontroli nie usuwają ograniczeń jakości historycznego źródła ani założeń wykonania.

Pełne dane: data/analysis/trades_90d.csv; średnie zdarzeń: data/analysis/event_mean_returns_90d.csv; scenariusze kosztów: data/analysis/cost_scenarios_90d.csv. Raporty: reports/backtest_90d.json, reports/event_aggregation_90d.json i reports/trade_output_validation.json. Obliczenia: scripts/analyze_trades.py, scripts/aggregate_event_results.py oraz scripts/validate_trade_outputs.py. Tabele zaokrąglono dopiero przy prezentacji.

## Zestawienie wszystkich sygnałów

Poniższe wartości są stopami zwrotu netto koszyków pięciu monet dla poszczególnych sygnałów i reguł wejścia. Nie sumowano ich ani nie traktowano jako kolejnych zmian wartości jednego portfela. Właściwy skład pochodzi z rankingu przypisanego osobno do każdego zdarzenia.

| Data sygnału UTC | Monety | Zwrot netto koszyka A | Zwrot netto koszyka B | Zwrot netto koszyka C |
| --- | --- | --- | --- | --- |
| 2020-03-12 | BCH, BSV, ETH, LTC, XRP | 80,46% | 45,17% | 24,32% |
| 2021-05-17 | ADA, BNB, DOGE, ETH, XRP | -11,47% | 53,25% | -0,26% |
| 2021-05-21 | ADA, BNB, DOGE, ETH, XRP | 26,07% | 25,06% | 26,83% |
| 2022-01-07 | ADA, BNB, ETH, SOL, XRP | -4,64% | -14,18% | -6,02% |
| 2022-01-21 | ADA, BNB, ETH, SOL, XRP | 1,44% | 3,13% | 6,12% |
| 2022-01-26 | ADA, BNB, ETH, SOL, XRP | -0,07% | -9,79% | 3,13% |
| 2022-05-09 | ADA, BNB, ETH, SOL, XRP | -17,34% | -9,62% | -3,88% |
| 2022-06-13 | ADA, BNB, ETH, SOL, XRP | 24,56% | 14,45% | 2,32% |
| 2022-07-01 | ADA, BNB, ETH, SOL, XRP | 22,28% | 10,21% | 9,07% |
| 2022-08-28 | ADA, BNB, ETH, SOL, XRP | -12,33% | -16,35% | -17,01% |
| 2022-09-06 | ADA, BNB, ETH, SOL, XRP | -15,12% | -25,56% | -18,56% |
| 2022-11-09 | ADA, BNB, DOGE, ETH, XRP | 29,06% | 4,18% | 8,30% |
| 2023-03-09 | ADA, BNB, DOGE, ETH, XRP | 13,02% | 0,39% | 13,52% |
| 2023-08-17 | ADA, BNB, DOGE, ETH, XRP | 27,63% | 14,41% | 16,97% |
| 2024-06-24 | BNB, ETH, SOL, TON, XRP | -2,55% | -1,56% | -2,94% |
| 2024-07-04 | BNB, ETH, SOL, TON, XRP | -2,07% | -3,61% | -5,35% |
| 2024-08-05 | BNB, ETH, SOL, TON, XRP | 7,92% | 14,29% | 0,08% |
| 2025-02-25 | BNB, DOGE, ETH, SOL, XRP | 7,35% | 6,14% | 4,08% |
| 2025-11-17 | BNB, ETH, SOL, TRX, XRP | -27,67% | -23,28% | -28,66% |
| 2025-11-19 | BNB, ETH, SOL, TRX, XRP | -27,23% | -29,83% | -27,12% |


# 5. Dyskusja i wnioski

## Odpowiedzi na pytania badawcze

W analizowanym horyzoncie 90 dni dodatnim stopom zwrotu altcoinów często towarzyszyły wyższe stopy zwrotu BTC. Ocena reguły wymaga zatem uwzględnienia zarówno zysku po kosztach, jak i porównania z alternatywną inwestycją.

| Pytanie badawcze | Odpowiedź na podstawie badanej próby |
| --- | --- |
| Czy wybrane altcoiny przynosiły zysk po kosztach? | Zysk wystąpił w 55–62 ze 100 pojedynczych porównań, w zależności od reguły. Mediany stóp zwrotu netto wyniosły A: 3,59%, B: 2,22%, C: 3,39%. Przy równych udziałach pięciu monet zysk wystąpił w 10–11 z 20 zdarzeń. |
| Czy altcoiny były lepszym wyborem niż BTC w tych samych terminach? | Wyższą stopę zwrotu niż BTC uzyskano w 34–37 ze 100 pojedynczych porównań. Średnie i mediany dopasowanych różnic były ujemne we wszystkich trzech regułach. Stopa zwrotu koszyka pięciu monet przewyższyła stopę zwrotu dopasowanego BTC w 4–5 z 20 zdarzeń. |
| Jak reguła wejścia zmieniała wynik i ryzyko? | Dla reguły A uzyskano najwyższą średnią stóp zwrotu monet. Reguła B miała najwyższy odsetek przewag nad BTC oraz najwyższą medianę stóp zwrotu koszyków. Mediany obu miar wskazywały na większe spadki cen altcoinów niż BTC. Wybór reguły zależy od przyjętego kryterium. |

Liczebności w tabeli opisują tę samą próbę, obejmującą zależne obserwacje. Każda reguła wykorzystuje 20 wspólnych sygnałów, a każdemu sygnałowi odpowiada pięć monet. Nie należy traktować 300 wierszy jako 300 niezależnych potwierdzeń skuteczności.

## Znaczenie porównania z BTC

Średnia stopa zwrotu netto pojedynczych altcoinów wyniosła 5,96% dla A, 2,84% dla B i 0,25% dla C. Odpowiadające średnie BTC wyniosły 11,51%, 8,01% i 6,49%. Średnia różnica altcoin minus BTC była zatem ujemna: odpowiednio −5,55, −5,16 i −6,24 punktu procentowego.

Samo wskazanie dodatnich stóp zwrotu mogłoby prowadzić do zbyt korzystnej oceny zakupu altcoinów. Dopasowanie BTC według giełdy oraz dat wejścia i wyjścia pokazuje, jaki wynik osiągała porównywana alternatywa w tym samym okresie. Wynik dodatni, lecz niższy od BTC, spełnia kryterium zysku i jednocześnie nie spełnia kryterium przewagi.

Mediana stóp zwrotu pojedynczych monet i mediana stóp zwrotu koszyków dla reguły A wyniosły odpowiednio 3,59% i 0,68%. Pierwszą obliczono ze 100 stóp zwrotu poszczególnych pozycji, a drugą z 20 stóp zwrotu koszyków. Stopa zwrotu koszyka jest średnią wyników pięciu monet przy równych początkowych udziałach po 20% i odrębnym budżecie dla każdego sygnału. Zestawienie koszyków dodano jako opisowe uzupełnienie po obliczeniu wyników indywidualnych.

## Termin wejścia i ryzyko

Porównanie A, B i C dotyczy pełnych reguł transakcji. Przesunięcie wejścia powoduje przesunięcie wyjścia, ponieważ każda pozycja jest utrzymywana przez 90 dni od własnego zakupu. Różnica wyników obejmuje więc inny okres ekspozycji na rynek. Nie pozwala przypisać całego efektu wyłącznie lepszej lub gorszej cenie zakupu.

Najwyższą średnią zwrotów netto pojedynczych monet uzyskano w wariancie A. Reguła B zapewniła natomiast najwyższą częstość przewag nad BTC: 37%. Najwyższa mediana stóp zwrotu koszyków również wystąpiła w regule B i wyniosła 1,76%. Żadna z tych obserwacji nie oznacza przewagi altcoinów nad BTC w większości zdarzeń.

Przykładowo dla A mediana spadku od wejścia wyniosła −21,26% dla altcoinów i −18,19% dla dopasowanego BTC. Mediana obsunięcia od szczytu ścieżki zamknięć wyniosła −32,97% i −20,93%. Dodatni wynik przy sprzedaży mógł zatem wymagać utrzymywania pozycji podczas znacznego spadku ceny. Te miary odnoszą się do pojedynczych pozycji, nie zawierają kosztów i nie opisują całej śróddziennej ścieżki ryzyka.

W osobnym uzupełnieniu odtworzono wspólną wartość pięciu monet w każdym zdarzeniu. Mediany MDD kapitału koszyków wyniosły −26,85%, −26,72% i −26,80% dla A, B i C, wobec −20,93% dla dopasowanego BTC. Koszyk miał płytsze obsunięcie w odpowiednio 1, 2 i 3 z 20 zdarzeń. Najgłębsze obsunięcie koszyka sięgnęło −54,76%. Wyniki opisują osobne 90-dniowe inwestycje z kosztami wejścia i wyjścia. Nie są obsunięciem jednego konta finansującego wszystkie nakładające się sygnały.

## Stabilność i wpływ kosztów

Dla sygnałów z lat 2023–2025 średnia stopa zwrotu altcoinów była ujemna we wszystkich regułach. Stopa zwrotu koszyka pięciu monet nie przewyższyła stopy zwrotu dopasowanego BTC w żadnym z ośmiu zdarzeń. To ogranicza argument za powtarzalną przewagą altcoinów w badanej próbie. Podział jest opisowy: nie przeprowadzono wyboru reguły na wcześniejszych danych i niezależnego testu na późniejszych.

Wrażliwość kosztowa pokazuje również, że niewielka dodatnia średnia wymaga ostrożnej interpretacji. Dla C zwiększenie modelowego poślizgu z 0,05% do 0,20% po każdej stronie zmieniło średnią stopę zwrotu netto pojedynczych altcoinów z 0,25% na −0,05%. Wszystkie te wartości są scenariuszami obliczeniowymi, a nie pomiarem historycznego kosztu wykonania zleceń.

Niezmienny odsetek przewag nad BTC w scenariuszach kosztowych wynika z zastosowania tego samego mnożnika kosztów do obu stron porównania. Ocena odporności na rzeczywistą różnicę płynności między BTC a altcoinami wymagałaby kosztów zależnych od aktywa, giełdy i wielkości zlecenia.

## Granice odpowiedzi i wiarygodność badania

Badanie ocenia wybór altcoinów względem BTC pod warunkiem wystąpienia określonego sygnału RSI. Ocena, czy sam sygnał poprawia moment zakupu, wymagałaby dodatkowego porównania z odpowiednio zdefiniowanymi wejściami w innych terminach lub inną regułą odniesienia. Wzrost ceny po sygnale sam w sobie tego nie rozstrzyga.

Historyczny dobór pięciu monet jest ponawiany dla każdego sygnału. Zastosowanie wcześniejszych rankingów ogranicza wykorzystanie późniejszej informacji o kapitalizacji, lecz nie rozwiązuje całego problemu dostępności danych. Zestawienia są wcześniejsze o 1–5 dni, a dokładne historyczne godziny ich publikacji nie są potwierdzone. Odtworzony koszyk jest przybliżeniem składu dostępnego w chwili decyzji. To założenie wpływa na interpretację zarówno zysków, jak i strat.

Pozostałe ograniczenia obejmują małą liczbę sygnałów, ich koncentrację w wybranych latach, współzależność monet, nakładanie się okresów oraz różnice giełd. Nie przeprowadzono formalnego testu istotności. Dzienne świece i modelowe koszty nie potwierdzają możliwości wykonania konkretnego zlecenia po podanej cenie. Wyniki dotyczą USDT; nie przeliczano ich na USD ani PLN i nie uwzględniano podatków.

Rzetelność obliczeń wspierają zachowane pliki źródłowe, kontrola ich integralności, jawne pochodzenie cen oraz zgodność z niezależnym przeliczeniem. Te kontrole pozwalają odtworzyć analizę i wykryć zmianę plików. Nie potwierdzają historycznej dostępności rankingu ani rzeczywistych warunków wykonania.

## Wniosek końcowy i dalsza praca

W badanej próbie sygnałów z lat 2020–2025 zakup pięciu historycznie dobranych altcoinów dawał dodatnie wyniki w części przypadków, lecz zwykle nie przewyższał zakupu dopasowanego BTC. Statystyki opisowe nie dostarczają podstaw do stwierdzenia przewagi altcoinów dla przyjętego horyzontu 90 dni i modelu kosztów. Różne reguły wejścia zmieniały wyniki, ale nie pozwoliły wskazać jednego powszechnie najlepszego terminu zakupu.

Dalsze badanie powinno zweryfikować historyczną dostępność rankingów i koszty zależne od płynności. Horyzonty 30 i 180 dni oraz inne terminy wejścia wymagają zapisania reguł przed obliczeniami. Powtarzalność należy ocenić na nowych danych, bez dostrajania do okresu oceny. Tych rozszerzeń nie wykonano.


# 6. Odtworzenie analizy i źródła

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
| raport/RAPORT.md | Główny dokument, składany z fragmentów raportu. |
| raport/wykresy/ | Pięć wykresów w PNG i SVG; dane pierwszych czterech w dane_do_wykresow.csv, piątego w data/analysis/summary_basket_capital_risk_90d.csv. |
| tableau/Altcoiny_RSI_BTC.twbx oraz tableau/INSTRUKCJA.md | Przenośny pakiet interaktywnych dashboardów i instrukcja filtrów oraz agregacji. |
| docs/ | Źródła, słowniki i dokumentacja metodologii. |

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

