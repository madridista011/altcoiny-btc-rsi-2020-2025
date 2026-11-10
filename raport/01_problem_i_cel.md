# Problem i cel studium przypadku

Status: cel zredagowany na podstawie wypowiedzi autora; zakres przyjęty w rozmowie. Fragment rozpoczynający raport do projektu Google Data Analytics; nie zawiera wniosków z wyników inwestycji.

## Roboczy tytuł

„Stopy zwrotu największych altcoinów po sygnałach wyprzedania Bitcoina: porównanie z BTC i analiza momentu wejścia w latach 2020–2025”.

## Cel — wersja po redakcji wypowiedzi autora

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

