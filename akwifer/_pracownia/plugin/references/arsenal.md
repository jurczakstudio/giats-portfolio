# Arsenał — co wywołujemy, kiedy i z jaką poprawką

Tablica rozdzielcza dla wszystkiego, co jest zainstalowane. Kolumna **Poprawka JS**
mówi, jak nagiąć cudzy skill pod nasz stack (Python → statyczny HTML/CSS/JS, bez frameworka).

Legenda etapów: 1 research · 2 kierunek · 3 marka · 4 generator · 5 ruch/3D · 6 audyt · 7 wdrożenie.

---

## A. Rdzeń — wywołuj domyślnie

| Skill | Etap | Po co u nas | Poprawka JS |
|---|---|---|---|
| `design-taste-frontend` | 2, 4 | Anty-szablonowy kierunek i pre-flight check przed kodem. Nasz główny bezpiecznik przed „stroną z generatora". | Pisany pod React/Next. Bierz **zasady kompozycji i audyt-first**, ignoruj wszystkie przykłady komponentowe. |
| `high-end-visual-design` | 2, 4 | Konkretne wartości: skala typografii, cienie, odstępy, struktura kart. To, co odróżnia 800 zł od 8000 zł. | Bierz wartości liczbowe, przepisz na nasze zmienne CSS. Nie instaluj bibliotek, które proponuje. |
| `impeccable` | 4, 6 | 23 komendy `/impeccable ...` — polish, audit, critique. Najostrzejszy krytyk jakiego mamy. | Uwaga: instaluje hooki na Edit/Write i Stop, skrypt POSIX-owy, na Windows może cicho failować. Jeśli hook wisi — wywołuj skill ręcznie. |
| `ui-ux-pro-max` | 2, 3, 6 | Baza danych: 79 stylów, 192 palety, 74 pary krojów, 119 wytycznych UX, 17 presetów GSAP. Najlepsze źródło par krojów i palet. | To biblioteka do przeszukania, nie wytyczna do wykonania. Pytaj o konkret („pary krojów dla marki funeralnej"), nie o cały styl. |
| `design-motion-principles` | 4, 6 | Dwa tryby: budowa ruchu i **audyt** wyłapujący wzorce ruchu typowe dla generatorów. Czyta czysty CSS/HTML, nie wymaga Reacta. | Tryb audytu bierz bez poprawek. Tryb budowy — **ostrożnie**: podaje gotowe krzywe i czasy, a nasze projekty bywają oparte na ruchu zmierzonym (meblex: krzywa domknięcia Blumotion jako easing całej strony). Gdy projekt ma własną fizykę, bierz **zasady**, nigdy wartości — inaczej sygnatura zostaje nadpisana cudzym presetem. |
| `web-design-guidelines` | 6 | Audyt zgodności z Web Interface Guidelines — dostępność, focus, kontrast, target size. Obowiązkowy przed wdrożeniem. | Działa na kodzie, nasz statyczny HTML czyta bez problemu. Bez poprawek. |
| `gpt-taste` | 5 | ScrollTriggery GSAP: pinning, stacking, scrubbing. Nasze „rzeźba sterowana scrollem" stąd. | Wymusza randomizację layoutu Pythonem i strukturę AIDA — u nas kierunek jest ustalony w etapie 2, więc **ignoruj jego reguły layoutu**, bierz wyłącznie warstwę ruchu. |
| `img2threejs` | 5 | Zdjęcie referencyjne → proceduralny model Three.js pisany kodem. Alternatywa, gdy nie mamy pliku FBX/GLB. | Czysty Python stdlib, zero zależności — pasuje do nas idealnie. Przy modelach z pliku zostajemy przy własnym parserze FBX→GLB (moszczynski). |
| `frontend-design` | 2 | Kierunek estetyczny, gdy brief jest mglisty i trzeba coś zaproponować od zera. | Bez poprawek. |
| `imagegen-frontend-web` | 2 | Referencje wizualne: jeden obraz na sekcję, do pokazania Szymonowi przed kodem. | Wymaga Higgsfield CLI. Jeśli niedostępny — opisz kierunek słowem i zrób szybki HTML-owy szkic. |
| `brandkit` | 3 | Logo, tablice brandowe, księga znaku (robiliśmy dla lewartowski). | Wymaga Higgsfield CLI. Fallback: logo jako SVG z tekstu zamienionego na ścieżki, jak w `lewartowski/brand/make_logo.py`. |
| `writing-guidelines` | 4, 6 | Audyt tekstów. Łapie „zapraszamy do zapoznania się". | Napisany pod angielską dokumentację produktową. Bierz **zasady** (krótkie zdania, konkret, brak waty), ignoruj przykłady i głos marki. |

## B. Sytuacyjne — wywołuj gdy pasuje

| Skill | Kiedy dokładnie |
|---|---|
| `redesign-existing-projects` | Przebudowa istniejącego projektu (v2, v8 „Nokturn" itd.). Audyt-first, nie psuje działającego. |
| `minimalist-ui` | Klient chce spokojnie i tanio w utrzymaniu. **Uwaga: jasne i papierowe — Szymon zwykle to odrzuca.** |
| `industrial-brutalist-ui` | Nigdy dla kamieniarstwa. Ewentualnie portfolio Szymona lub projekt komiksowy. |
| `image-to-code` | Gdy mamy makietę graficzną i trzeba ją odtworzyć 1:1. |
| `stitch-design-taste` | Gdy chcemy wygenerować `DESIGN.md` dla projektu jako kontrakt wizualny. |
| `ui-ux-pro-max:design-system`, `design:design-system` | Tokeny (primitive → semantic → component) przy większym projekcie. |
| `dataviz` | Wykresy w Hubie/SEO Command Center. Nigdy na stronie kamieniarskiej. |
| `anthropic-skills:pdf`, `:docx`, `:xlsx` | Dossier i blueprint do PDF, umowa DOCX, ewidencja XLSX. |
| `exa:search`, `exa:exa-agent` | Etap 1 — research konkurencji, opinie Google, NIP/REGON. |
| `build-with-wordpress:*` | Tylko projekty WP (grajkowski, u-beaty). Nie dotykać projektów statycznych. |
| `marketing:seo-audit` | Po wdrożeniu, wejście do SEO Command Center. |
| `deploy-to-vercel`, `vercel-*` | **Nie używamy.** Wdrażamy na Cloudflare Workers. Trzymaj na wypadek projektu Next.js. |
| `code-review`, `simplify`, `security-review` | Kod generatora i API (groby ma `api/`). |

## C. Nie dotykamy

`small-business:*`, `sales:*`, `apollo:*`, `marketing:campaign-plan|email-sequence|run-campaign`,
`higgsfield-marketplace-cards`, `higgsfield-youtube-thumbnail`, `higgsfield-soul-id`,
`higgsfield-video-explainer`, `higgsfield-websites`, `vercel-react-native-skills`,
`imagegen-frontend-mobile`, `design-taste-frontend-v1`, `productivity:*`, `cowork-plugin-management:*`.

Wyjątek: `higgsfield-generate` i `higgsfield-product-photoshoot` — kiedy klient nie ma
zdjęć realizacji i trzeba zrobić tło albo ujęcie poglądowe. **Zawsze oznaczaj takie zdjęcie
jako poglądowe** — nie wolno sprzedawać wygenerowanego nagrobka jako realizacji klienta.

## D. Skille, które trzeba trzymać krótko

- **`full-output-enforcement`** — zakazuje skrótów i placeholderów w kodzie. Włączaj
  świadomie przy generowaniu długiego `build.py`. Domyślnie **nie**, bo rozdmuchuje
  każdą odpowiedź.
- **`gpt-taste`** — patrz wyżej, tylko warstwa ruchu.
- **`vercel-react-view-transitions`** — pomysły na przejścia można przenieść na czyste
  CSS View Transitions, ale nie ciągnij za tym Reacta.

## D2. Narzędzia lokalne — mamy je i długo ich nie używaliśmy

Pomiar z 16.09.2026 pokazał, że głód obrazu jest główną przyczyną nudy wizualnej —
a narzędzia do jego zaspokojenia były zainstalowane i nietknięte.

| Narzędzie | Stan | Do czego |
|---|---|---|
| **higgsfield CLI** | zainstalowany (`~/AppData/Roaming/npm/higgsfield`) | makro materiału, tła, wizualizacje poglądowe — `_wzorce/obraz/prompty/` |
| **Blender 5.0 przez MCP** | podłączony | bryły do scen WebGL, rendery makro z kontrolą światła |
| **Playwright MCP** | podłączony | QA na sześciu szerokościach, zrzuty całej strony, wykrywanie pustych ekranów przy szybkim scrollu |
| **chrome-devtools MCP** | podłączony | **prawdziwy Lighthouse** i trace wydajności. Bramka etapu 9 mówi „zmierzony", nie „oszacowany" |
| **ffmpeg 9.0.1** | zainstalowany, **bez skrótu w PATH** | wideo w tle, kompresja materiału z telefonu klienta. Ścieżka: `%LOCALAPPDATA%/Microsoft/WinGet/Packages/Gyan.FFmpeg_.../bin/ffmpeg.exe` |
| **Pillow** | jest | `images.py` |

## D3. Skrypty własne — bramki

| Skrypt | Kiedy |
|---|---|
| `_wzorce/audyt/audyt.py` | etap 7 (po każdym buildzie) i 9 | 
| `_wzorce/audyt/podobienstwo.py` | etap 9, oraz przy etapie 3 jako sprawdzenie konceptu |
| `_wzorce/ruch/ruch.js` + `ruch.css` | kopiowane do projektu na etapie 7, **bez zmian** |

*(Do 16.09.2026 istniał osobny `audyt_sekcji.py` kopiowany do `dane/` każdego projektu —
scalony z `audyt.py`, żeby nie było dwóch bramek mierzących to samo.)*

## E. Agenci własni (w tym pluginie)

| Agent | Do czego |
|---|---|
| `js-lowca-bugow` | Odpala stronę w przeglądarce, klika, czyta konsolę i sieć, sprawdza mobile i dark. Zwraca listę potwierdzonych usterek. |
| `js-krytyk-designu` | Ogląda zrzuty i mówi, gdzie strona wygląda jak z generatora. Bezlitosny, po polsku. |
| `js-researcher` | Etap 1 — zbiera dane o firmie i konkurencji, zwraca gotowe dossier. |
