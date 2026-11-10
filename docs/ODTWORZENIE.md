# Odtworzenie projektu

## Środowisko

Sprawdzone wersje: Python 3.12, pandas 3.0.1 i Matplotlib 3.10.8. Wykonuj polecenia w katalogu głównym repozytorium, w aktywnym środowisku wirtualnym.

```bash
python -m pip install -r requirements-plots.txt
python scripts/run_analysis.py
```

Domyślna ścieżka korzysta z przygotowanych danych i oryginalnych odpowiedzi dostawców. Przelicza transakcje, agregacje koszyków i obsunięcie kapitału. Sprawdza wyniki niezależnymi obliczeniami pandas i przepływami hipotetycznego budżetu. Uruchamia 10 testów obliczeń, a na końcu porównuje sumy kontrolne 17 tabel wynikowych z opublikowaną wersją.

## Pełne przygotowanie i wykresy

```bash
python scripts/run_analysis.py --full --figures
```

Opcja `--full` rozpoczyna od przygotowania cen, obliczenia RSI, identyfikacji sygnałów, doboru historycznych koszyków i sprawdzenia pokrycia cen. Opcja `--figures` odtwarza pięć wykresów PNG/SVG. Parametry badania znajdują się w `config/trade_protocol_v1.json`; nie należy zmieniać ich tylko po to, aby poprawić wynik strategii.

W `reports/` znajdują się wyniki kontroli. Publiczne manifesty zawierają parametry źródeł, daty pobrania oraz sumy odpowiedzi. Pominięto pola opisujące środowisko i nagłówki identyfikacyjne pobierania; sumy samych manifestów dotyczą wersji w repozytorium. Dane cenowe i rankingowe zachowują oryginalne wartości.

## Interaktywna strona projektu

Do zbudowania strony wystarcza biblioteka standardowa Pythona:

```bash
python scripts/build_site.py
python -m http.server 8000 --directory _site
```

Otwórz `http://localhost:8000`. Strona zawiera raport, podgląd slajdów, pobieranie pliku Tableau, porównanie median stóp zwrotu oraz wykres obsunięcia kapitału dla wybranego sygnału i reguły. Źródła strony są w `web/`, a wygenerowane pliki w pomijanym przez Git katalogu `_site/`.

## Tableau i prezentacja

Otwórz `tableau/Altcoiny_RSI_BTC.twbx` w Tableau Public. Oba ekstrakty są osadzone, więc przeglądanie nie wymaga podłączania CSV. Zmiana CSV nie aktualizuje ekstraktów automatycznie. Szczegóły filtrów i interpretacji miar znajdują się w [instrukcji Tableau](../tableau/INSTRUKCJA.md).

Plik `prezentacja/Prezentacja.pptx` zawiera edytowalne wykresy i notatki. PDF raportu oraz prezentacja są opublikowanymi materiałami końcowymi. Odtworzenie obliczeń nie nadpisuje ich automatycznie.

## Nowe pobranie danych

Odtworzenie badania z zachowanych plików nie wymaga sieci. Skrypty `download_prices.py` i `download_event_rankings.py` służą do osobnego, kontrolowanego pobierania. Przed nowymi zapytaniami rankingowymi ustaw zmienną `RANKING_USER_AGENT` z identyfikatorem projektu i kontaktem wymaganym przez dostawcę. Ponowne pobranie może dać inne odpowiedzi; wymaga kontroli dat, historii symboli i warunków źródła.
