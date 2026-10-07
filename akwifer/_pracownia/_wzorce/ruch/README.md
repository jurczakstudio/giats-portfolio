# `_wzorce/ruch/` — biblioteka ruchu domu

Jedno nazewnictwo na zawsze. Powstała 16.09.2026, bo pomiar 16 stron pokazał **sześć różnych
nazw klas na to samo odsłonięcie** (`.rv`, `data-rv`, `.wej`, `.zakryty`, `data-reveal`,
`.idx-row`) — czyli nic się nie kumulowało i każdy projekt zaczynał ruch od zera.

## Jak wpiąć w projekt

1. Skopiuj `ruch.js` i `ruch.css` do projektu. **Nie zmieniaj ich.**
   Sygnaturę projektu (scena 3D, szew, stojak) pisz osobno, w `site.js` / `site.css`.
2. W `build.py`:

```python
# doklejamy do jednego CSS-a i jednego JS-a — reguła domu: jeden plik każdego
css = (WZORCE / 'ruch' / 'ruch.css').read_text(encoding='utf-8') + NASZ_CSS
js  = (WZORCE / 'ruch' / 'ruch.js').read_text(encoding='utf-8') + NASZ_JS
```

3. Skrypt ładuj z `defer`. `?v=` z `_ver()` obowiązuje jak zawsze.

## Atrybuty

| Atrybut | Działanie | Parametry |
|---|---|---|
| `data-rv` | odsłonięcie w kadrze | `up` (domyślne) / `mask` / `scale` / `split`; `data-rvd` = opóźnienie ms |
| `data-seq` | dzieci wchodzą po kolei | wartość = odstęp ms (domyślnie 60) |
| `data-par` | paralaksa warstwy | siła −1..1 |
| `data-pin` | sekcja przyklejona | wysokość w `vh`; wymaga dziecka `.pin__w` |
| `data-scrub` | postęp sekcji 0..1 jako `--p` | — |
| `data-count` | licznik | `data-count="12,5"` |
| `data-hover` | kursor jako `--mx/--my` | — |
| `data-drag` | przeciąganie + dryf | `data-drift="0.35"`, `0` = bez dryfu |

`data-rv="split"` wymaga struktury wierszy — inaczej nie zadziała:

```html
<h2 data-rv="split"><span class="w"><i>Pierwszy wiersz</i></span><span class="w"><i>drugi</i></span></h2>
```

`data-scrub` sam nic nie animuje — podaje `--p` do CSS-a projektu:

```css
.rzezba { transform: rotate(calc(var(--p) * 90deg)); }
.podpis { opacity: var(--p); }
```

## Bezpieczniki

1. `prefers-reduced-motion: reduce` — wszystko od razu w pozycji końcowej.
2. `?static=1` — to samo. **Audyt i zrzuty robimy zawsze z tym parametrem.**
3. Bramka JS — HTML jest kompletny; klasę ukrywającą `ruch` dokłada dopiero skrypt.
   Wyłączony JavaScript = strona bez ruchu, nie strona pusta.

Plus dwa czuwaki, których wcześniej nie mieliśmy:
- **pomiar prędkości przewijania** — powyżej 2200 px/s odsłanianie idzie bez opóźnień
  (szybki scroll u Lewartowskich zostawiał dwa puste ekrany);
- **`setTimeout(1200)`** — gdyby obserwator nie wystartował, strona i tak jest widoczna;
- `beforeprint` odsłania wszystko przed wydrukiem i przed Ctrl+F.

## Czego ta biblioteka NIE robi

Sygnatury. Ona daje rytm strony — wejścia, paralaksy, postęp, mikro-ruch. **Rzecz, której nie
da się wyciąć bez zabicia strony, piszesz sam, dla tego jednego klienta** (NASTART.md D3).

## Podgląd

`demo.html` — wszystkie atrybuty na jednej stronie. Otwórz też z `?static=1`, żeby zobaczyć
wersję bez ruchu; obie muszą być kompletne.
