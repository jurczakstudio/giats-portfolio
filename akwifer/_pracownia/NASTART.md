# NASTART.md — konstytucja Jurczak Studio

**Czytaj przed pierwszą linijką każdego projektu. Wracaj po każdym skończonym i dopisuj
wpis do dziennika na końcu.**

Ten plik jest krótki celowo. Nie powtarza treści warsztatów — mówi, co obowiązuje zawsze
i gdzie jest reszta. Jeśli zaczyna rosnąć, znaczy, że coś powinno trafić do `_wzorce/`.

---

## 1. Hierarchia prawdy

```
README.md projektu  >  NASTART.md  >  _plugin-jurczakstudio  >  _wzorce/  >  CLAUDE.md
```

Cztery warstwy, każda z inną rolą. **Warstwa niżej nigdy nie powtarza treści warstwy
wyżej — odwołuje się do niej.**

| Warstwa | Gdzie | Za co odpowiada |
|---|---|---|
| **KONSTYTUCJA** | `NASTART.md` | ten plik: nienegocjowalne, mapa etapów, bezpiecznik/kompas, protokół ze Szymonem |
| **PROCES** | `_plugin-jurczakstudio` | dyspozytor etapów, komendy, agenci, `dom.md`, `anti-slop.md`, `arsenal.md` |
| **WARSZTAT** | `_wzorce/` | wykonywalne skrypty, szablony artefaktów, wiedza branżowa, case studies |
| **PROJEKT** | `<klient>/dane/` | artefakty tego jednego projektu |

Mapa „co gdzie mieszka i czego już nie ma": `_wzorce/MIGRACJA.md`.
Stan wyjściowy, do którego porównujemy retrospektywy: `_wzorce/00-audyt-2026-09.md`.
Wynik ataku na własny system: `_wzorce/00-stress-test-2026-09.md`.

`STRONA_ALL/` to **migawka** całego systemu w jednym folderze — wygodna, gdy budujesz
i nie chcesz skakać po katalogach. Generowana przez `python STRONA_ALL/odswiez.py`.
**Nie jest źródłem prawdy**; przy rozbieżności wygrywa oryginał.

---

## 2. Dwanaście zasad domu

Pełne brzmienie w `dom.md` część A. Skrót, żeby nie trzeba było otwierać:

art direction zamiast szablonu · typografia jako narzędzie · materialność · ruch, który
coś znaczy · kompozycja przed dekoracją · charakter i narracja · jakość obrazu jako
warunek · odwaga · spójność przez całość · zero slopu · premium bez „premium look" ·
nie zmyślamy.

**Kierunek wizualny nie jest zasadą domu.** Ciemno-filmowo-luksusowo to jeden z ośmiu
rejestrów w `dom.md` część B, wybierany z researchu i tam uzasadniany. Do 16.09.2026 był
zapisany jako domyślny i to jest powód, dla którego dziewięć konceptów zbiegło się
do jednego wyglądu.

> **Reguła jednej decyzji własnej:** każdy projekt musi mieć co najmniej jedną decyzję,
> której nie da się uzasadnić stylem pracowni — tylko tym klientem, jego odbiorcą
> albo konkretnym wnioskiem z researchu.

---

## 3. Bezpiecznik i kompas

Każdy próg jest jednym albo drugim. Trzeciej możliwości nie ma.

| | **BEZPIECZNIK** | **KOMPAS** |
|---|---|---|
| Co robi | blokuje build | nigdy nie blokuje |
| Co mierzy | obecność katastrofy | dryf, w porównaniu z poprzednimi projektami |
| Warunek | **nie do przejścia samym dopisaniem atrybutu** | — |

> **Próg, który da się przejść dopisując `data-*`, jest kompasem, nie bramką.**
> Tak zginął próg „≥60 % sekcji z ruchem": najtańszym sposobem jego przejścia było
> posypanie `data-rv="up"` po wszystkim, czyli dokładnie to, czego zabrania `dom.md`.

Bezpieczniki egzekwuje `_wzorce/audyt/audyt.py` (jakość strony) i
`_wzorce/audyt/podobienstwo.py` (czy to nie jest nasza poprzednia strona).
Jeden skrypt każdego rodzaju. **Dwa mechanizmy sprawdzające to samo są zakazane.**

> **Dopisane po stress teście 16.09.2026:** bezpiecznik musi mierzyć **relację między
> formą a klientem**, a nie samą formę. Wszystkie dwanaście mierzy dziś formę — dlatego
> strona-szablon przeszła 12 z 12. Drugi wniosek jest twardszy: **mechanizm, który każe
> mi uzasadnić decyzję, jest mechanizmem, który zawsze przejdę.** Bramka oparta na jakości
> uzasadnienia mierzy sprawność retoryczną, nie jakość projektu.

---

## 4. Znane luki bramek — czego NIE wolno im ufać

Bramki przeszły własny atak i go przegrały. Pełny zapis: `_wzorce/00-stress-test-2026-09.md`.
**Zielona bramka nie znaczy dobra strona.** Oto, czego nie sprawdza:

| Bezpiecznik | Najtańsze przejście, które nie poprawia niczego |
|---|---|
| sekcja niesie obiekt | `<details>` z dwoma pytaniami liczy się jako „sterowanie" |
| rytm obiektów | `material` i `sterowanie` wolno powtarzać bez końca |
| rytm konstrukcji | jeden akapit więcej = inny odcisk |
| rozkład kadrów | 11 kadrów — kontrola startuje od 12 |
| rozkład ruchu | siedem typów po trochu |
| sygnatura poza hero | atrybut w pustym `<div>` |
| bezpieczniki ruchu | trzy ciągi znaków w JS, bez implementacji |
| **mobile** | **czyta plan TSV, nie zbudowany CSS** |
| **kierunek cytuje wnioski** | **dopisany numer wniosku; warunek prawdziwości też przechodzi** |
| **rozkład ruchu** | **`data-rv="split"` bez struktury `<span class="w">` liczy się jako ruch, choć element stoi (obserwacja 0010)** |
| — (brak kontroli) | **kolizja nazw klas w jednym pliku CSS: `.pole` sekcji vs `.pole` etykiety formularza — 12/12 przy rozwalonym formularzu (obserwacja 0011)** |
| — (brak kontroli) | **objętość i linkowanie: 12/12 przy serwisie na 1531 słów, podstronach po ~100 słów i jednym linku przychodzącym; `[P10]` widoczne na produkcji (obserwacja 0012)** |
| kierunek cytuje wnioski | **sprawdza zgodność dwóch dokumentów, nie to, czy wniosek dotarł do HTML-a — W1 nie miał ani jednego zdania na stronie** |
| materiał | pliki po 16 bajtów przechodzą jako kadry |

Trzy defekty do naprawy przy najbliższej okazji: `sekcje()` nie widzi atrybutów na samym
`<section>` (przez co bezpiecznik ruchu wyłącza się sam), „ostatnie trzy projekty"
w `podobienstwo.py` to trzy **alfabetycznie** ostatnie, brak walidacji plików mediów.

**System wykrywa 0 z 8 rodzajów fałszywego premium** (premium-template, motion wallpaper,
image wallpaper, concept cosplay, research cosplay, anti-template cosplay, dark-house trap,
mobile cosplay). Wszystkie to warianty jednego zjawiska: *spełniam formę, nie mam treści*.

---

## 5. Trzy poziomy decyzji — czym różni się dobra strona od poprawnej

| | Znaczy | Test |
|---|---|---|
| **JUSTIFIED** | decyzja ma sens dla tego klienta | czy potrafię napisać warunek prawdziwości? |
| **DISTINCTIVE** | trudno przenieść na innego klienta | ilu z sześciu klientów z innych branż mogłoby ją mieć? |
| **ESSENTIAL** | bez niej strona traci główny sens | po usunięciu zostaje **inna strona**, czy **ta sama minus element**? |

**Wszystkie obecne bramki mierzą wyłącznie JUSTIFIED.** Fikstura, która przeszła 12/12,
miała 5 × JUSTIFIED, 0 × DISTINCTIVE, 0 × ESSENTIAL.

> **Strona potrzebuje jednej decyzji ESSENTIAL. Ta decyzja jest sygnaturą.**
> Nie atrybut `data-sygnatura`, nie efekt wizualny — decyzja, po której wycięciu
> zostaje inna strona.

Nasze ESSENTIAL, które się obroniły: cennik jako oś (granitexpress), SZLIF (serwin),
stygnięcie 1200 → 20 °C (spieki). Nasze nie-ESSENTIAL: stojak z płytami u Lewartowskich
(dało się wyciąć — to był zarzut krytyka), ciemny premium w `groby v8`.

### Test nieprzenośności — mocniejszy niż „zdejmij logo"

> **Wskaż element, który po przeniesieniu do innej firmy przestaje działać — i powiedz,
> dlaczego przestaje.** Drugie zdanie jest testem; pierwsze da się zmyślić.

Nie zamieniać w próg. Wynikiem ma być zdanie, nie liczba.

---

## 6. Dwanaście etapów

Pełny opis, produkty i bramki: `pipeline.md`. Artefakty mieszkają w `<klient>/dane/`,
**nigdy w scratchpadzie** — generator Serwina był o jedno czyszczenie od utraty 27 stron.

| # | Etap | Artefakt | Bramka |
|---|---|---|---|
| 1 | RESEARCH | `01-fakty.json` | każdy fakt ma `id`, `status`, `zrodlo` |
| 2 | WNIOSKI | `02-wnioski.md` | maks. 5, każdy `F_ + F_ → dlatego X` + konsekwencja projektowa |
| 3 | KONCEPT | `03-koncept.md` | 10 pytań, rejestr, sygnatura, 3 konsekwencje strukturalne, decyzja własna |
| 4 | KIERUNEK | `04-kierunek.md` | **każda decyzja cytuje numer wniosku** |
| 5 | PODRÓŻ | `05-podroz.md` | akty nazwane rzeczownikiem stanu, rytm, moment kulminacyjny |
| 6 | SEKCJE | `06-sekcje.tsv` | obiekt, ruch, **kolumna `mobil`**, fraza, sygnatura |
| 7 | BUILD | `site/` | `build.py` przerywa bez plików 03–06 |
| 8 | MOBILE | `07-mobile.md` | osobna kompozycja, nie `flex-direction: column` |
| 9 | QA | raport | `audyt.py` + `podobienstwo.py` + agenci |
| 10 | WDROŻENIE | demo pod subdomeną | tryb DEMO: `noindex`, ale **bez** `Disallow` |
| 11 | RETRO | `08-retro.md` | te same pomiary co `00-audyt`; plan z 05 kontra wynik |
| 12 | WIEDZA | wpis w `_wzorce/` + `indeks.json` | odcisk trafia do indeksu, następny projekt się o niego potyka |

Etapów nie wolno przeskakiwać w dół. W górę wolno — audyt zastanej strony startuje od 9.

**Ruch nie jest osobnym etapem.** Jest kolumną w `06-sekcje.tsv` i powstaje razem
z sekcją. Dopóki był etapem piątym z siedmiu, był czymś, co się dodaje, jeśli zostanie
czas — stąd `granitexpress` z 1,4 kB JavaScriptu na 39 sekcji.

**To jest mechanizm, który sprawia, że research kończy się projektem, a nie PDF-em:**
etap 4 nie przechodzi bez cytatów, a etap 7 nie startuje bez etapu 4.

---

## 7. Warsztaty

| Katalog | Po co | Co tam jest wykonywalne |
|---|---|---|
| `_wzorce/research/` | kolejność źródeł, fakty, wnioski | `szablon-fakty.json` |
| `_wzorce/kierunek/` | koncept, podróż, sekcje, mobile | cztery szablony |
| `_wzorce/ruch/` | kontrakt nazw, bezpieczniki, biblioteka | `ruch.js`, `ruch.css`, `demo.html` |
| `_wzorce/obraz/` | prawo obrazu, kadrowanie, generowanie | `prompty/` |
| `_wzorce/tresc/` | silos SEO, intencje, GEO, język | — |
| `_wzorce/branze/` | wiedza o rynku | — |
| `_wzorce/audyt/` | bramki | `audyt.py`, `podobienstwo.py` |
| `_wzorce/NN-*.md` | case studies z projektów | — |

**Warsztat bez pliku uruchamialnego albo szablonu nie powstaje.**
`CLAUDE_MASTER_KNOWLEDGE.md` ma 42 kB znakomitej doktryny i nie zapobiegł żadnej
ze stron, które Szymon nazywa nudnymi — bo nic go nie odpalało w chwili budowania.

---

## 8. Protokół ze Szymonem

Proszę wprost i w ustalonych momentach, nie wtedy, kiedy utknę.

| Moment | Co zamawiam |
|---|---|
| **po researchu, przed konceptem** | zdjęcia (lista w `_wzorce/obraz/`) + rozstrzygnięcie faktów ze statusem `PYTANIE` |
| **po wyborze kierunku, przed budową** | 3–8 obrazów kluczowych, każdy z gotowym promptem do skopiowania |
| **po zbudowaniu, przed pokazaniem** | „tak/nie" na jednym zrzucie na akt, **390 px przed 1440** |

Formularz zamówienia obrazu:

```
ZAMÓWIENIE OBRAZU — <projekt> — <nazwa pliku>
Gdzie trafia:     akt 03 „Materia", tło pełnoszerokościowe
Czego potrzebuję: makro granitu Impala, krawędź po frezie 45°, światło z lewej,
                  bez napisów, bez ludzi, bez całego nagrobka
Proporcje:        21:9, min. 2400 px
Narzędzie:        higgsfield-product-photoshoot
PROMPT DO SKOPIOWANIA:
<dokładny prompt — gotowce w _wzorce/obraz/prompty/>
Jeśli wyjdzie źle: powiedz „inaczej" — mam trzy warianty w zapasie.
```

**Co robię sam, bez pytania:** tekstury proceduralne, SVG, bryły z Blendera, kadrowanie,
WebP, cały kod, cała treść, cały research. **Nie pytam o zgodę na odwagę wizualną.**

**Blokująco pytam tylko o:** brak danych firmy, brak materiału wizualnego, niejasny budżet.

---

## 9. Czego nie biorę z generatorów makiet

Kompozycję i paletę — tak. **Treść nigdy.** Stitch dopisuje normy, parametry, nazwiska
właścicieli i zmyślone numery telefonu; „zostaw pusty wiersz" jest ignorowane.

---

## 10. Dziennik projektów

Po każdym skończonym projekcie wracam tutaj. Nie opis projektu — **regułę, którą da się
zastosować gdzie indziej.**

```
## <data> — <projekt>
Liczby:          stron / sekcji / obiektów / rozkład ruchu / podobieństwo do poprzednich
Zamknięte bezpieczniki przy pierwszym przebiegu:
Co zadziałało:
Co nie zadziałało:
Reguła dla następnego projektu:
Czy Szymon to pochwalił:
```

### 22.09.2026 — KUBAR (Łomża), stolarz meblowy na fundamencie po Lewartowskim

**Zadanie:** „Klient się nie zdecydował. Zamieniamy bazę spod Lewartowskich na KUBAR z Łomży,
zachowaj wygląd, zamiast kamienia różne rodzaje drewna, nacisk na SEO/GEO/AIO, min. 750 słów
na stronę." Pełny pipeline 1–9 w jeden przebieg.

**Liczby:** 12 adresów, 74 sekcje, **9 568 słów** (najmniejsza podstrona 778), zero plików
graficznych poza `og.png`. Bramka **12/12** — przy pierwszym przebiegu zamknęła **5**.
Podobieństwo: najbliższy `lewartowski` 35 % układu przy limicie 60 %, budżet powtórzeń 1 z 5.

**Co zadziałało:** research znalazł rzecz, której nie było w dossier od Szymona —
**właściciel przez pięć lat był wychowawcą w Placówce Opiekuńczo-Wychowawczej w Łomży
i wrócił tam w 2022 zrobić dzieciom kuchnię**, z cytatem prasowym „Kuchnia to jest serce
domu". To jedyna rzecz w całym dossier, która przechodzi SWAP CLIENT, i to ona wybrała
rejestr: jasny, bo oś stoi na słowie „przytulnie". Sygnatura ŚCIANA wzięła z Lewartowskiego
**geometrię**, ale nie treść — front niesie *pomieszczenie*, nie materiał
(`Kuchnia · tu się rozmawia`). Akt o placówce jest jedyną sekcją bez przycisku i jedynym
ciemnym ekranem; ma przełącznik `PLACOWKA`, gdyby klient się nie zgodził.

**Czego nie zrobiłem dobrze — i to jest tu najważniejsze.** Zbudowałem własny zestaw
pomiarów w przeglądarce (przepełnienie, przeskoki nagłówków, puste ekrany, kontrast
na pikselach, odsłonięcia, linkowanie) i wszystkie świeciły na zielono. Potem uruchomiłem
`audyt.py` i **zablokował build na pięciu rzeczach, z których żadnej nie mierzyłem**:
35 sekcji było samym tekstem, `rv:up` pokrywał 67 % sekcji (mój pomiar liczył elementy
i pokazywał 36 % — bramka liczy sekcje i miała rację), sześć rozmiarów pisma poza systemem
i dwa poniżej 14 px, 41 decyzji w `04-kierunek.md` bez numeru wniosku, plus literówka
z cyrylicą w środku słowa.

**Reguła dla następnego projektu:** *Pomiar, który sam sobie projektujesz w trakcie pracy,
mierzy to, co akurat umiesz zmierzyć — i dlatego zawsze wychodzi zielony. Bramka mierzy to,
co pracownia już raz spaliła. Uruchom ją, zanim uznasz, że sprawdziłeś stronę, a nie po tym,
jak uznasz, że jest skończona.*

**Znalezisko, które wychodzi poza ten projekt:** `data-rv="mask"` z `_wzorce/ruch/ruch.css`
**nigdy się nie odsłania w Chrome**. `clip-path: inset(0 0 100% 0)` zeruje pole przecięcia,
a Chrome liczy `clip-path` przy IntersectionObserver — element dostaje `ratio 0,000`,
callback nie pada, klasa `.in` nie przychodzi nigdy. Czuwak tego nie ratuje, bo warunek brzmi
„obserwator nie dał znaku życia", a on go dał — na pozostałych wariantach. Zmierzone:
clip-path 100 % → 0,000; clip-path 99 % → 0,010; maska CSS → 1,000. Poprawka (maska zamiast
przycięcia) siedzi w `kubar/src/site.css`; **do przeniesienia do biblioteki i do sprawdzenia
w projektach, które już używają `rv:mask`** — to jest kandydat na wyjaśnienie zgłoszeń
„puste sekcje". Obserwacja 0023.

Druga reguła, tańsza: *nie ukrywaj elementu w sposób, który zeruje jego pole — obserwator,
który ma go odsłonić, mierzy właśnie to pole.*

**Czeka na decyzję Szymona:** (1) zgoda Arkadiusza na historię z placówki — bez niej strona
traci decyzję ESSENTIAL; (2) eksport zdjęć z Instagrama klienta, bo galeria stoi dziś na
wizualizacjach poglądowych; (3) widełki cenowe — nikt w Łomży ich nie podaje, `CENY = {}`
czeka puste; (4) wdrożenie na Workers, niewykonane bez polecenia.

**Dopisek 22.09.2026 — wdrożenie i pomiar NA PRODUKCJI.** Strona poszła na Workers
(**kubar.jurczakstudio.pl**, custom domain bez błędu 100117, DEMO/noindex, 12 adresów,
28 plików). Po wdrożeniu zmierzyłem odsłanianie na żywym adresie i dobrze, że nie na
localhoście: przy zwykłym przewijaniu 0 zaległych, ale **po jednym twardym skoku na dół
30 z 33 elementów zostawało nieodsłoniętych i wszystkie nad kadrem** — czyli po powrocie
do góry strona z pustych sekcji. IntersectionObserver zgłasza zmianę statusu przecięcia,
a przy skoku sekcja przechodzi z „pod kadrem" w „nad kadrem" nie przecinając go ani razu.
Zapas scrollowy dołożony, po nim zero zaległych (obserwacja 0025).

**Trzecia reguła z tego projektu:** *poprawka, która po raz trzeci powstaje w projekcie
zamiast w bibliotece, jest sygnałem o bibliotece.* Zapas scrollowy miał Lewartowski
(16.09), miał GRANES (19.09), musiał go dostać KUBAR (22.09) — a `_wzorce/ruch/ruch.js`
nadal go nie ma, więc każdy nowy projekt startuje z tą samą dziurą.

**I pułapka pomiarowa, w którą sam wszedłem:** `scrollTo` w pętli co 240 ms na stronie
ze `scroll-behavior: smooth` przeretargetowuje animację i strona szarpie zamiast przejechać.
Pokazało 31 zaległych i wyglądało jak katastrofa na produkcji; realne przewijanie
(małe kroki, `behavior: instant`, klatka przerwy) dało 0. **Test przewijania ma
odwzorowywać kółko myszy, nie wywoływać `scrollTo` w pętli.**

### 19.09.2026 — GŁAZ v4 (redesign formy)

**Liczby:** 10 stron / 41 sekcji / 9 bloków na głównej / seq×10, split×8, up×4, mask×3 /
podobieństwo 14% do najbliższego projektu. Bramka 12/12, zero przepełnienia na 121
kombinacjach, a11y 100, LCP 706 ms przy 4× CPU i Slow 4G.

**Zamknięte bezpieczniki przy pierwszym przebiegu:** 2 z 12 — „rytm obiektów"
(trzy fotografie pod rząd) i „rozkład ruchu" (jeden typ na 60% sekcji).

**Co zadziałało:** rozkrój płyty jako oś, z której ubywa — jeden rysunek niesie całą stronę
zamiast ilustrować jedną sekcję. Obie blokady bramki dało się zamknąć **treścią, nie
atrybutem**: pas materiałów rozbił rytm fotografii i jednocześnie dał stronie głównej
pierwsze wyjście na `/materialy/`, którego nie miała.

**Co nie zadziałało:** trzy rzeczy, każda innego rodzaju.
1. Nazwałem nową sekcję `.pole`, a `.pole` było etykietą formularza. Jeden plik CSS nie ma
   przestrzeni nazw; etykieta dostała 104 px paddingu sekcji i formularz się rozjechał.
   Bramka pokazywała 12/12 (obserwacja 0011).
2. Rozbiłem nadmiar `rv:up`, zamieniając nagłówki na `split` — a `split` wymaga struktury
   `<span class="w">`, której nie dostarczyłem. Bramka otworzyła się na ruchu, którego
   nie było (obserwacja 0010).
3. Siedem proceduralnych tekstur wstawionych inline rozdęło HTML z 18 kB do **965 kB**,
   bo gęstość ziarna była wpisana na sztywno dla płyty 800×437. Poszły do plików SVG,
   a `powierzchnia_plyty` skaluje gęstość do kadru.

**Reguła dla następnego projektu:** *Bramka mierzy to, co napisałeś, nie to, co widać.
Za każdym razem, gdy zamykasz kontrolę zmianą atrybutu albo nazwy klasy, otwórz stronę
i sprawdź, czy zmieniło się cokolwiek poza wynikiem kontroli.* Drugie, węższe: **jeden
zrzut całej strony na końcu**, bo rytm — jedyna rzecz, o którą w tym redesignie chodziło —
nie jest widoczny na żadnym pojedynczym ekranie ani w żadnej liczbie.

**Druga część tego samego dnia — audyt treści (`glaz/dane/22-audyt.md`).** Po redesignie
formy zmierzyłem, ile strona waży treścią: **1531 słów w całym serwisie**, podstrona usługowa
~100 słów i jeden link przychodzący, a w widocznej tabelce `CENA [widełki — od klienta, P10]`
— notatka dla wykonawcy pokazywana klientowi. **Bramka świeciła 12/12 przez cały ten czas.**
Dwa wnioski z etapu 2, w tym ten, który uzasadnił wybór konceptu, nie miały na stronie
ani jednego zdania. Dobudowa: 1531 → 3950 słów, 10 → 12 podstron, linki przychodzące 1 → 3–10.

**Druga reguła z tego projektu:** *Bramka mierzy formę i milczy o treści, a milczenie wygląda
jak zgoda. Zanim uznasz stronę za skończoną, policz słowa na podstronie i linki do niej —
oraz sprawdź, czy wniosek, który wybrał koncept, ma na stronie choć jedno zdanie.*
Trzy bezpieczniki do dołożenia: obserwacja 0012.

**Czy Szymon to pochwalił:** — (do oceny)

### 16.09.2026 — przebudowa systemu (wpis zakładający dziennik)

**Liczby:** patrz `_wzorce/00-audyt-2026-09.md`. 25 projektów, 102 zamknięte bezpieczniki
przy pierwszym przebiegu scalonej bramki.

**Co zadziałało:** Lewartowscy — ruch wpisany w koncept, 236 haków, 27 przejść, sygnatura
stojaka. To jedyny projekt, który wypada dobrze także w nowej bramce.

**Co nie zadziałało:** LUX — `if (!hero) return;` jako zapis sposobu myślenia.
Głód obrazu (`granitexpress`, `kamat` — zero zdjęć). Sześć nazw na jedno odsłonięcie.
Podstrony jako sieroty (`kamar` 0,27). **I mój własny błąd: zbudowałem drugą bramkę
obok istniejącej `audyt_sekcji.py`, nie sprawdziwszy, czy coś takiego już jest.**

**Reguła dla następnego projektu:** *Zanim dołożysz mechanizm, sprawdź, czy nie istnieje.
Dwa mechanizmy robiące to samo są gorsze niż jeden przeciętny — bo każda decyzja
zapada wtedy dwa razy i za każdym razem inaczej.*

### 16.09.2026 — stress test V2 (atak na własny system)

**Liczby:** fikstura „Wierzba" przeszła **12/12 bezpieczników i 3/3 osie podobieństwa**,
będąc szablonem premium z 16-bajtowymi atrapami obrazów i zerem `transition:`.
SWAP CLIENT na warsztat aut: **60 podmienionych słów, znaczniki HTML identyczne,
oba warianty 12/12**. REVERSE SWAP: gotowy design uzasadniony researchem kancelarii
prawnej w kilka minut — **6/6 decyzji**.

**Co zadziałało:** sam podział bezpiecznik/kompas okazał się właściwym narzędziem —
to nim wykryłem własne luki. Detektor OBIEKTU, materiał wyprowadzany z CSS i profil
mediów przez scroll bronią się i zostają.

**Co nie zadziałało:** wszystkie dwanaście bezpieczników mierzy formę, nie relację
forma↔klient. Warunek prawdziwości, który miał to naprawić, sprawdza falsyfikowalność
**faktu**, nie konieczność **związku** — dziesięć semantycznie fałszywych decyzji
przeszło bramkę. **I znalezisko głębsze niż wszystkie luki razem: `05-podroz.md` żąda
aktów, rytmu i kulminacji, czyli definiuje film — więc cennik-narzędzie, katalog
i archiwum dostają film o cenniku, katalogu i archiwum.** Zabezpieczyliśmy się przed
szablonem wizualnym i zapisaliśmy strukturalny w kręgosłupie procesu.

**Reguła dla następnego projektu:** *Zielona bramka nie znaczy dobra strona — znaczy tyle,
że nie popełniłem znanej katastrofy. Zanim pokażesz cokolwiek: wskaż jedną decyzję
ESSENTIAL i powiedz, dlaczego przestaje działać u innej firmy. Jeśli nie potrafisz —
to jest szablon, choćby wszystko świeciło na zielono.*

**Czeka na decyzję Szymona:** (1) czy minimum to „dwa kierunki z tych samych faktów"
w `03-koncept.md`; (2) czy szablon strukturalny z `05-podroz.md` naprawiamy razem z tym,
czy osobno; (3) czy „zawsze para krojów szeryf + grotesk" przestaje być zasadą domu.

### 16.09.2026 — MATCZAK I SYN (MŁOCK 26)

**Liczby:** 15 podstron, 86 sekcji, **zero plików graficznych**. Cztery bezpieczniki
zamknięte przy pierwszym przebiegu, potem 12/12 OK. Podobieństwo do najbliższego projektu
21 % (`spieki`), budżet powtórzeń **0 z 5**. Lighthouse mobile: dostępność 100,
praktyki 100. LCP 236 ms, CLS 0,04.

**Co zadziałało:** brak zdjęć klienta przestał być problemem, bo został **wejściem do wyboru
rejestru na etapie 1**. Nośnikiem strony jest rysunek prawdziwych danych — 1993 odcinki
dróg z OpenStreetMap i dwanaście tras policzonych przez OSRM. To jedyna treść, której nie
ma żadna inna strona kamieniarska w powiecie, i jedyny obraz, którego nie trzeba było
kupować, generować ani prosić o niego klienta. Zadziałał też wymóg **dwóch kierunków
z tych samych faktów**: kierunek B upadł na faktach, nie na guście.

**Co nie zadziałało:** pierwsza wersja **przeszła 12/12 bezpieczników i była nudna**.
Szymon: „spójna i poprawna, ale nudna i brzydka”. Dziewięć sekcji powtarzało
`nad → h2 → lid → treść` w jednej kolumnie 74 ch na środku ekranu, a mapa — jedyny
zasób, którego nikt w powiecie nie ma — leżała w obramowanym prostokącie w środku strony
jak widget pogodowy. Kamień leżał pod kurtyną 86–94 %: napisany, zmierzony, zaliczony
przez bramkę, niewidoczny dla oka.

**Reguła dla następnego projektu:** *Zrzut CAŁEJ strony na jednym obrazku jest osobnym
narzędziem i trzeba go zrobić, zanim uzna się projekt za skończony.* Bramka mierzy sekcje
pojedynczo, agent ogląda sekcje pojedynczo, przeglądarka pokazuje jeden ekran. **Rytm —
jedyna rzecz, która odróżnia stronę zaprojektowaną od poprawnie wygenerowanej — istnieje
wyłącznie w relacji między sekcjami i jest niewidoczny w każdym innym widoku.**
Reguła tańsza: *jeśli na stronie jest jeden zasób, którego nie ma nikt inny, to on jest
pierwszym ekranem — nie sekcją czwartą.*

**Czeka na decyzję Szymona:** rejestr **„arkusz mapy”** dopisany do `dom.md` część B jako
dziewiąty (wyprowadzony z W1 i W3, nie wybrany z listy) — do zatwierdzenia albo odrzucenia.

### 18.09.2026 — GRANES (Biel k. Siedlec), przebudowa systemu police pod nowego klienta

**Zadanie:** „Kamieniarz Police nie odbiera. Przebudujmy tę piękną stronę pod nowego
klienta" (GRANES, z CRM, kontakt: nigdy). Pełny pipeline w jeden przebieg: research →
fakty → koncept → build → bramki 12/12 + BEZ POWTÓRZEŃ (15% do najbliższego).

**Liczby:** 5 stron, 20 sekcji, ruch rv:up 37% / mask / krok / wjazd / count,
kadry maks. 31% w sekcji, 34 tokeny --fs-, 0 literałów. Zamknięte bezpieczniki przy
pierwszym przebiegu: 7 (obiekt, rytm, sygnatura, skala, ruch-bezpieczniki, mobile,
kierunek), potem jeszcze 2 (rozkład kadrów, rozkład ruchu).

**Co zadziałało:** (1) Rozdzielenie SYSTEMU od SILNIKA — z police pojechała czerń,
złoto i komponenty, ale oś („papiery mistrza": skan świadectwa czeladniczego 47578
i dyplomu mistrzowskiego 3624, które klient SAM publikuje) wyszła z researchu GRANES
i nie przeszłaby SWAP CLIENT — Mast-Kam nie ma czyich dokumentów pokazać. (2) Wady
danych obrócone w decyzje: firma od 2022 → licznik liczy lata FACHU od 2005; miniatury
200 px → taśma kwadratów i zakaz full-bleed; brak opinii Google → dowodem są dokumenty,
nie gwiazdki. (3) Bramki naprawiane architektonicznie, nie atrybutami: monokultura rv:up
padła przez nadanie finałom własnego wariantu „wjazd", a koncentrację kadrów zdjął
klon taśmy w JS (HTML niesie jeden zestaw).

**Co nie zadziałało od razu:** fonts.css linkowany bez `?v=` + ścieżki względne liczone
od położenia pliku CSS (fonts/…, nie assets/fonts/…) — fonty „działały" w fetch,
a FontFace rzucał NetworkError, bo dokument trzymał starą wersję arkusza z cache.
Playwright fullPage zrzucał gablotę PUSTĄ (lazy-load vs natychmiastowy zrzut) — skany
kulminacji muszą być eager. Tokeny obrazów Google Sites (`sitesv-images-rt`) żyją
per-render strony: pobieranie = rozgrzać URL w przeglądarce i curl-ować natychmiast;
i zanim planujesz kadry, sprawdź wymiar NATYWNY (9 z 11 „zdjęć" klienta to miniatury).

**Reguła dla następnego projektu:** *Przebudowa udanej strony pod nowego klienta to
dwa osobne transfery: system wizualny wolno przenieść w całości, silnik treści trzeba
zbudować od zera z faktów nowego klienta — a granicę sprawdza SWAP CLIENT na sekcji
kulminacyjnej.* I tańsza: *KAŻDY plik CSS dostaje `?v=` od pierwszego builda — także
fonts.css; „to tylko fonty" kosztowało godzinę.*

**19.09.2026 — warstwa wizualna v2 („strona wydaje się o wiele nudniejsza").**
Diagnoza z wzorca, nie z odczucia: police miało osiem komponentów, które je sprzedały
(`_wzorce/police-czarny-granit.md` §4), GRANES miał trzy — bo pięć brakujących opierało się
na materiale, którego ten klient „nie ma". Okazało się, że ma: skan ulotki 1573×2048,
wpisany przeze mnie na listę POMIJANE w images.py, zawierał jedyne duże zdjęcie realizacji,
fakturę granitu i logo. **Reguła: zanim plik trafi na listę pominiętych, otwórz go** —
materiał złożony (ulotka, baner, wizytówka) to ŹRÓDŁO do kadrowania, nie kadr
(obserwacja 0012). Zbudowane: hero na kadrze z Ken Burnsem, gablota jako gablota
(przechył, szkło, lupa za kursorem, numery do 7rem), dwa przeciwbieżne tory taśmy,
kafel granitu w dwóch wariantach generowany w images.py, rozdziały bez zygzaka
z numerem WYRYTYM w jasnej płytce, złoty obrys kadrów.
**Lekcja o bramkach:** odchudzenie hero z 4 kadrów do 1 zbiło bilans i `rozkład kadrów`
zablokował build (taśma 47%). Matematyka bramki przy 1 kadrze w hero nie miała
rozwiązania — wyjściem było BOGACENIE (powiększenia dokumentów w gablocie), nie ubożenie
taśmy. Bramka wymusiła lepszą stronę, nie gorszą. Po zmianach 12/12 i BEZ POWTÓRZEŃ
(najbliższy meustone 31% układu). Wdrożone tego samego dnia.

**Czeka na decyzję Szymona:** telefon do klienta (pierwszy w historii tego rekordu CRM).
Deploy wykonany 19.09.2026 na polecenie: **granes.jurczakstudio.pl** (Workers, custom
domain bez błędu 100117, 404.html dodana do generatora). Tego samego dnia naprawiony
błąd „pustych sekcji": skok suwakiem omija IntersectionObserver (status pod→nad kadrem
bez przecięcia = zero zdarzeń) — w site.js zapas scrollowy odsłaniający wszystko w kadrze
i nad nim; choreografia zostaje. Obserwacja 0008; test QA: skok na dół → powrót → 0 nieodsłoniętych.

### 21.09.2026 — MATCZAK I SYN, telefon klienta: „strona chyba nie dziala"

**Co sie stalo:** klient obejrzal demo na wlasnym telefonie i powiedzial, ze nie da sie
tego ogladac. Moje trzy wczesniejsze rundy mobilne swiecily na zielono.

**Dlaczego ich nie zlapalem:** mierzylem **bez dlawienia procesora**. Sprawdzalem uklad
(poziomy scroll, cele dotykowe, puste kadry) na maszynie, ktora jest kilkanascie razy
szybsza od telefonu za 700 zlotych. Po wlaczeniu dlawienia 6x liczby byly jednoznaczne:
**300 ms na klatke, 118 zlych klatek na 120** — trzy klatki na sekunde. To nie byla
usterka ukladu, tylko fakt, ze strona-jazda przelicza kadr i przerysowuje SVG powiatu
w kazdej klatce przewijania.

**Reguła, ktora z tego zostaje:** *kazdy pomiar wydajnosci pod telefon robimy
z `Emulation.setCPUThrottlingRate` 6x.* Bez tego mierzymy swoj komputer, nie telefon
klienta. I zawsze z punktem odniesienia: pusta strona w tych samych warunkach dala 17 ms,
wiec bylo wiadomo, ze 17 ms jest osiagalne, a 67 ms to nie „limit urzadzenia".

**Co zrobilem:** na telefonie jazda po mapie sie nie uruchamia (`html.jazda-off`), a kazda
mapa jest rysowana **raz na canvasie** zamiast malowana przy kazdym przewinieciu.
Najwiekszy pojedynczy zysk: mapa w sekcji kontaktu kosztowala 67 ms na klatke, po zamianie
na bitmape 17 ms. Do tego lekkie powierzchnie skal (bez dwoch warstw `feTurbulence`),
mniej warstw rysunku i `content-visibility` na sekcjach.

**Wynik na zywo, te same warunki:** klatka 17 ms (bylo 300), 2 zle klatki na 120 (bylo 118),
wczytanie 2,3 s (bylo 10,8), podstrony jak pusta strona. Desktop bez zmian.

**Przy okazji zlapana nieprawda:** liczby doliczane animacja zostawaly na przypadkowej
klatce, wiec na telefonie stalo „3,1 sredniej oceny" zamiast 5,0 i „6 opinii" zamiast 9.
Animowana liczba, ktora nie dojedzie, jest falszywa informacja o firmie.

### 18.09.2026 — MATCZAK I SYN, runda telefonowa

**Zadanie:** „przygotuj stronę pod telefon". Audyt na prawdziwym Chrome z emulacją
dotyku w czterech kadrach (390×844, 375×667, 360×640, poziomy 740×360) plus wariant
bez JavaScriptu, na wszystkich piętnastu podstronach. Dziewięć usterek, wszystkie
naprawione, bramki 12/12.

**Czego się nauczyliśmy:** trzy najgorsze rzeczy były **niewidoczne na desktopie
i niewidoczne w regule CSS** — wychodziły dopiero z pomiaru geometrii w przeglądarce.

1. **Skala zwycięża nad media query.** `.plyta3d--sama .plyta3d__scena` (0,2,0) biło
   mobilne `.plyta3d__scena` (0,1,0), a że mobilna reguła dokładała `height: 30svh`,
   proporcja policzyła *szerokość* 405 px w kontenerze 355 px. Lekcja: nigdy nie mieszaj
   `aspect-ratio` z jawną wysokością w nadpisaniu mobilnym — ustaw jedno i zeruj drugie.
2. **Efekt policzony w procentach wygląda inaczej przy trzykrotnie węższym ekranie.**
   Składana mapa miała cztery pasy i skalę końcową 0,16 — na desktopie to 58 px i widać
   złożoną mapę, na telefonie 16 px i widać czarny pasek. Liczby końcowe podawaj
   w pikselach docelowych (`66 / pw`), nie jako stały ułamek.
3. **`transform: scale(1.06)` w animacji wejścia to poziomy scroll.** Sekcja przed
   odsłonięciem jest szersza od okna; w orientacji poziomej dawało to cztery piksele
   przewijania w bok. `overflow-x: clip` na `html` **i** `body` — `clip` nie robi z nich
   kontenera przewijania, więc `position: sticky` działa dalej (`hidden` by je zabiło),
   a sama deklaracja na `body` nic nie daje, bo przy `html { overflow: visible }`
   wartość propaguje się do viewportu i body zostaje widoczne.

**Czego nie robić:** przyklejać na telefonie elementu wyższego niż jedna piąta ekranu
(płyta 3D w estymatorze zajmowała 41 % i formularz wjeżdżał pod nią ucięty w pół wiersza),
ani przyklejać czegokolwiek nad treścią, która bywa krótsza od tego czegoś (zakładka BLAT:
płyta zwisała poniżej końca formularza).

**Warsztat:** serwer stron zawiesił się w trakcie (stare zablokowane połączenia na 8123)
— podgląd przez `preview_start` na 8780 wystarczył i to jest właściwa droga. Skrypty
audytu i 60 zrzutów zostają w `matczak/dane/zrzuty/mobil/`, opis rundy w `dane/07-mobile.md`.

### 17.09.2026 — MATCZAK I SYN, przebudowa na jedną podróż

**Brief:** „nie rób ładniejszej strony, zaprojektuj doświadczenie" — mapa ma być
kręgosłupem, scroll ma wieźć, cena ma być zmianą świata. Cztery mapy przed kodem
(`dane/10-doswiadczenie.md`), potem implementacja. Bramki 12/12, Lighthouse 100/100,
zero błędów, wszystko bez bibliotek.

**Co zadziałało:** brief chciał trzech rzeczy, których fakty zabraniały (archiwalne zdjęcie
zakładu, galeria realizacji, kalkulator z mnożnikami) — i za każdym razem **odpowiedź
była w danych, nie w odmowie**: „archiwum" to trzydzieści lat na kamieniu, „realizacje" to
50 prawdziwych cmentarzy z OSM jako miejsca, dokąd jedzie pomnik, „kalkulator" to
estymator, który liczy wyłącznie opublikowane średnie i pokazuje puste rubryki jako treść.
Przejście mapa → kamień wybrane spośród pięciu kandydatów przeciw przykładowi z briefu
(LINIA → ŻYŁA), bo żyła jest geologią, a linia na tej stronie jest decyzją.

**Co nie zadziałało od razu:** focus mode oscylował (kadr leciał do celu liczonego dla
docelowej szerokości, punkt uciekał spod kursora — trzy podejścia, zanim punkt stanął
nieruchomo); karty stacji rozciągały się w fleksie i sticky nie miało gdzie się przykleić;
`--gora` zgadnięte na 104 px, zmierzone 128; smooth scroll w CSS psuł każdy zrzut testowy
(Playwright fotografował środek animacji). Trzy moodboardy z Gemini w folderze `zdjecia/`
wyglądały jak zasób i nim nie były.

**Reguła dla następnego projektu:** *Kiedy brief wymaga rzeczy, której fakty nie dają,
nie odmawiaj i nie zmyślaj — znajdź w danych klienta obiekt, który robi tę samą robotę
narracyjną.* I tańsza: *wysokości sticky mierz w JS, nie wpisuj w CSS; a przed zrzutem
testowym wyłącz `scroll-behavior: smooth`.*

**Czeka na decyzję Szymona:** (1) czy „jazda" ma wejść do `_wzorce/ruch/` jako wzorzec
przypiętej mapy z kamerą; (2) deploy demo na Workers — nie wykonany bez polecenia.

### 17.09.2026 — GŁAZ (Pruszków), pierwszy klient budowlany z makietą z Cowork

**Liczby:** 10 stron, 36 sekcji, 12/12 bezpieczników po drugim przebiegu (pierwszy: 4 zamknięte —
obiekt, rytm, rozkład kadrów, sygnatura poza hero). Zero zdjęć klienta, 11 kadrów poglądowych.
Podobieństwo: do zmierzenia `podobienstwo.py` po podmianie zdjęć.

**Co zadziałało:** dwa ataki na reżyserię przed kodem. Pierwszy zabił linię A—A' (zajęta przez
Matczaka i KAMAT), drugi zabił „jeden dom" ze zdjęć różnych domów i dał **stół** jako ciągłość.
Makieta z Cowork (Design canvas z maszyną stanów w JS) przeniosła się do generatora niemal 1:1 —
ta sama funkcja `rysuj(P)`, te same stałe geometrii; makieta była specyfikacją, nie obrazkiem.

**Co nie zadziałało:** obrazy sceny w HTML dały 71 % kadrów w jednej sekcji i „foto" pod rząd —
bramka nie odróżnia warstwy sterowania od treści. Rozwiązanie: scena JS buduje własne `<img>`,
HTML sekcji jazdy jest sterowaniem. Ukryty panel podglądu zatrzymuje rAF — testy stanów przez
hak `window.__glaz.rysuj(p)`, nie przez scroll.

**Reguła dla następnego projektu:** *Jeśli makieta ma logikę (stan → widok), pisz ją w makiecie
jako czystą funkcję od jednego parametru — wtedy build jest portem, a nie interpretacją.*
I tańsza: *sekcja, której treść buduje JS, nie powinna mieć `<img>` w HTML — bramka policzy je jako galerię.*

**Dopisek 18.09.2026 — v2 po ocenie Szymona („wygląda śmiesznie, naprawdę”).** Jazda po stole
przeniesiona 1:1 z makiety Cowork była prototypem mechanizmu, nie stroną: szary stół z CSS pod
zdjęciem, na którym już jest stół; zdjęcie pochylone trapezem; żółty przerywany prostokąt i czarna
dziura wyjeżdżająca z fotografii; jedna płyta w filtrze szarym i sepii udająca cztery; licznik, taca
miniatur i pasek stacji jak w odtwarzaczu. Wszystko wyleciało. Została prosta strona na
fotografiach z jednym odsłonięciem od krawędzi.
**Reguła, która zastępuje poprzednią:** *makieta interaktywna z Cowork jest dowodem, że mechanizm
da się zbudować — nie dowodem, że wygląda dobrze. Elementy udające fizyczne obiekty CSS-em (stół,
dziura, kawałek) obok prawdziwej fotografii tego samego obiektu zawsze przegrywają z fotografią.
Zanim przeniesiesz mechanikę, zrób jeden zrzut sceny w pełnej skali i zapytaj: czy to jest strona,
czy demo silnika.*

**Czeka na decyzję Szymona:** deploy demo na Workers (`glaz.jurczakstudio.pl`); zdjęcia klienta (P5).

### 30.09.2026 — Matczak: „nie podoba mi się, dziwnie działa" → strona od nowa

Klient odrzucił koncept „MŁOCK 26" (jazda po mapie sterowana przewijaniem). Nie z powodu wad
technicznych — po przebudowie telefonowej mierzyła 17 ms na klatkę przy procesorze 6× wolniejszym.
Odrzucił **trafienie**: sprzedaje nagrobki, a dostał mechanizm, który trzeba zrozumieć, zanim się
cokolwiek kupi. Poprosił o styl elegancki, prosty i przejrzysty.

Nowa strona: **„KAMIEŃ I MIEJSCE"**, rejestr redakcyjny jasny, 20 podstron, zero plików
graficznych. Oś: 22 cmentarze w zasięgu dojazdu z policzoną **odległością drogową**. Stara wersja
zachowana w całości jako `_wzorce/jazda-po-mapie/` + brief — do klienta, którego przewagą jest
dystans albo trasa.

**Cztery rzeczy warte przeniesienia dalej:**

1. **Liczba w dokumentacji bez metody zliczania jest nieodtwarzalna.** Trafiło dwa razy tego
   samego dnia: „50 cmentarzy z OSM" (27 nieużywalnych — bez nazwy albo wojenne) i „252 wpisy
   w archiwum" (recenzent zestawił to z 17 i w dobrej wierze zgłosił sprzeczność, której nie było —
   to były dwie różne miary tych samych danych). Przy każdej liczbie zapisuj polecenie, którym
   się ją odtwarza.

2. **Odległość w linii prostej podana jako dojazd to zmyślony fakt.** Na terenie wiejskim zaniża
   średnio o 23 %, skrajnie o 65 % (24,5 km w linii prostej to 40,5 km drogą). Doliczenie tras
   z OSRM kosztowało jedno zapytanie na pozycję i uratowało wiarygodność całej osi.

3. **Bramka musi umieć oblać z powodu, dla którego ją napisano.** Test mutacyjny znalazł dwie
   dziury, których nie zobaczyła żadna recenzja: pozycja bez zmierzonej trasy przechodziła na
   zielono (a spec wymagał podpisu „w linii prostej"), i lista zakazanych nazw w bramce była
   słabsza niż w filtrze, więc regresja by się prześlizgnęła. Psuj dane celowo i sprawdzaj,
   czy ktoś krzyknie.

4. **Panel podglądu wstrzymuje IntersectionObserver i rAF**, bo raportuje się jako karta w tle.
   Zdiagnozowałem na tej podstawie „wszystkie nagłówki sekcji niewidoczne na każdej podstronie"
   i byłem gotów zgłosić awarię. Dowód, że to artefakt: mój własny, świeżo utworzony obserwator
   też nigdy nie odpalił. Rozstrzygnięte dopiero pomiarem w prawdziwym Chrome — 7 z 7 odsłoniętych.
   **Do weryfikacji ruchu używaj Chrome DevTools MCP albo `?static=1`, nie panelu.**

**Poprawka do reguły domu:** dane strukturalne nie mogą nieść cudzych cen jako `Offer` firmy.
Specyfikacja kazała emitować `Offer` i `priceRange` ze średnimi kb.pl; podagent odmówił i miał
rację — powiedziałoby to Google i modelom „ten zakład bierze 7 330 zł". Cudza średnia nie staje
się ofertą przez opakowanie w schemat.
