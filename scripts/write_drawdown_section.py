"""Tekst uzupełniającej analizy ryzyka, budowany z tabel wynikowych."""

from analyze_trades import read_csv


def pct(value):
    return f'{float(value) * 100:.2f}%'.replace('.', ',').replace('-', '−')


def section():
    rows = read_csv('data/analysis/summary_basket_capital_risk_90d.csv')
    table = '\n'.join('| ' + ' | '.join([r['entry_rule'], pct(r['median_alt_mdd']), pct(r['median_btc_mdd']), pct(r['worst_alt_mdd']), pct(r['worst_btc_mdd']), r['alt_less_severe_mdd_count'] + '/20']) + ' |' for r in rows)
    return f'''## Maksymalne obsunięcie kapitału koszyka

Uzupełniająco odtworzono wartość każdego pięcioelementowego koszyka oraz dopasowanej inwestycji w BTC w trakcie 90 dni. Dla każdego sygnału i reguły przyjęto osobny budżet 1 000 USDT. Wyniki procentowe nie zależą od tej skali przy proporcjonalnych kosztach i pominięciu zaokrągleń giełdowych. Maksymalne obsunięcie (MDD) opisuje największy spadek od wcześniejszego maksimum wartości kapitału, a nie wyłącznie stratę względem początkowego wydatku.

| Reguła | Mediana MDD koszyka | Mediana MDD BTC | Najgłębsze MDD koszyka | Najgłębsze MDD BTC | Płytsze MDD koszyka niż BTC |
| --- | --- | --- | --- | --- | --- |
{table}

![Mediany i najgłębsze obsunięcia kapitału koszyków oraz dopasowanego BTC dla trzech reguł wejścia.](<wykresy/05_obsuniecie_kapitalu.png>)

**Wykres 5. Maksymalne obsunięcie kapitału.** Mediana obejmuje 20 osobnych zdarzeń w każdej regule. Najgłębsze obsunięcie jest skrajną obserwacją w danej grupie; po stronie altcoinów i BTC może pochodzić z innych sygnałów. Wartości ujemne oznaczają spadek względem wcześniejszego szczytu. Im dalej od zera, tym głębsze obsunięcie.

Mediany MDD koszyków wyniosły około −26,7% do −26,8%, wobec −20,93% dla BTC. Koszyk miał płytsze obsunięcie niż dopasowany BTC w 1/20 zdarzeń w regule A, 2/20 w B i 3/20 w C. Uzupełnienie wskazuje zatem na głębsze obsunięcia koszyków w większości porównań tej próby.

Najgłębsze MDD koszyka wystąpiło w regule A po sygnale z 17 maja 2021 r. i wyniosło −54,76%. Dla reguł B i C najgłębsze obsunięcia wyniosły odpowiednio −45,31% i −44,89%, po sygnale z 21 maja 2021 r. Najgłębsze MDD dopasowanego BTC wyniosło −40,35% w każdej regule, po sygnale z 9 maja 2022 r. Są to daty sygnałów; daty szczytu i dołka zapisano oddzielnie w tabeli szczegółowej.

Wyceny uwzględniają początkową gotówkę, wartość rynkową zaraz po zakupie, 90 dziennych zamknięć UTC i końcowy wpływ po sprzedaży. Koszty naliczono przy rzeczywistym modelowanym wejściu i wyjściu; nie odejmowano hipotetycznej prowizji sprzedaży przy każdej wycenie dziennej. Ta miara dotyczy kapitału całego koszyka, w odróżnieniu od wcześniej opisanych cenowych MDD pojedynczych monet. Nie jest średnią ich obsunięć.

Analizę dodano po opracowaniu pierwotnych wyników jako opisowe rozszerzenie. Dzienne wyceny nie odtwarzają obsunięć wewnątrz dnia. Nie połączono nakładających się inwestycji w jedną ścieżkę konta za lata 2020–2025. Dane szczegółowe: data/analysis/basket_capital_risk_90d.csv; pełne ścieżki: data/analysis/basket_capital_path_90d.csv. Końcowe kwoty wszystkich 60 ścieżek są zgodne z wcześniej obliczonymi zwrotami netto koszyków i BTC.

'''
