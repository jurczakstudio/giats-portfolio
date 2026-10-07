# 02 — WNIOSKI · AKWIFER v2 „ZLECENIE” (strona wzorcowa zawodu)

Odbiorca tej strony jest podwójny: **inwestor** szukający studni i **właściciel firmy studniarskiej**,
któremu pokazujemy demo. Strona ma przekonać drugiego, działając dla pierwszego.

**W1. F16 + F17 + F11 → Zapytania o studnie trafiają dziś do portali, które sprzedają je
wykonawcom; firma bez strony płaci za własnych klientów albo ich nie widzi.**
Konsekwencja projektowa: sercem strony jest wycena dla konkretnej gminy, która kończy się
gotowym zgłoszeniem do firmy (gmina, cel, osoby, termin) — to samo, co robi portal, tylko
bez pośrednika.

**W2. F13 + F14 + F15 → Głębokość, a więc cena i formalności, zależą od gminy, i są na to
prawdziwe dane: 14 gmin, od 14 do 110 m mediany.**
Konsekwencja projektowa: każda gmina dostaje własną podstronę z danymi PIG (nie szablon
z podmienioną nazwą), a wycena liczy widełki z najpłytszego ujęcia i mediany gminy.

**W3. F15 + F7 → W większości gmin pod Poznaniem studnia może przekroczyć 30 m — klient
boi się urzędu, a firma, która „załatwia papiery”, ma przewagę.**
Konsekwencja projektowa: wynik wyceny zawsze mówi, po której stronie 30 m leży gmina,
i co z tego wynika — formalności są częścią oferty, nie przypisem.

**W4. F17 → Klient chce czterech liczb przed telefonem: metry, złotówki, formalności, termin.**
Konsekwencja projektowa: karta zlecenia z czterema rubrykami jest sygnaturą — powstaje na
górze strony i towarzyszy klientowi na każdej podstronie (zapamiętana w przeglądarce).

**W5. Ocena Szymona v1 + reguła „demo musi być skończone” (wycena.md) → właściciel firmy
musi zobaczyć, na czym ta strona zarabia, bez czytania oferty.**
Konsekwencja projektowa: przełącznik „Oczami właściciela” odsłania przy każdej sekcji notatkę,
co ta sekcja robi dla firmy; osobna podstrona `/dla-firm/` zbiera to w ofertę.
Zdjęcia: dwa kadry generowane (wiertnica o zmierzchu, woda z nowej studni) — podpisane jako
poglądowe; żadnych przekrojów warstw (były w VIJACH i v1).

**W6. F18 + F8 → Najmocniejszy argument za studnią to rachunek za podlewanie: z kranu bez
podlicznika każdy metr sześcienny kosztuje 16,18 zł, bo płaci się też za ścieki, których nie ma.**
Konsekwencja projektowa: kalkulator „Rachunek ogrodu” — powierzchnia, dawka, sezon → m³ na rok,
koszt z wodociągu i liczba lat, po której studnia się zwraca (z widełek karty dla wybranej gminy).
Wszystkie założenia (dawka, sezon, prąd pompy) widoczne i edytowalne — nie zgadujemy za klienta.

**W7. F19 + W2 → Klient myśli o działce na mapie, nie w tabeli.**
Konsekwencja projektowa: na stronie głównej mapa powiatu z prawdziwych granic gmin, barwiona
medianą głębokości; kliknięcie gminy ustawia kartę zlecenia. Na podstronie gminy mała mapa
pokazuje, gdzie ta gmina leży. Gminy bez danych — szare i podpisane, nie ukryte.

## v3 „GŁĘBIEJ” — po researchu (dane/research/)

**W8. F24 + ocena Szymona („nudna”) → Strona ma wyglądać jak marka z branży ciężkiej, nie jak panel danych.**
Konsekwencja: dwie barwy — czerń maszyny i żółć ostrzegawcza hi-vis; nagłówki wersalikami w skali plakatu;
ziarno i siatka kreślarska jako materiał; jedna scena przypięta do przewijania jako „wow”.

**W9. F20 + F13 → Wycena musi być pierwszym ekranem, a nie sekcją niżej.**
Konsekwencja: hero = przyrząd: wybór gminy od razu pokazuje metry, złotówki i formalności na żywej
linijce głębokości. Zejście pod ziemię prowadzi do mediany wybranej gminy — personalizowane, nie ozdobne.

**W10. F21 → Największa obawa klienta to cena, która rośnie w trakcie wiercenia.**
Konsekwencja: „Gwarancja przejrzystości” (cena za metr dodatkowy z góry, punkt zatrzymania, koszt suchego
otworu) i trzy pakiety z dopłatą za metr — przykładowe zasady, które firma wpisuje swoje.

**W11. F22 + F23 → Rok 2026 daje dwa prawdziwe powody do telefonu: abolicja dla starych studni i susza.**
Konsekwencja: sekcja „Przepisy 2026” — drzewko „czy potrzebuję pozwolenia”, licznik dni do 31.12.2027,
ostrzeżenie PIG-PIB z ofertą pogłębienia. Na telefonie stały pasek: Zadzwoń · SMS · Wycena.
