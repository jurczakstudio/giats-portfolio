# `_wzorce/audyt/` — bramki

Dwa skrypty. **Trzeciego nie będzie** — dwa mechanizmy mierzące to samo są zakazane
(`NASTART.md` część 3).

| Skrypt | Pyta | Kiedy |
|---|---|---|
| `audyt.py` | czy ta strona jest dobrze zrobiona | etap 7 (każdy build) i 9 |
| `podobienstwo.py` | czy to nie jest nasza poprzednia strona | etap 9, oraz przy etapie 3 |

```bash
python ../_wzorce/audyt/audyt.py .              # z katalogu projektu
python _wzorce/audyt/audyt.py lewartowski       # wskazany projekt
python _wzorce/audyt/audyt.py --wszystkie       # cała pracownia
python _wzorce/audyt/audyt.py . --zapisz        # + odcisk do indeks.json
python _wzorce/audyt/podobienstwo.py --wszystkie
```

## Wpięcie w `build.py`

```python
import subprocess, sys
from pathlib import Path

BRAMKA = Path(__file__).resolve().parent.parent / '_wzorce' / 'audyt' / 'audyt.py'
if subprocess.run([sys.executable, str(BRAMKA), str(Path(__file__).parent)]).returncode:
    raise SystemExit('Bramka zamknięta — patrz lista wyżej.')
```

---

## Bezpiecznik kontra kompas

**BEZPIECZNIK** blokuje build i wykrywa katastrofę, nie mierzy piękna. Musi być
niemożliwy do przejścia samym dopisaniem atrybutu.
**KOMPAS** nigdy nie blokuje — pokazuje liczbę i dryf.

### Bezpieczniki

| Kontrola | Próg | Skąd wziął się próg |
|---|---|---|
| **sekcja niesie obiekt** | każda sekcja | reguła z `anti-slop.md`; Hormon miał dwie sekcje z samym tekstem |
| **rytm obiektów** | ten sam rodzaj nie dwa razy pod rząd | dwie siatki zdjęć pod rząd czytają się jak jedna długa sekcja |
| **rytm konstrukcji** | ta sama konstrukcja najwyżej 2× pod rząd | LUX: trzy identyczne układy „tekst + render + lista 01/02/03" |
| **rozkład kadrów** | ≤40 % kadrów w jednej sekcji (strony ≥5 sekcji) | Hormon: 73 z 79 zdjęć w jednej sekcji-galerii |
| **rozkład ruchu** | jeden typ ≤50 % sekcji z ruchem | zastępuje usunięty próg „≥60 % sekcji z ruchem" |
| **sygnatura poza hero** | `data-sygnatura` poza pierwszą sekcją, na każdej podstronie | „idea placu żyje przez jeden ekran i umiera" |
| **skala typograficzna** | zero wartości `font-size` spoza zadeklarowanych tokenów | lewartowski: 31 rozmiarów = przypadek, nie decyzja |
| **czytelność** | nic poniżej 14 px | odbiorca 50+ (`police-czarny-granit.md`) |
| **bezpieczniki ruchu** | `prefers-reduced-motion`, `?static=1`, bramka JS | reguła z gramar |
| **nagłówek hero** | H1 bez pustych fraz | anty-slop |
| **mobile** | przewrotki ≤60 %, ≥1 sekcja tylko na jednym urządzeniu | mobile był wcześniej tylko testem QA |
| **kierunek cytuje wnioski** | każda decyzja w `04-kierunek.md` ma numer `W_` | żeby research nie kończył się raportem |

### Kompasy

udział sekcji z ruchem · rozkład typów ruchu · **profil mediów przez scroll** ·
koncentracja kadrów · bogactwo podstron · tokeny typograficzne · mikro-ruch.

Profil mediów jest najcenniejszy: ciąg malejący to podpis zdania „skończyła mi się
energia po hero". Lewartowski: `7 / 5 / 1 / 0 / 1 / 21 / 2 / 2`. Hormon przed poprawką:
`100 / 76 / 33 / 2,5 / 25 / 28 / 0 / 0`.

## Tryby

Projekt z katalogiem `dane/` dostaje **komplet** bezpieczników, łącznie z tymi, które
wymagają deklaracji (sygnatura, tokeny, plan sekcji, cytaty). Projekt bez `dane/` to
strona zastana — te kontrole schodzą do kompasu, żeby dało się przebiec całą pracownię.

## Czego bramka nie widzi

Ikony SVG nie są materiałem wizualnym. **Powierzchnie malowane CSS-em są** — klasy
niosące teksturę wyprowadzamy z CSS, nie z konwencji nazw, bo detektor szukający `tlo-*`
przegapiał `.gr-szwed` u Lewartowskich i popychał nas w stronę fotografii, odwrotnie
niż reguła domu.

Bramka nie ocenia, czy strona jest ładna. To robi `js-krytyk-designu` na zrzutach —
w tym na zrzutach z **podmienioną nazwą, telefonem i miastem**: jeśli agent nie potrafi
powiedzieć, co to za firma, w projekcie jest branża zamiast klienta.

---

## Stan pracowni, 16.09.2026

25 projektów, **102 zamknięte bezpieczniki**. Najczęstsze: sekcja bez obiektu, brak
bezpieczników ruchu, czytelność poniżej 14 px.

Macierz podobieństwa: `marmokom ↔ piotrowski 73 %` (blokada), `meustone ↔ piotrowski 46 %`.
Nowsze projekty są strukturalnie różne — **poniżej 35 % każdy z każdym**. Nasze powtarzanie
się nie polega więc na układzie, tylko na rejestrze: cztery projekty mają akcent w niemal
identycznym ciepłym brązie (`#9a7f5c`, `#8d4d29`, `#8c6f46`, `#8f6247`). Dlatego
porównanie akcentów liczy **odległość odcienia**, a nie równość heksów.

Wszystkie zastane projekty oblewają część bezpieczników — próg dotyczy tego, co budujemy
od teraz. Starych stron nie przepisujemy hurtem.
