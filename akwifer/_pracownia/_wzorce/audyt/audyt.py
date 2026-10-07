# -*- coding: utf-8 -*-
"""audyt.py — jedyna bramka jakości Jurczak Studio.

Powstał 16.09.2026 ze scalenia dwóch skryptów, które mierzyły to samo zjawisko
różnymi metrykami:

  * `audyt_sekcji.py` (plugin, 15.09) — definicja OBIEKTU i rytm rodzajów.
    Powstał z uwagi Szymona zgłoszonej dwa razy (ArtStonex 10.09, Hormon 15.09):
    po hero jakość sekcji leci w dół. Pomiar na Hormonie: udział mediów
    w powierzchni sekcji szedł 100 / 76 / 33 / 2,5 / 25 / 28 / 0 / 0.
  * `_wzorce/audyt/audyt.py` (15.09) — przebieg po wszystkich podstronach,
    rytm kompozycji, skala, bezpieczniki.

Z pierwszego została **definicja OBIEKTU**, bo jest właściwa: obiekt to substancja,
nie markup. Atrybut `data-*` jest implementacją mechanizmu ruchu, nie dowodem
jakości sekcji — próg „≥60 % sekcji z hakiem" został usunięty, bo najtańszym
sposobem jego przejścia było posypanie `data-rv="up"` po wszystkim, czyli dokładnie
to, czego zabrania `dom.md` i `anti-slop.md`.

DWA POZIOMY KONTROLI
--------------------
BEZPIECZNIK  blokuje build. Wykrywa katastrofę, nie mierzy piękna.
             Musi być nie do przejścia samym dopisaniem atrybutu.
KOMPAS       nigdy nie blokuje. Pokazuje liczbę obok trzech poprzednich projektów.
             Każdy próg, który da się zgadać markupem, należy tutaj.

TRYBY
-----
Projekt z katalogiem `dane/` jest prowadzony wg architektury V2 — obowiązuje komplet
bezpieczników, łącznie z tymi, które wymagają deklaracji (sygnatura, tokeny, plan sekcji).
Projekt bez `dane/` to zastana strona — kontrole wymagające deklaracji schodzą do kompasu,
żeby skrypt dało się uruchomić na całej pracowni.

UŻYCIE
------
    python ../_wzorce/audyt/audyt.py              # z katalogu projektu
    python _wzorce/audyt/audyt.py lewartowski     # wskazany projekt
    python _wzorce/audyt/audyt.py --wszystkie     # tabela całej pracowni
    python _wzorce/audyt/audyt.py . --zapisz      # dopisz odcisk do _wzorce/indeks.json

Kod wyjścia 1, gdy padł którykolwiek BEZPIECZNIK.
"""
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

# ---- progi ---------------------------------------------------------------
MAX_UDZIAL_JEDNEGO_RUCHU = 0.50   # jeden typ ruchu / sekcje z ruchem
MIN_SEKCJI_DO_OCENY_RUCHU = 6     # poniżej tej liczby rozkład nic nie znaczy
MAX_KADROW_W_SEKCJI      = 0.40   # udział wszystkich kadrów w jednej sekcji
MAX_TEN_SAM_UKLAD        = 2      # ta sama konstrukcja pod rząd
MIN_PX                   = 14     # nic mniejszego w font-size
PROG_SLOWNICTWA          = 0.85   # kompas
MAX_PRZEWROTEK           = 0.60   # sekcje różniące się na mobile tylko kolumną

KATALOGI_WYNIKU = ('site', 'dist', 'build', 'public', 'out', 'www', '_site')
UZYTKOWE = ('polityk', 'regulamin', 'prywatn', 'cookie', 'dziekuj', 'mapa-strony')

RUCHY = ('data-rv', 'data-par', 'data-pin', 'data-scrub', 'data-count',
         'data-hover', 'data-drag', 'data-seq')

INDEKS = Path(__file__).resolve().parent.parent / 'indeks.json'

# Ten skrypt bywa kopiowany do migawki STRONA_ALL. Kopia może CZYTAĆ, ale nie może
# zapisywać indeksu — inaczej powstałby drugi indeks mówiący co innego niż pierwszy.
# Dokładnie ten błąd (dwa mechanizmy na jedną rzecz) kosztował nas przebudowę systemu.
ORYGINAL = (Path(__file__).resolve().parent.name == 'audyt'
            and Path(__file__).resolve().parent.parent.name == '_wzorce')

# Stosy zapasowe nie są krojami — bez tego każdy projekt miał 100% wspólnych krojów
# z każdym innym, bo wszystkie kończą się na system-ui, sans-serif.
GENERYCZNE = {'system', 'ui', 'sans', 'serif', 'monospace', 'Arial', 'Helvetica',
              'Georgia', 'Times', 'Courier', 'Segoe UI', 'Roboto', 'inherit',
              'ui sans', 'ui serif', 'system ui', 'sans serif', 'Apple Color Emoji',
              'Noto Color Emoji', 'Liberation Sans', 'Helvetica Neue'}


# ============================================================ pomocnicze
def czytaj(p):
    try:
        return p.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return ''


def bez_komentarzy(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def znajdz_wynik(baza):
    if baza.name in KATALOGI_WYNIKU and (baza / 'index.html').exists():
        return baza
    for k in KATALOGI_WYNIKU:
        if (baza / k / 'index.html').exists():
            return baza / k
    return None


def nazwa(p, korzen):
    if p.parent == korzen:
        return 'strona główna' if p.name == 'index.html' else p.stem
    return p.parent.name or p.stem


def sekcje(html):
    """Sekcje najwyższego poziomu wewnątrz <main>, z poprawnym liczeniem zagnieżdżeń.
    Metoda przeniesiona z audyt_sekcji.py — dzielenie po `<section` gubiło zagnieżdżone."""
    m = re.search(r'<main[^>]*>(.*)</main>', html, re.S)
    tresc = m.group(1) if m else html
    out = []
    for otw in re.finditer(r'<section\b([^>]*)>', tresc):
        start, glebokosc, koniec = otw.end(), 1, len(tresc)
        for z in re.finditer(r'<(/?)section\b', tresc[start:]):
            glebokosc += -1 if z.group(1) else 1
            if glebokosc == 0:
                koniec = start + z.start()
                break
        ident = re.search(r'id="([^"]+)"', otw.group(1))
        out.append((ident.group(1) if ident else '(bez id)', tresc[start:koniec]))
    return out


# ============================================================ OBIEKT
# Definicja przeniesiona z audyt_sekcji.py i rozszerzona o nośniki, których tamten
# skrypt nie znał: <picture>, <canvas>, <video>, tło materiałowe w stylu inline.
#
# OBIEKT to rzeczywista substancja wizualna albo interaktywna. Sam tekst, choćby
# najlepiej złożony, obiektem nie jest.
IKONA = re.compile(r'class="[^"]*(ikon|logo|sygnet|avatar|strzal)', re.I)


def klasy_materialu(css):
    """Klasy, które NIOSĄ powierzchnię — wyprowadzone z CSS, nie z konwencji nazw.

    Reguła domu (dom.md): „kolor kamienia niosą tekstury CSS, nie zdjęcia stockowe".
    Detektor szukający klas `tlo-*` przegapiał `.gr-szwed`, `.gr-labrador` itd.
    u Lewartowskich i uznawał ich sekcje za sam tekst — czyli bramka popychałaby
    nas w stronę fotografii, dokładnie odwrotnie niż reguła domu. Dlatego pytamy
    CSS, które klasy faktycznie malują powierzchnię."""
    out = set()
    for sel, blok in re.findall(r'([^{}]+)\{([^{}]*)\}', bez_komentarzy(css)):
        if re.search(r'\b(btn|button|cta__|badge|pill|chip|link)\b', sel, re.I):
            continue          # gradient na przycisku to nie powierzchnia
        if not re.search(r'background(-image)?\s*:', blok):
            continue
        if not re.search(r'gradient\(|url\(|image-set\(', blok):
            continue
        wlasciwosci = [w for w in blok.split(';') if ':' in w]
        nakladka = re.search(r'inset\s*:|position\s*:\s*absolute', blok)   # .gr::before
        swatch = len(wlasciwosci) <= 2                                     # .gr-szwed
        warstwy = blok.count('gradient(') >= 2 or 'url(' in blok or 'repeating' in blok
        if not (nakladka or swatch or warstwy):
            continue
        out.update(re.findall(r'\.([a-zA-Z][\w-]+)', sel))
    return out


MATERIAL_Z_CSS = set()


def obiekt(cialo):
    """Zwraca (rodzaj, szczegoly). rodzaj = None oznacza sekcję bez obiektu."""
    kadry = re.findall(r'<(?:img|picture)\b[^>]*>', cialo)
    realne = []
    for k in kadry:
        if IKONA.search(k):
            continue
        w = re.search(r'width="(\d+)"', k)
        if w and int(w.group(1)) < 120:      # miniatura poniżej 120 px to ikonka
            continue
        realne.append(k)

    rysunki = [s for s in re.findall(r'<svg\b[^>]*', cialo) if not IKONA.search(s)]
    duze_rysunki = [s for s in rysunki
                    if re.search(r'viewBox="[^"]*\s(\d{3,})[\s"]', s)
                    or re.search(r'class="[^"]*(rys|schemat|przekroj|wykres|mapa)', s, re.I)]

    bryly = re.findall(r'<canvas\b', cialo)
    filmy = re.findall(r'<video\b', cialo)
    material = re.findall(r'class="[^"]*(?:tlo-|material|tekstura|powierzchnia)', cialo) \
        + re.findall(r'style="[^"]*background-image', cialo)
    if MATERIAL_Z_CSS:
        uzyte = {k for m in re.findall(r'class="([^"]*)"', cialo) for k in m.split()}
        material += sorted(uzyte & MATERIAL_Z_CSS)
    sterowanie = [s for s in re.findall(r'<(?:button|input|select|details)\b', cialo)]

    szczegoly = {'kadry': len(realne), 'rysunki': len(duze_rysunki),
                 'bryly': len(bryly), 'filmy': len(filmy),
                 'material': len(material), 'sterowanie': len(sterowanie)}

    if filmy:
        return 'film', szczegoly
    if bryly:
        return 'bryla', szczegoly
    if len(realne) >= 6:
        return 'siatka', szczegoly
    if duze_rysunki:
        return 'rysunek', szczegoly
    if realne:
        return 'foto', szczegoly
    if material:
        return 'material', szczegoly
    if sterowanie:
        return 'sterowanie', szczegoly
    return None, szczegoly


def odcisk(cialo):
    """Konstrukcja sekcji — czego używa, a nie co pisze. Dwie sekcje o tym samym
    odcisku wyglądają tak samo."""
    r, s = obiekt(cialo)
    ma = [r or 'TEKST', 'K%d' % min(s['kadry'], 4),
          'LI%d' % min(len(re.findall(r'<li\b', cialo)) // 3, 3),
          'H%d' % len(re.findall(r'<h[23]\b', cialo)),
          'P%d' % min(len(re.findall(r'<p\b', cialo)), 5)]
    for zn, et in (('<table', 'TAB'), ('<form', 'FRM'), ('<blockquote', 'CYT')):
        if zn in cialo:
            ma.append(et)
    return '|'.join(ma)


def typy_ruchu(cialo):
    """Zbiór typów ruchu w sekcji. data-rv rozbijamy na warianty — 'up' i 'mask'
    to różne zdarzenia, choć ten sam atrybut."""
    out = set()
    for w in re.findall(r'data-rv="([^"]*)"', cialo):
        out.add('rv:' + (w or 'up'))
    if 'data-rv' in cialo and not re.search(r'data-rv="', cialo):
        out.add('rv:up')
    for h in RUCHY[1:]:
        if h in cialo:
            out.add(h.replace('data-', ''))
    return out


# ============================================================ zbieranie danych
def zbierz(korzen):
    strony = {}
    for p in sorted(korzen.rglob('*.html')):
        if '404' in p.name:
            continue
        strony[p] = czytaj(p)
    css = ''.join(czytaj(p) for p in korzen.rglob('*.css') if 'fonts' not in p.name)
    js = ''.join(czytaj(p) for p in korzen.rglob('*.js')
                 if p.stat().st_size < 200_000)
    global MATERIAL_Z_CSS
    MATERIAL_Z_CSS = klasy_materialu(css)
    return strony, css, js


def plan_sekcji(projekt):
    """`dane/06-sekcje.tsv` — plan, wobec którego mierzymy wynik."""
    f = projekt / 'dane' / '06-sekcje.tsv'
    if not f.exists():
        return None
    wiersze = []
    for linia in czytaj(f).splitlines():
        if not linia.strip() or linia.lstrip().startswith('#'):
            continue
        kol = [c.strip() for c in linia.split('\t')]
        if kol and kol[0].lower() in ('akt', 'lp', '#'):
            continue
        wiersze.append(kol)
    return wiersze or None


# ============================================================ BEZPIECZNIKI
def bezpieczniki(strony, css, js, korzen, projekt, v2):
    """Zwraca listę (nazwa, ok, opis). Każdy wpis może zablokować build."""
    out = []
    wszystkie_sekcje = []
    for p, html in strony.items():
        for ident, cialo in sekcje(html):
            wszystkie_sekcje.append((nazwa(p, korzen), ident, cialo))

    # --- 1. sekcja bez obiektu (reguła z anti-slop.md) --------------------
    puste = []
    for strona, ident, cialo in wszystkie_sekcje:
        r, s = obiekt(cialo)
        if r is None:
            tekst = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', cialo)).strip()
            puste.append('%s/%s (%d znaków, zero obiektu)' % (strona, ident, len(tekst)))
    out.append(('sekcja niesie obiekt', not puste,
                'wszystkie %d sekcji niosą obiekt' % len(wszystkie_sekcje) if not puste
                else '%d sekcji to sam tekst: %s' % (len(puste), '; '.join(puste[:4]))))

    # --- 2. rytm rodzaju obiektu ------------------------------------------
    zle = []
    for p, html in strony.items():
        poprz = None
        for ident, cialo in sekcje(html):
            r, _ = obiekt(cialo)
            if r and r == poprz and r in ('siatka', 'rysunek', 'foto'):
                zle.append('%s/%s: drugi raz pod rząd „%s"' % (nazwa(p, korzen), ident, r))
            poprz = r
    out.append(('rytm obiektów', not zle,
                'żaden rodzaj obiektu nie powtarza się pod rząd' if not zle
                else '; '.join(zle[:4])))

    # --- 3. rytm konstrukcji ----------------------------------------------
    zle = []
    for p, html in strony.items():
        poprz, ile = None, 0
        for ident, cialo in sekcje(html):
            o = odcisk(cialo)
            ile = ile + 1 if o == poprz else 1
            poprz = o
            if ile > MAX_TEN_SAM_UKLAD:
                zle.append('%s: %d identyczne konstrukcje pod rząd' % (nazwa(p, korzen), ile))
                break
    out.append(('rytm konstrukcji', not zle,
                'żadna konstrukcja nie powtarza się więcej niż %d× pod rząd' % MAX_TEN_SAM_UKLAD
                if not zle else '; '.join(zle[:4])))

    # --- 4. koncentracja kadrów (choroba galerii-śmietnika) ---------------
    # Hormon: 73 z 79 zdjęć siedziały w jednej sekcji.
    zle = []
    for p, html in strony.items():
        sek = sekcje(html)
        licz = [obiekt(c)[1]['kadry'] for _, c in sek]
        razem = sum(licz)
        if razem >= 12 and len(sek) >= 5:
            naj = max(licz)
            if naj / razem > MAX_KADROW_W_SEKCJI:
                i = licz.index(naj)
                zle.append('%s: %d%% kadrów w sekcji „%s" (%d z %d)'
                           % (nazwa(p, korzen), round(naj / razem * 100), sek[i][0], naj, razem))
    out.append(('rozkład kadrów', not zle,
                'kadry rozłożone na sekcje (galerie o mniej niż 5 sekcjach pominięte)'
                if not zle else '; '.join(zle[:3])))

    # --- 5. dominacja jednego typu ruchu ----------------------------------
    # Zastępuje usunięty próg „≥60 % sekcji z ruchem". Tamten premiował
    # data-rv="up" na wszystkim — czyli to, czego zabrania dom.md.
    licznik, z_ruchem = {}, 0
    for _, _, cialo in wszystkie_sekcje:
        t = typy_ruchu(cialo)
        if t:
            z_ruchem += 1
            for x in t:
                licznik[x] = licznik.get(x, 0) + 1
    if z_ruchem >= MIN_SEKCJI_DO_OCENY_RUCHU:
        naj, ile = max(licznik.items(), key=lambda kv: kv[1])
        udzial = ile / z_ruchem
        out.append(('rozkład ruchu', udzial <= MAX_UDZIAL_JEDNEGO_RUCHU,
                    '„%s" pokrywa %d%% sekcji z ruchem (limit %d%%), typów: %d'
                    % (naj, round(udzial * 100), round(MAX_UDZIAL_JEDNEGO_RUCHU * 100),
                       len(licznik))))
    else:
        out.append(('rozkład ruchu', True,
                    'za mało sekcji z ruchem (%d), żeby rozkład coś znaczył' % z_ruchem))

    # --- 6. sygnatura wraca poza hero -------------------------------------
    braki = []
    for p, html in strony.items():
        sek = sekcje(html)
        if len(sek) < 3:
            continue
        poza_hero = [c for _, c in sek[1:]]
        if not any('data-sygnatura' in c for c in poza_hero):
            braki.append(nazwa(p, korzen))
    ma_deklaracje = any('data-sygnatura' in h for h in strony.values())
    if v2 or ma_deklaracje:
        out.append(('sygnatura poza hero', not braki,
                    'sygnatura wraca na każdej podstronie' if not braki
                    else 'brak na: ' + ', '.join(braki[:5])))

    # --- 7. typografia: decyzja czy przypadek -----------------------------
    czysty = bez_komentarzy(css)
    tokeny = set()
    for m in re.findall(r'--[\w-]*(?:fs|font|stopien|krok)[\w-]*\s*:\s*([^;}]+)', czysty, re.I):
        tokeny.add(re.sub(r'\s+', ' ', m.strip()))
    literaly, male = set(), set()
    for m in re.findall(r'font-size\s*:\s*([^;}]+)', czysty):
        w = re.sub(r'\s+', ' ', m.strip())
        if w.startswith('var(') or w in ('inherit', 'initial', 'unset', '1em', '100%'):
            continue
        literaly.add(w)
        px = re.match(r'^([\d.]+)px$', w)
        if px and float(px.group(1)) < MIN_PX:
            male.add(w)
    poza = literaly - tokeny
    if v2:
        if not tokeny:
            out.append(('skala typograficzna', False,
                        'skala nie została zadeklarowana — brak tokenów --fs-*; '
                        '%d wartości font-size rozsypanych po CSS' % len(literaly)))
        else:
            out.append(('skala typograficzna', not poza and not male,
                        '%d tokenów, wszystkie wartości w systemie' % len(tokeny)
                        if not poza and not male else
                        'poza systemem: %s%s' % (', '.join(sorted(poza)[:6]),
                                                 '; poniżej %dpx: %s' % (MIN_PX, ', '.join(sorted(male)))
                                                 if male else '')))
    out.append(('czytelność (min %dpx)' % MIN_PX, not male,
                'nic poniżej %d px' % MIN_PX if not male
                else 'za małe: ' + ', '.join(sorted(male))))

    # --- 8. bezpieczniki ruchu --------------------------------------------
    braki = []
    if 'prefers-reduced-motion' not in czysty and 'prefers-reduced-motion' not in js:
        braki.append('prefers-reduced-motion')
    if 'static=1' not in js:
        braki.append('?static=1')
    if not re.search(r'classList\.add\(\s*[\'"](ruch|js|loaded)', js):
        braki.append('bramka JS')
    out.append(('bezpieczniki ruchu', not braki,
                'reduced-motion, static=1, bramka JS' if not braki
                else 'brakuje: ' + ', '.join(braki)))

    # --- 9. hero mówi czym firma wygrywa ----------------------------------
    html = strony.get(korzen / 'index.html', '')
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, flags=re.S)
    if not m:
        out.append(('nagłówek hero', False, 'brak H1 na stronie głównej'))
    else:
        tekst = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()
        puste_frazy = ('kompleksow', 'najwyższej jakości', 'profesjonaliz', 'z pasją',
                       'indywidualne podejście', 'zapraszamy', 'bogata oferta',
                       'wieloletnie doświadczenie', 'zadowolenie klienta')
        zlapane = [f for f in puste_frazy if f in tekst.lower()]
        out.append(('nagłówek hero', not zlapane,
                    '„%s"' % (tekst[:64] + ('…' if len(tekst) > 64 else ''))
                    + ('' if not zlapane else ' — puste frazy: ' + ', '.join(zlapane))))

    # --- 10. mobile: przewrotka kolumnowa ---------------------------------
    plan = plan_sekcji(projekt)
    if plan:
        kol = [w[4].lower() if len(w) > 4 else '' for w in plan]
        te_same = sum(1 for k in kol if k.startswith('ta-sama'))
        osobne = sum(1 for k in kol if k.startswith(('inna', 'tylko-mobil', 'pominieta')))
        udzial = te_same / len(kol) if kol else 0
        out.append(('mobile jako kompozycja', udzial <= MAX_PRZEWROTEK and osobne >= 1,
                    '%d z %d sekcji ma osobną kompozycję na telefonie'
                    % (osobne, len(kol))))
    elif v2:
        out.append(('mobile jako kompozycja', False,
                    'brak kolumny „mobil" w dane/06-sekcje.tsv'))

    # --- 11. research dotarł do kierunku ----------------------------------
    if v2:
        f = projekt / 'dane' / '04-kierunek.md'
        if not f.exists():
            out.append(('kierunek cytuje wnioski', False, 'brak dane/04-kierunek.md'))
        else:
            tresc = czytaj(f)
            decyzje = [l for l in tresc.splitlines()
                       if l.strip().startswith(('-', '*', '|')) and len(l.strip()) > 12
                       and not l.strip().startswith('|--')]
            bez = [l for l in decyzje if not re.search(r'\bW[1-9]\b', l)]
            out.append(('kierunek cytuje wnioski', not bez,
                        'wszystkie %d decyzji cytuje wniosek' % len(decyzje) if not bez
                        else '%d decyzji bez numeru wniosku (pierwsza: %s…)'
                             % (len(bez), bez[0].strip()[:50])))

    return out


# ============================================================ KOMPASY
def kompasy(strony, css, js, korzen, projekt):
    out = []
    wszystkie = [(p, ident, c) for p, html in strony.items() for ident, c in sekcje(html)]
    n = len(wszystkie) or 1

    z_ruchem = sum(1 for _, _, c in wszystkie if typy_ruchu(c))
    out.append(('udział sekcji z ruchem', '%d%% (%d z %d)'
                % (round(z_ruchem / n * 100), z_ruchem, n), z_ruchem / n))

    licznik = {}
    for _, _, c in wszystkie:
        for t in typy_ruchu(c):
            licznik[t] = licznik.get(t, 0) + 1
    opis = ', '.join('%s×%d' % (k, v) for k, v in
                     sorted(licznik.items(), key=lambda kv: -kv[1])[:5]) or 'brak'
    out.append(('rozkład typów ruchu', opis, len(licznik)))

    glowna = korzen / 'index.html'
    if glowna in strony:
        sek = sekcje(strony[glowna])
        profil = []
        for _, c in sek:
            s = obiekt(c)[1]
            waga = s['kadry'] * 3 + s['bryly'] * 6 + s['filmy'] * 6 + s['rysunki'] * 2 + s['material']
            tekst = len(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', c)))
            profil.append(round(waga * 400 / max(tekst, 400)))
        out.append(('profil mediów przez scroll', ' / '.join(str(x) for x in profil), profil))

    kadry = sum(obiekt(c)[1]['kadry'] for _, _, c in wszystkie)
    naj = max((obiekt(c)[1]['kadry'] for _, _, c in wszystkie), default=0)
    out.append(('koncentracja kadrów', '%d kadrów, najwięcej w jednej sekcji: %d (%d%%)'
                % (kadry, naj, round(naj / kadry * 100) if kadry else 0),
                naj / kadry if kadry else 0))

    if glowna in strony:
        baza = set(re.findall(r'class="([^"]*)"', strony[glowna]))
        bazak = set(k for m in baza for k in m.split() if k)
        pula = set()
        ile = 0
        for p, html in strony.items():
            if p == glowna or any(u in p.as_posix().lower() for u in UZYTKOWE):
                continue
            pula |= set(k for m in re.findall(r'class="([^"]*)"', html) for k in m.split() if k)
            ile += 1
        if ile and bazak:
            r = len(pula) / len(bazak)
            out.append(('bogactwo podstron', '%.2f (próg orientacyjny %.2f)'
                        % (r, PROG_SLOWNICTWA), r))

    czysty = bez_komentarzy(css)
    tok = len(set(re.findall(r'--[\w-]*(?:fs|font|stopien|krok)[\w-]*\s*:', czysty, re.I)))
    lit = len(set(re.findall(r'font-size\s*:\s*(?!var\()([^;}]+)', czysty)))
    out.append(('tokeny typograficzne', '%d zadeklarowanych, %d literałów' % (tok, lit), tok))

    out.append(('mikro-ruch', '%d deklaracji transition: (%.1f na sekcję)'
                % (len(re.findall(r'transition\s*:', czysty)),
                   len(re.findall(r'transition\s*:', czysty)) / n),
                len(re.findall(r'transition\s*:', czysty)) / n))
    return out


# ============================================================ odcisk projektu
def kroje(czysty):
    """Nazwy krojów, nie stosy zapasowe. Nasze projekty trzymają kroje w zmiennych
    (`font-family: var(--serif)`), więc samo czytanie `font-family` dawało „var"
    w każdym projekcie — i 100 % wspólnych krojów każdego z każdym."""
    nazwy = set(re.findall(r"['\"]([A-Z][\w][\w .-]{2,28})['\"]", czysty))
    nazwy |= set(re.findall(r'font-family\s*:\s*([A-Z][\w ]{2,28})', czysty))
    return sorted({n.strip() for n in nazwy} - GENERYCZNE)[:6]


def akcenty(czysty):
    """Kolor akcentu. Najpierw zmienne nazwane wprost, potem — gdy projekt nazywa
    akcent znaczeniowo (`--patyna`, `--mosiadz`) — barwne heksy spoza skali szarości."""
    nazwane = re.findall(
        r'--[\w-]*(?:akcent|accent|patyn|zlot|gold|mosiadz|brass|miedz|copper)[\w-]*\s*:\s*([^;}]+)',
        czysty, re.I)
    if nazwane:
        return sorted({w.strip().lower() for w in nazwane})[:3]
    barwne = []
    for h in set(re.findall(r'--[\w-]+\s*:\s*(#[0-9a-fA-F]{6})', czysty)):
        r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
        if max(r, g, b) - min(r, g, b) > 40:      # poza skalą szarości
            barwne.append(h.lower())
    return sorted(barwne)[:3]


def odcisk_projektu(strony, css, korzen):
    """Do _wzorce/indeks.json — karmi podobienstwo.py."""
    glowna = strony.get(korzen / 'index.html', '')
    czysty = bez_komentarzy(css)
    return {
        'sekcje': [odcisk(c) for _, c in sekcje(glowna)],
        'obiekty': [obiekt(c)[0] or 'TEKST' for _, c in sekcje(glowna)],
        'ruch': sorted({t for _, c in sekcje(glowna) for t in typy_ruchu(c)}),
        'kroje': kroje(czysty),
        'kolory': akcenty(czysty),
        'hero': (odcisk(sekcje(glowna)[0][1]) if sekcje(glowna) else ''),
        'stron': len(strony),
    }


# ============================================================ przebieg
def zbadaj(baza, cicho=False, zapisz=False):
    korzen = znajdz_wynik(baza)
    if not korzen:
        if not cicho:
            print('  Nie znalazłem zbudowanej strony w %s' % baza)
        return None
    strony, css, js = zbierz(korzen)
    if not strony:
        return None

    projekt = korzen.parent if korzen.name in KATALOGI_WYNIKU else korzen
    v2 = (projekt / 'dane').is_dir()

    bez = bezpieczniki(strony, css, js, korzen, projekt, v2)
    kom = kompasy(strony, css, js, korzen, projekt)

    if zapisz and not ORYGINAL:
        print('  --zapisz dziala tylko z _wzorce/audyt/audyt.py. '
              'Uruchamiasz kopie z migawki - indeks zostalby zapisany obok oryginalu.')
        zapisz = False
    if zapisz:
        dane = json.loads(czytaj(INDEKS) or '{}') if INDEKS.exists() else {}
        dane[projekt.name] = odcisk_projektu(strony, css, korzen)
        INDEKS.write_text(json.dumps(dane, ensure_ascii=False, indent=1), encoding='utf-8')

    if not cicho:
        print('\n  %s — %d stron, %d sekcji, tryb %s'
              % (projekt.name.upper(), len(strony),
                 sum(len(sekcje(h)) for h in strony.values()), 'V2' if v2 else 'zastany'))
        print('  ' + '=' * 74)
        print('  BEZPIECZNIKI — blokują build')
        for n_, ok, opis in bez:
            print('   %s %-26s %s' % ('  OK  ' if ok else 'BLOKADA', n_, opis))
        print('\n  KOMPASY — nie blokują, pokazują dryf')
        for n_, opis, _ in kom:
            print('   %-28s %s' % (n_, opis))
        zle = [n_ for n_, ok, _ in bez if not ok]
        print('  ' + '=' * 74)
        print('  %s\n' % ('BRAMKA OTWARTA' if not zle
                          else 'BRAMKA ZAMKNIĘTA — ' + ', '.join(zle)))
    return bez, kom


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--wszystkie' in sys.argv:
        baza = Path(__file__).resolve().parents[2]
        print('\n  %-16s %s' % ('PROJEKT', 'zamknięte bezpieczniki'))
        print('  ' + '-' * 74)
        razem = 0
        for d in sorted(p for p in baza.iterdir() if p.is_dir() and not p.name.startswith('_')):
            w = zbadaj(d, cicho=True, zapisz='--zapisz' in sys.argv)
            if not w:
                continue
            zle = [n for n, ok, _ in w[0] if not ok]
            razem += len(zle)
            print('  %-16s %s' % (d.name, ', '.join(zle) if zle else 'wszystko otwarte'))
        print('  ' + '-' * 74)
        print('  Razem zamkniętych bezpieczników: %d\n' % razem)
        return 0

    w = zbadaj(Path(args[0]).resolve() if args else Path.cwd(),
               zapisz='--zapisz' in sys.argv)
    if w is None:
        return 2
    return 1 if any(not ok for _, ok, _ in w[0]) else 0


if __name__ == '__main__':
    raise SystemExit(main())
