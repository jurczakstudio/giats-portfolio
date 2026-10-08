# CLAUDE.md — Jurczak Studio: jak robić strony na poziomie AKWIFER v3

Skopiuj ten plik do `Desktop\strony\CLAUDE.md` — Claude Code czyta CLAUDE.md z katalogów nadrzędnych,
więc zasady obejmą każdy projekt w `strony\`. Wzorzec: `akwifer/` (gałąź `studnie-wzorzec`),
na żywo: https://akwifer.jurczakstudio.pl. Pisz po polsku, konkretnie, bez pustych fraz.

## Hasła (czytaj przed każdą stroną)

1. **Strona ma sprzedawać, nie ładnie wyglądać.** Każda sekcja odpowiada na pytanie, z którym klient dziś dzwoni.
2. **Research przed projektem.** Cztery równoległe wątki: rynek PL (15–20 stron firm, portale z leadami, ceny z datą),
   świat (najlepsze firmy z branży w US/UK/DE/AU), konwersja + trendy wizualne (liczby ze źródłami, Awwwards),
   materiały (zdjęcia na licencjach, otwarte dane, biblioteki, kroje). Raporty zapisuj w `dane/research/`.
3. **Szukaj luki, nie średniej.** Co robi każdy (to minimum) i czego nie robi nikt (to nasza przewaga).
4. **Narzędzie w pierwszym ekranie, nie hasło.** Wycena / kalkulator / „sprawdź swoją działkę” od razu w hero.
   Wynik w liczbach (metry, złotówki, terminy), dopiero potem prośba o kontakt.
5. **Prawdziwe dane zamiast przymiotników.** Rejestry państwowe, taryfy, granice OSM — z datą i źródłem na stronie.
   Firma może być fikcyjna, dane nie.
6. **Każda lokalna podstrona ma inne liczby.** Nie „Usługi X — zapraszamy”, tylko odpowiedź na frazę z Google.
7. **Nazwij największy strach klienta i rozbrój go.** (AKWIFER: „planowałem 12 tys., wyszło 40” → gwarancja przejrzystości.)
8. **Daj aktualny powód do telefonu.** Przepisy, susza, dotacje, terminy — z datą, aktem i licznikiem dni.
9. **Ceny „od” i pakiety zamiast „do uzgodnienia”.** Dopłaty i zasady podane z góry.
10. **Kontakt jednym ruchem.** Pasek akcji na telefonie (Zadzwoń · SMS · Wycena), SMS z gotową treścią zamiast formularza.
11. **Tryb „Oczami właściciela”.** Notki przy sekcjach: co ta sekcja robi dla firmy. Link `?wlasciciel=1` do wysłania.

## Wygląd

12. **Dwie barwy + jeden głośny akcent.** Ciemna lub kremowa baza i jeden kolor, który pasuje do branży (hi-vis, woda, ziemia).
    Żadnych przygaszonych palet „z wieloma odcieniami”.
13. **Skala plakatu.** Nagłówki do ~9 rem, wersaliki, wąski krój; kontrapunkt: kursywa szeryfowa.
14. **Jedna scena „wow”, która coś liczy.** Przypięta do przewijania i spersonalizowana danymi użytkownika
    (AKWIFER: zejście do mediany wybranej gminy). Ruch opowiada, nie ozdabia.
15. **Wielkie liczby w wąskim kroju sans** (tabular-nums). Mono tylko w etykietach — przekreślone zero źle wygląda w dużej skali.
16. **Materiał zamiast płaskiej czerni:** ziarno (feTurbulence), siatka kreślarska, prawdziwe zdjęcia.
17. **Zdjęcia prawdziwe > plansze.** Pexels/Unsplash/Commons na licencji, podpis „zdjęcie poglądowe · fot. autor”.
    Kadr dobieraj do układu (portret → pionowy panel), sprawdź na zrzucie, czy nie zgubił sensu.
18. **Nigdy nie powtarzaj ilustracji ani motywu z poprzedniego projektu** — klient ogląda całe portfolio.
19. **Telefon to osobna kompozycja**, nie zwinięty desktop. Tekst w SVG ≥ 14 px (rysuj viewBox w szerokości ekranu).

## Uczciwość

20. Nie zmyślamy: firma fikcyjna i przykłady oznaczone („przykład”, „numer niemożliwy do wybrania”).
    Zero fałszywych opinii — miejsce na prawdziwe przy wdrożeniu. Założenia kalkulatorów nazwane i edytowalne.
21. DEMO = noindex (meta + X-Robots-Tag). Licencje i źródła w stopce i w `dane/01-fakty.json`.

## Weryfikacja (bez tego nie ma „gotowe”)

22. Bramka `_pracownia/_wzorce/audyt/audyt.py` musi być OTWARTA.
23. Zrzuty 1440 i 390 **z ruchem** (nie tylko `?static=1`), sceny przypięte w kilku fazach; oglądaj każdy kadr
    i poprawiaj, aż wygląda. Testy interakcji Playwrightem (kalkulatory, SMS, pamięć stanu, dotyk na mapie).
24. Zero błędów konsoli, zero poziomego przewijania, reduced-motion działa.

## Pułapki, które już znamy

- `audyt.py`: decyzje w `04-kierunek.md` muszą cytować **jednocyfrowe** W1–W9 (W10 nie jest rozpoznawane).
- `audyt.py`: font-size tylko z tokenów `--fs-*`; jeden typ ruchu ≤ 50% sekcji; nic poniżej 14 px.
- `ruch.css` wyłącza `data-pin` na ≤ 760 px — jeśli scena ma być przypięta na telefonie, nadpisz to w `site.css`.
- Wikimedia Commons: oryginały dają 429 z chmury → bierz miniatury `?width=2560`. Pexels działa (`images.pexels.com`).
- PIG-PIB (GZWP, CBDH) blokuje chmurę (403) — pobierz raz w przeglądarce i zapisz w repo. Overpass nie działa → Nominatim.
- `site/` jest generowany przez `build.py` — przed `git pull` lokalnie: `git checkout -- site` (WDROZ.cmd robi to sam).
- Okno „Press any key…” zjada pierwszy wpisany znak (`git` → `it`) — najpierw Enter.
- Wdrożenie z chmury wymaga `CLOUDFLARE_API_TOKEN` (edycja Workers) w ustawieniach środowiska; bez niego — WDROZ.cmd lokalnie.
  Nowa subdomena: `custom_domain: true` w wrangler.jsonc.
