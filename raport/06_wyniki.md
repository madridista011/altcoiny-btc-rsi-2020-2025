# Wyniki analizy 90-dniowej

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
