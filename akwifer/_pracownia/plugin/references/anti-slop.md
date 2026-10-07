# Anty-szablon — czerwona lista

Przeczytaj przed pierwszą linijką HTML. Jeśli którykolwiek punkt opisuje to, co masz
zamiar zbudować — zbuduj coś innego.

## Układ

- Hero z wycentrowanym nagłówkiem, podtytułem i dwoma przyciskami obok siebie.
- Sekcja trzech kart w równym rzędzie, każda z ikonką na górze, nagłówkiem i akapitem.
- „Dlaczego my?" z czterema kafelkami: Jakość · Doświadczenie · Terminowość · Cena.
- Karuzela opinii z awatarami i gwiazdkami.
- Pasek liczników („500+ realizacji", „30 lat doświadczenia") lecących od zera.
- Sekcja CTA na kolorowym tle tuż nad stopką.
- Naprzemienne bloki tekst-lewo/obraz-prawo, tekst-prawo/obraz-lewo, w kółko.
- Karta w karcie w karcie.

## Wizualnie

- Gradient fioletowo-niebieski. Jakikolwiek gradient jako tło sekcji.
- `border-radius: 12px` i miękki cień na wszystkim.
- Ikonki z biblioteki (Font Awesome, Lucide) wrzucone jako dekoracja.
- Zdjęcia stockowe ludzi w kaskach i garniturach.
- Emoji jako ikony sekcji.
- Więcej niż jeden kolor akcentu.
- Tekst na zdjęciu bez przyciemnienia, z nadzieją że będzie czytelny.

## Tekst

- „Zapraszamy do zapoznania się z naszą ofertą."
- „Jesteśmy firmą z wieloletnim doświadczeniem."
- „Stawiamy na jakość i zadowolenie klienta."
- „Kompleksowa obsługa", „indywidualne podejście", „konkurencyjne ceny".
- Nagłówek, który nie niesie informacji: „Nasze usługi", „O nas", „Oferta".
  Lepiej: „Co robimy w warsztacie w Cielimowie", „Trzy rzeczy, które robimy sami".

## Ruch

- `fade-in-up` na każdej sekcji po kolei.
- Parallax na tle hero.
- Animowany kursor.
- Preloader z procentami.

## Test przed pokazaniem

Zadaj sobie trzy pytania. Jeśli którekolwiek ma złą odpowiedź — wracaj do etapu 2.

1. **Czy da się tę stronę odróżnić od strony konkurenta z tego samego miasta, gdyby
   zasłonić logo i nazwę?** Musi się dać.
2. **Czy jest tu jedna rzecz, której klient nigdzie indziej nie zobaczy?**
   (płyty granitu w 3D, rzeźba sterowana scrollem, kronika zakładu, tablica z rokiem założenia)
3. **Czy wyjaśniłbym każdą decyzję zdaniem zaczynającym się od „bo klient tego zakładu…"?**

## Czego sekcja MUSI mieć (część dodatnia)

Cała lista wyżej jest zakazowa. Jeśli usuniesz wszystkie klisze i nie dodasz nic
w zamian, zostaje tekst na tle z włoskowymi liniami — czyli dokument. Szymon zgłaszał
to dwa razy (ArtStonex 10.09.2026, Hormon 15.09.2026): **po hero jakość sekcji leci
w dół, zostaje czarny tekst na jasnym tle i może jedno zdjęcie.**

Pomiar na Hormonie przed poprawką, udział mediów w powierzchni kolejnych sekcji:
`100 / 76 / 33 / 2,5 / 25 / 28 / 0 / 0`. Dwie ostatnie sekcje nie miały nic poza tekstem,
a 73 z 79 zdjęć siedziały w jednej sekcji-galerii.

**Reguła: każda sekcja niesie obiekt.** Obiektem jest:

- zdjęcie w realnej skali — miniatura poniżej 120 px to ikonka, nie obiekt,
- rysunek techniczny (przekrój, skala, schemat),
- powierzchnia materiału jako tło sekcji (makro kamienia pod ciemną powłoką),
- wielkoformatowa liczba albo inskrypcja jako bryła, nie jako podpis,
- sterowanie, którym użytkownik coś robi.

Sam tekst, choćby najlepiej złożony, obiektem nie jest.

**Bramka:** `python ../_wzorce/audyt/audyt.py .` — bezpieczniki „sekcja niesie obiekt"
i „rytm obiektów". Kończy kodem 1, gdy któraś sekcja jest samym tekstem albo gdy dwie
sekcje pod rząd mają ten sam rodzaj obiektu.

*(Do 16.09.2026 robił to osobny `audyt_sekcji.py` kopiowany do `dane/` każdego projektu.
Został scalony z `_wzorce/audyt/audyt.py`, żeby nie istniały dwie bramki mierzące to samo
różnymi metrykami. Definicja OBIEKTU przeszła stamtąd bez zmian i jest rozszerzona
o `<picture>`, `<canvas>`, `<video>` oraz powierzchnie malowane CSS-em.)*

**Trzy nawyki, które to powodują — pilnuj ich świadomie:**

1. Zdjęcia zbierają się w jednej sekcji-galerii. **Rozdziel kadry do konkretnych sekcji
   w blueprincie**, zanim zaczniesz kodować.
2. Od czwartej sekcji pytanie zmienia się z „jaki jest tu pomysł wizualny" na „jak
   czytelnie ułożyć te cztery punkty". Sekcja staje się pojemnikiem na treść.
3. `build.py` pisze się od góry do dołu, więc kontakt i przebieg powstają, kiedy koncept
   jest już wydany na hero. **Wróć na dół strony na świeżo.**

**Test przed pokazaniem:** zrzuć osiem sekcji osobno i obejrzyj miniatury obok siebie.
Jeśli dwie wyglądają tak samo, jedna nie jest zaprojektowana.
