# -*- coding: utf-8 -*-
"""podobienstwo.py — czy ta strona to już nie jest nasza poprzednia strona.

Powód istnienia: mamy dziewięć konceptów („Dwa kamienie", „Lapidarium", „Kronika",
„Kamień i światło", „Nokturn", „Plac z płytami", „Korona", „Monolit", „Regestr")
i wszystkie zbiegają się do jednego domowego stylu. Nic tego nie mierzyło.

Trzy osie:
  A. wobec naszych własnych projektów   — z `_wzorce/indeks.json`
  B. wobec typowych szablonów Webflow/WP — sygnatury układów wykrywalne w HTML
  C. wobec konkurencji klienta           — z `dane/01-fakty.json`, jeśli research je zebrał

Oś D („zdejmij logo") nie da się policzyć — robi ją agent `js-krytyk-designu`
na zrzutach z podmienionymi nazwami.

    python _wzorce/audyt/podobienstwo.py lewartowski
    python _wzorce/audyt/podobienstwo.py --wszystkie      # macierz całej pracowni

Kod wyjścia 1, gdy padł bezpiecznik.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audyt import (INDEKS, czytaj, klasy_materialu, obiekt, odcisk,  # noqa: E402
                   sekcje, znajdz_wynik, zbierz)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

# ---- progi ---------------------------------------------------------------
PROG_SEKWENCJI   = 0.60   # podobieństwo ciągu konstrukcji — bezpiecznik
PROG_OSTRZEZENIA = 0.45   # niżej: tylko sygnał
MAX_POWTORZEN    = 2      # ile z pięciu cech może wrócić z ostatnich trzech projektów

CECHY = ('kroje', 'kolory', 'hero', 'ruch', 'obiekty')


def podobne(a, b):
    return SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def odcien(h):
    """Barwa 0-360 z heksa; None dla szarości."""
    h = h.strip().lstrip('#')
    if len(h) != 6:
        return None
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return None
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 0.12:
        return None
    if mx == r:
        k = (60 * ((g - b) / (mx - mn)) + 360) % 360
    elif mx == g:
        k = 60 * ((b - r) / (mx - mn)) + 120
    else:
        k = 60 * ((r - g) / (mx - mn)) + 240
    return k


def bliskie_akcenty(a, b, prog=22):
    """Jaccard na heksach nie łapie tego, co widać gołym okiem: #9a7f5c, #8c6f46
    i #8f6247 to dla zbiorów trzy różne wartości, a dla oka ten sam ciepły brąz."""
    for x in a:
        hx = odcien(x)
        if hx is None:
            continue
        for y in b:
            hy = odcien(y)
            if hy is None:
                continue
            d = abs(hx - hy)
            if min(d, 360 - d) <= prog:
                return True
    return False


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a or b) else 0.0


# ============================================================ OŚ A
def wobec_naszych(nazwa_projektu, indeks):
    """Zwraca (bezpieczniki, raport)."""
    ja = indeks.get(nazwa_projektu)
    if not ja:
        return [], ['  Projektu nie ma w indeksie — uruchom: audyt.py %s --zapisz'
                    % nazwa_projektu]

    inne = [(k, v) for k, v in indeks.items() if k != nazwa_projektu]
    if not inne:
        return [], ['  Indeks ma tylko ten projekt — nie ma z czym porównać.']

    wiersze, najblizszy, najwyzsze = [], None, 0.0
    for k, v in inne:
        s_sek = podobne(ja['sekcje'], v['sekcje'])
        s_obj = podobne(ja['obiekty'], v['obiekty'])
        s_krj = jaccard(ja['kroje'], v['kroje'])
        s_ruch = jaccard(ja['ruch'], v['ruch'])
        s_hero = 1.0 if ja['hero'] and ja['hero'] == v['hero'] else 0.0
        s_akc = 1.0 if bliskie_akcenty(ja.get('kolory', []), v.get('kolory', [])) else 0.0
        wiersze.append((s_sek, k, s_obj, s_krj, s_ruch, s_hero, s_akc))
        if s_sek > najwyzsze:
            najwyzsze, najblizszy = s_sek, k

    wiersze.sort(reverse=True)
    raport = ['  %-16s %7s %7s %7s %7s %6s %7s' %
              ('PROJEKT', 'ukladu', 'obiekt', 'kroje', 'ruch', 'hero', 'akcent')]
    for s_sek, k, s_obj, s_krj, s_ruch, s_hero, s_akc in wiersze[:6]:
        raport.append('  %-16s %6.0f%% %6.0f%% %6.0f%% %6.0f%% %6s %7s'
                      % (k, s_sek * 100, s_obj * 100, s_krj * 100, s_ruch * 100,
                         'TEN SAM' if s_hero else '—',
                         'BLISKI' if s_akc else '—'))

    bezp = [('powtórzenie układu', najwyzsze <= PROG_SEKWENCJI,
             'najbliższy projekt „%s" — %.0f%% wspólnej sekwencji konstrukcji (limit %.0f%%)'
             % (najblizszy, najwyzsze * 100, PROG_SEKWENCJI * 100))]

    # budżet powtórzeń wobec trzech ostatnich
    ostatnie = [v for k, v in list(indeks.items())[-4:] if k != nazwa_projektu][-3:]
    powtorzone = []
    for cecha in CECHY:
        for v in ostatnie:
            if cecha == 'kolory':
                if bliskie_akcenty(ja.get('kolory', []), v.get('kolory', [])):
                    powtorzone.append(cecha)
                    break
            elif cecha in ('kroje', 'ruch'):
                if jaccard(ja.get(cecha, []), v.get(cecha, [])) >= 0.6:
                    powtorzone.append(cecha)
                    break
            elif cecha == 'hero':
                if ja.get('hero') and ja['hero'] == v.get('hero'):
                    powtorzone.append(cecha)
                    break
            elif podobne(ja.get(cecha, []), v.get(cecha, [])) >= 0.7:
                powtorzone.append(cecha)
                break
    bezp.append(('budżet powtórzeń', len(powtorzone) <= MAX_POWTORZEN,
                 '%d z %d cech wraca z ostatnich trzech projektów (limit %d)%s'
                 % (len(powtorzone), len(CECHY), MAX_POWTORZEN,
                    ': ' + ', '.join(powtorzone) if powtorzone else '')))
    return bezp, raport


# ============================================================ OŚ B
# Sygnatury z anti-slop.md, przełożone na coś, co da się wykryć w HTML.
def wobec_szablonow(strony):
    zlapane = []
    for p, html in strony.items():
        sek = sekcje(html)
        if not sek:
            continue

        # hero wycentrowany z dwoma przyciskami obok siebie
        hero = sek[0][1]
        if re.search(r'text-align:\s*center|class="[^"]*(center|srodek|hero--c)', hero) \
                and len(re.findall(r'class="[^"]*btn', hero)) >= 2:
            zlapane.append('%s: hero wycentrowany + dwa przyciski' % p.parent.name)

        # trzy równe karty z ikoną
        for ident, cialo in sek:
            karty = re.findall(r'class="[^"]*\bcard\b[^"]*"', cialo)
            if len(karty) == 3 and len(re.findall(r'<svg', cialo)) >= 3:
                zlapane.append('%s/%s: trzy równe karty z ikoną' % (p.parent.name, ident))

        # naprzemienne tekst-lewo / obraz-prawo dłużej niż dwa razy
        ciag, poprz = 0, None
        for ident, cialo in sek:
            r, s = obiekt(cialo)
            wzor = (r == 'foto' and s['kadry'] in (1, 2)
                    and len(re.findall(r'<p\b', cialo)) >= 2)
            if wzor and poprz:
                ciag += 1
                if ciag > 2:
                    zlapane.append('%s: %d naprzemiennych bloków tekst/obraz'
                                   % (p.parent.name, ciag + 1))
                    break
            else:
                ciag = 0
            poprz = wzor

        # karuzela opinii i pasek liczników
        if re.search(r'class="[^"]*(karuzel|carousel|slider|opinie__s)', html) \
                and re.search(r'★|gwiazd|rating|opinia', html, re.I):
            zlapane.append('%s: karuzela opinii' % p.parent.name)

    zlapane = sorted(set(zlapane))
    return [('sygnatury szablonu', not zlapane,
             'brak układów z czerwonej listy' if not zlapane
             else '; '.join(zlapane[:4]))], []


# ============================================================ OŚ C
def wobec_konkurencji(projekt):
    f = projekt / 'dane' / '01-fakty.json'
    if not f.exists():
        return [], []
    try:
        dane = json.loads(czytaj(f))
    except json.JSONDecodeError:
        return [], ['  dane/01-fakty.json nie jest poprawnym JSON-em']
    konk = dane.get('konkurencja', [])
    if not konk:
        return [], ['  Research nie zebrał układów konkurencji (pole „konkurencja").']
    opisy = ['  %s — %s / %s' % (k.get('nazwa', '?'), k.get('uklad', '?'), k.get('paleta', '?'))
             for k in konk[:5]]
    return [], ['  Konkurencja wg researchu:'] + opisy + \
        ['  Koncept musi różnić się od nich na co najmniej dwóch osiach '
         '(układ, paleta, typografia, nośnik, ruch) — sprawdź dane/03-koncept.md.']


# ============================================================ przebieg
def zbadaj(baza, cicho=False):
    korzen = znajdz_wynik(baza)
    if not korzen:
        return None
    strony, css, js = zbierz(korzen)
    projekt = korzen.parent if korzen.name != baza.name else baza
    indeks = json.loads(czytaj(INDEKS)) if INDEKS.exists() else {}

    b1, r1 = wobec_naszych(projekt.name, indeks)
    b2, _ = wobec_szablonow(strony)
    b3, r3 = wobec_konkurencji(projekt)
    bezp = b1 + b2 + b3

    if not cicho:
        print('\n  PODOBIEŃSTWO — %s' % projekt.name.upper())
        print('  ' + '=' * 74)
        for n, ok, opis in bezp:
            print('   %s %-24s %s' % ('  OK  ' if ok else 'BLOKADA', n, opis))
        if r1:
            print('\n  Odległość od naszych projektów:')
            print('\n'.join(r1))
        if r3:
            print()
            print('\n'.join(r3))
        print('  ' + '=' * 74)
        zle = [n for n, ok, _ in bezp if not ok]
        print('  %s\n' % ('BEZ POWTÓRZEŃ' if not zle else 'POWTARZAMY SIĘ — ' + ', '.join(zle)))
    return bezp


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--wszystkie' in sys.argv:
        indeks = json.loads(czytaj(INDEKS)) if INDEKS.exists() else {}
        klucze = sorted(indeks)
        if len(klucze) < 2:
            print('Indeks pusty. Uruchom: python _wzorce/audyt/audyt.py --wszystkie --zapisz')
            return 2
        print('\n  MACIERZ PODOBIEŃSTWA UKŁADU (%% wspólnej sekwencji konstrukcji)\n')
        print('  %-15s %s' % ('', ' '.join('%5s' % k[:5] for k in klucze)))
        gorace = []
        for a in klucze:
            rzad = []
            for b in klucze:
                v = 0 if a == b else podobne(indeks[a]['sekcje'], indeks[b]['sekcje'])
                rzad.append('%4.0f%%' % (v * 100) if a != b else '    —')
                if a < b and v > PROG_OSTRZEZENIA:
                    gorace.append((v, a, b))
            print('  %-15s %s' % (a[:15], ' '.join(rzad)))
        print()
        for v, a, b in sorted(gorace, reverse=True)[:8]:
            znak = 'BLOKADA' if v > PROG_SEKWENCJI else 'uwaga  '
            print('  %s %s ↔ %s: %.0f%%' % (znak, a, b, v * 100))
        print()
        return 0

    w = zbadaj(Path(args[0]).resolve() if args else Path.cwd())
    if w is None:
        print('Nie znalazłem zbudowanej strony.')
        return 2
    return 1 if any(not ok for _, ok, _ in w) else 0


if __name__ == '__main__':
    raise SystemExit(main())
