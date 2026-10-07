# Wycena — widełki i zakres

> **Status: propozycja, nie cennik.** Twarde dane, jakie mamy, to dokładnie dwa punkty:
> umowa `grajkowski` na **800 zł** (sprzedana 27.08.2026) i budżet klienta `lewartowski`
> **ok. 1500 zł**. Reszta poniżej to progi wyprowadzone z tych dwóch kotwic i z realnego
> nakładu na dotychczasowe projekty. **Zanim podasz klientowi cenę z tej tabeli,
> potwierdź ją u Szymona.** Kiedy potwierdzi — usuń tę ramkę i zostaw sam cennik.

---

## Trzy progi

### Próg I — 800 zł · „Wizytówka"

Dla zakładu, który nie ma nic i potrzebuje istnieć w sieci. Kotwica: `grajkowski`.

**Wchodzi:**
- 1 strona przewijana (hero, usługi, realizacje, kontakt) albo motyw WordPress
- do 10 zdjęć klienta: kadrowanie, WebP, `srcset`
- teksty pisane przez nas na podstawie opinii Google
- JSON-LD `LocalBusiness`, `sitemap.xml`, `robots.txt`
- formularz kontaktowy albo `tel:` + mapa dojazdu
- hosting demo pod `*.jurczakstudio.pl` do czasu decyzji
- instrukcja obsługi w PDF

**Nie wchodzi:** logo, 3D, podstrony, blog, wielojęzyczność, opieka po wdrożeniu.

---

### Próg II — 1500 zł · „Zakład"

Standard pracowni. Kotwica: `lewartowski` (11 podstron + logo + księga znaku).

**Wchodzi wszystko z progu I, plus:**
- 8–12 podstron: usługi osobno, galeria z filtrami, materiały, o zakładzie, kontakt
- **własny koncept wizualny z nazwą** (metafora trzymająca całą stronę)
- logo SVG + sygnet + favicon, kroje osadzone lokalnie
- JSON-LD `FAQPage` i `BreadcrumbList`, strony pod miejscowości w okolicy
- animacje scrollem z `prefers-reduced-motion` i trybem `?static=1`
- dossier + blueprint jako PDF dla klienta
- wdrożenie na Cloudflare, DNS, certyfikat

**Nie wchodzi:** model 3D, sesja zdjęciowa, SEO po wdrożeniu.

---

### Próg III — od 2500 zł · „Monolit"

Gdy strona ma być argumentem sprzedażowym, nie wizytówką.
Odpowiada nakładowi na `moszczynski`, `royalgranit`, `serwin`, `groby`.

**Wchodzi wszystko z progu II, plus:**
- **model 3D sterowany scrollem** (Three.js, własny parser FBX→GLB albo `img2threejs`),
  z fallbackiem dla słabych urządzeń i braku WebGL
- pełna księga znaku
- 20+ URL-i, rozbudowana architektura informacji
- treści pod SEO lokalne, wejście do SEO Command Center
- opcjonalnie: wideo tła, sesja zdjęciowa realizacji

Model 3D to **osobna, największa pozycja kosztowa** — parser, dziesiątki iteracji
sculptu, optymalizacja wagi, testy wydajności na mobile. Jeśli klient go nie chce,
próg III schodzi do II.

---

## Dodatki

| Pozycja | Widełki | Uwaga |
|---|---|---|
| Model 3D sterowany scrollem | +800–1200 zł | Największy nakład. Wymaga pliku źródłowego albo dobrego zdjęcia. |
| Logo + księga znaku osobno | +400 zł | Wchodzi w próg II. |
| Sesja zdjęciowa realizacji | wycena osobno | Dojazd + obróbka. Bez zdjęć klienta strona jest o połowę słabsza. |
| Strona pod dodatkową miejscowość | +80 zł/szt. | SEO lokalne, sensowne od 3 sztuk w górę. |
| Opieka miesięczna | 100–200 zł/mies. | Aktualizacje treści, kopie, monitoring. **Do decyzji, czy w ogóle to sprzedajemy.** |
| Migracja na domenę klienta po sprzedaży | w cenie | `DEMO = False`, `BASE`, `pattern`, GSC. |

## Zasady rozmowy o cenie

1. **Nie podawaj ceny przed dossier.** Najpierw research, potem zakres, na końcu kwota.
   Cena bez zakresu zawsze wyjdzie za wysoka.
2. **Podawaj próg, nie kwotę z sufitu.** „Zakład — 1500 zł, w tym logo i 11 podstron",
   nie „no, jakieś półtora tysiąca".
3. **Demo jest darmowe i to jest nasz atut.** Klient widzi swoją stronę zanim zapłaci.
   Dlatego demo musi być skończone, nie szkicowe.
4. **Nie schodź z ceny — schodź z zakresu.** Klient chce taniej? Zdejmij 3D albo podstrony,
   nie rabat. Rabat uczy, że pierwsza cena była zmyślona.
5. **Zdjęcia to najczęstszy powód, dla którego strona wygląda tanio.** Jeśli klient nie ma
   zdjęć realizacji, powiedz to wprost przy wycenie i zaproponuj sesję.
6. **Wygenerowane obrazy nigdy nie idą jako realizacje klienta.** Tło i ujęcia poglądowe —
   tak, oznaczone. Nagrobek, którego klient nie zrobił — nigdy.

## Kalkulacja przed podaniem ceny

Zanim podasz kwotę, policz na głos: liczba podstron × ~1 h, koncept i marka ~4 h,
generator ~6 h, 3D ~15 h, audyt i poprawki ~3 h, wdrożenie ~1 h. Jeśli wychodzi więcej
godzin niż kwota podzielona przez ~60 zł/h, to nie jest ten próg.
