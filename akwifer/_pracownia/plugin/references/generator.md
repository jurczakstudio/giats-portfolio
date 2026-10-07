# Generator — konwencja Pythona

Każdy projekt to katalog w `C:\Users\szymo\Desktop\strony\<klient>` z tym samym szkieletem.
Wzory do skopiowania: `lewartowski` (najczystszy, 11 podstron), `piryt`, `moszczynski` (3D).

## Pliki

| Plik | Rola |
|---|---|
| `content.py` | **Wyłącznie dane.** `BIZ`, `TOWNS`, `SERVICES`, `HOME`, `GALLERY`, `MATERIALS`. Zero HTML. |
| `brand.py` | Paleta, tokeny, sygnet SVG. |
| `fonts.py` | Pobiera kroje z Google Fonts do `site/assets/fonts`, generuje `fonts.css`. Uruchamiane raz. |
| `images.py` | Kadrowanie, skalowanie, WebP → `site/assets/img/w/*.webp` + `manifest.json`. |
| `build.py` | Generator: powłoka, podstrony, JSON-LD, sitemap, robots. `python build.py` → `site/`. |
| `make_model.py` | Opcjonalnie: FBX/GLB → model do Three.js. |
| `README.md` | **Obowiązkowy.** Brand, adres demo, status DEMO, port, komendy przebudowy, struktura. |
| `site/` | Produkt. Tylko to trafia na Cloudflare. |

## Kolejność przebudowy

```bash
python fonts.py     # raz na projekt
python images.py    # po zmianie zdjęć
python build.py     # zawsze
```

## Wzorce z `build.py`, których się trzymamy

- `BASE` — pełny adres, z którego biorą się kanoniczne URL-e, sitemapa i `og:image`.
- `DEMO = True/False` — steruje `noindex,nofollow` i sitemapą.
- `_ver()` — md5 z treści `site.css` + `site.js`, pierwsze 8 znaków, doklejane jako `?v=`.
  Osobno `FV` dla `fonts.css`. Bez tego klient widzi stary CSS po podmianie.
- `ICO` — słownik ikon SVG inline. Zero bibliotek ikon, zero sprite'ów.
- `pic(slug, sizes, alt, cls, eager)` — jedna funkcja generująca `<picture>` z `srcset`
  z manifestu. Wszystkie obrazy przez nią.
- Kodowanie: `# -*- coding: utf-8 -*-` na górze, `encoding='utf-8'` przy każdym `open`.
  Windows domyślnie da cp1250 i polskie znaki się rozjadą.

## Port lokalny

Zajęte: 5173, 8748, 8749, 8756, 8760, 8761, 8762, 8763, 8764. Dodatkowo 8103, 8107, 8108
dla podglądów live. **Nowy projekt bierze kolejny wolny od 8765 w górę.**

Wpis do `strony/.claude/launch.json`:

```json
{ "name": "<klient>", "runtimeExecutable": "python",
  "runtimeArgs": ["-m","http.server","<port>","--directory","<klient>/site"],
  "port": <port> }
```

Podgląd odpalamy przez `preview_start` z tą nazwą, nigdy przez Bash.

## Czego w generatorze nie robimy

- Nie budujemy HTML-a w `content.py`. Dane osobno, składanie osobno.
- Nie wklejamy tego samego bloku do dziesięciu podstron — jedna funkcja powłoki.
- Nie dodajemy zależności pip. Standardowa biblioteka wystarcza (Pillow tylko w `images.py`,
  jeśli naprawdę trzeba).
- Nie commitujemy `__pycache__`.

## Build sprząta po sobie

`build.py` ma **usuwać z katalogu wynikowego podstrony, których już nie produkuje.**
Bez tego osierocony katalog przeżywa każdą przebudowę: bramki sprawdzające zawartość
`site/` przechodzą na tym, co zostało, czyli potwierdzają stan, którego nie ma w kodzie,
a na Cloudflare jedzie publicznie dostępna podstrona, której w generatorze nie ma.
Jeśli powstała przed wprowadzeniem trybu DEMO — bez `noindex`.

Kasujemy **wyłącznie katalogi podstron produkowane w danym cyklu**. Nigdy `assets/`,
`img/`, pobranych krojów, `CNAME`, `.git` ani niczego wgranego ręcznie.

Sprawdzenie jest zachowaniem, nie czytaniem nazw funkcji: zbuduj, dorzuć do `site/`
katalog `zzz-widmo/index.html`, zbuduj ponownie, sprawdź, czy przeżył.

Wzór razem z testem: `meblex/build.py` (commit `0804eeb`). Znalezione testem mutacyjnym
20.09.2026 — pierwszy przebieg złapał 9 z 10 mutacji i to właśnie ta przeżyła.

**Stan reszty pracowni nie jest sprawdzony.** Zanim wdrożysz cokolwiek ponownie
w starszym projekcie, porównaj listę adresów produkowanych przez generator z tym,
co faktycznie leży w `site/`.
