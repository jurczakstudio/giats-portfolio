# AKWIFER — strona wzorcowa zawodu „studnie głębinowe” (Jurczak Studio)

**Koncept v2: ZLECENIE.** Strona, która przyjmuje zlecenia, zamiast tylko ładnie wyglądać.
Firma jest **fikcyjna** (telefon `000 000 000`, termin, paszport — przykłady, oznaczone na stronie);
**dane gmin są prawdziwe**: rejestr PIG-PIB przez mapastudni.pl (14 gmin powiatu poznańskiego, 08.06.2026).

Adres: `akwifer.jurczakstudio.pl` (DEMO = noindex). Gałąź `studnie-wzorzec` w repo `giats-portfolio`;
katalog `akwifer/` jest niezależny od aplikacji Next.js w korzeniu repo.

## Co pokazuje klientowi (firmie studniarskiej)
- **Karta zlecenia** (sygnatura) — gmina + cel + liczba osób → metry, złotówki, formalności (granica 30 m), termin.
  Przelicza się na żywo, pamięta się między stronami, wysyła się **SMS-em** z gotową treścią.
- **14 podstron gmin** z innymi liczbami i tekstem (FAQ + JSON-LD) — pod frazy „studnia głębinowa <gmina>”.
- **Paszport studni** — dokument po odbiorze: głębokość, filtr, zwierciadło, wydajność, badanie wody, przeglądy.
- **Tryb „Oczami właściciela”** (przycisk w nagłówku, `/?wlasciciel=1`) — żółte notki tłumaczą, co każda sekcja robi dla firmy.
- **/dla-firm/** — droga zgłoszenia i kalkulator kosztu leadów z portali.

## Budowa
    python fonts.py     # raz (Archivo wdth/wght, Source Serif 4 italic, DM Mono)
    python images.py    # po wrzuceniu obrazów do zrodla/gen/
    python build.py     # zawsze — na końcu bramka _pracownia/_wzorce/audyt/audyt.py

Obrazy: dwa kadry z Higgsfield wg `dane/zamowienie-obrazow.md` (`hero-wiertnica.png`, `woda-szklanka.png`).
Do czasu ich wrzucenia strona używa plansz wektorowych podpisanych „plansza zastępcza”.
Alternatywa bez Higgsfield: lokalny generator (FLUX.1-schnell / SDXL) — `generator/README.md`.

Zrzuty i testy: `python3 -m http.server 8788 --directory site`, potem `node dane/zrzuty/zrzut.mjs / /gmina/kornik/`
i `node dane/zrzuty/kadr.mjs`.

Wdrożenie (lokalnie, wymaga zalogowanego wranglera): `WDROZ.cmd`.
