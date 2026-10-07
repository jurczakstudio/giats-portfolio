# 04 — KIERUNEK · AKWIFER

Każda decyzja cytuje wniosek.

## Paleta i kroje
- Tło: papier mapy `--papier #f1ede3`, druga warstwa `--papier-2 #e7e1d2` — jak arkusz MhP (W5).
- Tekst: atrament `--atrament #1a232b`, drugi stopień `--olowek #4e5861` (W5).
- Jedyny akcent: niebieski hydroizohips `--izolinia #1f5f9e` — ten sam kolor rysuje linie i przyciski (W1).
- Lej depresji barwi pole odrobinę głębszym błękitem — tylko tam, gdzie woda jest naprawdę obniżona (W1, W2).
- Spectral (szeryf z kursywą) w nagłówkach — rejestr opisu mapy, nie reklamy (W5).
- Onest w tekście, IBM Plex Mono dla rzędnych, wzorów i liczb (W2).
- Skala tokenami `--fs-*`, nic poniżej 14 px (W4).

## Sygnatura
- Pełnoekranowe płótno WebGL z polem zwierciadła wody i hydroizohipsami co 0,5 m (W1).
- Kursor/palec = pompa; lej depresji liczony kształtem Dupuita, promień Sichardtem (W1, W2).
- Klik/tap na otwartej mapie = wiercenie stałej studni (maks. 6), z numerem otworu (W1).
- Arkusze z oknami-otworami; pod każdym oknem odczyt rzędnej z tego samego pola (W1, W5).
- Mapa przesuwa się z przewijaniem, więc przez kolejne okna widać kolejne fragmenty tej samej mapy (W1).
- Na telefonie przycisk „Pompuj” zamiast kursora; bez WebGL statyczny wzór izolinii w CSS (W4).

## Struktura
- `/` — otwarta mapa → zwierciadło → próba pompowania → przebieg → rachunek → 30 m → karta zgłoszenia (W1–W4).
- `/proba-pompowania/` — pełny symulator, krzywa depresji, tabela gruntów (W2).
- `/przebieg/` — karta otworu: etapy od pomiaru do protokołu pompowania (W2, W3).
- `/formalnosci/` — granica 30 m i 5 m³/d, odległości (W4).
- `/kontakt/` — karta zgłoszenia składana w SMS (W4).

## Treść
- Każda liczba ze wzorem albo źródłem; model podpisany „poglądowy” (W2, W3).
- Cennik firmy oznaczony „PRZYKŁAD — do podmiany” obok cen rynkowych ze źródłem (W4).
- Baner „strona wzorcowa · firma fikcyjna” na każdej stronie; telefon przykładowy (W5).

## Ruch
- `rv:split` na nagłówkach arkuszy, `rv:mask` na oknach, `seq` na listach, `scrub` na krzywej depresji (W1).
- Bezpieczniki z biblioteki + shader zatrzymany przy `prefers-reduced-motion` i `?static=1` — mapa stoi, lej pokazany w stanie końcowym (W4).
