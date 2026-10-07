# -*- coding: utf-8 -*-
"""AKWIFER v2 „ZLECENIE” — strona wzorcowa zawodu „studnie głębinowe”. Firma fikcyjna, dane gmin prawdziwe.

    python fonts.py     # raz
    python images.py    # po wrzuceniu obrazów do zrodla/gen/ (bez nich: plansze zastępcze)
    python build.py     # zawsze — na końcu bramka audyt.py

Dane: content.py + dane/00-gminy-pig.json. Paleta i skala: brand.py. CSS/JS: src/. Plan: dane/01–07.
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import brand
from content import FIRMA as F, GMINY, SREDNIA_POWIATU, ZRODLO_PIG, RYNEK, ZUZYCIE_OS, CELE, ETAPY, PASZPORT
from content import WODOCIAG, PRAD_M3, OGROD, BEZ_DANYCH, GWARANCJA, PAKIETY, ABOLICJA, NIZOWKA
import datetime

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
WZORCE = ROOT / '_pracownia' / '_wzorce'
if not WZORCE.exists():
    WZORCE = ROOT.parent / '_wzorce'

BRAK = [f for f in ('03-koncept.md', '04-kierunek.md', '05-podroz.md', '06-sekcje.tsv')
        if not (ROOT / 'dane' / f).exists()]
if BRAK:
    raise SystemExit('Brak artefaktów: %s — patrz pipeline.md' % ', '.join(BRAK))

BASE = 'https://akwifer.jurczakstudio.pl'
DEMO = True
e = html.escape
MANP = SITE / 'assets/img/w/manifest.json'
MAN = json.loads(MANP.read_text(encoding='utf-8')) if MANP.exists() else {}
PO_SLUGU = {g['slug']: g for g in GMINY}

STRZALKA = ('<svg class="ikona" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
SMS = ('<svg class="ikona" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" '
       'stroke-width="1.8" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg>')


def pl(x, d=0):
    s = ('%.*f' % (d, x)).replace('.', ',')
    return s


def zl(x):
    return '{:,}'.format(int(round(x / 100) * 100)).replace(',', ' ')


def split(*wiersze, tag='h2'):
    return '<%s data-rv="split">%s</%s>' % (tag, ' '.join('<span class="w"><i>%s</i></span>' % w for w in wiersze), tag)


def notka(tekst):
    """Notka „Oczami właściciela” — widoczna tylko w trybie właściciela (W5)."""
    return ('<aside class="notka" data-notka><p class="notka__t mono">oczami właściciela</p><p>%s</p></aside>' % tekst)


# ---------------------------------------------------------------- wycena (to samo w site.js)
def wycena(g, cel='dom', osoby=4):
    mnoz = dict((k, m) for k, _, m in CELE)[cel]
    lo, hi = g['min'], max(g['mediana'], g['min'])
    koszt = (lo * RYNEK['mb'][0] + RYNEK['osprzet'][0], hi * RYNEK['mb'][1] + RYNEK['osprzet'][1])
    if hi <= 30:
        formal = ('zwykle bez zgłoszeń', 'połowa otworów w gminie jest płytsza niż %s m — studnia domowa zwykle mieści się w 30 m' % pl(g['mediana'], 1 if g['mediana'] % 1 else 0))
    elif lo > 30:
        formal = ('prawie na pewno ponad 30 m', 'nawet najpłytsze ujęcie w rejestrze ma %s m — potrzebny projekt robót geologicznych; przygotowujemy go' % pl(lo, 1 if lo % 1 else 0))
    else:
        formal = ('zależy od działki', 'najpłytsze ujęcia mieszczą się w 30 m, ale połowa otworów jest głębsza — jeśli przekroczymy 30 m, papiery są po naszej stronie')
    zuz = osoby * ZUZYCIE_OS * mnoz
    return {'lo': lo, 'hi': hi, 'koszt': koszt, 'formal': formal, 'zuzycie': zuz}


def metry(x):
    return pl(x, 1 if x % 1 else 0)


# ---------------------------------------------------------------- obrazy
def plansza_hero():
    """Plansza zastępcza (wektor) do czasu kadru z Higgsfield — zmierzch, pole, dom w stanie surowym, wiertnica z lampami."""
    topole = ''.join('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#0b1013"/>' % (x, 560 - h // 2, w, h // 2)
                     for x, w, h in [(90, 14, 120), (130, 12, 104), (168, 15, 128), (205, 11, 96), (238, 13, 118),
                                     (1190, 13, 110), (1228, 15, 126), (1268, 12, 98), (1302, 14, 116)])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1a2a"/><stop offset=".45" stop-color="#1d3346"/><stop offset=".62" stop-color="#7a5a4a"/><stop offset=".68" stop-color="#c98a55"/></linearGradient>
<linearGradient id="z" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151b18"/><stop offset="1" stop-color="#07090a"/></linearGradient>
<radialGradient id="l" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd7a3" stop-opacity=".95"/><stop offset=".25" stop-color="#ff9a4d" stop-opacity=".45"/><stop offset="1" stop-color="#ff6b2c" stop-opacity="0"/></radialGradient>
<linearGradient id="m" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb3c2" stop-opacity="0"/><stop offset=".5" stop-color="#9fb3c2" stop-opacity=".18"/><stop offset="1" stop-color="#9fb3c2" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1600" height="620" fill="url(#n)"/>
{topole}
<rect x="0" y="555" width="1600" height="345" fill="url(#z)"/>
<rect x="0" y="520" width="1600" height="90" fill="url(#m)"/>
<g fill="#0d1215"><rect x="760" y="430" width="250" height="132"/><polygon points="745,432 885,372 1025,432"/></g>
<g fill="#1a2126"><rect x="790" y="470" width="34" height="46"/><rect x="860" y="470" width="34" height="46"/><rect x="935" y="470" width="34" height="46"/></g>
<g fill="#121719"><rect x="1080" y="560" width="230" height="34" rx="4"/><circle cx="1120" cy="600" r="16"/><circle cx="1270" cy="600" r="16"/>
<rect x="1150" y="300" width="20" height="262"/><rect x="1140" y="292" width="40" height="16"/><polygon points="1150,560 1110,560 1150,470"/>
<rect x="1240" y="520" width="90" height="42" rx="3"/></g>
<line x1="1160" y1="300" x2="1160" y2="560" stroke="#ff6b2c" stroke-width="3" opacity=".7"/>
<circle cx="1186" cy="330" r="90" fill="url(#l)"/><circle cx="1186" cy="330" r="5" fill="#fff1dc"/>
<circle cx="1300" cy="525" r="70" fill="url(#l)"/><circle cx="1300" cy="525" r="4" fill="#fff1dc"/>
<path d="M0 640 Q 400 610 800 650 T 1600 630 L1600 900 L0 900Z" fill="#0a0e10" opacity=".7"/>
</svg>'''


def plansza_woda():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" preserveAspectRatio="xMidYMid slice">
<defs><radialGradient id="t" cx=".55" cy=".35" r=".8"><stop offset="0" stop-color="#2b3a42"/><stop offset="1" stop-color="#0b1013"/></radialGradient>
<linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe6ef" stop-opacity=".85"/><stop offset="1" stop-color="#5aa9bd" stop-opacity=".55"/></linearGradient>
<radialGradient id="s" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd9a8" stop-opacity=".8"/><stop offset="1" stop-color="#ff6b2c" stop-opacity="0"/></radialGradient></defs>
<rect width="800" height="1000" fill="url(#t)"/><circle cx="560" cy="300" r="260" fill="url(#s)"/>
<rect x="388" y="0" width="34" height="250" fill="#14191c"/><rect x="380" y="240" width="60" height="26" rx="6" fill="#c9a25a"/>
<path d="M405 266 C 404 420 402 560 400 640" stroke="#cfeef5" stroke-width="9" opacity=".75" fill="none"/>
<path d="M300 560 L500 560 L478 900 L322 900 Z" fill="#ffffff" fill-opacity=".08" stroke="#e9f3f6" stroke-opacity=".55" stroke-width="3"/>
<path d="M311 700 L489 700 L478 900 L322 900 Z" fill="url(#w)"/>
<ellipse cx="400" cy="700" rx="89" ry="10" fill="#e8f7fb" opacity=".6"/>
</svg>'''


def obraz(slug, plansza, alt, sizes, cls='', eager=False, media=None):
    """Zdjęcie z manifestu, a gdy go jeszcze nie ma — plansza zastępcza SVG (W5)."""
    lad = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    if slug in MAN:
        m = MAN[slug]
        w = m['w'][-1]
        zr = ''
        if media and media[0] in MAN:
            mm = MAN[media[0]]
            zr = '<source media="%s" srcset="%s" sizes="100vw">' % (media[1], ', '.join('/assets/img/w/%s-%d.webp %dw' % (media[0], x, x) for x in mm['w']))
        return ('<picture>%s<img src="/assets/img/w/%s-%d.webp" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s" class="%s"%s></picture>'
                % (zr, slug, m['w'][min(1, len(m['w']) - 1)], ', '.join('/assets/img/w/%s-%d.webp %dw' % (slug, x, x) for x in m['w']),
                   sizes, w, round(w * m['ratio']), e(alt), cls, lad))
    w, h = (1600, 900) if plansza == 'hero' else (800, 1000)
    return '<img src="/assets/img/plansza-%s.svg" width="%d" height="%d" alt="%s" class="%s plansza"%s>' % (plansza, w, h, e(alt), cls, lad)


# ---------------------------------------------------------------- komponenty
def karta(prefill=None, id_='k', tryb='pelna'):
    """Karta zlecenia — sygnatura (W4). Wartości liczone też tutaj, żeby bez JS karta nie była pusta."""
    g = PO_SLUGU[prefill] if prefill else PO_SLUGU['mosina']
    w = wycena(g)
    opcje = ''.join('<option value="%s"%s>%s</option>' % (x['slug'], ' selected' if x['slug'] == g['slug'] else '', e(x['nazwa']))
                    for x in sorted(GMINY, key=lambda x: x['nazwa']))
    cele = ''.join('<label class="karta__cel"><input type="radio" name="%s-cel" value="%s"%s><span>%s</span></label>'
                   % (id_, k, ' checked' if k == 'dom' else '', e(n)) for k, n, _ in CELE)
    return f'''<form class="karta karta--{tryb}" data-karta data-sygnatura="karta"{' data-gmina-stala="%s"' % prefill if prefill else ''} aria-labelledby="{id_}-t" onsubmit="return false">
<div class="karta__glowa"><p class="karta__nr mono" id="{id_}-t">karta zlecenia</p><p class="karta__info mono">przelicza się na żywo</p></div>
<div class="karta__pola">
<label class="karta__pole"><span>Gmina działki</span><select name="gmina" data-gmina>{opcje}</select></label>
<fieldset class="karta__pole karta__cele"><legend>Na co woda</legend>{cele}</fieldset>
<label class="karta__pole karta__osoby"><span>Osób w domu</span><input name="osoby" type="number" min="1" max="12" value="4" inputmode="numeric" data-osoby></label>
</div>
<dl class="karta__rubryki">
<div><dt>metrów</dt><dd class="mono" data-r-m>{metry(w['lo'])}–{metry(w['hi'])}</dd><small data-r-m2>od najpłytszego ujęcia do mediany w gminie</small></div>
<div><dt>złotych</dt><dd class="mono" data-r-zl>{zl(w['koszt'][0])}–{zl(w['koszt'][1])}</dd><small>wiercenie {RYNEK['mb'][0]}–{RYNEK['mb'][1]} zł/m + pompa i hydrofor</small></div>
<div><dt>formalności</dt><dd data-r-f>{e(w['formal'][0])}</dd><small data-r-f2>{e(w['formal'][1])}</small></div>
<div><dt>termin</dt><dd class="mono" data-r-t>{e(F['termin'])}</dd><small>przykład — firma wpisuje sama</small></div>
</dl>
<p class="karta__zuzycie mono" data-r-z>zużycie ok. {pl(w['zuzycie'], 1)} m³/dobę · limit bez pozwolenia: 5 m³/dobę</p>
<div class="karta__akcje"><a class="btn btn--sygnal" href="sms:{F['tel_e164']}" data-sms>{SMS}<span>Wyślij kartę SMS-em</span></a><button class="btn" type="button" data-kopiuj>Skopiuj</button></div>
<p class="karta__zrodlo">Metry: {e(ZRODLO_PIG)} — rejestr obejmuje głównie studnie komunalne i zakładowe, więc górna granica bywa zawyżona. Złotówki: średnie rynkowe (kb.pl, 08.2026), nie cennik firmy.</p>
</form>'''


def wykres(akt=None, id_='w'):
    """14 gmin: pas od najpłytszego ujęcia do mediany, linia 30 m, średnia powiatu. Wiersze linkują do podstron (W2)."""
    gm = sorted(GMINY, key=lambda g: g['mediana'])
    W, L, wiersz, top = 760, 170, 34, 46
    sx = (W - L - 30) / 120
    H = top + len(gm) * wiersz + 30
    o = ['<svg class="wykres" viewBox="0 0 %d %d" role="img" aria-label="Głębokość studni w 14 gminach powiatu poznańskiego: %s">'
         % (W, H, e('; '.join('%s od %s do %s m' % (g['nazwa'], metry(g['min']), metry(g['mediana'])) for g in gm)))]
    for m in range(0, 121, 20):
        x = L + m * sx
        o.append('<line class="w__siatka" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/><text class="w__m" x="%.1f" y="%d">%d m</text>' % (x, x, top - 10, H - 24, x, H - 6, m))
    x30 = L + 30 * sx
    o.append('<line class="w__30" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/><text class="w__30t" x="%.1f" y="%d">30 m — granica formalności</text>' % (x30, x30, top - 22, H - 24, x30 + 6, top - 26))
    xs = L + SREDNIA_POWIATU * sx
    o.append('<line class="w__sr" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (xs, xs, top - 10, H - 24))
    for i, g in enumerate(gm):
        y = top + i * wiersz
        cls = ' w__wiersz--akt' if g['slug'] == akt else ''
        o.append('<a href="/gmina/%s/" class="w__wiersz%s" data-rv="up"><rect class="w__tlo" x="0" y="%d" width="%d" height="%d"/>'
                 '<text class="w__n" x="0" y="%d">%s</text>'
                 '<rect class="w__pas" x="%.1f" y="%d" width="%.1f" height="12" rx="6"/>'
                 '<circle class="w__med" cx="%.1f" cy="%d" r="6"/><text class="w__v" x="%.1f" y="%d">%s m</text></a>'
                 % (g['slug'], cls, y - 4, W, wiersz - 4, y + 15, e(g['nazwa']), L + g['min'] * sx, y + 4, max(4, (g['mediana'] - g['min']) * sx),
                    L + g['mediana'] * sx, y + 10, L + g['mediana'] * sx + 12, y + 15, metry(g['mediana'])))
    o.append('</svg>')
    return ('<figure class="wykres-f" data-seq="40">%s<figcaption class="mono"><span class="leg leg--pas"></span> od najpłytszego ujęcia do mediany '
            '<span class="leg leg--sr"></span> średnia powiatu %s m · %s</figcaption></figure>' % (''.join(o), pl(SREDNIA_POWIATU, 1), e(ZRODLO_PIG)))


# ---------------------------------------------------------------- mapa powiatu (W7)
GRANICE = json.loads((ROOT / 'dane' / '00-gminy-granice.json').read_text(encoding='utf-8'))


def _pierscienie(gj):
    pol = gj['coordinates'] if gj['type'] == 'MultiPolygon' else [gj['coordinates']]
    return [p[0] for p in pol]          # tylko obrysy zewnętrzne — dziur w gminach powiatu nie ma (Poznań ma swoją granicę)


def _rzut():
    """Rzut równoodległościowy z poprawką cos(φ) — na skalę powiatu wystarczy. Zwraca funkcję lon,lat → x,y."""
    import math
    pts = [p for g in GRANICE.values() for r in _pierscienie(g['geojson']) for p in r]
    lon0, lon1 = min(p[0] for p in pts), max(p[0] for p in pts)
    lat0, lat1 = min(p[1] for p in pts), max(p[1] for p in pts)
    k = math.cos(math.radians((lat0 + lat1) / 2))
    W = 800
    s = (W - 20) / ((lon1 - lon0) * k)
    H = round((lat1 - lat0) * s + 20)
    return (lambda lon, lat: (10 + (lon - lon0) * k * s, 10 + (lat1 - lat) * s)), W, H


RZUT, MAPA_W, MAPA_H = _rzut()


def _sciezka(gj, prog=.8):
    out = []
    for r in _pierscienie(gj):
        xy, ost = [], None
        for lon, lat in r:
            p = RZUT(lon, lat)
            p = (round(p[0], 1), round(p[1], 1))
            if ost is None or abs(p[0] - ost[0]) + abs(p[1] - ost[1]) >= prog:
                xy.append(p)
                ost = p
        out.append('M' + 'L'.join('%g %g' % p for p in xy) + 'Z')
    return ''.join(out)


def _srodek(gj):
    """Środek ciężkości największego obrysu (wzór na pole wielokąta)."""
    best = None
    for r in _pierscienie(gj):
        xy = [RZUT(*p) for p in r]
        a = cx = cy = 0
        for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
            c = x0 * y1 - x1 * y0
            a += c
            cx += (x0 + x1) * c
            cy += (y0 + y1) * c
        if a and (best is None or abs(a) > best[0]):
            best = (abs(a), cx / (3 * a), cy / (3 * a))
    return best[1], best[2]


def barwa(med):
    """Mediana → krycie barwy wody: płytko jasno-przejrzyście, głęboko pełna barwa (W7)."""
    return round(.16 + .74 * min(1, max(0, (med - 10) / 100)), 2)


def mapa(akt=None, mini=False, id_='m'):
    o = []
    for slug, g in GRANICE.items():
        d = _sciezka(g['geojson'], 2.2 if mini else .8)
        if slug in PO_SLUGU:
            x = PO_SLUGU[slug]
            cls = 'm__g' + (' m__g--akt' if slug == akt else '')
            if mini:
                o.append('<path class="%s" d="%s"/>' % (cls, d))
            else:
                o.append('<a href="/gmina/%s/" class="%s" data-g="%s" style="--a:%s" aria-label="%s: mediana %s m, najpłytsze ujęcie %s m">'
                         '<path d="%s"/></a>' % (slug, cls, slug, barwa(x['mediana']), e(x['nazwa']), metry(x['mediana']), metry(x['min']), d))
        else:
            o.append('<path class="m__g m__g--brak" d="%s"><title>%s — brak danych w zestawie</title></path>' % (d, e(BEZ_DANYCH.get(slug, slug))))
    if not mini:
        for slug, g in GRANICE.items():
            x, y = _srodek(g['geojson'])
            if slug in PO_SLUGU:
                o.append('<text class="m__l" x="%.0f" y="%.0f">%s</text>' % (x, y + 5, metry(PO_SLUGU[slug]['mediana'])))
    elif akt:
        x, y = _srodek(GRANICE[akt]['geojson'])
        o.append('<circle class="m__pkt" cx="%.0f" cy="%.0f" r="9"/>' % (x, y))
    tytul = ('Mapa powiatu poznańskiego: gmina %s' % PO_SLUGU[akt]['nazwa']) if mini else 'Mapa gmin powiatu poznańskiego barwiona medianą głębokości studni'
    return ('<svg class="mapa%s" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>'
            % (' mapa--mini' if mini else '', MAPA_W, MAPA_H, e(tytul), ''.join(o)))


OSM = '© współtwórcy <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> (ODbL)'


# ---------------------------------------------------------------- rachunek ogrodu (W6) — ta sama matematyka w site.js
def rachunek_dane(g, m2=OGROD['m2'], dawka=OGROD['dawka'], tyg=OGROD['tygodnie'], cena=WODOCIAG['woda'] + WODOCIAG['scieki']):
    w = wycena(g)
    m3 = m2 * dawka * tyg / 1000
    roczna = m3 * cena
    oszcz = m3 * max(0.01, cena - PRAD_M3)
    return {'m3': m3, 'roczna': roczna, 'lo': w['koszt'][0], 'hi': w['koszt'][1],
            'zwrot': (w['koszt'][0] / oszcz, w['koszt'][1] / oszcz), 'cena': cena}


def rachunek_svg(r):
    W, H, L, R, T, B, LAT = 640, 300, 64, 16, 16, 40, 15
    ymax = max(r['roczna'] * LAT, r['hi'] + r['m3'] * PRAD_M3 * LAT) * 1.08
    X = lambda t: L + t / LAT * (W - L - R)
    Y = lambda v: T + (1 - v / ymax) * (H - T - B)
    o = []
    krok = 10 ** len(str(int(ymax / 4))) // 10 or 1
    krok = next(k * krok for k in (1, 2, 2.5, 5, 10) if ymax / (k * krok) <= 5)
    v = 0
    while v <= ymax:
        o.append('<line class="r__siatka" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="r__os" x="%d" y="%.1f">%s</text>'
                 % (L, W - R, Y(v), Y(v), L - 8, Y(v) + 5, zl(v) if v < 1000 else '%s tys.' % pl(v / 1000, 0 if v % 1000 == 0 else 1)))
        v += krok
    for t in range(0, LAT + 1, 5):
        o.append('<text class="r__os r__os--x" x="%.1f" y="%d">%d %s</text>' % (X(t), H - 12, t, 'lat' if t >= 5 else ''))
    pas = 'M%.1f %.1fL%.1f %.1fL%.1f %.1fL%.1f %.1fZ' % (X(0), Y(r['lo']), X(LAT), Y(r['lo'] + r['m3'] * PRAD_M3 * LAT),
                                                     X(LAT), Y(r['hi'] + r['m3'] * PRAD_M3 * LAT), X(0), Y(r['hi']))
    o.append('<path class="r__pas" d="%s"/>' % pas)
    o.append('<path class="r__kran" d="M%.1f %.1fL%.1f %.1f"/>' % (X(0), Y(0), X(LAT), Y(r['roczna'] * LAT)))
    for z in r['zwrot']:
        if z <= LAT:
            o.append('<circle class="r__zw" cx="%.1f" cy="%.1f" r="6"/>' % (X(z), Y(r['roczna'] * z)))
    return ('<svg class="wykres wykres--rachunek" viewBox="0 0 %d %d" role="img" aria-label="Skumulowany koszt wody z kranu i koszt studni w ciągu %d lat" data-rachunek-svg>%s</svg>'
            % (W, H, LAT, ''.join(o)))


def lata(z):
    lo, hi = z
    f = lambda x: '%d' % round(x) if x >= 1.5 else pl(x, 1)
    if lo > 30:
        return 'ponad 30 lat'
    return '%s–%s lat' % (f(lo), f(hi)) if hi <= 30 else 'od %s lat' % f(lo)


def faq(pytania):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p class="key">%s</p><p>%s</p></details>' % (e(q), e(a), e(b)) for q, a, b in pytania)



# ---------------------------------------------------------------- v3 „GŁĘBIEJ”: przyrząd w hero (W9)
def linijka(g):
    """Linijka 0–120 m: pas widełek (najpłytsze–mediana), linia 30 m, znacznik wody na medianie."""
    w = wycena(g)
    podz = ''.join('<span class="linijka__t mono" style="top:%.2f%%;--t:%.2f">%d</span>' % (m / 120 * 100, m / 120 * 100, m) for m in range(0, 121, 10))
    return ('<div class="linijka" data-linijka aria-hidden="true" style="--lo:%.4f;--hi:%.4f">'
            '<div class="linijka__os">%s</div><div class="linijka__30"><span class="mono">30 m</span></div>'
            '<div class="linijka__pas"></div><div class="linijka__wiertlo"></div>'
            '<div class="linijka__woda"><span class="mono" data-h-med>woda ~%s m</span></div></div>'
            % (w['lo'] / 120, w['hi'] / 120, podz, metry(w['hi'])))


def przyrzad(g):
    w = wycena(g)
    opcje = ''.join('<option value="%s"%s>%s</option>' % (x['slug'], ' selected' if x['slug'] == g['slug'] else '', e(x['nazwa']))
                    for x in sorted(GMINY, key=lambda x: x['nazwa']))
    return f'''<form class="przyrzad" action="/#karta" data-przyrzad>
<label class="przyrzad__g"><span class="mono">gmina działki</span><select name="gmina" data-gmina-hero>{opcje}</select></label>
<dl class="przyrzad__w">
<div><dt class="mono">wiercimy</dt><dd class="mono" data-h-m>{metry(w['lo'])}–{metry(w['hi'])} m</dd></div>
<div><dt class="mono">kosztuje</dt><dd class="mono" data-h-zl>{zl(w['koszt'][0])}–{zl(w['koszt'][1])} zł</dd></div>
<div><dt class="mono">papiery</dt><dd data-h-f>{e(w['formal'][0])}</dd></div>
</dl>
<div class="przyrzad__a"><button class="btn btn--sygnal btn--duzy" type="submit">Zarezerwuj oględziny {STRZALKA}</button><a class="btn btn--duzy btn--obrys" href="tel:{F['tel_e164']}">Zadzwoń · {F['tel']}</a></div>
</form>'''


# ---------------------------------------------------------------- zejście pod ziemię (W8, W9)
def warstwy(D):
    """Schemat poglądowy warstw do mediany D (m). Zwraca listę (nazwa, od, do, klasa). Ta sama funkcja w site.js."""
    a, b, c = max(3, round(D * .3)), max(6, round(D * .55)), max(9, round(D * .82))
    return [('gleba i korzenie', 0, 1, 'w-gleba'), ('glina zwałowa', 1, a, 'w-glina'), ('piaski i żwiry — sucho', a, b, 'w-piasek'),
            ('iły — warstwa szczelna', b, c, 'w-il'), ('piaski wodonośne', c, D + 12, 'w-woda')]


def zejscie(g):
    D = g['mediana']
    H = D + 12
    ws = ''.join('<div class="z__w %s" style="top:%.3f%%;height:%.3f%%"><span class="z__wn mono">%s<b>od %s m</b></span></div>'
                 % (k, od / H * 100, (do - od) / H * 100, n, metry(od)) for n, od, do, k in warstwy(D))
    lin30 = '<div class="z__30" style="top:%.3f%%"><span class="mono">30 m — granica formalności</span></div>' % (30 / H * 100) if D > 30 else ''
    lin30 += ''.join('<div class="z__m" style="top:%.3f%%"><span>%d</span></div>' % (m / H * 100, m) for m in range(5, int(H), 5))
    lin30 += '<div class="z__otwor" style="height:%.3f%%"></div>' % (D / H * 100)
    return f'''<section id="zejscie" class="zejscie" data-pin="340" data-zejscie style="--zs:{D / H:.4f}">
<div class="pin__w zejscie__w">
<div class="zejscie__t wrap">
<p class="etyk mono">zejście · gmina <span data-z-gmina>{e(g['nazwa'])}</span></p>
<p class="zejscie__licznik mono" aria-live="off"><span data-z-m>{metry(D)}</span><small>m</small></p>
<p class="zejscie__opis" data-z-opis>Woda. Mediana {g['otworow']} otworów w rejestrze PIG.</p>
</div>
<div class="zejscie__kol" aria-hidden="true"><div class="z__swiat" data-z-swiat style="--H:{H}">{ws}{lin30}<div class="z__lustro" style="top:{D / H * 100:.3f}%"></div></div>
<div class="z__zerdz"></div><svg class="schemat z__wiertlo" viewBox="0 0 120 120"><path d="M36 0h48v34l-10 40-14 46-14-46-10-40z" fill="currentColor"/><path d="M48 30l24 14M48 50l24 14" stroke="#111214" stroke-width="5"/></svg></div>
<p class="zejscie__podpis mono">schemat poglądowy dla mediany gminy — prawdziwy profil zapisujemy co metr w karcie otworu</p>
</div>
</section>'''


def pakiet(x):
    cena = x['do'] * RYNEK['mb'][0] + RYNEK['osprzet'][0]
    wyr = ' pak__k--wyr' if x['slug'] == 'dom' else ''
    dop = '<p class="pak__dop mono">+ projekt i pozwolenie wg wyceny</p>' if x['do'] > 30 else '<p class="pak__dop mono">bez zgłoszeń</p>'
    return ('<article class="pak__k%s"><p class="pak__do mono">do %d m</p><h3>%s</h3><p class="pak__c mono"><small>od</small> %s <small>zł</small></p>%s'
            '<ul>%s</ul><button class="btn%s" type="button" data-pakiet="%s" data-cel="%s">Policz dla mojej gminy %s</button></article>'
            % (wyr, x['do'], e(x['nazwa']), zl(cena), dop, ''.join('<li>%s</li>' % e(c) for c in x['co']),
               ' btn--sygnal' if wyr else ' btn--obrys', x['slug'], x['cel'], STRZALKA))


def dni_do(data):
    return (datetime.date.fromisoformat(data) - datetime.date.today()).days


# ---------------------------------------------------------------- powłoka
NAV = [('/#karta', 'Wycena'), ('/#powiat', 'Mapa gmin'), ('/#ogrod', 'Rachunek ogrodu'), ('/paszport-studni/', 'Paszport studni'), ('/dla-firm/', 'Dla firm')]


def powloka(sciezka, tytul, opis, tresc, ld=None):
    nav = ''.join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if sciezka == u else '', n) for u, n in NAV)
    graf = [{'@type': 'WebPage', 'name': tytul, 'url': BASE + sciezka, 'description': opis,
             'isPartOf': {'@type': 'WebSite', 'name': 'AKWIFER — strona wzorcowa Jurczak Studio'}}] + (ld or [])
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(tytul)}</title>
<meta name="description" content="{e(opis)}">
{'<meta name="robots" content="noindex,nofollow">' if DEMO else ''}
<link rel="canonical" href="{BASE + sciezka}">
<meta property="og:title" content="{e(tytul)}"><meta property="og:description" content="{e(opis)}">
<meta name="theme-color" content="#111214">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo-400-800-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css?v={FV}">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
<script type="application/ld+json">{json.dumps({'@context': 'https://schema.org', '@graph': graf}, ensure_ascii=False)}</script>
<script src="/assets/js/site.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="nag">
<a class="nag__logo" href="/" aria-label="AKWIFER — strona główna">{brand.SYGNET}<span>AKWIFER</span></a>
<nav class="nag__menu" id="menu" aria-label="Główna">{nav}</nav>
<button class="nag__wl" type="button" aria-pressed="false" data-tryb-wl><span class="nag__wl-kropka" aria-hidden="true"></span><span>Oczami właściciela</span></button>
<button class="nag__przycisk" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
</header>
<main id="tresc">
{tresc}
</main>
<nav class="pasek" aria-label="Szybki kontakt" data-pasek><a href="tel:{F['tel_e164']}">Zadzwoń</a><a href="sms:{F['tel_e164']}" data-sms>SMS z kartą</a><a class="pasek__w" href="/#karta">Wycena</a></nav>
<footer class="stopka">
<div class="wrap stopka__kol">
<div><p class="stopka__logo">{brand.SYGNET}<span>AKWIFER</span></p><p>Strona wzorcowa dla firm studniarskich. Firma, telefon ({F['tel']}), termin i paszport są przykładowe; dane gmin są prawdziwe.</p></div>
<div><p class="etyk mono">Gminy powiatu poznańskiego</p><nav class="stopka__gminy" aria-label="Gminy">{''.join('<a href="/gmina/%s/">%s</a>' % (g['slug'], e(g['nazwa'])) for g in sorted(GMINY, key=lambda g: g['nazwa']))}</nav></div>
<div><p class="etyk mono">Źródła</p><p>Głębokości: {e(ZRODLO_PIG)}. Ceny: kb.pl, 08.2026. Przepisy: Prawo wodne art. 395, Prawo budowlane art. 29, Pgig art. 3 pkt 2a.</p><p>Projekt i wykonanie: <a href="https://jurczakstudio.pl" rel="noopener">Jurczak Studio</a> — <a href="/dla-firm/">co ta strona robi dla firmy</a>.</p></div>
</div>
</footer>
<p class="wzor mono">strona wzorcowa · firma fikcyjna</p>
</body>
</html>
'''


# ---------------------------------------------------------------- strona główna
def strona_glowna():
    etapy = ''.join('<li><span class="mono">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(n), e(t)) for i, (n, t) in enumerate(ETAPY))
    szybko = ''.join('<a class="szybko__g" href="/gmina/%s/" style="--a:%.3f;--b:%.3f"><span>%s</span><span class="mono">%s m</span><i aria-hidden="true"></i></a>'
                     % (g['slug'], g['min'] / 120, g['mediana'] / 120, e(g['nazwa']), metry(g['mediana']))
                     for g in sorted(GMINY, key=lambda g: g['mediana']))
    pz = PASZPORT
    R0 = rachunek_dane(PO_SLUGU['mosina'])
    tresc = f'''
<section id="start" class="hero3">
<div class="hero3__tlo" data-par=".06">{obraz('hero', 'hero', 'Wiertnica studzienna nocą w świetle lamp roboczych' if MAN.get('hero', {}).get('podpis', '').startswith('zdjęcie') else 'Wiertnica studni o zmierzchu na działce z domem w stanie surowym', '(max-width: 760px) 100vw, 56vw', 'hero3__img', eager=True, media=('hero-pion', '(max-width: 760px)'))}</div>
<div class="wrap hero3__u">
<div class="hero3__t">
<p class="kicker mono">Studnie głębinowe · {F['baza']}</p>
{split('Wiercimy', 'do wody.', '<em>Cenę znasz, zanim zadzwonisz.</em>', tag='h1')}
{przyrzad(PO_SLUGU['mosina'])}
<ul class="hero3__dowody mono"><li>cena za metr z góry</li><li>papiery powyżej 30 m po naszej stronie</li><li>oddzwaniamy w 15 min</li></ul>
</div>
{linijka(PO_SLUGU['mosina'])}
</div>
<p class="hero3__podpis mono">{MAN['hero'].get('podpis', 'ilustracja poglądowa') if 'hero' in MAN else 'plansza zastępcza · docelowo kadr z generatora'}</p>
{notka('Klient wchodzi wieczorem z telefonu i <b>w pierwszym ekranie dostaje odpowiedź, z którą dziś dzwoni do pięciu firm</b>: ile metrów, ile złotych, czy są papiery. 93% klientów mówi, że natychmiastowa wycena wpływa na wybór wykonawcy — a żadna z 18 sprawdzonych polskich firm jej nie ma.')}
</section>

<section id="gwarancja" class="sek sek--gw">
<div class="tlo tlo-siatka" aria-hidden="true"></div>
<div class="wrap">
<div class="sek__t sek__t--waski">
{split('Gwarancja', '<em>przejrzystości.</em>')}
<p class="key">Najczęstszy strach przy studni: planowałem 12 tysięcy, wyszło 40. Dlatego zasady piszemy przed wierceniem, nie po.</p>
</div>
<ol class="gw" data-seq="90">{''.join('<li><span class="gw__n mono">%s</span><b>%s</b><p>%s</p></li>' % (e(n), e(t), e(d)) for n, t, d in GWARANCJA)}</ol>
<p class="zrodlo">Przykładowe zasady wzorca — firma wpisuje swoje. 200 zł/m to dolna granica średniej rynkowej (kb.pl, 08.2026); 100 zł/m za suchy otwór to praktyka jednej z krakowskich firm.</p>
{notka('To odpowiedź na pytanie, które klient boi się zadać przez telefon. <b>Firma, która pisze zasady wprost, wygląda pewniej niż ta, która obiecuje „najniższe ceny”</b> — żadna z przebadanych firm w Polsce tego nie robi.')}
</div>
</section>

{zejscie(PO_SLUGU['mosina'])}

<section id="karta" class="sek sek--karta">
<div class="wrap sek__uklad">
<div class="sek__t">
{split('Karta zlecenia.', '<em>Cztery liczby, które chcesz znać.</em>')}
<p class="key">Karta liczy metry z danych Państwowego Instytutu Geologicznego dla Twojej gminy, złotówki ze średnich rynkowych i mówi, po której stronie 30 m — granicy formalności — leży Twoja działka.</p>
<p>Karta zapamiętuje się w przeglądarce: zobaczysz ją na każdej stronie, a jednym dotknięciem wyślesz nam SMS-em. Oddzwonimy, wiedząc już, o co pytasz.</p>
{notka('Zgłoszenie przychodzi SMS-em w stałym formacie: <b>gmina, cel, liczba osób, przewidywane metry</b>. Oddzwaniasz do kogoś, kto zna widełki i już się na nie zgodził — zamiast tłumaczyć przez telefon, czemu nie da się podać ceny.')}
</div>
{karta(id_='k0')}
</div>
</section>

<section id="powiat" class="sek sek--powiat">
<div class="wrap">
<div class="sek__t sek__t--waski">
{split('Powiat.', '<em>Od 14 do 110 metrów.</em>')}
<p class="key">Pod Luboniem połowa otworów w rejestrze ma mniej niż 14 m, w Komornikach — ponad 110 m; o głębokości studni decyduje gmina i warstwa, nie firma.</p>
<p>Najedź na gminę albo ją dotknij — zobaczysz liczby z rejestru i jednym przyciskiem przeniesiesz je do karty zlecenia.</p>
</div>
<div class="mapa-u">
<figure class="mapa-f" data-mapa data-rv="mask">{mapa()}
<figcaption class="mapa__leg mono"><span class="leg-skala" aria-hidden="true"><i style="left:{(30 - 10) / 100 * 100:.0f}%"></i></span><span class="leg-opis"><span>10 m</span><span>30 m — granica formalności</span><span>110 m</span></span>
<span class="leg-brak"><span class="leg leg--brak"></span> brak danych w zestawie</span><span class="mapa__zr">Granice: {OSM}. Głębokości: {e(ZRODLO_PIG)}.</span></figcaption></figure>
<aside class="mapa__info" data-mapa-info aria-live="polite">
<p class="etyk mono">wybrana gmina</p>
<p class="mapa__n" data-mi-n>Mosina</p>
<dl><div><dt>mediana</dt><dd class="mono" data-mi-med>{metry(PO_SLUGU['mosina']['mediana'])} m</dd></div><div><dt>najpłytsze ujęcie</dt><dd class="mono" data-mi-min>{metry(PO_SLUGU['mosina']['min'])} m</dd></div>
<div><dt>otworów w rejestrze</dt><dd class="mono" data-mi-otw>{PO_SLUGU['mosina']['otworow']}</dd></div><div><dt>granica 30 m</dt><dd data-mi-f>{e(wycena(PO_SLUGU['mosina'])['formal'][0])}</dd></div></dl>
<div class="mapa__akcje"><button class="btn btn--sygnal" type="button" data-mi-karta>Przenieś do karty {STRZALKA}</button><a class="link" href="/gmina/mosina/" data-mi-link>Strona gminy {STRZALKA}</a></div>
</aside>
</div>
{notka('Mapa jest z otwartych danych, liczby z rejestru PIG — <b>klient widzi swoją gminę i od razu ma powód, żeby zadzwonić</b>. Dla Twojej firmy zaznaczymy dokładnie te gminy, w których wiercisz, a resztę wyszarzymy.')}
</div>
</section>

<section id="szybko" class="sek szybko" aria-label="Gminy — szybki wybór">
<div class="wrap"><p class="etyk mono">Twoja gmina — mediana głębokości</p><div class="szybko__lista">{szybko}</div></div>
</section>

<section id="pakiety" class="sek sek--pak">
<div class="wrap">
<div class="sek__t sek__t--waski">
{split('Pakiety.', '<em>Cena „od”, nie „do uzgodnienia”.</em>')}
<p class="key">Trzy pakiety z ceną startową i stałą dopłatą za każdy metr ponad pakiet. Wybierz pakiet — karta przeliczy go dla Twojej gminy.</p>
</div>
<div class="pak" data-seq="90">{''.join(pakiet(x) for x in PAKIETY)}</div>
<p class="zrodlo">Ceny przykładowe: metry pakietu × 200 zł + pompa i hydrofor od 2 500 zł (średnie rynkowe, kb.pl 08.2026). Dopłata za metr ponad pakiet: 200 zł. Firma wpisuje swój cennik.</p>
{notka('Niemieckie firmy studniarskie sprzedają tak od lat: <b>trzy pakiety i cena za metr</b>. Klient wybiera, zamiast negocjować — a Ty dostajesz zgłoszenie z już zaakceptowaną ceną startową.')}
</div>
</section>

<section id="robota" class="sek sek--robota">
<div class="wrap sek__uklad sek__uklad--odwr">
<figure class="robota__kadr" data-rv="mask">{obraz('woda', 'woda', 'Ekipa przy wiertnicy studziennej na osiedlu domów jednorodzinnych' if MAN.get('woda', {}).get('podpis', '').startswith('zdjęcie') else 'Czysta woda nalewana do szklanki z kranu przy nowej studni', '(max-width: 760px) 100vw, 40vw', 'robota__img')}<figcaption class="mono">{MAN['woda'].get('podpis', 'ilustracja poglądowa') if 'woda' in MAN else 'plansza zastępcza · docelowo kadr z generatora'}</figcaption></figure>
<div class="sek__t">
{split('Robota.', '<em>Pięć kroków, jeden dzień wiercenia.</em>')}
<p class="key">Od karty do wody: rozmowa, oględziny z papierami, wiercenie, próbne pompowanie i odbiór z paszportem studni.</p>
<ol class="etapy" data-seq="70">{etapy}</ol>
{notka('Tu stoją <b>Twoje zdjęcia z budów</b>. Kadr poglądowy trzyma miejsce, dopóki ich nie mamy — przy najbliższym wierceniu robimy sesję albo bierzemy zdjęcia od klientów z opinii Google.')}
</div>
</div>
</section>

<section id="ogrod" class="sek sek--ogrod">
<div class="wrap sek__uklad">
<div class="sek__t">
{split('Rachunek ogrodu.', '<em>Kiedy studnia się zwraca.</em>')}
<p class="key">Podlewanie z kranu bez osobnego podlicznika kosztuje u Aquanetu {pl(WODOCIAG['woda'] + WODOCIAG['scieki'], 2)} zł za każdy metr sześcienny — {pl(WODOCIAG['woda'], 2)} zł za wodę i {pl(WODOCIAG['scieki'], 2)} zł za ścieki, których z trawnika nie ma.</p>
<form class="ogrod" data-ogrod onsubmit="return false" aria-label="Rachunek ogrodu">
<label><span>Ogród do podlewania, m²</span><input type="number" min="0" step="50" value="{OGROD['m2']}" data-o-m2 inputmode="numeric"></label>
<label><span>Dawka, litrów na m² w tygodniu</span><input type="number" min="0" step="5" value="{OGROD['dawka']}" data-o-dawka inputmode="numeric"></label>
<label><span>Tygodni podlewania w roku</span><input type="number" min="0" max="52" value="{OGROD['tygodnie']}" data-o-tyg inputmode="numeric"></label>
<label><span>Cena wody z kranu, zł/m³</span><input type="number" min="0" step="0.01" value="{WODOCIAG['woda']}" data-o-woda inputmode="decimal"></label>
<label class="ogrod__ch"><input type="checkbox" checked data-o-scieki><span>Bez podlicznika — płacę też za ścieki ({pl(WODOCIAG['scieki'], 2)} zł/m³)</span></label>
</form>
<p class="zrodlo">Ceny: {e(WODOCIAG['zrodlo'])}; u innego wodociągu wpisz swoją. Dawka i sezon to założenia — zmień je. Prąd pompy liczymy {pl(PRAD_M3, 2)} zł/m³ (pompa 1,1 kW, 3 m³/h). Bez kosztu serwisu.</p>
</div>
<figure class="ogrod__w" data-rv="up">
<dl class="ogrod__liczby">
<div><dt>wody w roku</dt><dd class="mono" data-o-m3>{pl(R0['m3'], 0)} m³</dd></div>
<div><dt>z kranu rocznie</dt><dd class="mono" data-o-rok>{zl(R0['roczna'])} zł</dd></div>
<div class="ogrod__zw"><dt>studnia się zwraca po</dt><dd class="mono" data-o-zwrot>{lata(R0['zwrot'])}</dd></div>
</dl>
{rachunek_svg(R0)}
<p class="ogrod__leg mono"><span><i class="leg leg--kran"></i>woda z kranu, razem</span><span><i class="leg leg--studnia"></i>studnia: widełki kosztu + prąd pompy</span><span><i class="leg leg--zw"></i>tu się zwraca</span></p>
<figcaption class="mono">koszt studni z karty zlecenia dla gminy <b data-o-gmina>Mosina</b>: <span data-o-koszt>{zl(R0['lo'])}–{zl(R0['hi'])} zł</span> · <a href="#karta">zmień gminę</a></figcaption>
</figure>
</div>
{notka('Klient, który ma ogród, <b>sam sobie policzy, że studnia jest tańsza od wodociągu</b> — i przychodzi już przekonany. Ty nie musisz go namawiać, tylko potwierdzić widełki.')}
</section>

<section id="przepisy" class="sek sek--prawo">
<div class="wrap sek__uklad">
<div class="sek__t">
{split('Przepisy 2026.', '<em>Trzy pytania zamiast urzędu.</em>')}
<form class="drzewko" data-drzewko onsubmit="return false" aria-label="Czy potrzebuję pozwolenia na studnię">
<fieldset><legend>Jak głęboka będzie studnia?</legend><label><input type="radio" name="dz-g" value="do30" checked><span>do 30 m</span></label><label><input type="radio" name="dz-g" value="ponad"><span>ponad 30 m</span></label></fieldset>
<fieldset><legend>Ile wody na dobę?</legend><label><input type="radio" name="dz-q" value="do5" checked><span>do 5 m³</span></label><label><input type="radio" name="dz-q" value="ponad"><span>więcej</span></label></fieldset>
<fieldset><legend>Na co?</legend><label><input type="radio" name="dz-c" value="dom" checked><span>dom i ogród</span></label><label><input type="radio" name="dz-c" value="firma"><span>działalność gospodarcza</span></label></fieldset>
<output class="drzewko__w" data-dz-wynik><b>Bez zgłoszeń i pozwoleń.</b> To „zwykłe korzystanie z wód” (Prawo wodne, art. 395). Wiercimy po oględzinach.</output>
</form>
</div>
<div class="prawo__karty">
<article class="prawo__k prawo__k--ab"><p class="etyk mono">abolicja dla starych studni</p><p class="prawo__n mono"><span data-dni-do="{ABOLICJA['do']}">{dni_do(ABOLICJA['do'])}</span><small>dni</small></p>
<p>Do 31.12.2027 zalegalizujesz studnię wykonaną bez zgody <b>bez opłaty {ABOLICJA['oplata']}</b> i bez kary. Operat i mapy dalej kosztują — przygotujemy je.</p><p class="zrodlo"><a href="{ABOLICJA['zrodlo']}" rel="noopener">{e(ABOLICJA['akt'])}</a></p></article>
<article class="prawo__k prawo__k--su"><p class="etyk mono">susza 2026</p><p class="prawo__h">Płytkie studnie tracą wodę.</p>
<p>Państwowa Służba Hydrogeologiczna ostrzegała przed niżówką w Wielkopolsce przez {e(NIZOWKA['miesiace'])}. Pogłębiamy stare kręgi i wiercimy obok.</p><p class="zrodlo"><a href="{NIZOWKA['zrodlo']}" rel="noopener">PIG-PIB, ostrzeżenie hydrogeologiczne nr {NIZOWKA['nr']}</a></p></article>
</div>
</div>
{notka('Dwa prawdziwe powody do telefonu w tym roku: <b>abolicja</b> (nowa linia usług — legalizacja starych studni) i <b>susza</b> (pogłębianie). Licznik dni liczy się sam, a strona mówi o tym pierwsza w regionie.')}
</section>

<section id="paszport" class="sek sek--paszport">
<div class="wrap sek__uklad">
<div class="sek__t">
{split('Paszport.', '<em>Studnia z dokumentami.</em>')}
<p class="key">Po odbiorze dostajesz paszport studni: głębokość, filtr, zwierciadło, wydajność z pompowania, model pompy, wynik badania wody i terminy przeglądów.</p>
<a class="link" href="/paszport-studni/">Zobacz przykładowy paszport {STRZALKA}</a>
{notka('Klient dostaje link albo naklejkę z kodem na pokrywę studzienki. <b>Za trzy lata, kiedy pompa zacznie szwankować, dzwoni do Ciebie</b> — Twój numer jest na paszporcie, a Ty wiesz, co jest w otworze, zanim przyjedziesz.')}
</div>
<div class="paszport-mini tekstura-dok" data-rv="up">
<p class="mono">paszport studni · {pz['numer']}</p>
<dl><div><dt>gmina</dt><dd>{pz['gmina']}</dd></div><div><dt>głębokość</dt><dd class="mono">{pl(pz['glebokosc'], 1)} m</dd></div>
<div><dt>zwierciadło</dt><dd class="mono">{pl(pz['zw_stat'], 1)} m</dd></div><div><dt>wydajność</dt><dd class="mono">{pl(pz['Q'], 1)} m³/h</dd></div></dl>
<p class="paszport-mini__p mono">przykład · dane wymyślone</p>
</div>
</div>
</section>

<section id="zgloszenie" class="sek sek--zgl">
<div class="wrap sek__uklad">
<div class="sek__t">
{split('Zgłoszenie.', '<em>Jeden SMS zamiast formularza.</em>')}
<p class="zgl__wielki mono"><a href="tel:{F['tel_e164']}">{F['tel']}</a></p>
<p class="key">Karta, którą wypełniłeś na górze, jest gotowym zgłoszeniem — wysyłasz ją SMS-em ze swojego telefonu, bez pól na e-mail i zgód na pół ekranu.</p>
<p class="mono zgl__tel">{F['tel']} · {F['godziny']} · numer przykładowy</p>
{notka('Bez formularza, bez skrzynki, której nikt nie czyta. <b>SMS przychodzi na Twój telefon na budowie</b>, z gotową treścią — odpisujesz albo oddzwaniasz między dwoma metrami rury.')}
</div>
<div class="zgl__podglad" data-sygnatura="karta"><p class="mono zgl__etyk">tak wygląda Twój SMS</p><pre class="mono" data-sms-podglad>Dzień dobry, pytam o studnię głębinową.</pre><a class="btn btn--sygnal" href="sms:{F['tel_e164']}" data-sms>{SMS}<span>Wyślij SMS</span></a><button class="btn zgl__kop" type="button" data-kopiuj>Skopiuj treść</button></div>
</div>
</section>
'''
    return powloka('/', 'Studnia głębinowa — wycena dla Twojej gminy, powiat poznański | AKWIFER (wzorzec)',
                   'Ile metrów, ile złotych, czy trzeba zgłaszać i kiedy termin — karta zlecenia z danymi PIG dla 14 gmin '
                   'powiatu poznańskiego. Strona wzorcowa dla firm studniarskich.', tresc)


# ---------------------------------------------------------------- gminy
def strona_gminy(g):
    w = wycena(g)
    srodek = 'płycej' if g['mediana'] < SREDNIA_POWIATU else 'głębiej'
    po30 = w['hi'] > 30
    akap = []
    if g['mediana'] <= 30:
        akap.append('W gminie %s woda bywa płytko: połowa z %d otworów w rejestrze PIG ma mniej niż %s m, a najpłytsze ujęcie — %s m. '
                    'Dla domu jednorodzinnego to zwykle studnia w granicy 30 m, bez zgłoszeń i pozwoleń.'
                    % (g['nazwa'], g['otworow'], metry(g['mediana']), metry(g['min'])))
    elif g['min'] > 30:
        akap.append('W gminie %s nawet najpłytsze ujęcie w rejestrze PIG ma %s m, a mediana %d otworów to %s m. '
                    'Studnia przekroczy tu najpewniej 30 m — a to oznacza projekt robót geologicznych zatwierdzany przez starostę, '
                    'dokumentację hydrogeologiczną po wierceniu i pozwolenie wodnoprawne.'
                    % (g['nazwa'], metry(g['min']), g['otworow'], metry(g['mediana'])))
    else:
        akap.append('W gminie %s rozrzut jest duży: najpłytsze ujęcie w rejestrze PIG ma %s m, a połowa z %d otworów jest głębsza niż %s m. '
                    'Czy studnia zmieści się w 30 m, rozstrzyga konkretna działka — i dlatego na oględzinach zaczynamy od sprawdzenia okolicznych otworów.'
                    % (g['nazwa'], metry(g['min']), g['otworow'], metry(g['mediana'])))
    akap.append('Mediana gminy jest %s niż średnia powiatu poznańskiego (%s m). Rejestr obejmuje głównie studnie komunalne i zakładowe, '
                'które schodzą głębiej niż przydomowe, więc górną granicę traktuj jako ostrożną.' % (srodek, pl(SREDNIA_POWIATU, 1)))
    if g['otworow'] < 10:
        akap.append('Uwaga: w rejestrze jest tu tylko %d otworów — liczby są orientacyjne, a jeden głęboki otwór zakładowy mocno podnosi medianę.' % g['otworow'])
    if g['gzwp']:
        akap.append('Gmina leży w obrębie Głównego Zbiornika Wód Podziemnych: %s.' % g['gzwp'])
    pytania = [
        ('Jak głęboka będzie studnia w gminie %s?' % g['nazwa'],
         'Według rejestru PIG od %s m (najpłytsze ujęcie) do ok. %s m (mediana %d otworów).' % (metry(g['min']), metry(g['mediana']), g['otworow']),
         'Dokładną głębokość ustala się po oględzinach i sprawdzeniu otworów w okolicy działki — rejestr podaje rozkład dla całej gminy.'),
        ('Ile kosztuje studnia głębinowa w gminie %s?' % g['nazwa'],
         'Na średnich rynkowych: od ok. %s do ok. %s zł razem z pompą i hydroforem.' % (zl(w['koszt'][0]), zl(w['koszt'][1])),
         'Liczymy %d–%d zł za metr wiercenia (kb.pl, 08.2026) i 2,5–8 tys. zł osprzętu. To widełki, nie cennik.' % RYNEK['mb']),
        ('Czy w gminie %s trzeba zgłaszać studnię?' % g['nazwa'],
         'Studni do 30 m na potrzeby domu, z poborem do 5 m³ na dobę, nie trzeba zgłaszać — powyżej 30 m potrzebny jest projekt robót geologicznych.',
         'W tej gminie: %s.' % w['formal'][1]),
    ]
    inne = ''.join('<a href="/gmina/%s/">%s <span class="mono">%s m</span></a>' % (x['slug'], e(x['nazwa']), metry(x['mediana']))
                   for x in sorted(GMINY, key=lambda x: x['nazwa']) if x['slug'] != g['slug'])
    ld = [{'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a + ' ' + b}} for q, a, b in pytania]},
          {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'AKWIFER', 'item': BASE + '/'},
                                                          {'@type': 'ListItem', 'position': 2, 'name': g['nazwa'], 'item': BASE + '/gmina/%s/' % g['slug']}]}]
    tresc = f'''
<section id="glowa" class="glowa">
<div class="tlo tekstura-noc" aria-hidden="true"></div>
<div class="wrap glowa__uklad">
<div>
<p class="okruchy mono"><a href="/">AKWIFER</a> / <a href="/#powiat">gminy</a> / {e(g['nazwa'])}</p>
{split('Studnia głębinowa', '<em>%s</em>' % e(g['nazwa']), tag='h1')}
<p class="lead">{akap[0]}</p>
</div>
<div class="glowa__prawa"><figure class="mapa-mini" data-rv="scale">{mapa(g['slug'], mini=True)}<figcaption class="mono">powiat poznański · granice {OSM}</figcaption></figure>
<p class="glowa__liczba mono" aria-label="Mediana głębokości {metry(g['mediana'])} metra"><span>{metry(g['mediana'])}</span><small>m · mediana</small></p></div>
</div>
{notka('Ta podstrona powstała automatycznie z danych rejestru PIG — <b>dla każdej gminy, w której wiercisz, inna treść i inne liczby</b>. Nie ma tu „Studnie %s — zapraszamy”, jest odpowiedź na pytanie, które klient wpisuje w Google.' % e(g['nazwa']))}
</section>

<section id="karta" class="sek sek--karta">
<div class="wrap sek__uklad">
<div class="sek__t"><h2 data-rv="up">Karta dla gminy {e(g['nazwa'])}</h2>
<p class="key">Karta jest już ustawiona na gminę {e(g['nazwa'])} — zmień cel i liczbę osób, a zobaczysz zużycie wody i widełki kosztu.</p>
<p>Średnio na rynku: od {zl(w['koszt'][0])} do {zl(w['koszt'][1])} zł z osprzętem. Formalności: {e(w['formal'][0])}.</p></div>
{karta(prefill=g['slug'], id_='k1')}
</div>
</section>

{zejscie(g)}

<section id="pytania" class="sek">
<div class="wrap sek__uklad">
<div class="sek__t"><h2>Pytania o studnię w gminie {e(g['nazwa'])}</h2>{faq(pytania)}</div>
<nav class="inne" aria-label="Inne gminy" data-seq="30"><p class="etyk mono">inne gminy powiatu</p>{inne}</nav>
</div>
</section>

<section id="dane" class="sek sek--powiat">
<div class="wrap">
<div class="sek__t sek__t--waski"><h2>Liczby z rejestru</h2>
<p class="key">{akap[1]}</p>
{''.join('<p>%s</p>' % a for a in akap[2:])}</div>
<div data-scrub>{wykres(akt=g['slug'], id_='w1')}</div>
</div>
</section>
'''
    return powloka('/gmina/%s/' % g['slug'], 'Studnia głębinowa %s — głębokość i koszt | AKWIFER (wzorzec)' % g['nazwa'],
                   'Jak głęboka będzie studnia w gminie %s: od %s do %s m według rejestru PIG (%d otworów). Koszt, formalności, karta zlecenia.'
                   % (g['nazwa'], metry(g['min']), metry(g['mediana']), g['otworow']), tresc, ld)


# ---------------------------------------------------------------- paszport
def strona_paszport():
    pz = PASZPORT
    wiersze = []
    for i, (n, v, norma, j) in enumerate(pz['woda']):
        y = 30 + i * 64
        szer = min(1.6, v / norma) * 300
        ok = v <= norma
        wiersze.append('<text class="p__n" x="0" y="%d">%s</text><rect class="p__tlo" x="140" y="%d" width="480" height="18" rx="9"/>'
                       '<rect class="p__pas%s" x="140" y="%d" width="%.1f" height="18" rx="9"/><line class="p__norma" x1="440" x2="440" y1="%d" y2="%d"/>'
                       '<text class="p__v" x="140" y="%d">%s %s · norma %s</text>'
                       % (y + 14, n, y, '' if ok else ' p__pas--ponad', y, szer, y - 6, y + 24, y + 42, pl(v, 2), j, pl(norma, 2 if norma < 1 else 0)))
    woda = ('<svg class="wykres wykres--woda" viewBox="0 0 640 220" role="img" aria-label="Badanie wody: %s">%s</svg>'
            % (e('; '.join('%s %s %s, norma %s' % (n, pl(v, 2), j, pl(no, 2)) for n, v, no, j in pz['woda'])), ''.join(wiersze)))
    przegl = ''.join('<li><span class="mono">%s</span>%s</li>' % (d, e(t)) for d, t in pz['przeglady'])
    tresc = f'''
<section id="glowa" class="glowa">
<div class="tlo tekstura-noc" aria-hidden="true"></div>
<div class="wrap glowa__uklad">
<div><p class="okruchy mono"><a href="/">AKWIFER</a> / paszport studni</p>
{split('Paszport studni', '<em>— dokument na lata.</em>', tag='h1')}
<p class="lead">Studnia jest pod ziemią i nikt jej więcej nie zobaczy. Paszport mówi, co w niej jest: od głębokości filtra po wynik badania wody i terminy przeglądów.</p></div>
<p class="glowa__liczba mono"><span>{pl(pz['glebokosc'], 0)}</span><small>m · przykład</small></p>
</div>
</section>

<section id="dokument" class="sek sek--paszport">
<div class="wrap">
<article class="paszport tekstura-dok" data-rv="mask">
<header class="paszport__g"><p class="mono">paszport studni · {pz['numer']} · odbiór {pz['data']}</p><p class="mono paszport__przyklad">PRZYKŁAD — dane wymyślone</p></header>
<dl class="paszport__dane">
<div><dt>gmina</dt><dd>{pz['gmina']}</dd></div><div><dt>głębokość</dt><dd class="mono">{pl(pz['glebokosc'], 1)} m</dd></div>
<div><dt>filtr</dt><dd class="mono">{pz['filtr']}</dd></div><div><dt>zwierciadło statyczne</dt><dd class="mono">{pl(pz['zw_stat'], 1)} m</dd></div>
<div><dt>zwierciadło przy pompowaniu</dt><dd class="mono">{pl(pz['zw_dyn'], 1)} m</dd></div><div><dt>wydajność z próby</dt><dd class="mono">{pl(pz['Q'], 1)} m³/h</dd></div>
<div><dt>pompa</dt><dd>{pz['pompa']}</dd></div><div><dt>zbiornik</dt><dd>{pz['zbiornik']}</dd></div>
</dl>
<h2 class="paszport__h">Badanie wody</h2>
{woda}
<p class="paszport__uwaga">Żelazo ponad normę to w Wielkopolsce częsty wynik — w paszporcie od razu widać, czy potrzebny jest odżelaziacz. Normy: Fe 0,2 mg/l, Mn 0,05 mg/l, azotany 50 mg/l.</p>
<h2 class="paszport__h">Przeglądy</h2><ol class="paszport__przegl">{przegl}</ol>
</article>
{notka('Paszport to <b>powód, żeby klient wrócił do Ciebie, a nie do konkurencji</b>: na pokrywie studzienki naklejka z kodem, w kodzie link do tej strony, na stronie Twój numer i data następnego przeglądu.')}
</div>
</section>

<section id="karta" class="sek sek--karta">
<div class="wrap sek__uklad">
<div class="sek__t"><h2 data-rv="up">Paszport zaczyna się od karty</h2><p class="key">Każdy paszport zaczyna się od karty zlecenia — tej samej, którą wypełniasz na stronie głównej.</p></div>
{karta(id_='k2', tryb='zwarta')}
</div>
</section>
'''
    return powloka('/paszport-studni/', 'Paszport studni — co dostajesz po wierceniu | AKWIFER (wzorzec)',
                   'Przykładowy paszport studni głębinowej: głębokość, filtr, zwierciadło, wydajność z próbnego pompowania, '
                   'badanie wody i terminy przeglądów.', tresc)


# ---------------------------------------------------------------- dla firm
def strona_dla_firm():
    kroki = [('klient', 'wieczorem, z telefonu'), ('karta', 'metry, zł, papiery'), ('SMS', 'na Twój numer'), ('Ty', 'oddzwaniasz')]
    o = ['<svg class="wykres wykres--droga" viewBox="0 0 900 200" role="img" aria-label="Droga zgłoszenia: klient, karta, SMS, Ty">']
    for i, (n, d) in enumerate(kroki):
        x = 20 + i * 220
        o.append('<g data-rv="up"><rect class="d__box%s" x="%d" y="50" width="180" height="96" rx="10"/><text class="d__n" x="%d" y="92">%s</text>'
                 '<text class="d__d" x="%d" y="120">%s</text></g>' % (' d__box--ak' if i == 1 else '', x, x + 18, n, x + 18, d))
        if i < 3:
            o.append('<path class="d__s" d="M%d 98 h28 m-8 -7 l8 7 l-8 7"/>' % (x + 186))
    o.append('</svg>')
    tresc = f'''
<section id="glowa" class="glowa">
<div class="tlo tekstura-noc" aria-hidden="true"></div>
<div class="wrap glowa__uklad">
<div><p class="okruchy mono"><a href="/">AKWIFER</a> / dla firm studniarskich</p>
{split('Strona, która', '<em>przyjmuje zlecenia.</em>', tag='h1')}
<p class="lead">To jest wzorzec. Firma jest fikcyjna, ale wszystko inne działa: wycena z danymi Twoich gmin, karta wysyłana SMS-em, podstrony gmin pod Google, paszport studni. Tak może wyglądać Twoja strona.</p>
<p><a class="btn btn--sygnal" href="/?wlasciciel=1">Obejrzyj stronę oczami właściciela {STRZALKA}</a></p></div>
<p class="glowa__liczba mono"><span>14</span><small>gmin z danymi PIG we wzorcu</small></p>
</div>
</section>

<section id="droga" class="sek sek--powiat">
<div class="wrap">
<div class="sek__t sek__t--waski"><h2>Droga jednego zgłoszenia</h2>
<p class="key">Klient z gminy pod Twoją bazą wypełnia kartę wieczorem, a rano masz SMS z gminą, celem, liczbą osób i widełkami, które już widział.</p></div>
<figure class="droga" data-seq="90">{''.join(o)}</figure>
<div class="droga__sms" data-sygnatura="karta"><p class="mono zgl__etyk">przykładowy SMS z karty</p><pre class="mono" data-sms-podglad>Dzień dobry, pytam o studnię głębinową.</pre></div>
</div>
</section>

<section id="rachunek" class="sek sek--karta">
<div class="wrap sek__uklad">
<div class="sek__t"><h2 data-rv="up">Twój rachunek</h2>
<p class="key">Wpisz swoje liczby — kalkulator nie zgaduje za Ciebie, tylko mnoży to, co znasz z własnej firmy.</p>
<p>Portale z zapytaniami pobierają opłatę za każde przekazane zapytanie; strona z własną wyceną zbiera te same zapytania bezpośrednio do Ciebie.</p></div>
<form class="kalk" data-kalk onsubmit="return false" aria-label="Kalkulator dla firmy">
<label><span>Zapytań z portali miesięcznie</span><input type="number" min="0" value="10" data-k-zap inputmode="numeric"></label>
<label><span>Koszt jednego zapytania w portalu (zł)</span><input type="number" min="0" value="30" data-k-koszt inputmode="numeric"></label>
<label><span>Ile zleceń z 10 zapytań</span><input type="number" min="0" max="10" value="2" data-k-konw inputmode="numeric"></label>
<label><span>Średnia wartość zlecenia (zł)</span><input type="number" min="0" value="15000" step="500" data-k-war inputmode="numeric"></label>
<dl class="kalk__wynik"><div><dt>wydajesz na zapytania rocznie</dt><dd class="mono" data-k-rok>—</dd></div>
<div><dt>jedno dodatkowe zlecenie miesięcznie to rocznie</dt><dd class="mono" data-k-jedno>—</dd></div></dl>
<p class="zrodlo">Wartości domyślne są przykładowe — zmień je na swoje. Kalkulator niczego nie zapisuje.</p>
</form>
</div>
</section>

<section id="co" class="sek sek--co">
<div class="tlo tekstura-noc" aria-hidden="true"></div>
<div class="wrap">
<h2 data-rv="mask">Co dostajesz</h2>
<p class="key">Stronę zrobioną pod Twoją firmę: Twoje gminy, Twoje zdjęcia, Twój numer — w tym samym układzie co ten wzorzec.</p>
<ul class="co__lista" data-seq="60">
<li><b>Wycena dla gmin</b><span>z danych PIG dla gmin, w których wiercisz</span></li>
<li><b>Karta zlecenia SMS-em</b><span>zgłoszenia z gminą, celem i widełkami</span></li>
<li><b>Podstrona na każdą gminę</b><span>pod lokalne wyszukiwania w Google</span></li>
<li><b>Mapa Twojego zasięgu</b><span>gminy, w których wiercisz, z danymi głębokości</span></li>
<li><b>Rachunek ogrodu</b><span>klient sam liczy, kiedy studnia się zwraca</span></li>
<li><b>Paszport studni</b><span>dokument dla klienta i powód, żeby wrócił</span></li>
<li><b>Twoje zdjęcia i opinie</b><span>z wizytówki Google; sesja przy wierceniu na życzenie</span></li>
<li><b>Demo za darmo</b><span>najpierw oglądasz swoją stronę, potem decydujesz</span></li>
</ul>
<p>Projekt: <a class="link" href="https://jurczakstudio.pl" rel="noopener">Jurczak Studio {STRZALKA}</a></p>
</div>
</section>
'''
    return powloka('/dla-firm/', 'Strona dla firmy studniarskiej, która przyjmuje zlecenia | Jurczak Studio',
                   'Wzorzec strony dla firm wiercących studnie: wycena z danymi PIG dla gmin, karta zlecenia SMS-em, '
                   'podstrony gmin, paszport studni. Demo za darmo.', tresc)


# ---------------------------------------------------------------- zapis
def sieroty(doc):
    czesci = re.split(r'(<script.*?</script>|<svg.*?</svg>|<pre.*?</pre>)', doc, flags=re.S)
    return ''.join(c if c.startswith(('<script', '<svg', '<pre')) else re.sub(r'(?<=[\s>(„])([aiouwzAIOUWZ]) (?=\S)', r'\1&nbsp;', c) for c in czesci)


def _ver():
    h = hashlib.md5()
    for p in ('assets/css/site.css', 'assets/js/site.js'):
        h.update((SITE / p).read_bytes())
    return h.hexdigest()[:8]


def main():
    global VER, FV
    for d in ('assets/css', 'assets/js', 'assets/img'):
        (SITE / d).mkdir(parents=True, exist_ok=True)
    css = brand.css_root() + (WZORCE / 'ruch' / 'ruch.css').read_text(encoding='utf-8') + (ROOT / 'src' / 'site.css').read_text(encoding='utf-8')
    dane_js = json.dumps({'gminy': GMINY, 'rynek': RYNEK, 'zuzycie': ZUZYCIE_OS, 'cele': {k: [n, m] for k, n, m in CELE},
                          'termin': F['termin'], 'tel': F['tel_e164'], 'wodociag': WODOCIAG, 'prad': PRAD_M3}, ensure_ascii=False)
    js = (WZORCE / 'ruch' / 'ruch.js').read_text(encoding='utf-8') + (ROOT / 'src' / 'site.js').read_text(encoding='utf-8').replace('__DANE__', dane_js)
    (SITE / 'assets/css/site.css').write_text(css, encoding='utf-8')
    (SITE / 'assets/js/site.js').write_text(js, encoding='utf-8')
    (SITE / 'favicon.svg').write_text(brand.FAVICON, encoding='utf-8')
    (SITE / 'assets/img/plansza-hero.svg').write_text(plansza_hero(), encoding='utf-8')
    (SITE / 'assets/img/plansza-woda.svg').write_text(plansza_woda(), encoding='utf-8')
    VER = _ver()
    FV = hashlib.md5((SITE / 'assets/css/fonts.css').read_bytes()).hexdigest()[:8]

    strony = {'/': strona_glowna(), '/paszport-studni/': strona_paszport(), '/dla-firm/': strona_dla_firm()}
    for g in GMINY:
        strony['/gmina/%s/' % g['slug']] = strona_gminy(g)
    produkowane = {s.strip('/') for s in strony if s != '/'}
    for idx in SITE.rglob('index.html'):
        rel = idx.parent.relative_to(SITE).as_posix()
        if rel != '.' and not rel.startswith('assets') and rel not in produkowane:
            shutil.rmtree(idx.parent)
            print('  usunięto osieroconą podstronę:', rel)
    for s, t in strony.items():
        p = SITE / s.strip('/') / 'index.html' if s != '/' else SITE / 'index.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(sieroty(t), encoding='utf-8')
    (SITE / '404.html').write_text(sieroty(powloka('/404.html', 'Nie ma takiej strony — AKWIFER', 'Brak strony.',
        '<section class="glowa"><div class="wrap"><h1>Tu nie ma wody.</h1><p class="lead">Ten adres nie istnieje. <a class="link" href="/">Wróć do wyceny</a>.</p></div></section>')), encoding='utf-8')
    naglowki = '/assets/*\n  Cache-Control: public, max-age=86400\n'
    if DEMO:
        naglowki = '/*\n  X-Robots-Tag: noindex, nofollow, noarchive, noimageindex\n' + naglowki
    (SITE / '_headers').write_text(naglowki, encoding='utf-8')
    (SITE / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
    slow = {s: len(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|svg|style).*?</\1>', ' ', t, flags=re.S))).split()) for s, t in strony.items()}
    print('%d adresów, v=%s · słowa: / %d, gmina min %d, paszport %d, dla-firm %d' % (
        len(strony), VER, slow['/'], min(v for k, v in slow.items() if k.startswith('/gmina')), slow['/paszport-studni/'], slow['/dla-firm/']))
    bramka = WZORCE / 'audyt' / 'audyt.py'
    if bramka.exists() and subprocess.run([sys.executable, str(bramka), str(ROOT)]).returncode:
        raise SystemExit('Bramka zamknięta — patrz lista wyżej.')


VER = FV = ''
if __name__ == '__main__':
    main()
