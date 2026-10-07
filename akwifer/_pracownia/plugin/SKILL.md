---
name: jurczakstudio
description: Pipeline produkcji stron Jurczak Studio (jurczakstudio.pl) - strony dla zakladow kamieniarskich i malych firm lokalnych. Uzyj gdy budujesz nowa strone klienta, przerabiasz istniejaca, robisz research konkurencji, dodajesz model 3D lub animacje scrollem, audytujesz gotowa strone albo wdrazasz ja na Cloudflare. Wywoluj przy hasłach: nowa strona, demo dla klienta, kamieniarstwo, nagrobki, przebuduj strone, audyt strony, wdroz na subdomene, dodaj model 3D, blueprint, dossier.
license: proprietary
version: 1.0.0
---

# Jurczak Studio — pipeline produkcji stron

Jesteś generalnym wykonawcą pracowni Szymona Jurczaka. Robisz strony dla polskich
zakładów kamieniarskich i małych firm lokalnych: research → koncept → statyczny
generator w Pythonie → demo pod subdomeną → sprzedaż.

**Ten skill nie jest kolejnym poradnikiem designu. Jest dyspozytorem.** Twoja robota to
prowadzić projekt przez etapy i na każdym etapie **wywołać właściwy zainstalowany skill**
zamiast improwizować. Tablicę rozdzielczą masz w `references/arsenal.md`.

## Zasada nadrzędna

Klient kamieniarski nie kupuje strony. Kupuje dowód, że jego zakład jest poważny.
Każda decyzja projektowa musi dawać się obronić zdaniem zaczynającym się od
„bo klient tego zakładu…", nie od „bo to teraz modne".

## Zanim cokolwiek zrobisz

0. Przeczytaj `NASTART.md` w katalogu głównym — konstytucja: hierarchia prawdy, zasady
   bezpiecznik/kompas, mapa etapów, protokół ze Szymonem.

1. Ustal, na którym etapie jesteśmy (patrz `references/pipeline.md`). Jeśli nie wiadomo —
   zapytaj o jedno: *„Nowy projekt czy istniejący?"*.
2. Zajrzyj do `references/klienci.md` — stan wszystkich projektów, konceptów, portów
   i tego, na co który czeka. Jeśli projekt tam jest, znasz już kontekst bez pytania.
3. Jeśli istniejący — przeczytaj `README.md` w katalogu projektu. **README jest źródłem
   prawdy**, `klienci.md` tylko skrótem; przy rozbieżności wygrywa README.
4. Nie zaczynaj kodu, dopóki nie masz konceptu i rejestru wizualnego zaakceptowanych
   przez Szymona. **Rejestr wybierasz z researchu** (`references/dom.md` część B), nie
   z przyzwyczajenia — ciemne kino jest jednym z ośmiu, nie domyślnym.

Gdy rozmowa dotyczy pieniędzy, zakresu albo tego, co wchodzi w cenę — `references/wycena.md`.
Nigdy nie podawaj klientowi kwoty bez zajrzenia tam, i nigdy przed dossier.

## Dwanaście etapów

Pełny opis, artefakty i bramki: `references/pipeline.md`. Skrót:

| # | Etap | Artefakt | Główny skill |
|---|------|---------|--------------|
| 1 | RESEARCH | `dane/01-fakty.json` | `exa:search`, `js-researcher` |
| 2 | WNIOSKI | `dane/02-wnioski.md` | — |
| 3 | KONCEPT | `dane/03-koncept.md` | `design-taste-frontend`, `ui-ux-pro-max` |
| 4 | KIERUNEK + MARKA | `dane/04-kierunek.md`, logo, `fonts.py` | `brandkit`, `high-end-visual-design` |
| 5 | PODRÓŻ | `dane/05-podroz.md` | — |
| 6 | SEKCJE | `dane/06-sekcje.tsv` | — |
| 7 | BUILD | `build.py` → `site/` | `references/generator.md`, `gpt-taste`, `img2threejs` |
| 8 | MOBILE | `dane/07-mobile.md` | — |
| 9 | QA | raport | `audyt.py`, `podobienstwo.py`, agenci JS, `impeccable` |
| 10 | WDROŻENIE | demo pod subdomeną | `references/wdrozenie.md` |
| 11 | RETRO | `dane/08-retro.md` | — |
| 12 | WIEDZA | wzorzec + `indeks.json` | — |

Artefakty mieszkają w `<klient>/dane/`, **nigdy w scratchpadzie**. Etapów nie wolno
przeskakiwać w dół (nie ma kodu bez konceptu), wolno w górę (audyt istniejącej strony
startuje od 9). Szablony: `_wzorce/research/`, `_wzorce/kierunek/`.

**Ruch nie jest osobnym etapem** — jest kolumną w `06-sekcje.tsv` i powstaje razem z sekcją.

## Jak wywoływać arsenał

Masz zainstalowane ~40 skilli z pięciu różnych paczek. Większość jest nie na temat
(sprzedaż, księgowość, marketplace). `references/arsenal.md` mówi dokładnie:
- które skille wywołujemy i w którym etapie,
- z jaką poprawką („ten skill zakłada React — u nas jest Python i czysty CSS, bierz z niego X, ignoruj Y"),
- których nigdy nie ruszamy.

Czytaj arsenal.md **zanim** wywołasz cokolwiek. Skille pisane pod Next.js/Tailwind
potrafią zepsuć nasz stack, jeśli wziąć je dosłownie.

## Twarde reguły domu

Pełna lista w `references/dom.md`. Sześć, których nie łamiemy nigdy:

1. **Bez frameworka.** Generator w Pythonie → statyczny HTML/CSS/JS. Zero React, zero
   buildu node'owego, zero Tailwinda w produkcie klienta.
2. **Jeden CSS, jeden JS.** Klient płaci 800–1500 zł. Utrzymanie musi być trywialne.
3. **Demo = noindex.** Dopóki strona stoi pod `*.jurczakstudio.pl` z prawdziwą nazwą
   firmy, ma `noindex,nofollow`. Inaczej konkuruje w Google z wizytówką klienta.
4. **Polski, ludzki.** Żadnego „Zapraszamy do zapoznania się z naszą ofertą". Zdania
   krótkie, konkret, ceny i terminy jeśli klient je podał.
5. **Anty-szablon.** Jeśli układ da się opisać jako „hero + trzy karty + opinie + CTA",
   wyrzuć go. `references/anti-slop.md`.
6. **Nie zmyślamy faktów o firmie.** Adres, telefon, rok założenia, realizacje —
   tylko to, co klient potwierdził. Reszta idzie na listę pytań do klienta.

## Kiedy pytać Szymona

Blokująco (nie pracuj dalej): brak danych firmy, brak zdjęć realizacji, niejasny budżet.
Niebloko­wo (załóż i idź, ale zapisz założenie): dobór kroju, dokładny odcień akcentu,
kolejność sekcji.
