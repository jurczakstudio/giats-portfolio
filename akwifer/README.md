# AKWIFER — strona wzorcowa zawodu „studnie głębinowe” (Jurczak Studio)

**Status:** zbudowana (etapy 1–9), bramka `audyt.py` otwarta 12/12. Nie wdrożona.
**Firma fikcyjna** — telefon (`600 000 000`), godziny, zasięg i cennik są PRZYKŁADOWE, oznaczone na stronie.
Adres planowany: `akwifer.jurczakstudio.pl` (DEMO = noindex). Gałąź `studnie-wzorzec` w repo `giats-portfolio`
— katalog `akwifer/` jest niezależny od aplikacji Next.js w korzeniu repo i jej nie dotyka.

## Koncept: LEJ
Tło każdej strony to żywa mapa hydroizohips (WebGL): poziomice zwierciadła wody co 0,25 m.
**Kursor jest pompą** — wokół niego zwierciadło opada w lej depresji (kształt Dupuita, promień Sichardta,
przewyższenie ×3, podpisane w legendzie). Klik wierci studnię. Arkusze z treścią mają **okna-otwory**,
przez które widać tę samą mapę, a pod oknem odczyt głębokości liczony z tego samego pola, co obraz.
**Kulminacja:** model próby pompowania — suwak Q i grunt (k) liczą depresję s, R i wydajność jednostkową,
a lej w oknie obok rośnie razem z liczbami.

Z `giats-portfolio` (MIT, E. Giatsidis) wzięte są **techniki**: okna w treści i tło z liniami w shaderze.
Kod jest własny, bez Nexta/R3F/GSAP i bez grafik — przypisanie w stopce strony.

Druga strona studniarska pracowni, po VIJACH „ZWIERCIADŁO” (jasna mgła + zdjęcia klientów). Tu: papier mapy,
zero zdjęć (firma fikcyjna — nie udajemy realizacji), obrazem jest fizyka wody.

## Pliki
| | |
|---|---|
| `dane/01–07` | fakty zawodu ze źródłami, wnioski W1–W5, koncept, kierunek, podróż, sekcje, mobile |
| `content.py` | dane (model, cennik przykładowy, etapy, pytania) |
| `brand.py` | paleta, tokeny `--fs-*`, sygnet |
| `build.py` | generator 5 adresów + 404, `_headers` (noindex), bramka |
| `src/site.css`, `src/site.js` | jeden CSS, jeden JS (shader w JS) |
| `_pracownia/` | kopia warsztatu: `_wzorce/ruch`, `_wzorce/audyt`, NASTART, plugin |

## Komendy
```bash
python fonts.py     # raz (zrobione)
python build.py     # zawsze — kończy się bramką
python -m http.server 8788 --directory site
node dane/zrzuty/zrzut.mjs / /kontakt/      # całe strony 390 i 1440 (?static=1)
node dane/zrzuty/kadr.mjs / 1440            # kadr z pompą pod kursorem i oknem próby
node dane/zrzuty/test.mjs                   # odsłonięcia, okna, symulator, karta, poziomy scroll
```
Wdrożenie (lokalnie, `wrangler` zalogowany): dwuklik `WDROZ.cmd`.

## Do zrobienia lokalnie
`podobienstwo.py` (porównanie z innymi projektami), Lighthouse i pomiar z dławieniem CPU 6× (shader na telefonie),
`js-krytyk-designu`. Przy sprzedaży konkretnej firmie: nazwa, telefon, zasięg, cennik, opinie, zdjęcia realizacji.

## Zauważone przy okazji
`fonts.py` z VIJACH nazywał pliki bez wagi — przy krojach statycznych (JetBrains Mono 400/500) druga waga
nadpisywała pierwszą. Tu poprawione (waga w nazwie pliku); w VIJACH do sprawdzenia.
