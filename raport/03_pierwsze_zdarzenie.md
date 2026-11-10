# Przykład kontrolny na rzeczywistych danych: ETH i BTC

## Zdarzenie i reguła

Pierwszy chronologiczny sygnał BTC w badaniu: **2020-03-12**. Ranking z **2020-03-08** kwalifikował ETH do historycznego top 5. Wybrano pierwszą monetę pierwszego zdarzenia według kolejności danych, bez oceny jej późniejszego wyniku.

Reguła A: zakup na otwarciu **2020-03-13**, sprzedaż na otwarciu **2020-06-11**, po **90 dniach kalendarzowych**. Ceny referencyjne obu aktywów: Binance Spot, USDT. Protokół reguł zapisano w config/trade_protocol_v1.json przed tym obliczeniem.

## Wynik kontrolny

| Aktywo | Otwarcie przy wejściu, USDT | Otwarcie przy wyjściu, USDT | Stopa brutto | Stopa netto w scenariuszu |
| --- | ---: | ---: | ---: | ---: |
| ETH | 107,67 | 247,78 | 130,13% | 129,44% |
| BTC | 4800,01 | 9885,22 | 105,94% | 105,32% |

Różnica ETH minus BTC: **24,19 punktu procentowego brutto** i **24,11 punktu procentowego netto**.

Różnice obliczamy przed zaokrągleniem prezentowanych stóp, dlatego mogą minimalnie różnić się od odejmowania wartości widocznych w tabeli.

## Dlaczego koszty są częścią projektu

Pytanie badawcze dotyczy wyniku po kosztach. Scenariusz przyjmuje prowizję 0,10% i niekorzystny poślizg 0,05% przy zakupie oraz przy sprzedaży. Są to parametry modelowe, a nie odtworzone historyczne opłaty i faktyczne ceny realizacji. Obliczenie netto uwzględnia całkowity wydatek przy wejściu i wpływ po kosztach przy wyjściu.

Dla hipotetycznego budżetu 1 000 USDT wynik końcowy w tym modelu to 2294,40 USDT dla ETH i 2053,25 USDT dla BTC. To symulacja na historycznych cenach, nie opis zrealizowanych zleceń.

## Interpretacja i granice

To jeden przykład sprawdzający powiązanie cen, dat, kosztów i benchmarku. Nie pozwala wnioskować o skuteczności strategii w całym okresie ani wybierać najlepszej reguły wejścia. Właściwa analiza musi objąć wszystkie zdarzenia, monety i ustalone reguły, w tym straty oraz przypadki bez wejścia.

Historyczna godzina publikacji rankingu pozostaje niepotwierdzona. Wykonanie zlecenia po modelowej cenie otwarcia i poślizgu jest założeniem. Nie modelowano zaokrągleń liczby monet, minimalnego zlecenia ani ograniczeń kapitału dla wielu pozycji.

Pochodzenie czterech cen i pełna precyzja obliczeń: data/processed/control_trade.csv. Sposób odtworzenia: python scripts/build_control_trade.py.
