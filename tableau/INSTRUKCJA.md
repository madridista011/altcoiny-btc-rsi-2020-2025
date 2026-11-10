# Interaktywne wykresy w Tableau

Otwórz **Altcoiny_RSI_BTC.twbx** w Tableau Public. To docelowy plik z dashboardami i dwoma osadzonymi ekstraktami danych. Do oglądania oraz filtrowania nie trzeba podłączać CSV. Plik sprawdzono w zainstalowanym Tableau Public 2026.2.

## Pierwsze użycie

1. Zmaksymalizuj okno Tableau. Gdy panel **Show Me** zasłania wykresy, schowaj go tym samym przyciskiem.
2. Na dolnym pasku wybierz zakładkę **MONETY - porównanie z BTC** albo **KOSZYKI 5 - porównanie z BTC**. Są za zakładkami pojedynczych wykresów.
3. Rozwiń filtr po prawej. Aby wybrać jedną pozycję, odznacz **(All)**, a potem zaznacz np. **SOL** lub **XRP**. Zaznaczenie **(All)** przywraca pełny wybór.
4. Łącz filtry reguły, okresu i daty sygnału. Dotyczą wszystkich wykresów danego dashboardu. Jeżeli ich przecięcie nie zawiera danych, wykres będzie pusty.
5. Najedź na słupek lub komórkę, aby odczytać szczegóły. Kliknięcie znaku może go wyróżnić; kliknięcie pustego miejsca usuwa zaznaczenie.

## Dwa poziomy analizy

| Dashboard | Zawartość | Filtry |
| --- | --- | --- |
| MONETY | Mediana zwrotu netto altcoinów i dopasowanego BTC, częstość zysku i przewagi, mediany MAE i MDD. | Moneta, reguła wejścia, okres sygnałów, data sygnału. |
| KOSZYKI 5 | Częstość zysku i przewagi pełnego koszyka, mediana zwrotu koszyka i BTC, mapa różnic w każdym sygnale. | Reguła wejścia, okres sygnałów, data sygnału. |

W widoku monet przed filtrowaniem jest **100 par zdarzenie–moneta na regułę**, czyli 300 wierszy dla A/B/C. W widoku koszyków jest **20 zdarzeń na regułę**, czyli 60 wierszy. Liczebności w bocznym opisie oznaczają pełną próbę. Podpowiedź słupka lub komórki pokazuje **liczbę par lub koszyków po filtrach** oraz **liczbę odrębnych sygnałów w danym znaku**. Tych liczebności nie należy sumować między miarami ani regułami: dotyczą powiązanych obserwacji. SOL występuje w 14 sygnałach, XRP w 20. Wybór SOL nie dodaje jej do wcześniejszych koszyków.

Filtr monety nie zmienia dashboardu koszyków. Koszyki zachowują historycznie dobrane pięć monet i równe początkowe udziały po 20%. BTC ma dopasowane terminy i wagi giełd. To wyniki osobnych hipotetycznych budżetów zdarzeń, bez wspólnej ścieżki kapitału.

## Jak czytać wyniki

- **A** — wejście na otwarciu D+1 po świecy sygnałowej. **B** — otwarcie D+7 od daty tej świecy. **C** — następne otwarcie po pierwszym powrocie RSI do co najmniej 30 w dniach D+1–D+30. Każde wyjście następuje T+90 od faktycznego wejścia.
- Wykresy stóp zwrotu, MAE i MDD pokazują **mediany**. Wykresy częstości pokazują średnią flag 0/1 wyrażoną w procentach, czyli odsetek obserwacji spełniających warunek. Przy jednej dacie sygnału koszyk ma jedną obserwację na regułę, więc jego kryterium wynosi 0% albo 100%.
- **Zysk netto**: stopa zwrotu altcoina lub koszyka po kosztach > 0. **Przewaga**: stopa zwrotu netto wyższa niż dla dopasowanego BTC. **Oba warunki**: zysk netto i przewaga jednocześnie. Osiągnięcie zysku nie musi oznaczać pokonania BTC.
- Niebieskie słupki porównania zwrotu i ryzyka oznaczają altcoiny, pomarańczowe — BTC. Procenty sukcesów mają osobne kolory i podpisy.
- **MAE** to największy spadek ceny względem wejścia. **MDD** to największe obsunięcie od wcześniejszego maksimum ścieżki zamknięć z cenami wejścia i wyjścia. Pokazujemy mediany miar pojedynczych pozycji; nie jest to ryzyko całego koszyka. Wartość bliższa zeru oznacza mniejszy spadek.
- Mapa koszyków pokazuje **różnicę zwrotów netto w punktach procentowych**. Wartość dodatnia oznacza przewagę koszyka, ujemna — BTC. Skala kolorów dostosowuje się do filtrów; porównuj także liczby i aktualną legendę.

Ceny są wyrażone w USDT, stopy zwrotu i spadki w procentach, a różnice stóp zwrotu na mapie w punktach procentowych. Model uwzględnia 0,10% prowizji i 0,05% niekorzystnego poślizgu przy zakupie oraz sprzedaży. MAE i MDD są miarami cenowymi, bez tych kosztów. Dwadzieścia sygnałów i ich monety są zależne. Rankingi poprzedzają sygnał o 1–5 dni; ich historyczne godziny publikacji pozostają niepotwierdzone. Dashboard opisuje tę próbę, bez formalnego testu istotności ani potwierdzenia skuteczności strategii w przyszłości.

## Trzy przykłady z projektu

| Ustawienie | Odczyt kontrolny |
| --- | --- |
| MONETY → Moneta: XRP; pozostałe: All | Mediany netto XRP: A 17,76%, B 7,81%, C 11,70%; po 20 obserwacji. |
| MONETY → Moneta: SOL; pozostałe: All | Mediany netto SOL: A −3,29%, B −16,23%, C −13,21%; po 14 obserwacji. |
| KOSZYKI 5 → Okres: 2023–2025; pozostałe: All | Koszyk pokonał BTC w 0 z 8 sygnałów w każdej regule. |

## Pliki i odtworzenie

**Altcoiny_RSI_BTC.twbx** jest finalnym pakietem. Skoroszytu nie opublikowano w Tableau Public.

CSV **monety.csv** i **koszyki.csv** pochodzą odpowiednio z data/analysis/trades_90d.csv i event_mean_returns_90d.csv. Skrypt scripts/prepare_tableau.py przygotowuje oba poziomy bez zmiany wyników. Stopy zwrotu są ułamkami (0.05 = 5%), PrzewagaPP jest już w punktach procentowych. Zapis: UTF-8 BOM, przecinek jako separator, kropka dziesiętna. Przy ponownym imporcie CSV ustaw poprawną interpretację liczb i sprawdź wartości kontrolne.

Nie łącz fizycznie tabel koszyków i monet: powielenie wierszy może zniekształcić statystyki i filtry. Nie sumuj stóp zwrotu do wykresów porównawczych. Zwroty i ryzyko agregujemy medianą, a flagi sukcesu średnią.

Natywne ekstrakty utworzono w Tableau Public. W repozytorium znajduje się gotowy, przenośny pakiet TWBX. Skrypt scripts/prepare_tableau.py przygotowuje tabele CSV z wyników analizy. Mediany, częstości i dane ekstraktów sprawdzono przed publikacją. Ponowne utworzenie ekstraktów wymaga Tableau Public.

Pakiet przechowuje statyczny stan analizy. Nowy eksport CSV nie odświeża automatycznie ekstraktów. Zmiana danych wymaga odtworzenia ekstraktów w Tableau, ponownego eksportu i sprawdzenia wyników. Do normalnego korzystania wystarczy plik TWBX.

Uzupełniająca analiza maksymalnego obsunięcia kapitału całych koszyków jest dostępna w pełnym raporcie, na stronie projektu oraz w data/analysis/basket_capital_risk_90d.csv i basket_capital_path_90d.csv. Nie została dodana do ekstraktów tego skoroszytu. Jej definicja różni się od cenowych MAE/MDD pojedynczych pozycji; szczegóły podaje docs/OBSUNIECIE_KAPITALU.md.

Oznaczenie źródeł: **Data: CryptWatch, based on CoinMarketCap**. Ceny: Binance Spot / Binance Vision oraz KuCoin. Metodologię i warunki korzystania ze źródeł opisano w raporcie oraz w pliku docs/ZRODLA_DANYCH.md.

## Zasady prezentacji analizy

Redakcja odwołuje się do zasad rozumienia problemu, oceny wyniku względem celu oraz wyjaśniania ograniczeń danych omawianych w książce: Foster Provost, Tom Fawcett, *Analiza danych w biznesie. Sztuka podejmowania skutecznych decyzji*, tłum. Leszek Sielicki, Helion, 2014. Dashboard prowadzi od pytania o zysk i przewagę nad BTC do porównania wyników i oceny spadków. Podaje jednostki, agregację oraz liczebność próby. Są to samodzielnie zredagowane opisy; książka nie stanowi źródła danych inwestycyjnych projektu.
