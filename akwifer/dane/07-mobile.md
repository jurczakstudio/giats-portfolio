# 07 — MOBILE · AKWIFER v2 „ZLECENIE”

Telefon to główny kanał (W1: klient pyta wieczorem z telefonu). Każda sekcja z `inna-kompozycja` w 06-sekcje.tsv:

- **Zmierzch** — kadr pionowy (40svh) na górze, pod nim H1, lead i wybór gminy z przyciskiem na całą szerokość; wycena mieści się w pierwszym ekranie 390×844 (W1).
- **Karta** — rubryki jedna pod drugą (etykieta | wartość), przycisk SMS na całą szerokość pod kciukiem (W4).
- **Powiat** — wykres SVG ukryty; zastępuje go sekcja „Szybki wybór” (tylko-mobil): 14 gmin z paskiem od najpłytszego ujęcia do mediany i kreską 30 m, każda linkuje do podstrony (W2).
- **Robota** — kadr kwadratowy od krawędzi do krawędzi, etapy pod nim (W5).
- **Paszport** — karta paszportu bez obrotu, pełna szerokość.
- **Zgłoszenie** — podgląd SMS jak dymek w telefonie, dwa przyciski pełnej szerokości (W4).
- **Podstrony** — liczba (mediana) nad tytułem; wykres gmin, badanie wody i schemat drogi zgłoszenia przewijane w bok z podpisem „przewiń w bok” — tekst w SVG zostaje czytelny (≥14 px).
- **Pasek „strona wzorcowa”** — na telefonie statyczny na końcu strony, nie zasłania treści.

Sprawdzone: zrzuty 390 i 1440 (`dane/zrzuty/`), bez poziomego scrolla strony, bez błędów konsoli; `kadr.mjs` testuje kartę, SMS, pamięć karty między stronami, tryb właściciela i kalkulator.
