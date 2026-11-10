# Rejestr źródeł danych

Zweryfikowano: **2026-11-08**. Faktyczne czasy pobrania każdej strony API są w manifestach `data/raw/binance/2026-11-08/manifest.json` i `data/raw/binance/2026-11-08_sol/manifest.json`. Wspólny zestaw odnośników znajduje się w `data/metadata/with_sol/manifest.json`.

## 1. Ceny — wykorzystane

**Dostawca:** Binance Spot. **Interfejs danych:** Binance Spot, dzienne świece cenowe. Przechowano jego odpowiedzi JSON w postaci zwróconej w polu tekstowym, z opakowaniem `result`; to nie jest przechwycony surowy pakiet HTTP.

- Dokumentacja: [Binance Spot — Market](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market).
- Endpoint: `GET /api/v3/klines`; interwał `1d`, strefa `0` (UTC), do 1000 świec na stronę.
- Zakres: BTC 2019-01-01–2026-07-31; ETH, XRP, BCH i LTC 2020-01-01–2026-07-31; EOS do 2025-05-26; A od 2025-05-28 do 2026-07-31; SOL od 2020-08-11 do 2026-07-31.
- Jednostka cen: USDT za jednostkę aktywa. Kapitalizacja z rankingu jest w USD, ale nie służy obliczaniu stóp zwrotu.
- Pobrano: pierwotnie 18 stron i 14 788 świec; SOL to 3 strony i 2 181 świec; BNB, ADA, DOGE i TRX to 12 stron i 9 616 świec. Łącznie zasób Binance ma 33 strony, 26 585 świec, 12 par i 11 identyfikatorów aktywów (EOS/A jako jeden). Nowe źródła są w data/raw/binance/2026-11-08_ranked_assets/, wspólny manifest w data/metadata/event_prices/manifest.json.
- Dostęp: publiczne dane rynkowe, bez prywatnego konta, klucza i zakupionej subskrypcji; pobranie potwierdzone dla wszystkich wymienionych par, także dawnego symbolu EOSUSDT.
- Endpoint do ponownego pobrania: [publiczny interfejs danych Binance](https://data-api.binance.vision/api/v3/klines). Sprawdzono zapytanie o BTC z 1–3 stycznia 2020 r.; pełnego skryptu ponownego pobrania nie uruchamiano.

**Ograniczenia:** ceny z jednej giełdy; dzienna świeca nie dowodzi dostępności handlu przez całą dobę ani możliwości realizacji zlecenia bez poślizgu. API może podlegać limitom i zmianom. Dostawca może korygować dane. Identyfikator symbolu należy interpretować wraz z historią migracji.

**Warunki:** [Binance Vision Dataset Terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md), wersja 1.0, aktualizacja 2026-08-26. Dokument obejmuje archiwa i powiązane endpointy; wskazuje bezpłatny dostęp oraz CC BY-NC-SA 4.0 i dodatkowe warunki. Zastosowanie edukacyjne i osobiste historyczne badania mieszczą się w opisanych zastosowaniach niekomercyjnych. Przy udostępnianiu prac pochodnych wymagane są odpowiednie oznaczenie Binance Vision i wskazane warunki licencji. Nie zakładamy zgody na wykorzystanie komercyjne.

**Archiwum alternatywne:** [Binance Public Data](https://github.com/binance/binance-public-data) i [Binance Data Collection](https://data.binance.vision/). Dokumentacja opisuje miesięczne ZIP-y, CSV i sumy kontrolne. Nie pobierano tych archiwów do obecnego zbioru; lokalne SHA-256 dotyczą zapisanych odpowiedzi. Ostrzeżenie o mikrosekundach od stycznia 2025 r. dotyczy plików archiwum; w pobranych odpowiedziach API znaczniki są w milisekundach.

## 2. Wybór początkowego koszyka — wykorzystany jako punkt odniesienia

**Status po korekcie autora:** ten sposób doboru wycofano. Poniższy zapis dokumentuje historię przygotowania, a nie aktualną regułę kwalifikacji. Obowiązuje zmienny top 5 przed każdym sygnałem; rozpoznanie nowego źródła opisano w punkcie 6.

**Źródło:** [CoinMarketCap — Historical Snapshot, 29 December 2019](https://coinmarketcap.com/historical/20191229/).

- Zakres wykorzystania: odczyt kolejności na jednej stronie historycznej przed początkiem badania; zapisano własną tabelę doboru koszyka z odnośnikiem, bez kopiowania pełnej strony i pełnej bazy.
- Data odczytu: 2026-11-08. Data historycznego zestawienia: 2019-12-29.
- Wybór: ETH (miejsce 2), XRP (3), BCH (5), LTC (6), EOS (7). BTC (1) jest benchmarkiem, czyli punktem odniesienia. USDT (4) pominięto jako stablecoin. W tych pozycjach nie wybrano tokenów opakowanych.
- Ograniczenie: koszyk jest stały; nie posiadamy pełnej historii rankingów ani potwierdzenia niezmienności dzisiejszej wersji historycznej strony.
- Dostęp do strony był publiczny. Nie uznano tego za otwartą licencję na kopiowanie całej bazy.
- Warunki i dostęp API: [warunki CoinMarketCap](https://coinmarketcap.com/terms/) oraz [oferta API](https://coinmarketcap.com/api/pricing/), sprawdzone 2026-11-08. Warunki ograniczają pozyskiwanie i kopiowanie treści; nie wykonano automatycznego zbierania całego archiwum. Cennik rozróżnia długość historii między planami. Nie kupowano dostępu ani nie potwierdzono uprawnień do endpointu pełnych historycznych rankingów na koncie autora.

## 3. Migracja EOS → Vaulta — wykorzystana

**Źródło pierwotne:** [Binance — EOS token swap and rebranding to Vaulta](https://www.binance.com/en/support/announcement/detail/1e89a9ca957c4b0ca7502e60b993e201).

- Ogłoszenie: 2025-05-14; sprawdzone 2026-11-08.
- EOS Spot zatrzymano 2025-05-26 o 03:00 UTC; A Spot otwarto 2025-05-28 o 08:00 UTC; wymiana 1 EOS = 1 A.
- Wykorzystano fakty do opisania migracji i flag jakości. Nie archiwizowano pełnego tekstu ogłoszenia.
- Fakty z danych: ostatnia świeca EOS kończy się 2025-05-26 o 02:59:59.999 UTC; 2025-05-27 brakuje świecy; pierwsza świeca A ma znacznik dnia 2025-05-28 00:00 UTC, mimo rozpoczęcia handlu dopiero o 08:00.
- Wniosek do przygotowania danych: zachować oba symbole, powiązać wspólnym identyfikatorem i stosunkiem 1:1, oznaczyć dwa niepełne dni, nie tworzyć ceny na dzień przerwy. Politykę transakcji przez przerwę ustalimy przed badaniem wyników.
- Warunki publikacji strony: odnośniki dostawcy w ogłoszeniu; nie przypisujemy tekstowi ogłoszenia licencji danych Binance Vision.

## 4. CoinGecko — sprawdzone, niewykorzystane do pobrania cen

[Oficjalna informacja o historii danych](https://support.coingecko.com/articles/5723073761-what-granularity-do-you-support-for-historical-data), sprawdzona 2026-11-08, podaje ograniczenie historii publicznego planu do ostatnich 365 dni. Sam taki dostęp nie obejmuje lat 2020–2025. Nie kupowano planu, nie pobierano danych i nie przyjęto założenia, że dawna historia jest bezpłatna. Warunki wykorzystania wymagają sprawdzenia właściwego planu, jeśli to źródło zostanie dodane w przyszłości.

## 5. Dostępność SOL/USDT — wykorzystana

**Źródło pierwotne:** [Binance — nowe pary z 11 sierpnia 2020 r.](https://www.binance.com/en/support/announcement/detail/cf77f566c9b64cc791fc152679175de8), sprawdzone 2026-11-08. Ogłoszenie wskazuje rozpoczęcie handlu SOL/USDT 2020-08-11 o 06:00 UTC. Odpowiedź API na zapytanie od początku 2020 r. zaczyna się od świecy 2020-08-11.

Pobrano 2 181 świec do 2026-07-31. Nie wykorzystujemy daty pierwszego notowania SOL w innych parach lub na innej giełdzie jako początku SOL/USDT na Binance. Pierwszą świecę oznaczono jako niepełną; jej cena `open` nie była dostępna o północy. Okres 2020-01-01–2020-08-10 (223 dni) zapisano jako niedostępność pary przed listingiem, oddzielnie od braków w istniejących notowaniach. Nie dopisano żadnych cen.

Ceny SOL pobrano na życzenie autora. W bieżącym badaniu kwalifikacja SOL zależy od historycznego top 5 przed konkretnym sygnałem. Warunki danych cenowych są opisane w punkcie 1; z ogłoszenia wykorzystano fakty, bez kopiowania pełnego tekstu.

## 6. Zmienny historyczny ranking — sprawdzony kandydat

[CryptWatch — dokumentacja i warunki](https://cryptwat.ch/api), [specyfikacja API](https://cryptwat.ch/api/v1/openapi.json), sprawdzone 2026-11-08. Źródło danych wskazane przez dostawcę: CoinMarketCap. Oznaczenie: **Data: CryptWatch, based on CoinMarketCap**.

- Pobrano indeks 2 215 dat od 2013-04-28 do 2026-11-08 i trzy odpowiedzi rankingu: 2020-03-08, 2022-04-03, 2025-06-01. Zachowano odpowiedzi JSON i specyfikację; nie pobrano jeszcze kompletu rankingów dla zdarzeń RSI.
- Dostęp bez klucza i rejestracji. Limit 60 zapytań/min; dostawca prosi o identyfikator narzędzia i kontakt w User-Agent. Przy krótkim rozpoznaniu podano nazwę projektu i jawnie brak kontaktu; przed większym pobieraniem należy ustalić identyfikację zgodną z wymaganiem dostawcy. Nie przekazano adresu e-mail autora ani nie kontaktowano się z dostawcą.
- Deklarowane wykorzystanie badawcze z oznaczeniem źródła; zakaz odsprzedaży surowych danych jako osobnej usługi. Bez gwarancji kompletności.
- Starsze daty są tygodniowe, późniejsze zasadniczo dzienne. Endpoint może zwrócić wcześniejszy snapshot: kontrolować data.date i wiek. Weryfikacja kalendarza wykazała maksymalnie 9 dni od wcześniejszej daty, bez badania czasu publikacji.
- Pierwszych 15 pozycji z 2020-03-08 porównano z [historyczną tabelą CMC](https://coinmarketcap.com/historical/20200308/): kolejność zgodna. Nie potwierdza to wszystkich pozostałych rankingów.
- Otwarte: publikacja, klasyfikacja aktywów w czasie, mapowanie późniejszych nazw (np. LUNC), pełne ceny wybranych monet.

Oficjalne [listings/historical CoinMarketCap](https://coinmarketcap.com/api/documentation/pro-api-reference/cryptocurrency) są alternatywą dzienną; dostawca opisuje je jako koniec dnia UTC. [Oficjalny poradnik](https://coinmarketcap.com/api/resources/how-to-retrieve-historical-cryptocurrency-rankings/) potwierdza wymóg płatnego planu. Nie kupowano dostępu. Ograniczona częstotliwość danych bezpłatnych nie uzasadnia powrotu do stałego koszyka.

Aktualizacja po obliczeniu sygnałów: pobrano 19 potrzebnych rankingów (po 30 pozycji) dla 20 sygnałów. Parametry, rzeczywiste daty odpowiedzi, czasy pobrania, nagłówki i SHA-256 są w data/raw/rankings/cryptwatch/2026-11-08_events/manifest.json. Zapytania rozdzielono odstępem 1,4 s. Publikacyjny manifest zachowuje daty, zapytania i sumy kontrolne odpowiedzi; pominięto nagłówki identyfikujące środowisko pobrania. Skład wybierano według rankingu, zanim uzupełniono ceny. Oryginalne nazwy znormalizowane przez dostawcę zachowano w kolumnie źródłowej.

## 7. KuCoin — ceny BSV, TON i dopasowanego BTC

Źródła: [oficjalna dokumentacja świec](https://www.kucoin.com/docs-new/rest/spot-trading/market-data/get-klines), [publiczne API i dane do badań](https://www.kucoin.com/api), [warunki wykorzystania](https://www.kucoin.com/legal/terms-of-use), sprawdzone 2026-11-08. GET /api/v1/market/candles, type=1day, znaczniki w sekundach; do 1500 świec na zapytanie. API nie publikuje świecy, gdy brak transakcji.

Pobrano cztery odpowiedzi: BSV-USDT i BTC-USDT z 2020-03-13–2020-10-10 oraz GRAM-USDT (historyczny TON) i BTC-USDT z 2024-06-25–2025-03-05. Łącznie 932 świece; potrzebne okna kończą się dzień wcześniej. Dostęp potwierdzono bez konta i klucza. Szczegółowe zapytania, SHA-256 i czasy zapisania są w data/metadata/kucoin_manifest.json. Odpowiedzi rozpoznawcze BSV i GRAM wykorzystano bez zmiany jako dane źródłowe.

KuCoin zwraca kolejność pól: czas, open, close, high, low, wolumen aktywa, wolumen wyceny; ceny są w USDT. Sprawdzono UTC, wartości OHLC i ciągłość potrzebnych okien. Nie przypisano tym danym licencji CC BY-NC-SA Binance. Publiczne API i możliwość pobrania do badań nie oznaczają otwartej licencji do odsprzedaży lub publicznej redystrybucji całej bazy; obowiązują warunki KuCoin.

Tożsamość TON: zachowana odpowiedź CryptWatch podaje id CMC 11419 i historyczne aliasy TON ważne w 2024 r. [Bitfinex](https://support.bitfinex.com/hc/en-us/articles/17019918187801-Gram-GRAM) potwierdza późniejsze przemianowanie. Nazwa GRAM-USDT w bieżącym API nie oznacza innego aktywa kupowanego w 2024 r. [Binance](https://www.binance.com/en/support/announcement/detail/abba626aa0974b828f91c166bdc12afd) potwierdza rozpoczęcie własnych notowań TON dopiero 2024-08-08, dlatego nie użyto go do wcześniejszych dat.

W porównaniach BSV i TON benchmark BTC będzie pochodził również z KuCoin. Źródłem sygnału RSI pozostaje wspólne Binance BTC/USDT. Różnice giełd i płynności zostaną opisane w ograniczeniach.
