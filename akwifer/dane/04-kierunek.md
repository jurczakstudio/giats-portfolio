# 04 — KIERUNEK · AKWIFER v2 „ZLECENIE”

## Paleta i kroje
- Tło zmierzchu `--noc #0e1316`, druga warstwa `--noc-2 #161d21` — kadry generowane są o zmierzchu, strona je przedłuża (W5).
- Tekst `--kosc #ece6da`, drugi `--popiol #a7a69f` — kontrast ≥ 4,5:1 na nocy (W4).
- Jedyny akcent: pomarańcz lamp roboczych `--sygnal #ff6b2c` — przyciski, karta zlecenia, liczby wyceny (W1, W4).
- Woda w danych (słupki gmin) w chłodnym `--woda #7cc4d6` jako barwa informacyjna, nigdy na przyciskach (W2).
- Archivo w szerokości 75 i wadze 800 w nagłówkach — industrialne, jak tabliczka wiertnicy (W5).
- Source Serif 4 kursywa tylko w notkach właściciela — głos „z boku”, odróżniony od strony klienta (W5).
- DM Mono dla metrów, złotówek i dat (W4).
- Skala tokenami `--fs-*`, nic poniżej 14 px (W4).

## Sygnatura
- Karta zlecenia: gmina, cel, osoby → metry (najpłytsze–mediana PIG), złotówki (rynek × metry + osprzęt), formalności (≤ / > 30 m), termin (przykład) (W1, W2, W3, W4).
- Karta zapisuje się w przeglądarce i wraca na każdej podstronie; na stronie gminy wypełnia się nią sama (W4).
- Przycisk „Wyślij zgłoszenie” składa SMS z rubryk karty — firma dostaje gotowe zlecenie (W1).

## Struktura
- `/` — hero z wyceną → karta → mapa powiatu → przebieg ze zdjęciem → rachunek ogrodu → paszport studni → zgłoszenie (W1–W4, W6, W7).
- Mapa powiatu: granice OSM, barwa = mediana głębokości (skala `--woda`), szare gminy bez danych, podpis ODbL (W7).
- Rachunek ogrodu: wykres skumulowanego kosztu wodociągu przecina pas kosztu studni — punkt zwrotu w latach (W6).
- Podstrona gminy: mała mapa z podświetloną gminą obok liczby mediany (W2, W7).
- `/gmina/<slug>/` ×14 — dane PIG gminy, karta wypełniona, pytania lokalne, sąsiednie gminy (W2).
- `/paszport-studni/` — przykładowy paszport po odbiorze: dane studni, badanie wody, przeglądy (W5).
- `/dla-firm/` — oferta dla właściciela firmy: co robi każda część strony (W5).

## Obraz
- Hero: wiertnica o zmierzchu na działce z domem w stanie surowym — generowana, podpisana „ilustracja poglądowa” (W5).
- Przebieg: woda nalewana do szklanki z nowej studni — generowana, podpisana (W5).
- Do czasu wygenerowania: plansza zastępcza z gotowym promptem w README (W5).

## Tryb właściciela
- Przełącznik w nagłówku „Oczami właściciela”, `?wlasciciel=1` otwiera stronę od razu w tym trybie — link do wysłania firmie (W5).
- Notki w kursywie szeryfowej, przy każdej sekcji: co sekcja robi dla firmy, liczbowo, jeśli się da (W5).

## Uczciwość
- Baner „strona wzorcowa · firma fikcyjna”; telefon `000 000 000` (nie da się połączyć) (W5).
- Dane gmin z rejestru PIG z zastrzeżeniem, że mediany są zawyżone (W2).
- Brak opinii — nie zmyślamy; notka właściciela mówi, gdzie pojawią się prawdziwe (W5).

## v3 „GŁĘBIEJ” (zastępuje paletę i hero z v2)
- Paleta: czerń `#111214` + żółć hi-vis `#ffd21f` jako jedyny akcent; krem `#f3eee4` tylko na kartach i tekście (W8).
- Nagłówki wersalikami, Archivo w szerokości 72 i wadze 800, skala plakatu do 9 rem; kursywa szeryfowa jako kontrapunkt (W8).
- Ziarno (feTurbulence) na całej stronie i siatka kreślarska w sekcjach technicznych (W8).
- Hero: wybór gminy + żywa linijka głębokości 0–120 m z pasem widełek, linią 30 m i medianą (W9).
- Zejście pod ziemię: sekcja przypięta, licznik metrów rośnie do mediany wybranej gminy, na dnie woda (W8, W9).
- Gwarancja przejrzystości: cztery zasady z dużymi liczbami (W10, W4).
- Pakiety: Ogród / Dom / Głęboko z ceną „od” ze średnich rynkowych i dopłatą za metr (W10, W4).
- Przepisy 2026: drzewko decyzji, licznik abolicji, ostrzeżenie PIG-PIB (W11, W3).
- Telefon: stały pasek akcji po zejściu z hero; desktop: stopka z ogromnym numerem (W11, W3).
