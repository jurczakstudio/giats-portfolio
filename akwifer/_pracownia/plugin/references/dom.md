# Dom — system projektowy Jurczak Studio

Ten plik ma dwie części i **nie wolno ich mylić**:

| | Co to jest | Czy podlega dyskusji |
|---|---|---|
| **A. ZASADY DOMU** | jak pracujemy — obowiązuje w każdym projekcie | nie |
| **B. REJESTRY WIZUALNE** | jak strona może wyglądać — wybierane z researchu | tak, co projekt |

Do 16.09.2026 te dwie rzeczy były zlepione w jedno zdanie: *„domyślaj się w stronę ciemną,
filmową, luksusową"*. To sprawiło, że **kierunek wizualny stał się konstytucją** — dziewięć
konceptów pod rząd zbiegło się do jednego wyglądu, a `podobienstwo.py` zaczął to wreszcie
mierzyć. Ciemne kino zostaje jednym z rejestrów, mocnym i dobrze nam znanym, ale przestaje
być domyślną odpowiedzią na pytanie, którego nikt nie zadał.

---

# A. ZASADY DOMU

Charakteryzują pracę pracowni niezależnie od tego, jak strona wygląda.

### 1. Art direction zamiast szablonu
Układ wynika z konceptu, nie z listy sekcji. Jeśli stronę da się opisać jako
„hero + trzy karty + opinie + CTA", nie ma art directionu — jest wypełniony szablon.

### 2. Typografia jest narzędziem, nie ustawieniem
Para krojów z charakterem. Skala **zadeklarowana jako tokeny**, nie zbierana po drodze
(u Lewartowskich narosły 23 rozmiary na stronie głównej — to nie była decyzja).
Nic poniżej 14 px: nasz odbiorca ma często 50+ lat.

### 3. Materialność
Strona o kamieniu ma nieść kamień: teksturę, ziarno, krawędź, światło na polerze.
Powierzchnię wolno malować CSS-em, renderem, bryłą 3D albo fotografią — **byle była**.

### 4. Ruch znaczy coś
Rzeźba obracana scrollem pokazuje bryłę z każdej strony i to jest argument sprzedażowy.
Ruch, który nie poprawia zrozumienia, hierarchii, materialności ani sprzężenia zwrotnego —
wypada. `fade-in-up` na wszystkim to nie warstwa ruchu, to tapeta.

### 5. Kompozycja przed dekoracją
Każda sekcja niesie **obiekt** — zdjęcie w realnej skali, rysunek, powierzchnię, bryłę,
film albo sterowanie. Sam tekst, choćby najlepiej złożony, obiektem nie jest.
Egzekwuje to `_wzorce/audyt/audyt.py`.

### 6. Charakter i narracja
Strona ma przebieg, nie listę. Akty mają nazwy będące rzeczownikami stanu („Cisza",
„Materia", „Archiwum"), nie funkcji („O nas", „Usługi", „CTA").

### 7. Jakość obrazu jest warunkiem, nie ozdobą
Zdjęcia zamawiamy na etapie 1, nie przed wdrożeniem. Głód obrazu jest głównym powodem,
dla którego sekcje zamieniają się w akapity — `_wzorce/obraz/`.

### 8. Odwaga
Wersja bezpieczna jest wersją przegraną. Jeśli po obejrzeniu strony nie ma się ochoty
pokazać jej komuś, kto nie jest klientem — nie jest skończona.

### 9. Spójność przez całość
To, co zaczyna hero, ma wracać na każdej podstronie. Sygnatura wycinalna bez straty
nie jest sygnaturą, tylko dekoracją hero.

### 10. Zero slopu
`anti-slop.md` — czerwona lista. Czytana przed pierwszą linijką HTML, nie po.

### 11. Premium bez „premium look"
Nie robimy złotych gradientów i marmurowych teł na siłę. Wrażenie klasy bierze się
z typografii, odstępów, kadrowania i konsekwencji — nie z efektów.

### 12. Nie zmyślamy
Adres, telefon, rok, realizacje — tylko potwierdzone. Obraz generowany oznaczony
jako poglądowy. Zawsze.

---

# B. REJESTRY WIZUALNE

Rejestr to **odpowiedź na klienta**, nie gust pracowni. Wybierany w `dane/03-koncept.md`
i tam uzasadniony. Lista jest otwarta i **nie jest menu** — jeśli research prowadzi
gdzie indziej, idziemy gdzie indziej i dopisujemy rejestr tutaj.

| Rejestr | Kiedy pasuje | Nasze próby |
|---|---|---|
| **ciemne kino** | marka funeralna, emocja, wieczór, telefon w ręku; firma sprzedaje powagę | groby v8 „Nokturn", kamar, liternik |
| **redakcyjny** | dużo do powiedzenia, treść jest towarem, klient ma wiedzę i archiwum | jasta „Płyta", memorial |
| **architektoniczny** | precyzja, wymiar, rysunek techniczny, budowlanka i wnętrza | spieki „1200°" |
| **jasny materiałowy** | wnętrza, blaty, spieki; klient sprzedaje powierzchnię, nie nastrój | kamat (od 15.09), artstonex |
| **brutal / minimal** | jedna przewaga i nic poza nią; cena, termin, konkret | granitexpress „Skład" |
| **ciepłe rzemiosło** | jeden człowiek przy warsztacie, ręka, narzędzie, portret | serwin częściowo |
| **typograficzny** | zero zdjęć od klienta, a słowo jest mocne (liternictwo, inskrypcja) | liternik „RYT" |
| **jasny przedmiotowy** | klient ma JEDEN mocny przedmiot sfotografowany na bieli (butelka, etykieta, pocztówka); jeden przedmiot na ekran, biel papieru przechodząca w mgłę, ogromna typografia za przedmiotem | bergkolonie „SFORA" (28.09) |
| **eksperymentalny** | portfolio, projekt autorski, klient o wysokiej tolerancji ryzyka | portfolio „Regestr" |

### Jak wybrać rejestr

1. Kto czyta, w jakim stanie i o której. *(Córka po telefonie ze szpitala, 23:40, telefon —
   to nie jest ten sam projekt co poniedziałek rano na desktopie.)*
2. Czym firma wygrywa i czy to widać, czy trzeba to opowiedzieć.
3. Co ma klient: zdjęcia, film, warsztat, archiwum, cennik, jednego charyzmatycznego człowieka.
4. Czym jeżdżą konkurenci — **rejestr musi różnić się od nich na co najmniej dwóch osiach**
   (układ, paleta, typografia, nośnik, ruch).

### Reguła jednej decyzji własnej

> **Każdy projekt musi mieć co najmniej jedną decyzję, której nie da się uzasadnić
> samym stylem pracowni — tylko tym klientem, jego odbiorcą albo konkretnym wnioskiem
> z researchu.**

Zapisywana w `dane/03-koncept.md` w formie: *decyzja → wniosek W_n → czego dzięki temu
nie dałoby się przenieść na inną firmę.* Nie chodzi o łamanie reguł dla samego łamania.
Chodzi o to, żeby w każdym projekcie była rzecz, której nie da się wytłumaczyć zdaniem
„bo tak robi Jurczak Studio".

---

# C. Wartości, które przenosimy między projektami

Te rzeczy działały i wolno je brać — **pod warunkiem że `podobienstwo.py` nie zgłosi
powtórzenia** (budżet: najwyżej 2 z 5 cech mogą wrócić z ostatnich trzech projektów).

## Typografia

Zawsze **para**: szeryfowy nagłówek o charakterze + neutralny grotesk na tekst.
Trzeci krój tylko jako inskrypcja, jeśli koncept tego wymaga.

| Projekt | Nagłówki | Tekst |
|---|---|---|
| gramar | Playfair Display (Bodoni Moda gubił napisy — zamiana 15.09) | Albert Sans |
| angela | Marcellus | Hanken Grotesk |
| graniton | Fraunces | Archivo |
| police | Instrument Serif | Instrument Sans |
| lewartowski | Bricolage Grotesque + Newsreader Italic | Instrument Sans |
| groby v8 | Bodoni Moda | Jost |
| hormon | EB Garamond | Geist |

Kroje pobieramy lokalnie (`fonts.py` → `site/assets/fonts` + `fonts.css`). Zero CDN,
zero `@import`. Powód: prędkość, prywatność, **działa bez sieci na pokazie u klienta**.
Sprawdzaj `latin-ext` przed wpisaniem kroju — Prata, Italiana i Antic Didone nie mają
ą ę ł ń ś ż. Kroje szeryfowe wymuszaj `font-variant-numeric: lining-nums`, inaczej
Cormorant i spółka dadzą „0" wysokości małego „o".

Skala: **deklarowana jako tokeny `--fs-*` w `brand.py`**. Każda wartość `font-size`
w CSS musi być tokenem albo `var()`. Wartość spoza zbioru to przypadek, nie decyzja —
`audyt.py` to blokuje. Liczba stopni jest wolna: sześć u jasty było świadome i dobre.

## Kolor

Jedno tło, jeden akcent, reszta to odcienie tła. Akcent niesie **znaczenie**:
patyna (lewartowski), mosiądz znicza (groby), złoto (royalgranit), miedź (liternik).
Dwa akcenty naraz to zawsze błąd.

Kontrast: tekst min. 4,5:1, duże nagłówki min. 3:1. Sprawdzane, nie zakładane.

## Ruch

Biblioteka i kontrakt nazw: `_wzorce/ruch/`. Obowiązkowo trzy bezpieczniki
(`prefers-reduced-motion`, `?static=1`, bramka JS) i dwa czuwaki
(pomiar prędkości scrolla, `setTimeout` 1200 ms).

Nie robimy: karuzeli opinii, liczników „lat doświadczenia" lecących od zera,
parallaxu na tle hero, `fade-in-up` na każdej sekcji z rzędu.
**Bezpiecznik:** żaden pojedynczy typ ruchu nie pokrywa więcej niż 50 % sekcji z ruchem.

## Treść

Polski, ludzki, konkretny. Zdanie ma nieść fakt albo emocję, najlepiej fakt.

- Dobrze: „Robimy w Cielimowie od 1991. Płyty tniemy u siebie, nie u pośrednika."
- Źle: „Zapraszamy do zapoznania się z naszą bogatą ofertą produktów kamieniarskich."

Nagłówek hero mówi, **czym ta firma wygrywa**, zdaniem, którego konkurencja nie mogłaby
skopiować, bo u niej byłoby nieprawdziwe. Telefon jako `tel:` w nagłówku i stopce,
widoczny bez scrolla na telefonie.

## Techniczne minimum każdej strony

- Semantyczny HTML, jeden `h1` na podstronę, `main`/`nav`/`footer`.
- JSON-LD: `LocalBusiness`, `FAQPage` gdzie są pytania, `BreadcrumbList`.
- `sitemap.xml` i `robots.txt` z `build.py`.
- Obrazy: WebP, `srcset`, `width`/`height`, `loading="lazy"` poza hero.
- Cache-busting: hash treści CSS/JS w `?v=`.
- Focus widoczny, nawigacja klawiaturą, skip-link.
- Zero poziomego scrolla na 375 px.
- **Mobile jest osobną kompozycją**, nie tą samą w jednej kolumnie — `_wzorce/kierunek/`.
