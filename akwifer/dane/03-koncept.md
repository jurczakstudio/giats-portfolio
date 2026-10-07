# 03 — KONCEPT · AKWIFER (strona wzorcowa zawodu „studnie głębinowe”)

Druga strona studniarska pracowni, po VIJACH „ZWIERCIADŁO” (jasna mgła, zdjęcia klientów,
zejście przez przekrój). Zadanie Szymona: „wejdź na wyższy poziom, strona poglądowa dla zawodu,
bez klienta”. Repo: `giats-portfolio` — z niego bierzemy **techniki** (okna w treści, tło
z liniami w shaderze), nie kod Nexta i nie grafiki.

## 1. Dziesięć pytań

1. **Za co ten zawód bierze pieniądze i czego nie widać?** Za trafienie w warstwę, która odda
   wodę, i sprawdzenie tego pompowaniem. Nie widać pola wody pod działką i tego, jak studnia
   je zmienia (W1).
2. **Co robi lepiej niż sąsiad?** Wzorzec: firma, która liczy i pokazuje — Q, s, R zamiast
   „woda będzie” (W2).
3. **Kto czyta?** Inwestor budujący dom, wieczorem, często na telefonie; drugi raz z partnerem
   przy komputerze. Racjonalny, chce zrozumieć, za co płaci 10–20 tys. zł (W4).
4. **Zdanie w głowie:** „Każda studnia zmienia mapę wody — oni to umieją policzyć.”
5. **Czynność jako interakcja:** pompowanie. Kursor/palec = pompa; suwak = wydajność (W1, W2).
6. **Fizyczny bohater:** pole zwierciadła wody — hydroizohipsy (W1).
7. **Gdzie zmienia się rytm:** na próbie pompowania — przed nią strona tłumaczy (arkusze
   z oknami, wolno), od niej liczy i załatwia (sterowanie, gęsto, mono) (W2).
8. **Decyzja nie do uzasadnienia stylem pracowni:** cała strona leży na żywej mapie
   hydroizohips, którą odkształca pompa — czyli na fizyce wody podziemnej (W1).
9. **Czego nie ma, a ma konkurencja:** zdjęć wiertnic, listy miast, „bezpłatnej wyceny”,
   liczników „500+ studni”. Zyskuje: jedną rzecz, której nikt nie pokazuje (W5).
10. **Dlaczego nie mogłaby należeć do kamieniarza czy dekarza:** bo jej obraz to pole wody,
    a interakcja to lej depresji — oba istnieją wyłącznie w tym zawodzie.

## 2. Koncept

| | |
|---|---|
| **Nazwa** | **LEJ** |
| **Metafora** | Strona jest arkuszem mapy hydrogeologicznej, a Ty stoisz na nim z pompą. |
| **Zdanie pamięciowe** | „Każda studnia zmienia mapę wody.” |
| **Fizyczny bohater** | hydroizohipsy i lej depresji |
| **Rejestr** | **arkusz mapy** (dom.md B, wniosek Matczak) — papier, niebieskie izolinie, okna-otwory wycięte w arkuszach (W5). Inny niż VIJACH na pięciu osiach: zero zdjęć, papier zamiast mgły, kroje, nośnik (shader), ruch (pole zamiast przypięcia). |

### Sygnatura

| | Co to jest | Gdzie wraca |
|---|---|---|
| **interakcja** | kursor/palec pompuje → lej depresji na mapie; klik = wiercenie stałej studni | każda strona: okna w arkuszach pokazują to samo pole |
| **ruch** | pole wody pod spodem przesuwa się z przewijaniem (mapa jedzie), lej rośnie z suwakiem Q | wszystkie podstrony |
| **materiał** | papier mapy, niebieskie hydroizohipsy co 0,5 m, co piąta pogrubiona | okna z odczytem rzędnej na żywo |

## 3. Trzy konsekwencje strukturalne

1. **Tło nie jest dekoracją, tylko modelem.** Te same funkcje liczą obraz w shaderze i liczby
   w odczytach okien — odczyt „zwierciadło 4,8 m” pod oknem jest wartością tego pola.
2. **Każda sekcja to arkusz z co najmniej jednym otworem** albo otwarta mapa. Nie ma sekcji
   na pełnym kolorze tła.
3. **Każda liczba ma wzór albo źródło** — symulator pokazuje wzór, z którego liczy; cennik
   jest jawnie przykładowy, ceny rynkowe mają źródło.

## 4. Decyzja własna

| | |
|---|---|
| **Decyzja** | Kursor jako pompa: interakcja, która jest fizycznie prawdziwa (lej depresji wg Dupuita/Sichardta), a nie efektem. |
| **Wniosek** | W1, W2 |
| **Czego nie da się przenieść** | Na stronie kamieniarza „pole, które ugina się wokół kursora” jest tapetą; tutaj jest tym, co studnia naprawdę robi z wodą. |

## 5. Różnica wobec konkurencji (F11)

| Oś | Oni | My |
|---|---|---|
| układ | hero + usługi + miasta | otwarta mapa → arkusze z oknami |
| paleta | niebieski + biel | papier mapy + niebieskie izolinie |
| typografia | systemowy grotesk | Spectral + Onest + IBM Plex Mono |
| nośnik | zdjęcia maszyn | shader pola wody, przekroje SVG |
| ruch | slider | lej depresji pod kursorem, mapa jedzie z przewijaniem |

## 6. Z giats-portfolio biorę (MIT, przypisane w stopce)

1. **Okna w treści** — wycięcia, przez które widać animowane tło. U nas okno = otwór studni.
2. **Tło z liniami szumu w shaderze** — u nas linie mają znaczenie: to hydroizohipsy.
3. Nie biorę: Nexta, R3F, symulacji płynu (za ciężka na telefon klienta), żadnych grafik.
