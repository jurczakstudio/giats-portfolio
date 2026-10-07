# Pipeline — dwanaście etapów

Każdy etap ma **artefakt** (plik w `<klient>/dane/`) i **bramkę** (czego nie wolno
przekroczyć bez zgody Szymona albo bez przejścia skryptu). Etap bez artefaktu = etap
niezrobiony.

Artefakty mieszkają w katalogu projektu, **nigdy w scratchpadzie**. Generator Serwina
żył w katalogu tymczasowym sesji i był o jedno czyszczenie od utraty warstwy generującej
27 stron. Jeśli plik produkuje stronę, nie jest jednorazowy.

Szablony do skopiowania: `_wzorce/research/`, `_wzorce/kierunek/`.
Etapów nie wolno przeskakiwać w dół. W górę wolno — audyt zastanej strony startuje od 9.

| # | Etap | Artefakt |
|---|---|---|
| 1 | RESEARCH | `dane/01-fakty.json` |
| 2 | WNIOSKI | `dane/02-wnioski.md` |
| 3 | KONCEPT | `dane/03-koncept.md` |
| 4 | KIERUNEK + MARKA | `dane/04-kierunek.md`, logo, `fonts.py` |
| 5 | PODRÓŻ | `dane/05-podroz.md` |
| 6 | SEKCJE | `dane/06-sekcje.tsv` |
| 7 | BUILD | `build.py` → `site/` |
| 8 | MOBILE | `dane/07-mobile.md` |
| 9 | QA | raport z bramek i agentów |
| 10 | WDROŻENIE | demo pod subdomeną |
| 11 | RETRO | `dane/08-retro.md` |
| 12 | WIEDZA | wpis w `_wzorce/`, odcisk w `indeks.json` |

---

## 1. RESEARCH → `dane/01-fakty.json`

Kolejność źródeł i czego nie robić: **`_wzorce/research/README.md`**. Szablon:
`_wzorce/research/szablon-fakty.json`.

Zbierz: pełna nazwa i forma prawna, adres, telefon, e-mail, rok założenia, właściciel
z imienia, ocena i liczba opinii Google, co powtarza się w opiniach, czy mają stronę,
czy mają wizytówkę, konkurencja w promieniu 30 km — **ze zrzutem, układem i paletą każdej**
(karmi oś C w `podobienstwo.py`).

Osobno: **czy klient ma materiał wizualny.** Zero zdjęć nie jest problemem do odkrycia
w połowie buildu — jest wejściem do wyboru rejestru.

Wywołaj `exa:search`, WebSearch. Agent: `js-researcher`.

**Bramka:** każdy fakt ma `id`, `status` (`POTWIERDZONE` / `WNIOSKOWANE` / `PYTANIE`)
i `zrodlo`. Fakt bez źródła jest błędem, nie faktem. Lista pytań do klienta wychodzi
do Szymona razem z listą potrzebnych zdjęć.

## 2. WNIOSKI → `dane/02-wnioski.md`

Maksymalnie pięć. Każdy w formie `F3 + F7 → dlatego X` i każdy kończy się zdaniem
zaczynającym się od „Konsekwencja projektowa:".

**Bramka — trzy testy:** test 500 konkurentów (wniosek prawdziwy dla każdego kamieniarza
w Polsce nie jest wnioskiem), test konsekwencji, test falsyfikacji. Szczegóły:
`_wzorce/research/README.md`.

## 3. KONCEPT → `dane/03-koncept.md`

Szablon: `_wzorce/kierunek/szablon-koncept.md`. Dziesięć pytań, rejestr wizualny
z `dom.md` część B, sygnatura (interakcja + ruch + materiał), **trzy konsekwencje
strukturalne** i **decyzja własna** — ta, której nie da się uzasadnić stylem pracowni.

Nasze dotychczasowe koncepty: „Dwa kamienie" (gramar), „Lapidarium" (lapinski),
„Kronika" (police), „Kamień i światło" (serwin), „Nokturn" (groby), „Plac z płytami"
(lewartowski), „Korona" (royalgranit), „Monolit" (moszczynski), „Regestr" (portfolio),
„RYT" (liternik), „1200°" (spieki), „Skład" (granitexpress), „Plac" (kamar).

Wywołaj `design-taste-frontend`, `frontend-design`, `ui-ux-pro-max` (kroje i paleta).

**Bramka:** Szymon akceptuje nazwę konceptu, rejestr i paletę. Bez tego nie piszesz kodu.
Nazwa bez trzech konsekwencji strukturalnych jest etykietą, nie konceptem.

## 4. KIERUNEK i MARKA → `dane/04-kierunek.md` + logo + `fonts.py`

**Każda decyzja projektowa cytuje numer wniosku z etapu 2.** Decyzja bez cytatu jest
decyzją z powietrza — kasujesz ją albo dopisujesz wniosek, z którego naprawdę wynika.
To jest mechanizm, który zamienia research w projekt. `audyt.py` to sprawdza.

Marka: logo jako SVG z tekstu zamienionego na ścieżki (wzór `lewartowski/brand/make_logo.py`),
sygnet osobno, favicon z sygnetu. `fonts.py` pobiera kroje lokalnie do `site/assets/fonts`.
**Sprawdź `latin-ext`** — Prata, Italiana i Antic Didone nie mają polskich znaków.
Skala typograficzna deklarowana jako tokeny `--fs-*` w `brand.py`.

Wywołaj `brandkit` (fallback: SVG), `high-end-visual-design` po wartości liczbowe,
`imagegen-frontend-web` po referencje wizualne.

**Bramka:** zero decyzji bez numeru wniosku. Tokeny typograficzne zadeklarowane.

## 5. PODRÓŻ → `dane/05-podroz.md`

Szablon: `_wzorce/kierunek/szablon-podroz.md`. **Ten etap nie istniał do 16.09.2026
i to jest powód, dla którego energia stron zawsze spadała po hero** — sekcje 5, 6, 7
powstawały jako pojemniki na resztę treści.

Akty nazwane rzeczownikiem stanu (test z Serwina), co czytelnik wie wchodząc i wychodząc
z każdego, gdzie zmienia się rytm i dlaczego tam, jeden moment kulminacyjny, powrót
sygnatury na każdej podstronie.

**Bramka:** „wychodzi wiedząc" aktu N = „wchodzi wiedząc" aktu N+1. Zero nazw
funkcjonalnych („O nas", „Usługi", „CTA").

## 6. SEKCJE → `dane/06-sekcje.tsv`

Szablon: `_wzorce/kierunek/szablon-sekcje.tsv`. Maszynowy, czytany przez `audyt.py` —
plan i wynik mierzone tym samym plikiem.

Kolumny: akt · podstrona · **obiekt** · **ruch** · **mobil** · typ · fraza · sygnatura.

Kolejność jest nienegocjowalna: `KONCEPT → PODRÓŻ → potrzeba czytelnika → wydarzenie
wizualne → dopiero typ kompozycji`. Katalog typów **nie jest menu**; typ wpisujesz
na końcu, jako nazwę tego, co wyszło z aktu.

**Bramka:** każda sekcja ma obiekt (nie „tekst"). Kolumna `mobil` wypełniona wszędzie.

## 7. BUILD → `build.py` + `site/`

Konwencja: `generator.md`. **Ruch nie jest osobnym etapem** — jest kolumną w `06-sekcje.tsv`
i powstaje razem z sekcją. Do 16.09.2026 był etapem piątym z siedmiu, czyli czymś, co się
dodaje, jeśli zostanie czas; stąd `granitexpress` z 1,4 kB JavaScriptu na 39 sekcji.

Biblioteka ruchu: `_wzorce/ruch/` — kopiuj `ruch.js` i `ruch.css` bez zmian, sygnaturę
pisz osobno. 3D: własny parser FBX→GLB (`moszczynski/make_model.py`) albo `img2threejs`.
Model musi mieć fallback, gdy WebGL niedostępny.

Wywołaj `gpt-taste` (tylko warstwa ruchu), `writing-guidelines` na teksty.
Przeczytaj `anti-slop.md` przed pierwszą linijką HTML.

**Bramka:** `build.py` przerywa, gdy brakuje `dane/03`–`dane/06`:

```python
BRAK = [f for f in ('03-koncept.md', '04-kierunek.md', '05-podroz.md', '06-sekcje.tsv')
        if not (Path(__file__).parent / 'dane' / f).exists()]
if BRAK:
    raise SystemExit('Brak artefaktów: %s — patrz pipeline.md' % ', '.join(BRAK))
```

## 8. MOBILE → `dane/07-mobile.md`

Szablon: `_wzorce/kierunek/szablon-mobile.md`. Osobny przebieg projektowy **po** buildzie
desktopowym, **przed** audytem. Mobile jest osobną kompozycją, nie tą samą w jednej kolumnie.

**Bramka:** przewrotki kolumnowe poniżej 60 % sekcji, co najmniej jedna sekcja istniejąca
tylko na jednym urządzeniu, sygnatura działa na 390 px.

## 9. QA → raport

Kolejno:

1. `python ../_wzorce/audyt/audyt.py .` — bezpieczniki i kompasy.
2. `python ../_wzorce/audyt/podobienstwo.py .` — czy to nie jest nasza poprzednia strona.
3. `js-lowca-bugow` — przeglądarka, konsola, sieć, mobile 390, klawiatura.
4. `web-design-guidelines` — dostępność i wytyczne interfejsu.
5. `impeccable` — polish/critique.
6. `js-krytyk-designu` — na zrzutach, „gdzie to wygląda jak z generatora".
   Osobno: **zrzuty z podmienionymi nazwą, telefonem i miastem** — jeśli agent nie potrafi
   powiedzieć, co to za firma, w projekcie jest branża zamiast klienta.
7. `writing-guidelines` — teksty.

**Bramka:** zero zamkniętych bezpieczników, zero błędów w konsoli, zero poziomego scrolla
na 390 px, Lighthouse mobile ≥ 90 w Performance i Accessibility — **zmierzony**
(chrome-devtools), nie oszacowany.

## 10. WDROŻENIE → `https://<klient>.jurczakstudio.pl`

Szczegóły: `wdrozenie.md`. Zawsze tryb DEMO (`noindex,nofollow`) dopóki klient nie kupił.
Uwaga: w DEMO **nie blokujemy crawlu** w `robots.txt` — `Disallow` uniemożliwia robotowi
przeczytanie `noindex`.

Do klienta idą: link do demo, dossier, blueprint, wycena.

## 11. RETRO → `dane/08-retro.md`

Te same pomiary co w `_wzorce/00-audyt-2026-09.md`, żeby dało się porównać. Plus:
plan z `05-podroz.md` kontra to, co faktycznie wyszło. Które akty przetrwały, które
zamieniły się w pojemniki na treść i dlaczego.

## 12. WIEDZA → `_wzorce/` + `indeks.json`

```bash
python ../_wzorce/audyt/audyt.py . --zapisz     # odcisk do indeksu
```

Jeśli Szymon ocenił projekt dobrze — nowy wzorzec `_wzorce/NN-<klient>-wzorzec.md`
wg struktury z `_wzorce/README.md`. **Sekcja „czego projekt nie rozwiązał" jest
obowiązkowa i jest najcenniejszą częścią.**

Zawsze: wpis do dziennika w `NASTART.md` — nie opis projektu, tylko reguła, którą da się
zastosować gdzie indziej.
