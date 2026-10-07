# Wdrożenie — Cloudflare Workers

Wdrażamy statyczny katalog `site/` prosto na sieć brzegową Cloudflare. Nie ma kodu Workera.

## Raz na maszynę

```bash
npx wrangler login
```

## Konfiguracja projektu — `wrangler.jsonc`

Wzór: `lewartowski/wrangler.jsonc`. Nazwa projektu `<klient>-kamieniarstwo`,
`pattern` wskazuje na `<klient>.jurczakstudio.pl`. Rekord DNS zakłada się sam
przy pierwszym wdrożeniu.

## Wdrożenie

```bash
python build.py
npx wrangler deploy
```

## Tryb DEMO — nie pomijać

Dopóki klient nie kupił, strona nosi jego prawdziwą nazwę, adres i telefon, ale stoi
pod naszą subdomeną. Zaindeksowana konkurowałaby w Google z wizytówką klienta —
to realna szkoda dla niego i argument przeciw nam.

Dlatego przy `DEMO = True`:
- każda podstrona ma `<meta name="robots" content="noindex,nofollow">`,
- `robots.txt` nie podaje sitemapy,
- `sitemap.xml` można generować, ale nie zgłaszamy go do GSC.

## Po sprzedaży

1. `DEMO = False` w `build.py`.
2. `BASE` → docelowa domena klienta.
3. `pattern` w `wrangler.jsonc` → docelowa domena.
4. `python build.py && npx wrangler deploy`.
5. Zgłoszenie sitemapy w Google Search Console.
6. Wpis w `Jurczak-Studio-ewidencja-projektow.xlsx`.
7. Aktualizacja pliku pamięci projektu (`~/.claude/projects/.../memory/`).

## Czego nie robimy

- Nie wdrażamy na Vercel. Skille `deploy-to-vercel` i `vercel-*` zostają nieużywane,
  chyba że projekt jest wyjątkowo w Next.js.
- Nie wystawiamy demo z indeksowaniem „bo klient chce zobaczyć w Google".
- Nie kupujemy domeny za klienta bez jego pisemnej zgody.

## Pułapka: „hostname already has externally managed DNS records"

Serwer stron (`strony-server`) skanuje `Desktop\strony` co 30 s i **sam dodaje
każdy nowy katalog** jako stronę, a nazwany tunel zakłada dla niej rekord DNS
`<katalog>.jurczakstudio.pl`. Zanim zdążysz wdrożyć projekt na Workers,
hostname jest więc już zajęty i `custom_domain: true` kończy się błędem 100117.

Rozwiązanie: zamiast domeny własnej użyj **trasy** na istniejącym rekordzie —
działa on na proxowanym DNS i przejmuje ruch przed tunelem, więc demo stoi
niezależnie od tego, czy komputer jest włączony:

```jsonc
"routes": [
  { "pattern": "klient.jurczakstudio.pl/*", "zone_name": "jurczakstudio.pl" }
]
```

Nie kasuj rekordu założonego przez tunel — to zepsuje podgląd lokalny w panelu.

## robots.txt bywa nadpisany przez Cloudflare

Na tej strefie Cloudflare wstrzykuje własny blok „Managed content" z
`User-agent: * / Allow: /` PRZED naszą treścią. Nasz `Disallow: /` zostaje,
ale reguły się mieszają i nie można na nim polegać.

Dlatego przy trybie DEMO robots.txt jest **trzecią warstwą, nie pierwszą**.
Właściwa ochrona to `noindex` w HTML i nagłówek `X-Robots-Tag` z pliku
`site/_headers` — nagłówek obejmuje też zdjęcia, których nikt nie parsuje
jako HTML:

```
/*
  X-Robots-Tag: noindex, nofollow, noarchive, noimageindex
```
