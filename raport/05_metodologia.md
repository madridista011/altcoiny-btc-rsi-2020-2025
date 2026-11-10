# Metodologia analizy

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
