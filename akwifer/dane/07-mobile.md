# 07 — MOBILE · AKWIFER v2 „ZLECENIE”

Telefon to główny kanał (W1: klient pyta wieczorem z telefonu). Każda sekcja z `inna-kompozycja` w 06-sekcje.tsv:

- **Zmierzch** — kadr pionowy (40svh) na górze, pod nim H1, lead i wybór gminy z przyciskiem na całą szerokość; wycena mieści się w pierwszym ekranie 390×844 (W1).
- **Karta** — rubryki jedna pod drugą (etykieta | wartość), przycisk SMS na całą szerokość pod kciukiem (W4).
- **Powiat** — mapa gmin od krawędzi do krawędzi, bez liczb na mapie (byłyby < 14 px); pierwsze dotknięcie wybiera gminę, karta gminy pod mapą pokazuje liczby, drugie dotknięcie otwiera podstronę. Pod spodem „Szybki wybór” (tylko-mobil): 14 gmin z paskiem od najpłytszego ujęcia do mediany i kreską 30 m (W2, W7).
- **Rachunek ogrodu** — odwrócona kolejność: najpierw wynik (lata zwrotu) i wykres, potem pokrętła; wykres rysowany w prawdziwej szerokości ekranu, więc opisy mają pełne 14 px; legenda pod wykresem zamiast podpisów w środku (W6).
- **Robota** — kadr kwadratowy od krawędzi do krawędzi, etapy pod nim (W5).
- **Paszport** — karta paszportu bez obrotu, pełna szerokość.
- **Zgłoszenie** — podgląd SMS jak dymek w telefonie, dwa przyciski pełnej szerokości (W4).
- **Podstrony** — mini-mapa z podświetloną gminą i liczba (mediana) obok siebie; wykres gmin, badanie wody i schemat drogi zgłoszenia przewijane w bok z podpisem „przewiń w bok” — tekst w SVG zostaje czytelny (≥14 px).
- **Pasek „strona wzorcowa”** — na telefonie statyczny na końcu strony, nie zasłania treści.

Sprawdzone: zrzuty 390 i 1440 (`dane/zrzuty/`), bez poziomego scrolla strony, bez błędów konsoli; `kadr.mjs` testuje kartę, SMS, pamięć karty między stronami, tryb właściciela i kalkulator.
