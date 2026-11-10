# Założenia kosztów — propozycja robocza

Status: roboczy scenariusz symulacji użyty w pierwszym przykładzie kontrolnym na historycznych cenach. Nie jest odtworzeniem rzeczywistych historycznych opłat użytkownika lub wszystkich giełd. Pełnej oceny strategii jeszcze nie wykonano; protokół roboczy zapisano w config/trade_protocol_v1.json przed obliczeniem przykładu.

## Scenariusz podstawowy — propozycja

| Parametr | Zakup | Sprzedaż |
| --- | --- | --- |
| Prowizja od wartości wykonanej transakcji | 0,10% | 0,10% |
| Niekorzystny poślizg względem ceny referencyjnej | 0,05% | 0,05% |

To robocze wartości modelowe, wybrane do przejrzystego porównania reguł. Nie są skalibrowane do historycznych arkuszy zleceń ani indywidualnych poziomów prowizji. Wspólny scenariusz dla altcoinów i BTC upraszcza porównanie, ale nie dowodzi identycznej płynności i kosztów rzeczywistych. Przed przykładem kontrolnym zapisano także warianty wrażliwości: ta sama prowizja z poślizgiem 0% oraz z poślizgiem 0,20% po każdej stronie. Nie oceniano jeszcze ich wyników.

## Znaczenie pojęć

Prowizja jest opłatą za wykonanie transakcji. W modelu naliczamy ją od wartości zakupu i od wartości sprzedaży oraz rozliczamy w USDT.

Poślizg jest różnicą między ceną referencyjną a ceną wykonania. W tej symulacji przyjmujemy poślizg niekorzystny: zakup następuje drożej, a sprzedaż taniej niż wskazywałaby sama cena referencyjna.

Przykład fikcyjny: przy cenie referencyjnej 100 USDT i poślizgu 0,05% modelowa cena zakupu wynosi 100,05 USDT, a modelowa cena sprzedaży 99,95 USDT. Prowizję naliczamy osobno. To przykład działania modelu, nie ceny z badania.

## Wzór obliczeń

Dla tej samej liczby jednostek aktywa, prowizji f oraz poślizgu s po obu stronach:

stopa netto = [cena wyjścia × (1 − s) × (1 − f)] / [cena wejścia × (1 + s) × (1 + f)] − 1

Parametry jako ułamki: f = 0,001; s = 0,0005. Cena wejścia i wyjścia to ceny referencyjne zgodne z regułą transakcji. Model zakłada prowizję zakupu doliczaną do wydatku oraz prowizję sprzedaży potrącaną z wpływu. Wzór nie jest modelem portfela ani dowodem wykonalności realizacji o danej cenie.

## Zastosowanie w projekcie

Model zastosowano do pierwszej chronologicznej okazji: ETH i BTC, wejście na otwarciu 2020-03-13 i wyjście na otwarciu 2020-06-11, po 90 dniach. Ceny, wynik brutto i wynik netto opisano w 03_pierwsze_zdarzenie.md. To kontrola konstrukcji wiersza analizy; wnioski o skuteczności strategii wymagają wszystkich ustalonych zdarzeń i reguł.
