# 02 — Rynek polski: strony firm wiertniczych (studnie głębinowe), portale leadowe, ceny, przepisy, dotacje

Research date: **2026-10-07**. Method: WebSearch + WebFetch (page content converted to text), plus one `curl` pass with a mobile UA that checked each firm page for a viewport meta, `tel:` links and WhatsApp links.
**Limits:** I did not render pages visually, so "mobile quality" means HTML signals only. I could not open Google Business profiles, so Google review counts appear only where a site printed them. Fixly returned 403. I found no Polish portal called "Builderchain", and Pewni Fachowcy and Kowalski did not appear in any search for well drilling.
Legend: **[S]** = seen directly in a source (linked). **[I]** = my inference.

---

## 1. TL;DR

1. **No firm offers a real price calculator.** Two firms publish a clear price list (studnie.poznan.pl, studniekrakow.pl). TechDrill has a "kalkulator", but it deliberately shows no prices ("Bez podawania cen"). Every other firm hides prices behind "wycena indywidualna" [S].
2. **Social proof is weak everywhere.** Ratings appear without a review count ("4.8/5" or "5.0") [S]. Studnie Kraków shows 7 reviews, the newest from 4 years ago [S]. On Oferteo, the best-reviewed Poznań-area firm has 74 reviews and **no website at all** [S].
3. **The client's real fear is the unknown final bill**: "koszt wzrósł z 12 do 40 tys.", "wiercili coraz głębiej, a wody nie było" (kb.pl, Jul/Aug 2026) [S]. Only one firm (gotowa-studnia.pl, Pomorze) addresses it with a "gwarancja na wodę" [S].
4. **Water quality is a hidden cost.** Iron and manganese exceed the limits (0.2 mg Fe/l, 0.05 mg Mn/l) in many wells, and a treatment station costs 5–20 tys. zł [S]. No Poznań firm site connects drilling with a water test and a treatment budget in one flow [S, for the sites reviewed].
5. **2026 context is a ready-made hook.** PIG-PIB issued hydrogeological low-water warnings (niżówka) covering wielkopolskie in July, August and September 2026 (nr 6, 7 and 8/2026) [S]. A Prawo wodne amendment (Dz.U. 2026 poz. 1033), in force from 18.08.2026, offers fee-free legalisation of unregistered wells until 31.12.2027 [S]. Mikroretencja (WFOŚiGW Poznań) has been taking applications since 22.06.2026: up to 90% / 8 000 zł, but for rainwater systems, not deep wells [S].
6. **Most Poznań search results are lead-gen networks or template pages** (kopiemystudnie.pl, extrastudnie.pl, wiercenia-studni.pl) [S]. A real local firm with a credible modern site would stand out [I].

---

## 2. Firm websites — audit (18 sites)

Platform column: WP = WordPress (wp-content found), El = Elementor, J = Joomla. All 18 pages have a `viewport` meta [S, curl]. WhatsApp links appear only on goldwiert, kopiemystudnie and studnielubelskie [S, curl].

| # | Firm / URL | City / area | Hero (gist) | Prices shown? | Calculator? | Reviews shown | Photos | Contact / form | Notable | Weaknesses |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [studnie.poznan.pl](https://studnie.poznan.pl/) | Poznań + powiat, ~100 km | "Wiercenie studni Poznań i okolice"; title "Pod Klucz w 1 Dzień"; "bez pozwolenia wodnoprawnego (do 30 m, 5 m³/d)" | **Yes**: 2490 zł up to 10 m + 199 zł per extra metre; pump 500–5000; underground housing from 1500; connection 250 zł/mb; worked examples 3290 / 4285 / 7970 zł ([cennik](https://studnie.poznan.pl/koszt-studni-glebinowej)) | No | "4.8/5 Google", **no count** | "Nasz sprzęt w akcji" (likely real, base64-embedded) | **Phone only** (6 tel links); no form, no email | Best Poznań price transparency; 3 well types (seasonal, all-year, "hybrydowa" with a hand pump); 5-step process; FAQ schema; 120 cm gate access | Phone-only; warranty with no term; typos; ©2018 vs "blisko 10 lat"; partner links to unrelated sites (drwal, świeże jaja) |
| 2 | [studnie24.pl](https://studnie24.pl/) | Garby / Poznań, ~100 km | "Studnie głębinowe oraz odwierty pod pompy ciepła" | No (separate "Cennik" page; homepage says "atrakcyjne ceny") | No | None | Many job-named photos (one duplicated) | Phone, email, address, hours; **no form** | 25 years, up to 200 m, heat-pump boreholes, help with paperwork | No proof, FAQ or reviews; SEO location pages |
| 3 | [geomtech.pl](https://geomtech.pl/wiercenie-studni-poznan) | Suchy Las / Wielkopolska | "Wiercenie studni Poznań", Ø110–415 mm | No ("wycena indywidualna") | No | None | 1 generic header image | 2 phones, email, NIP/REGON; form only on /kontakt | 6-step process, as-built documentation, water-treatment cross-sell | Text-only, no realizacje; vague permit info |
| 4 | [abde.pl](https://abde.pl/studnie-odwierty/studnie-glebinowe/) (Art-Bart) | Dopiewo / Wlkp + Lubuskie | "Studnie głębinowe", plus real estate and development | No | No | None | 1 tap-water image | Form with 4 fields + math captcha; 2 *different* phone numbers | Agricultural focus (30 m³/h) | Mixes wells with real estate; inconsistent phones; privacy policy from 2020 |
| 5 | [studnieperfekt.pl](https://www.studnieperfekt.pl/) | ~150 km around Poznań | "wiercenie… metodą płuczkową", "NA CZYSTO" (no drainage pits) | Separate "Cennik" tab | Mentioned (depth + equipment estimate), not on homepage | Link to a Google search, no on-site reviews | Placeholders/gallery | 2 phones, email, FB/YT | 30-step process; compact rig reaches ROD allotments; signed contract; FAQ (8 questions) | Typos; confusing 30 m vs 60 m text; no social proof on page |
| 6 | [kopiemystudnie.pl/poznan](https://kopiemystudnie.pl/poznan/) | "Poznań" (network) | "Wiercenie studni głębinowych Poznań" | No | No | None | Logo only | **3-field form** (phone, "Interesuje mnie" select, RODO); no phone number on page | 3-step "find city → form → we call you" | **Lead-gen network** ("Dołącz do Nas jako firma"); dowsing; keyword stuffing; stray cat-breeder link |
| 7 | [extrastudnie.pl](https://www.extrastudnie.pl/wielkopolskie/wiercenie-studni-poznan.php) | "300+ miast" | "Wiercenie studni Poznań" | Vague ("od kilkunastu tysięcy") | No | Unattributed "opinie"; AggregateRating schema with no visible source | ~15 gallery images, same alt text | 5-field form (name, email, phone, message, captcha) | "500+ studni / 15+ lat" | **Template network** (footer links to "Kurs paznokci", "Skup mieszkań"); credited "Gotowe Strony PL" |
| 8 | [wiercenia-studni.pl/swarzedz](https://www.wiercenia-studni.pl/swarzedz/) | Swarzędz (network) | "Wiercenie otworów pod studnie głębinowe" | No ("Zapytaj o cennik!") | No | None | SVG placeholder; "Miejsce na Twoją reklamę" | Phone, email, form | **Lead-gen**: operator in Warsaw sells leads to "jedną firmę" per area | Placeholder socials, blog last updated Jan 2024 |
| 9 | Wiercenie-Studni (Swarzędz) — [Oferteo profile](https://www.oferteo.pl/wiercenie-studni/firma/1547947) | Swarzędz | — | 150–250 zł (offer); "Cena ustalona indywidualnie" | — | **4.95/5, 74 reviews** | Gallery on Oferteo | Oferteo only | Since 1992 | **No website**: the best-reviewed local firm depends on a portal [S]. Typical sales target for our demo [I] |
| 10 | [studniekrakow.pl](https://studniekrakow.pl/studnie-glebinowe/) | Kraków / Małopolska | "Studnie… od 150 zł za mb kompleksowo z materiałem" | **Yes, full table**: 80 mm 150; 115 mm 230; 120 mm 250; 165 mm 280 zł/mb; dowser 700; no water 100 zł/mb; filter 700… | No | 4.9 from **7** reviews (newest 4 years old) | Rigs + references | **Phone only**; no form, no email | 30 years, ~7000 jobs, fleet listed (3 rigs, 3 compressors), tracked rig "nie zostawiamy kolein" | Price inconsistencies; cennik on another domain; references from 2016–17; template vars `{title}` left in footer |
| 11 | [szukamywody.pl](https://szukamywody.pl/cennik-wiercenie-studni-glebinowej/) (Aquawiert) | Śląsk / Małopolska | Water searching + drilling | **Yes**: search from 700; 260–300 zł/mb; connection 4000/5000; ≤30 m ≈ 7–10 tys. | "Zobacz przykładową wycenę" (static) | Section exists, no text | Partner logos (Grundfos) | Phone, email, form | ERT (electrical tomography) water search; "otwór kontrolny" | FAQ duplicated; casing price contradictions; no-water policy unclear |
| 12 | [goldwiert.pl](https://goldwiert.pl/) | Warszawa + 200 km | "NAJLEPSZE STUDNIE… 24H Woda*FREE" | No ("Przebijamy Każdą Cenę") | No | 3 testimonials, no stars; Oferteo 5.0 | Partly stock (pexels file names) [I] | 4-field form; 11 tel links; WhatsApp | "REZERWACJE" buttons, promo urgency | Typos, conflicting hours, stale "Maj 2025" banner, BBB/Yelp logos (US badges, irrelevant in PL) |
| 13 | [studniewjedendzien.pl](https://studniewjedendzien.pl/) | Wrocław + 50 km | "Studnia głębinowa nawet w jeden dzień"; stats 20+ / 99% / 100% | No | No | None | 1 hero image | 4-field form; 3 phones | Clean, fast (22 KB); footnote on the 99% claim | No reviews, warranty or address |
| 14 | [twojastudnia.eu](https://www.twojastudnia.eu/studnie-glebinowe) (Przem-Wiert) | Wrocław / Dolny Śląsk | "Wiercenie studni… we Wrocławiu" | No ("Cena obejmuje:" list) | No | None | 10 job photos | 3 phones, address, NIP; no form | Geologist supervision | No CTA, ©2020, typos |
| 15 | [budar.net.pl](https://budar.net.pl/oferta/wiercenie-studni-glebinowych/wiercenie-studni-wroclaw) | Mokronos / Wrocław | H1 only | No | No | None | None of the work | Phone, email; no form | Up to 200 m, threaded certified pipes | ©2018; keyword-heavy; dowsing |
| 16 | [gotowa-studnia.pl](https://gotowa-studnia.pl/) | Pomorze / Kuj-Pom / N. Mazowsze (3 bases) | "Studnie głębinowe **z gwarancją na wodę**" | No ("nie da się… jedną stałą kwotą") + cost guide | No | "5,0/5" with 4 reviews shown, **one negative** | Own rigs, fleet, office | 3 phones (one per base), form | **"Nie znaleźliśmy wody? Nie płacisz za nieudaną realizację."** Strongest promise found | Terms of the guarantee hidden; GA4 + FB Pixel |
| 17 | [techdrill-studnie.pl](https://techdrill-studnie.pl/) | Lubuskie / Wlkp / Dolnośląskie | "Studnie głębinowe i pompy ciepła…"; ✓ own rig, ✓ docs, ✓ quote in 24 h, ✓ guarantee up to 5 years | Homepage no; **[cennik 2026](https://techdrill-studnie.pl/cennik-studni-glebinowych-2026)** yes (see §4) | **"Asystent doboru studni"** in 4 steps (purpose → scale → location → result), based on PN-92/B-01706 and PIG maps, **no prices** | "5.0 Google", no count | 12 real job photos (lubuskie) | Phone, /kontakt | Most modern of the set; 2-year labour / 5-year materials warranty; blog May 2026; rich schema (GeneralContractor, GeoCircle) | Address mismatch (Kożuchów vs Zielona Góra); "highest rating" claim unsourced |
| 18 | [studnielubelskie.pl](https://studnielubelskie.pl/) | Lubelskie | "Odwierty pod studnie głębinowe i pompy ciepła!" | No | No | None | 1 team photo | Popup form (~1 field + consent); separate phone lines | Rubber-track rigs; "70 m w 1 dzień" | Counters show "0 +"; "#" links; ©2021 |

### Patterns across the sample
- **Prices:** 4 of 18 publish real numbers (#1, #10, #11, #17-cennik) [S].
- **Calculator:** 0 of 18 give an interactive price estimate. TechDrill's assistant explicitly gives none [S].
- **Review count shown:** 1 of 18 (studniekrakow: 7) [S].
- **Stated guarantee:** 3 (#16 water guarantee, #17 2y/5y, #1 unspecified) [S].
- **Contact:** phone dominates; 5 sites have no form on the main page (#1, #2, #10, #14, #15) [S]. Forms have 3–5 fields, mostly generic (name, email, phone, message), and none asks for depth, purpose or location [S]. Oferteo's form, by contrast, asks purpose, building type, depth band, documents and timing [S].
- **Stack:** mostly WordPress/Elementor, some Joomla [S, curl].
- **Copy quality:** typos, stale copyright years, template leftovers and `#` links are common (#1, #4, #10, #12, #14, #15, #18) [S].
- **Pseudo-science:** dowsing ("radiesteta") is still offered as a selling point (#6, #10 at 700 zł, #15) [S].

---

## 3. Lead portals

| Portal | What the client sees / fills in | Firm side | Notes |
|---|---|---|---|
| **Oferteo** ([Poznań](https://www.oferteo.pl/studnie-glebinowe/poznan), [Warszawa](https://www.oferteo.pl/studnie-glebinowe/warszawa)) | Form fields: **cel** (Domowe / Gospodarcze / Przemysłowe / Inne) → **obiekt** (Dom, Budynek gosp., Dom letniskowy, Ogród działkowy, Działka/pole) → **głębokość** (do 10 / 11–30 / 31–50 mb / do uzgodnienia) → **dokumenty** (none, needs advice / badania geologiczne) → **termin** (ASAP / within a month / within 3 months) → free text. Shows "Średnio 16 263 PLN" (range 10 747–21 779 zł netto) for a well [S] | Free account; pay in **points per contact**; the price depends on industry, size and location; leads with a distant deadline are 50% cheaper; 20% off the first package ([cennik](https://www.oferteo.pl/cennik)) [S]. No zł amounts are public [S] | Poznań: "981 firm", avg 4.89 from 635 reviews. Rankings mix in non-drillers (roofers, builders, even a window-film firm) [S]. Real request examples: replacing a 6.5 m well losing water; deepening a 4 m well; 3 wells for 3 neighbouring plots; ROD allotment; well + heat-pump probes [S] |
| **Fixly** | 403 to the fetcher, not verified | Reported max 5 responders per request; Fixly PRO app ([source](https://nano.komputronik.pl/n/aplikacja-fixly-opinie-cena/)) [S, secondary] | — |
| **daibau.pl** ([Kórnik](https://www.daibau.pl/firmy/wiercenie_studni/kornik_62-035)) | "Wyślij zapytanie w 1 minutę", "Bezpłatnie, bez prowizji"; firm scores out of 10 (9.1 avg across 10 ratings) [S] | Firm pricing model not shown [S] | Lists AQUA ZIEM (Śrem), STUDNIE NET (Kórnik), GEOGRUNT etc. [S] |
| **cenauslug.pl** ([national](https://cenauslug.pl/dom-i-ogrod/wiercenie-studni-glebinowej)) | Price aggregator | — | Says 346 zł/mb average for 2026 **from 8 offers** (labour only), range 240 (Suwałki) to 450 (Warszawa); no Poznań data; Poznań page returned 410 [S]. The sample is tiny [I] |
| **OLX / Sprzedajemy / Allegro Lokalnie** | Anonymous ads ("FIRMA"), "od 140–200 zł/mb" | — | Low trust signals [S] |
| Builderchain / Pewni Fachowcy / Kowalski / Google Local Services | **Not found** for this category in PL | — | I could not confirm that Google Local Services Ads run in Poland [I, unverified] |

**Implication [I]:** Oferteo's 5-question form is the de facto Polish standard for qualifying a well lead. Our demo should **own those exact questions**, so the firm receives Oferteo-quality leads directly and for free, and does not have to buy points.

---

## 4. Prices 2025–2026 (with sources and dates)

### Per metre (zł/mb)
| Source (date) | Value |
|---|---|
| [kb.pl](https://kb.pl/aktualnosci/dom/koszt-i-metody-wiercenia-studni-_z/) (01.08.2026) | 200–350 typical; >400 in difficult geology |
| [muratordom](https://muratordom.pl/instalacje/instalacja-wodna/cena-studni-glebinowej-2026-ile-kosztuje-studnia-glebinowa-aa-PqTD-CSKT-5dwF.html) (27.04.2026) | 80 mm test borehole from 150; **115 mm 200–230; 120 mm 220–250; 125 mm 250–280; 165 mm 280–350**; 200 mm from 350; no water / <1000 l/d from 100; hard rock up to 400–500; steel casing from 150 |
| [TechDrill cennik 2026](https://techdrill-studnie.pl/cennik-studni-glebinowych-2026) | PCV 110: 220–250; **PCV 125: 250–300**; PCV 160: 350–450; steel 168: 450–600 |
| [extradom](https://www.extradom.pl/porady/artykul-wiercenie-studni-cena-za-wykonanie-i-aktualny-cennik) (upd. 18.06.2025) | Average 150–300; **Poznań & Wielkopolska 200–400**; Warszawa 250–400; Kraków 150–280; Wrocław 150–430 |
| [studnie.poznan.pl](https://studnie.poznan.pl/koszt-studni-glebinowej) (live 2026) | **2490 zł up to 10 m + 199 zł/mb** (pipes, filter, travel ≤100 km included) |
| [studniekrakow.pl](https://studniekrakow.pl/studnie-glebinowe/) ("Cennik 2026") | 115 mm 230; 120 mm 250; 165 mm 280 |
| Wiercenie-Studni Swarzędz ([Oferteo](https://www.oferteo.pl/wiercenie-studni/firma/1547947)) | 150–250 |
| [cenauslug.pl](https://cenauslug.pl/dom-i-ogrod/wiercenie-studni-glebinowej) (12.05.2026) | Average 346 (labour only, n=8) |

**Working range for a Poznań demo [I]:** 200–300 zł/mb for Ø115–125 mm in the Wielkopolska lowland (sand/gravel), with a fixed minimum of about 2.5 tys. zł. The demo should show this as a range, never a promise.

### Components
| Item | Range | Source |
|---|---|---|
| Submersible pump (pompa głębinowa) | 1 500–5 000 (kb.pl 2026); 2 000–6 000 (TechDrill); 1.2–3.5k at ~25 m → 2–6k at 50–60 m ([kb.pl 02.08.2026](https://kb.pl/aktualnosci/infrastruktura/wysoki-koszt-studni-glebinowej/)) | [S] |
| Hydrofor set | 1 000–3 000 (kb.pl); 1 500–3 500 (TechDrill); 100–200 l tank 500–1 200 (extradom) | [S] |
| Housing (obudowa/studzienka) | 800–2 500 (TechDrill); underground from 1 500 (studnie.poznan.pl) | [S] |
| Controller / automation | 500–1 500 (TechDrill) | [S] |
| Connection to house | 250 zł/mb (studnie.poznan.pl); 4 000–5 000 (Aquawiert) | [S] |
| Water test | micro 100–200, physico-chemical 200–500 ([kb.pl 23.07.2026](https://kb.pl/aktualnosci/ogrod/wywiercil-studnie-za-20-tys-zl/)); 300–800 (TechDrill) | [S] |
| Treatment (Fe/Mn removal, softening) | 5 000–20 000 (TechDrill); 7–15k (kb.pl); simple softener from ~1 000 (kb.pl) | [S] |
| Hydrogeological docs (>30 m) | 1 500–3 000 (TechDrill, kb.pl); water permit 2 000–5 000 (extradom) | [S] |
| Geophysical survey | "kilkaset zł" (kb.pl); geological survey 800–1 500 (extradom) | [S] |

### Turnkey totals
- **8 000–15 000 zł** for a typical 25–35 m house well; >20 000 for larger systems (kb.pl, 08/2026) [S].
- **18 000–22 000 zł** for a 30–50 m well with PCV 125, pump, hydrofor and housing (TechDrill 2026) [S].
- **14 200–25 900 zł** for 30 m including paperwork (extradom 2025) [S].
- Oferteo national average **16 263 zł** (10 747–21 779 netto) [S].
- Real cases: 21 000 zł including treatment (kb.pl); planned 12k ending at **40k** after hitting rock (kb.pl, illustrative scenario) [S].
- Cheap end: garden well 10 m with a suction pump **3 290 zł** (studnie.poznan.pl) [S].

**Water price for ROI [S, outdated]:** Aquanet Poznań tariff from Dec 2023: water 5.82 zł/m³ brutto, sewage 9.01 zł/m³ brutto ([komunikat](https://www.aquanet.pl/wp-content/uploads/2023/12/komunikat_nowa_taryfa.pdf)). A newer tariff exists, but I could not find its amounts. Extradom cites Wrocław 14.1 and Gorzów 16.64 zł/m³ (combined) [S].

---

## 5. Law (state as of Oct 2026)

- **≤30 m deep and ≤5 m³/day, own household or farm** = "zwykłe korzystanie z wód": **neither a water permit nor a water-law notification** (art. 395 Prawa wodnego). Table in [infor.pl 17.08.2026](https://nieruchomosci.infor.pl/7635786,masz-niezgloszona-studnie-mozna-uniknac-oplaty-legalizacyjnej-i-kary.html); confirmed by [farmer.pl 26.08.2026](https://www.farmer.pl/finanse/abolicja-nie-oznacza-automatycznej-legalizacji-studni-weszla-nowelizacja-prawa-wodnego,182051.html) [S].
- **>30 m deep** (or more than 5 m³/day): **water permit** (Wody Polskie) and hydrogeological documentation [S].
- **Note:** several sites and articles mix up the units "5 m³/h" and "5 m³/doba" and the paths "zgłoszenie budowlane" vs "nic" (e.g. kb.pl 08/2026 says "5 m3/h… zgłoszenia budowlanego"). Extradom states explicitly "na dobę, nie na godzinę" [S]. **For the demo [I]:** show a simple decision tree and have the firm confirm it. Do not overclaim.
- **New in 2026: legalisation amnesty.** Ustawa z 19.06.2026 o zmianie Prawa wodnego (Dz.U. 2026 poz. 1033), art. 524a, in force **18.08.2026**. Wells built before that date without the required consent can be legalised **without the legalisation fee (6 601,67 zł in 2026)** and without the administrative fine. A complete application is due by **31.12.2027** [S]. The private costs of the operat, maps and hydrogeology are **not** waived [S]. This creates new paid work for drilling and documentation firms [I].
- **Enforcement:** Wody Polskie imposed over 14 mln zł in fines for illegal groundwater abstraction in 2025–2026 ([sadyogrody.pl](https://www.sadyogrody.pl/pozostale/108/susza_wody_polskie_14_mln_zl_kar_za_nielegalny_pobor_wod_podziemnych,52763.html)) [S, secondary].
- **Siting distances** (Rozp. MI 12.04.2002, per extradom): 5 m from the plot boundary; 7.5 m from a roadside ditch axis; **15 m** from a cesspit, compost bin or livestock building; 30 m from a treated-sewage drainage field; 70 m from untreated-sewage drainage [S].

---

## 6. Grants / subsidies 2026

| Programme | Status | Relevant to deep wells? |
|---|---|---|
| **Mikroretencja** (successor of "Moja Woda"; FEnIKS, 173 mln zł nationally) — [WFOŚiGW Poznań](https://www.wfosgw.poznan.pl/aktualnosci-z-funduszu/mikroretencja-w-wielkopolsce-22-czerwca-ruszy-nabor-wnioskow/) | **Open since 22.06.2026**, continuous until funds run out. Up to **90%, max 8 000 zł**. Only completed projects, costs from 01.07.2024 to 31.12.2027. Apply via GWD (gwd.nfosigw.gov.pl). A property already funded by "Moja Woda" is excluded [S] | **No, not directly.** Eligible items are rainwater collection, tanks ≥2 m³, infiltration wells (studnie *chłonne*), pumps and sprinklers for retained water [S]. Deep wells are not listed [S]. **Upsell angle [I]:** a firm that also installs rainwater tanks or irrigation can pair a well with a grant-funded retention system. |
| "Moja Woda" (NFOŚiGW, earlier editions) | Replaced by Mikroretencja in 2026 ([farmer.pl 03.01.2026](https://www.farmer.pl/finanse/dotacje-na-zbiorniki-na-deszczowke-wracaja-w-2026-co-obejmie-program-moja-woda,170718.html)) [S] | Earlier editions: up to 6 000 zł / 80% [S, secondary] |
| **Gminne dotacje do studni** | Exist ad hoc, e.g. [Gmina Krempna 2026](https://samorzad.gov.pl/web/gmina-krempna/ogloszenie-o-naborze-wnioskow-o-udzielenie-dotacji-na-dofinansowanie-budowy-studni-glebinowych): 80%, max 8 000 zł, applications 16–31.03.2026 [S] | Legally contested: RIO Łódź and a WSA ruling said gminas cannot subsidise household wells ([rp.pl](https://pro.rp.pl/administracja/art39581091-gmina-nie-moze-dokladac-mieszkancom-do-budowy-studni)) [S]. I found **no Wielkopolska gmina** with a well subsidy [S, negative result] |

**Demo copy recommendation [I]:** "Studnia głębinowa nie jest objęta Mikroretencją, ale zbiornik na deszczówkę i nawadnianie — tak (do 8 000 zł). Pomożemy połączyć oba." This is honest and differentiating.

---

## 7. Water quality and drought in Wielkopolska

- **Iron and manganese:** limits are 0.2 mg Fe/l and 0.05 mg Mn/l. PIG-PIB notes Quaternary groundwater in Poland often carries Fe/Mn at levels that make it unsuitable without treatment ([gq.pgi.gov.pl](https://gq.pgi.gov.pl/article/view/13621)). In the kb.pl case (07/2026), a 20 tys. zł well had water "nie nadaje się do picia ani do celów gospodarczych" [S]. Wielkopolska is a lowland of Quaternary sands and gravels, so the Fe/Mn issue is very likely relevant there [I]. Older regional data: of 6 public wells tested in Wlkp (2012), 2 failed on **nitrates and turbidity** ([umww.pl](https://bip.umww.pl/pliki/eradni/3/115/4596/16389/uchwala-xxxiv-679-2013z.pdf)) [S]. Nitrates are a farming-area risk for shallow wells [I].
- **Hardness:** I found no Wielkopolska-specific well data [S, negative]. Scale: 180–350 mg CaCO₃/l "średnio twarda", 350–530 "twarda"; legal limit 500 [S]. Do not claim numbers without a source.
- **Drought 2026:** PIG-PIB **hydrogeological warnings nr 6/2026 (July), 7/2026 (August) and 8/2026 (September)** all include **wielkopolskie** (low-water / niżówka state) ([nr 8/2026](https://www.pgi.gov.pl/psh/psh-2/aktualna-sytuacja-hydrogeologiczna/11982-ostrzezenie-hydrogeologiczne-psg-nr-8-2026/file.html)) [S]. One secondary source (superbiz.se.pl) reports October as well [S, unverified]. PIG says this mainly threatens **shallow private wells** [S]. That directly feeds demand for **pogłębianie studni** and replacement drilling. The Oferteo Poznań requests already include "6.5 m well loses water" and "4 m well, insufficient yield" [S].
- **Seasonality:** a firm in Małopolska says June is the peak month; TechDrill says April–September is peak season, with booking advised 4–6 weeks ahead and 5–10 working days for rig mobilisation in Wielkopolska [S, company claims]. Autumn and winter have shorter queues ([infomia](https://infomia.pl/lifestyle/kiedy-najlepiej-wiercic-studnie-glebinowa-wplyw-por-roku-i-poziomu-wod-gruntowych-na-prace-wiertnicze/)) [S]. Drought years plausibly pull demand forward into spring and summer [I]. I did not check Google Trends.

---

## 8. What clients ask (from ranking articles and Oferteo requests)

From muratordom 2026, extradom 2025, kb.pl 2026, firm FAQs and Oferteo requests [S]:
1. Ile to będzie kosztować *razem*, nie tylko za metr?
2. Jak głęboko trzeba wiercić u mnie?
3. Czy potrzebuję pozwolenia / zgłoszenia? (the 30 m / 5 m³ rule)
4. Co jeśli nie trafią na wodę / trzeba wiercić głębiej, kto płaci? (kb.pl 29.07.2026)
5. Czy woda będzie pitna? Żelazo? Badanie wody?
6. Czy wjadą na małą działkę / zniszczą trawnik i kostkę? (studnie.poznan.pl FAQ, studniekrakow "nie zostawiamy kolein")
7. Jak długo trwa? (1 dzień vs kilka dni)
8. Pompa głębinowa czy hydrofor / ssąca? Studnia całoroczna czy sezonowa?
9. Czy się opłaca vs wodociąg? (kb.pl "darmowa woda" pieces)
10. Pogłębianie istniejącej studni, legalizacja starej studni (new in 2026).

---

## 9. GAP analysis — what no Polish firm site does well

| Gap | Evidence | Opportunity |
|---|---|---|
| **G1. Interactive, honest price estimator** | 0/18 have one; TechDrill's assistant refuses prices; only 4/18 publish any numbers [S] | Depth slider, diameter, purpose, pump type, housing and connection length → **range** (min–max) with a line-item breakdown, plus a "+ ryzyko: głębiej niż zakładano" band |
| **G2. Risk transparency (the "12k → 40k" fear)** | kb.pl 07–08/2026 articles; only gotowa-studnia promises "nie płacisz, gdy brak wody", with hidden terms [S] | Publish the **rules up front**: price per extra metre, cap or stop-loss point, what you pay when the hole is dry (e.g. the 100 zł/mb "bez wody" practice in studniekrakow) |
| **G3. "How deep at MY address?"** | No firm site has a map or locality data. TechDrill uses PIG maps internally for priority cities only [S] | Map or locality picker with **typical depth bands for Poznań-area gminy** taken from the firm's own past jobs ("Realizacje na mapie": Dopiewo 24 m, Kórnik 31 m…) [I]. Note: there is no public per-parcel Bank HYDRO API; the data must be requested from PIG-PIB [S] |
| **G4. Verifiable social proof** | Ratings without counts; old reviews; the best local firm lives only on Oferteo (74 reviews) [S] | Live Google rating + count, dated reviews, photo-backed case studies (location, depth, Ø, yield, days, price band) |
| **G5. Water quality to treatment journey** | Fe/Mn is a known hidden cost of 5–20k; Poznań firm sites don't connect it [S] | "Po wierceniu" module: test package (micro + physico-chemical), what the results mean, treatment price ranges |
| **G6. Clear 2026 legal decision tree** | Contradictory "5 m³/h vs /doba" claims across the market [S] | 3-question widget: depth >30 m? >5 m³/doba? household/farm use? → "nic / pozwolenie wodnoprawne". Plus a **legalisation amnesty** explainer (deadline 31.12.2027) as a new service line |
| **G7. Qualified lead form** | Firm forms ask name/email/message; Oferteo asks 5 qualifying questions [S] | Multi-step form reusing Oferteo's questions plus photos of the gate/access and existing well; ends with a calendar "termin wizji" |
| **G8. Season / drought urgency done honestly** | Nobody references PIG warnings; goldwiert uses fake urgency [S] | "Stan zagrożenia hydrogeologicznego – wielkopolskie (PIG-PIB, wrzesień 2026)" banner with source link, plus a "pogłębianie płytkiej studni" CTA |
| **G9. Polish UX polish** | Typos, stale copyright years, `#` links, template variables everywhere [S] | Flawless copy, current dates, fast static site. This alone sells against the competitors [I] |
| **G10. ROI vs wodociąg** | kb.pl articles debate "darmowa woda"; no firm site computes it [S] | Watering-season ROI: m³ per season × local tariff vs well cost + electricity |

---

## 10. Top 10 ideas for our demo (Poznań firm)

1. **"Wycena w 60 sekund" calculator.** Inputs: purpose (ogród sezonowo / dom całoroczny / gospodarstwo), expected depth (with a "nie wiem → pokaż typową dla mojej gminy" option), Ø110/125/160, pump (ssąca+hydrofor / głębinowa), housing, connection metres. Output: a **min–max range** and line items, using constants drawn from the §4 sources (e.g. base ≤10 m, then zł/mb, pump 1.5–5k, hydrofor 1–3k). Clearly mark it "szacunek, nie oferta".
2. **"Mapa realizacji" for Poznań county.** Pins with depth, water table, diameter, yield, days and date (demo data clearly labelled). This answers "jak głęboko u mnie?" and doubles as social proof.
3. **"Gwarancja przejrzystości" box.** Fixed price per extra metre, stop-loss rule ("po X m bez wody zatrzymujemy się i dzwonimy"), price for a dry hole. Neutralises the kb.pl "12k → 40k" fear. No competitor states these terms openly.
4. **Oferteo-grade multi-step lead form.** Cel → obiekt → głębokość → dokumenty → termin → address + gate width + photo upload → preferred contact (tel / SMS / WhatsApp). Pitch line to the firm owner [I]: "leady jak z Oferteo, ale bez płacenia za punkty".
5. **Legal decision tree 2026 plus amnesty landing section.** "Czy potrzebuję pozwolenia?" (30 m / 5 m³/doba) and "Masz starą, niezgłoszoną studnię? Legalizacja bez opłaty 6 601,67 zł do 31.12.2027" (Dz.U. 2026 poz. 1033). This opens a new revenue line.
6. **Drought-aware hero or banner.** Cite PIG-PIB warning nr 8/2026 for wielkopolskie, with CTAs "Pogłębianie płytkiej studni" and "Studnia zamiast podlewania z wodociągu".
7. **Water quality module.** "Żelazo i mangan w Wielkopolsce": limits 0.2 / 0.05 mg/l, test package pricing (100–500 zł), treatment ranges, before/after photos. Upsell to treatment stations.
8. **Grant helper (honest).** "Studnia głębinowa nie jest objęta Mikroretencją, ale zbiornik ≥2 m³ + nawadnianie — do 90% / 8 000 zł (WFOŚiGW Poznań, nabór od 22.06.2026)". Bundle offer: well + rainwater tank.
9. **Real proof stack.** Google rating **with count and date** (embed), 3 detailed case studies with real job photos, fleet card (rig type, minimum gate width, tracks / "bez kolein"), NIP/REGON, warranty in years. Each targets a weakness seen in §2.
10. **ROI and seasonal planner.** "Ile zaoszczędzisz na podlewaniu?" (m³/season × tariff, Aquanet figures with a date) plus a "Zarezerwuj termin na wiosnę" seasonal calendar (peak April–September; book 4–6 weeks ahead).

Also: one-tap call and SMS sticky bar on mobile; all prices dated ("Cennik obowiązuje od 2026-…"); FAQ with FAQPage schema (competitors #1 and #7 already use it); one URL per Poznań-county gmina only where there is real case content (avoid the doorway-page spam the networks run).

---

## 11. Source list (all opened or seen in this session)
- Firms: studnie.poznan.pl (+ /koszt-studni-glebinowej), studnie24.pl, geomtech.pl/wiercenie-studni-poznan, abde.pl, studnieperfekt.pl, kopiemystudnie.pl/poznan, extrastudnie.pl, wiercenia-studni.pl/swarzedz, oferteo.pl/wiercenie-studni/firma/1547947, studniekrakow.pl, szukamywody.pl, goldwiert.pl, studniewjedendzien.pl, twojastudnia.eu, budar.net.pl, gotowa-studnia.pl, techdrill-studnie.pl (+ /cennik-studni-glebinowych-2026, /kalkulator), studnielubelskie.pl
- Portals: oferteo.pl/studnie-glebinowe/poznan, /warszawa, oferteo.pl/cennik (via search), daibau.pl Kórnik, cenauslug.pl
- Articles: kb.pl (01.08.2026, 02.08.2026, 29.07.2026, 23.07.2026), muratordom.pl (27.04.2026), extradom.pl (upd. 18.06.2025)
- Law: nieruchomosci.infor.pl (17.08.2026), farmer.pl (26.08.2026)
- Grants: wfosgw.poznan.pl (01.06.2026), farmer.pl (03.01.2026), samorzad.gov.pl Krempna, pro.rp.pl
- Hydro: pgi.gov.pl warnings 6, 7 and 8/2026; wir.org.pl; gq.pgi.gov.pl; sadyogrody.pl
