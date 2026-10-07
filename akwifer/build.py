# -*- coding: utf-8 -*-
"""AKWIFER — strona wzorcowa zawodu „studnie głębinowe” (koncept LEJ). Firma fikcyjna.

    python fonts.py     # raz na projekt
    python build.py     # zawsze — na końcu bramka audyt.py

Dane: content.py. Paleta i skala: brand.py. CSS/JS źródłowe: src/. Plan: dane/01–07.
Techniki „okna” i tła z liniami w shaderze — za giats-portfolio (MIT, E. Giatsidis); kod własny.
"""
import hashlib
import html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import brand
from content import FIRMA as F, MODEL, RYNEK, CENNIK, ETAPY, PYTANIA_PROBA, PYTANIA_PRZEBIEG, PYTANIA_FORMAL

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
STRON = 5

STRZALKA = ('<svg class="ikona" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
SLUCHAWKA = ('<svg class="ikona" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" '
             'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>')


def pl(x, d=1):
    return ('%.*f' % (d, x)).replace('.', ',')


def split(*wiersze, tag='h2'):
    return '<%s data-rv="split">%s</%s>' % (tag, ' '.join('<span class="w"><i>%s</i></span>' % w for w in wiersze), tag)


def okno(n, etyk, cls=''):
    """Okno-otwór w arkuszu: przez nie widać żywą mapę wody (sygnatura). JS wycina dziurę w papierze
    i wpisuje odczyt głębokości zwierciadła z tego samego pola, które rysuje shader."""
    return ('<div class="okno %s" data-okno data-sygnatura="okno" data-rv="mask">'
            '<span class="okno__nr mono">otwór %s</span>'
            '<span class="okno__odczyt mono" data-odczyt aria-live="off">zwierciadło — m</span>'
            '<span class="okno__etyk">%s</span></div>' % (cls, n, e(etyk)))


def znak(n, opis):
    return '<p class="znak mono">%d / %d · %s</p>' % (n, STRON, e(opis))


def zadzwon(nad='Zadzwoń'):
    return ('<a class="btn btn--akcent" href="tel:%s">%s<span><small>%s · numer przykładowy</small> %s</span></a>'
            % (F['tel_e164'], SLUCHAWKA, e(nad), F['tel']))


def faq(pytania):
    return '<div class="faq">%s</div>' % ''.join(
        '<details><summary>%s</summary><p class="key">%s</p><p>%s</p></details>' % (e(q), e(a), e(b))
        for q, a, b in pytania)


# ---------------------------------------------------------------- model (to samo co w site.js)
def proba(Q_m3h, k, H=MODEL['H'], r=MODEL['r_studni']):
    """Dupuit (zwierciadło swobodne) + Sichardt: zwraca (s, R) albo None, gdy warstwa się odwodni."""
    Q = Q_m3h / 3600

    def f(s):
        R = max(3000 * s * math.sqrt(k), r * 1.01)
        return math.pi * k * (2 * H * s - s * s) / math.log(R / r) - Q
    lo, hi = 1e-4, H * .95
    if f(hi) < 0:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    s = (lo + hi) / 2
    return s, 3000 * s * math.sqrt(k)


# ---------------------------------------------------------------- rysunki
def przekroj_zwierciadla():
    """Dwa przekroje obok siebie: zwierciadło swobodne i napięte (F9). Rura po prawej, opisy po lewej."""
    def panel(x0, napiete):
        o = ['<g transform="translate(%d 0)">' % x0]
        o.append('<rect x="0" y="40" width="300" height="300" fill="var(--piasek)"/>')
        if napiete:
            o.append('<rect x="0" y="150" width="300" height="46" fill="var(--glina)"/>')
            o.append('<rect x="0" y="196" width="300" height="144" fill="var(--wodonosny)"/>')
            o.append('<line class="zw-linia" x1="0" x2="300" y1="196" y2="196"/>')
            o.append('<rect class="rura" x="236" y="30" width="16" height="250"/><rect class="filtr" x="236" y="230" width="16" height="50"/>')
            o.append('<rect class="woda-w-rurze" x="239" y="104" width="10" height="176"/>')
            o.append('<line class="zw-linia zw-linia--w" x1="200" x2="290" y1="104" y2="104"/>')
            o.append('<text x="10" y="100">woda w rurze</text><text x="10" y="118">— wyżej niż strop</text>'
                     '<text x="10" y="178">glina przykrywa</text><text x="10" y="224">strop warstwy</text>')
        else:
            o.append('<rect x="0" y="120" width="300" height="220" fill="var(--wodonosny)"/>')
            o.append('<line class="zw-linia zw-linia--w" x1="0" x2="300" y1="120" y2="120"/>')
            o.append('<rect class="rura" x="236" y="30" width="16" height="250"/><rect class="filtr" x="236" y="200" width="16" height="80"/>')
            o.append('<rect class="woda-w-rurze" x="239" y="120" width="10" height="160"/>')
            o.append('<text x="10" y="110">zwierciadło</text><text x="10" y="150">piasek z wodą</text>')
        o.append('<rect x="0" y="34" width="300" height="8" fill="var(--atrament)" opacity=".75"/>')
        o.append('<text class="panel-t" x="0" y="20">%s</text></g>' % ('napięte' if napiete else 'swobodne'))
        return ''.join(o)
    return ('<svg class="rys rys--zwierciadlo" viewBox="0 0 660 350" role="img" aria-label="Dwa przekroje: zwierciadło '
            'swobodne, w którym poziom wody w studni równa się stropowi wody, i zwierciadło napięte pod gliną, gdzie woda '
            'po nawierceniu podnosi się w rurze powyżej stropu warstwy">%s%s</svg>' % (panel(0, False), panel(360, True)))


def krzywa_depresji(id_='kd'):
    """Profil zwierciadła wokół studni z Dupuita: h(x)² = h_w² + Q·ln(x/r)/(π k) — aktualizowany przez JS."""
    W, Hpx = 640, 260
    return ('<svg class="rys rys--krzywa" id="%s" viewBox="0 0 %d %d" role="img" aria-label="Krzywa depresji: '
            'przekrój zwierciadła wody wokół pompowanej studni" data-krzywa>'
            '<rect x="0" y="30" width="%d" height="%d" fill="var(--wodonosny)" opacity=".55"/>'
            '<path class="kd__woda" d="" />'
            '<line class="kd__H" x1="0" x2="%d" y1="40" y2="40"/>'
            '<rect class="rura" x="%d" y="10" width="12" height="%d"/>'
            '<text class="kd__t" x="10" y="32">zwierciadło przed pompowaniem</text>'
            '<text class="kd__s mono" x="%d" y="80" data-kd-s>s = —</text>'
            '<text class="kd__R mono" x="%d" y="%d" data-kd-R>R = —</text>'
            '</svg>' % (id_, W, Hpx + 40, W, Hpx, W, W // 2 - 6, Hpx, W // 2 + 16, W - 150, Hpx + 30))


def karta_otworu():
    """Karta otworu — przykładowy profil (opis gruntu co warstwę), tak jak w dokumentacji po wierceniu."""
    warstwy = [(0, 0.4, '#6b5a48', 'gleba'), (0.4, 6.5, 'var(--piasek)', 'piasek drobny'),
               (6.5, 14.2, 'var(--glina)', 'glina piaszczysta'), (14.2, 26.0, 'var(--wodonosny)', 'piasek średni, wodonośny'),
               (26.0, 30.0, '#8a8f88', 'mułek — spąg')]
    ppm = 11
    o = ['<svg class="rys rys--karta przekroj" viewBox="0 0 520 %d" role="img" aria-label="Przykładowa karta otworu: '
         'gleba, piasek drobny do 6,5 m, glina piaszczysta do 14,2 m, piasek średni wodonośny do 26 m, mułek">' % (30 * ppm + 40)]
    for od, do, kol, n in warstwy:
        y0, h = 20 + od * ppm, (do - od) * ppm
        o.append('<rect x="70" y="%.1f" width="90" height="%.1f" fill="%s"/>' % (y0, h, kol))
        if od == 0 or (h > 14 and od >= 1):
            o.append('<text class="k__m" x="0" y="%.1f">%s m</text>' % (y0 + 5, pl(od)))
        if h > 14:
            o.append('<text class="k__n" x="180" y="%.1f">%s</text>' % (y0 + h / 2 + 5, e(n)))
    o.append('<text class="k__m" x="0" y="%.1f">30,0 m</text>' % (20 + 30 * ppm))
    o.append('<rect class="rura" x="108" y="10" width="14" height="%.1f"/>' % (26 * ppm))
    o.append('<rect class="filtr" x="108" y="%.1f" width="14" height="%.1f"/>' % (20 + 17 * ppm, 8 * ppm))
    o.append('<line class="zw-linia zw-linia--w" x1="60" x2="170" y1="%.1f" y2="%.1f"/>' % (20 + 9.6 * ppm, 20 + 9.6 * ppm))
    o.append('<text class="k__z" x="180" y="%.1f">zwierciadło ustalone 9,6 m</text>' % (20 + 9.6 * ppm - 8))
    o.append('<text class="k__z" x="180" y="%.1f">filtr 17–25 m</text>' % (20 + 21 * ppm + 22))
    o.append('</svg>')
    return ''.join(o)


def granica_30():
    ppm = 6
    o = ['<svg class="rys rys--granica przekroj" viewBox="0 0 560 %d" role="img" aria-label="Skala głębokości 0–60 m '
         'z granicą 30 m: do niej bez formalności, poniżej projekt robót geologicznych">' % (60 * ppm + 40)]
    o.append('<rect x="80" y="20" width="60" height="%d" fill="var(--piasek)"/>' % (30 * ppm))
    o.append('<rect x="80" y="%d" width="60" height="%d" fill="var(--wodonosny)"/>' % (20 + 30 * ppm, 30 * ppm))
    for m in range(0, 61, 10):
        y = 20 + m * ppm
        o.append('<text class="k__m" x="0" y="%d">%d m</text><line class="kreska" x1="66" x2="80" y1="%d" y2="%d"/>' % (y + 5, m, y, y))
    y = 20 + 30 * ppm
    o.append('<line class="zw-linia zw-linia--w" x1="60" x2="560" y1="%d" y2="%d"/>' % (y, y))
    o.append('<text class="k__z" x="160" y="%d">30 m — granica</text>' % (y - 10))
    o.append('<text class="k__n" x="160" y="%d">do 30 m i 5 m³/d: bez zgłoszeń</text>' % (20 + 15 * ppm))
    o.append('<text class="k__n" x="160" y="%d">głębiej: projekt, dokumentacja, pozwolenie</text>' % (20 + 45 * ppm))
    o.append('</svg>')
    return ''.join(o)


def plan_odleglosci():
    odl = [(5, 'granica działki'), (7.5, 'oś rowu przydrożnego'), (15, 'budynki inwentarskie'),
           (30, 'rozsączanie ścieków'), (70, 'nieszczelne zrzuty ścieków')]
    o = ['<svg class="rys rys--plan przekroj" viewBox="0 0 620 360" role="img" aria-label="Plan: minimalne odległości '
         'studni: %s">' % e('; '.join('%s m — %s' % (pl(a).replace(',0', ''), b) for a, b in odl))]
    cx, cy = 160, 180
    for r_, _ in reversed(odl):
        o.append('<circle class="plan__krag" cx="%d" cy="%d" r="%.1f"/>' % (cx, cy, 14 + r_ * 2.1 if r_ < 70 else 166))
    for i, (r_, n) in enumerate(odl):
        y = 52 + i * 62
        o.append('<text class="k__z" x="350" y="%d">%s m</text><text class="k__n" x="420" y="%d">%s</text>'
                 % (y, pl(r_).replace(',0', ''), y, e(n)))
    o.append('<circle cx="%d" cy="%d" r="8" fill="var(--izolinia)"/></svg>' % (cx, cy))
    return ''.join(o)


# ---------------------------------------------------------------- symulator
def symulator(id_, duzy=False):
    sup = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')

    def potega(k):
        m, w = ('%.0e' % k).split('e')
        return ('%s·10%s' % (m, str(int(w)).translate(sup))).replace('1·10', '10')
    opcje = ''.join('<option value="%g"%s>%s · k = %s m/s</option>'
                    % (k, ' selected' if i == 1 else '', e(n), potega(k))
                    for i, (n, k) in enumerate(MODEL['grunty']))
    s, R = proba(MODEL['Q_dom'], MODEL['grunty'][1][1])
    return f'''<form class="sym{' sym--duzy' if duzy else ''}" data-sym data-H="{MODEL['H']}" data-r="{MODEL['r_studni']}" aria-label="Model próby pompowania" onsubmit="return false">
<label class="sym__etyk" for="{id_}-q">Wydajność pompowania <b class="mono"><output data-q-out for="{id_}-q">{pl(MODEL['Q_dom'])}</output> m³/h</b></label>
<input class="sym__suwak" id="{id_}-q" type="range" min="{MODEL['Q_min']}" max="{MODEL['Q_max']}" step="0.1" value="{MODEL['Q_dom']}" data-q>
<label class="sym__etyk" for="{id_}-k">Grunt warstwy wodonośnej</label>
<select class="sym__grunt" id="{id_}-k" data-k>{opcje}</select>
<dl class="sym__wynik">
<div><dt>depresja s</dt><dd class="mono" data-s>{pl(s, 2)} m</dd></div>
<div><dt>promień leja R</dt><dd class="mono" data-rl>{pl(R, 0)} m</dd></div>
<div><dt>wydajność jednostkowa q</dt><dd class="mono" data-qj>{pl(MODEL['Q_dom'] / s, 1)} m³/h·m</dd></div>
</dl>
<p class="sym__uwaga" data-sym-uwaga hidden>Przy tej wydajności warstwa w modelu się odwadnia — studnia nie da tyle wody. W praktyce: mniejsza pompa albo inna warstwa.</p>
<p class="zrodlo mono">Q = π·k·(H² − h²) / ln(R/r) · R = 3000·s·√k · H = {pl(MODEL['H'], 0)} m, r = {pl(MODEL['r_studni'] * 1000, 0)} mm · model poglądowy, nie pomiar</p>
</form>'''


def karta_zgloszenia(id_):
    pola = [('miejsce', 'Miejscowość działki', 'text', 'np. gmina, wieś'), ('osoby', 'Ile osób w domu', 'number', '4')]
    znaczniki = [('ogrod', 'Podlewany ogród'), ('dojazd', 'Wiertnica dojedzie (szer. ok. 2,5 m)'),
                 ('prad', 'Jest prąd na działce'), ('szambo', 'Znam miejsce szamba / oczyszczalni')]
    p = ''.join('<label class="kz__pole" for="%s-%s"><span>%s</span><input id="%s-%s" name="%s" type="%s" placeholder="%s"%s></label>'
                % (id_, k, e(t), id_, k, k, typ, e(ph), ' min="1" max="20" inputmode="numeric"' if typ == 'number' else '')
                for k, t, typ, ph in pola)
    z = ''.join('<label class="kz__znak" for="%s-%s"><input id="%s-%s" name="%s" type="checkbox"><span>%s</span></label>'
                % (id_, k, id_, k, k, e(t)) for k, t in znaczniki)
    return f'''<form class="kz" data-kz aria-labelledby="{id_}-t" onsubmit="return false">
<p class="kz__t" id="{id_}-t"><span class="mono">karta zgłoszenia</span> Co wiesz o działce</p>
{p}{z}
<p class="kz__szac mono" data-kz-szac>Zużycie szacunkowe: — m³/d</p>
<pre class="kz__podglad mono" data-kz-podglad aria-live="polite">Dzień dobry, pytam o studnię głębinową.</pre>
<div class="kz__przyciski"><button class="btn btn--akcent" type="button" data-kz-kopiuj>Skopiuj zgłoszenie</button></div>
<p class="zrodlo">Na stronie klienta ten przycisk otwiera SMS na jego numer. Tutaj — wersja wzorcowa — tylko kopiuje treść.</p>
</form>'''


# ---------------------------------------------------------------- powłoka
NAV = [('/proba-pompowania/', 'Próba pompowania'), ('/przebieg/', 'Przebieg'), ('/formalnosci/', 'Formalności'),
       ('/kontakt/', 'Zgłoszenie')]


def powloka(sciezka, tytul, opis, tresc):
    nav = ''.join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if sciezka == u else '', n) for u, n in NAV)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'WebPage', 'name': tytul, 'description': opis,
                     'url': BASE + sciezka, 'isPartOf': {'@type': 'WebSite', 'name': 'AKWIFER — strona wzorcowa Jurczak Studio'}},
                    ensure_ascii=False)
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(tytul)}</title>
<meta name="description" content="{e(opis)}">
{'<meta name="robots" content="noindex,nofollow">' if DEMO else ''}
<link rel="canonical" href="{BASE + sciezka}">
<meta property="og:title" content="{e(tytul)}">
<meta property="og:description" content="{e(opis)}">
<meta name="theme-color" content="#f1ede3">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/spectral-300-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css?v={FV}">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
<script type="application/ld+json">{ld}</script>
<script src="/assets/js/site.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
<p class="wzor mono">strona wzorcowa · firma fikcyjna<span class="wzor__dlugie"> · Jurczak Studio</span></p>
<header class="nag">
<a class="nag__logo" href="/" aria-label="AKWIFER — strona główna">{brand.SYGNET}<span>AKWIFER</span></a>
<nav class="nag__menu" id="menu" aria-label="Główna">{nav}</nav>
<a class="nag__tel mono" href="tel:{F['tel_e164']}">{F['tel']}</a>
<button class="nag__przycisk" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
</header>
{'' if 'class="mapa"' in tresc else '<canvas class="mapa" aria-hidden="true"></canvas>'}
<main id="tresc">
{tresc}
</main>
<footer class="stopka arkusz">
<div class="wrap stopka__kol">
<div><p class="etyk mono">AKWIFER — studnie głębinowe</p><p>Firma fikcyjna. Telefon, godziny i cennik są przykładowe — do podmiany na dane klienta.</p><p class="mono">{F['tel']} · {F['godziny']} · {F['zasieg']}</p></div>
<div><p class="etyk mono">Strona</p><nav aria-label="Stopka"><a href="/">Mapa</a>{nav}</nav></div>
<div><p class="etyk mono">Źródła i licencje</p><p>Wzory: Dupuit, Sichardt (Uniwersytet Przyrodniczy w Poznaniu, hydraulika, wykład 8). Przepisy: Prawo wodne art. 395, Prawo budowlane art. 29, Pgig art. 3 pkt 2a. Ceny rynkowe: kb.pl, 08.2026.</p><p>Okna w treści i tło z liniami w shaderze — technika za giats.me (E. Giatsidis, MIT). Szum: S. Gustavson (MIT).</p></div>
</div>
</footer>
</body>
</html>
'''


# ---------------------------------------------------------------- strony
def strona_glowna():
    s, R = proba(MODEL['Q_dom'], MODEL['grunty'][1][1])
    etapy = ''.join('<li><span class="mono">%s</span><h3>%s</h3><p>%s</p></li>' % (e(m), e(n), e(t)) for m, n, t in ETAPY)
    cennik = ''.join('<tr><td>%s</td><td class="mono">%s</td><td class="mono">%s</td></tr>' % (e(a), e(b), e(c)) for a, b, c in CENNIK)
    r = RYNEK
    tresc = f'''
<section id="mapa" class="mapa-sek" data-hover>
<canvas class="mapa" aria-label="Mapa hydroizohips: linie jednakowej głębokości zwierciadła wody. Kursor działa jak pompa i tworzy lej depresji." role="img"></canvas>
<div class="mapa-sek__w">
<p class="kicker mono">AKWIFER · studnie głębinowe · strona wzorcowa zawodu</p>
{split('Każda studnia', '<em>zmienia mapę wody.</em>', tag='h1')}
<p class="lead">Linie pod tekstem to hydroizohipsy — poziomice zwierciadła wody podziemnej, co 25 cm. <b class="tylko-kursor">Rusz kursorem: pracuje pompa i wokół niej robi się lej depresji. Kliknij, żeby wywiercić studnię.</b><b class="tylko-dotyk">Przytrzymaj palec na mapie — pracuje pompa.</b></p>
<p class="mapa-sek__skala mono" aria-hidden="true"><span></span>10 m</p>
</div>
<p class="mapa-sek__legenda mono" aria-hidden="true"><span class="leg leg--l"></span> hydroizohipsa co 0,25 m <span class="leg leg--g"></span> co 1 m · lej z przewyższeniem ×3</p>
</section>

<section id="pompa" class="pompa arkusz" aria-label="Pompa na telefonie">
<p>Na telefonie nie ma kursora. Włącz pompę — lej rośnie przez kilka sekund, tak jak w czasie pompowania.</p>
<button class="btn btn--akcent btn--szeroki" type="button" data-pompuj>Włącz pompę na środku mapy</button>
<details><summary>Co widać na mapie?</summary><p>Poziomice głębokości zwierciadła wody. Im gęściej, tym szybciej zwierciadło opada — wokół pompy najszybciej.</p></details>
</section>

<section id="zwierciadlo" class="arkusz arkusz--z">
<div class="wrap arkusz__uklad">
<div class="arkusz__t">
{znak(1, 'okno w arkuszu')}
{split('Zwierciadło.', '<em>Woda ma kształt.</em>')}
<p class="key">Zwierciadło wody podziemnej nie jest płaskim „jeziorem pod ziemią” — to powierzchnia, która wznosi się i opada jak teren, a woda płynie nią w poprzek hydroizohips, od wyższych do niższych.</p>
<p>Bywa swobodne — wtedy poziom w studni to strop wody — albo napięte: warstwa leży pod gliną, a woda po nawierceniu podnosi się w rurze wyżej, niż ją nawiercono. Dlatego głębokość studni jest cechą miejsca, a nie obietnicą firmy.</p>
</div>
{okno(1, 'Przez otwór widać mapę, która leży pod całą stroną. Odczyt liczy się z tego samego pola (lej z przewyższeniem ×3).')}
</div>
<figure class="wrap arkusz__rys" data-rv="mask">{przekroj_zwierciadla()}<figcaption class="mono">zwierciadło swobodne i napięte — schemat</figcaption></figure>
</section>

<section id="proba" class="arkusz arkusz--p">
<div class="wrap arkusz__uklad arkusz__uklad--odwr">
{okno(2, 'Lej w tym otworze rośnie z suwakiem — to te same liczby, co w tabeli.', 'okno--duze okno--sym')}
<div class="arkusz__t">
<p class="znak mono">kulminacja · model próby pompowania</p>
<h2 data-rv="up">Próba. <em>Ile odda studnia, zanim się osuszy.</em></h2>
<p class="key">Próbne pompowanie daje dwie liczby — wydajność Q i depresję s — a z nich wychodzi wydajność jednostkowa i dobór pompy; tu możesz sprawdzić, jak zależą od gruntu.</p>
{symulator('s0')}
<a class="link" href="/proba-pompowania/">Krzywa depresji i tabela gruntów {STRZALKA}</a>
</div>
</div>
</section>

<section id="karta" class="arkusz arkusz--k">
<div class="wrap arkusz__uklad">
<figure class="arkusz__karta">{karta_otworu()}<figcaption class="mono">przykładowa karta otworu · 30 m</figcaption></figure>
<div class="arkusz__t">
{split('Karta otworu.', '<em>Sześć etapów, każdy na piśmie.</em>')}
<p class="key">Studnia głębinowa powstaje w sześciu krokach — od rozpoznania mapy po protokół pompowania — i po każdym zostaje dokument.</p>
<ol class="etapy" data-seq="70">{etapy}</ol>
</div>
</div>
</section>

<section id="rachunek" class="arkusz arkusz--r">
<div class="tlo tekstura-kratka" aria-hidden="true"></div>
<div class="wrap rach">
{split('Rachunek.', '<em>Przykład i rynek obok siebie.</em>')}
<p class="key">Na rynku wiercenie kosztuje {r['mb'][0]}–{r['mb'][1]} zł za metr, a studnia przydomowa 25–35 m z osprzętem 8–15 tys. zł.</p>
<table class="cennik" data-seq="60"><caption class="mono">cennik PRZYKŁADOWY — do podmiany na cennik klienta</caption>
<thead><tr><th>pozycja</th><th>jednostka</th><th>cena</th></tr></thead><tbody>{cennik}</tbody></table>
<p class="zrodlo mono">Rynek: {e(r['zrodlo'])} · pompa {r['pompa'][0]}–{r['pompa'][1]} zł · hydrofor {r['hydrofor'][0]}–{r['hydrofor'][1]} zł</p>
</div>
</section>

<section id="granica" class="arkusz arkusz--g">
<div class="wrap arkusz__uklad">
<div class="arkusz__t">
<h2 data-rv="up">Granica. <em>Trzydzieści metrów.</em></h2>
<p class="key">Studni do 30 m, z której pobierasz do 5 m³ wody na dobę na potrzeby domu, nie trzeba ani zgłaszać, ani uzyskiwać na nią pozwolenia.</p>
<p>Głębiej — projekt robót geologicznych zatwierdzony przez starostę, dokumentacja hydrogeologiczna i pozwolenie wodnoprawne. <a class="link" href="/formalnosci/">Szczegóły i odległości {STRZALKA}</a></p>
</div>
<figure class="arkusz__rys2" data-rv="mask">{granica_30()}</figure>
</div>
</section>

<section id="zgloszenie" class="arkusz arkusz--zg">
<div class="wrap arkusz__uklad arkusz__uklad--odwr">
{okno(3, 'Wróciliśmy na powierzchnię — mapa pod spodem ta sama.', 'okno--male')}
<div class="arkusz__t">
{split('Zgłoszenie.', '<em>Pięć rzeczy przed telefonem.</em>')}
<p class="key">Do wyceny wystarczy miejscowość, liczba osób i trzy odpowiedzi o działce — z nich wychodzi zapotrzebowanie na wodę i to, czy wiertnica dojedzie.</p>
{karta_zgloszenia('k0')}
{zadzwon()}
</div>
</div>
</section>
'''
    return powloka('/', 'Studnie głębinowe — jak działa studnia i ile odda wody | AKWIFER (strona wzorcowa)',
                   'Strona wzorcowa zawodu: żywa mapa hydroizohips, lej depresji pod kursorem i model próby pompowania '
                   '(Dupuit, Sichardt). Przebieg wiercenia, ceny rynkowe, formalności do 30 m.', tresc)


def glowa(kicker, wiersze, lead, liczba):
    return f'''<section id="glowa" class="glowa">
<div class="tlo tekstura-kratka" aria-hidden="true"></div>
<div class="wrap glowa__uklad">
<div><p class="kicker mono">{kicker}</p>{split(*wiersze, tag='h1')}<p class="lead">{lead}</p></div>
<p class="glowa__liczba mono" aria-hidden="true">{liczba}</p>
</div>
</section>'''


def strona_proba():
    tab = ''.join('<tr><td>%s</td><td class="mono">%s</td></tr>' % (e(n), e(k)) for n, k in [
        ('piasek gruboziarnisty', '≈ 10⁻⁴ m/s'), ('piasek', '≈ 10⁻⁵ m/s'), ('piasek zwarty', '≈ 10⁻⁶ m/s'),
        ('glina piaszczysta', '≈ 10⁻⁷ m/s'), ('glina', '≈ 10⁻⁸ m/s')])
    tresc = glowa('Próbne pompowanie · model', ('Ile wody odda studnia', '<em>— i skąd to wiadomo</em>'),
                  'Dwie liczby z pompowania i dwa wzory sprzed stu lat. Poniżej możesz nimi poruszać — '
                  'lej na mapie pod stroną liczy się z tych samych wartości.', 'Q/s') + f'''
<section id="symulator" class="arkusz arkusz--p">
<div class="wrap arkusz__uklad arkusz__uklad--odwr">
{okno(4, 'Lej depresji w tym otworze odpowiada suwakom obok.', 'okno--duze okno--sym')}
<div class="arkusz__t">
{znak(2, 'okno na lej')}
<h2>Model próby pompowania</h2>
<p class="key">Przy wydajności 2,5 m³/h w piasku średnim model daje depresję ok. 1,2 m i lej o promieniu ok. 25 m — w piasku gruboziarnistym ten sam pobór to ok. 0,5 m, a w drobnym warstwa w modelu się odwadnia.</p>
{symulator('s1', duzy=True)}
</div>
</div>
</section>

<section id="krzywa" class="arkusz arkusz--k">
<div class="wrap">
<h2>Krzywa depresji</h2>
<p class="key">Krzywa depresji to przekrój leja: zwierciadło opada najmocniej przy rurze i wypłaszcza się aż do promienia R, gdzie pompa przestaje mieć wpływ.</p>
<figure data-scrub>{krzywa_depresji()}<figcaption class="mono">h(x)² = h_w² + Q·ln(x/r)/(π·k) · skala pionowa przesadzona</figcaption></figure>
<p>Dlatego dwie studnie wiercone za blisko siebie zabierają sobie wodę: ich leje nakładają się i każda pompuje z głębszym zwierciadłem. Na mapie u góry widać to, gdy wywiercisz kliknięciem dwie studnie obok siebie.</p>
</div>
</section>

<section id="grunty" class="arkusz arkusz--r">
<div class="tlo tekstura-kratka" aria-hidden="true"></div>
<div class="wrap rach">
<h2>Grunt decyduje</h2>
<p class="key">Współczynnik filtracji k mówi, jak łatwo woda przepływa przez grunt — piasek gruboziarnisty przepuszcza ją sto razy szybciej niż zwarty.</p>
<table class="cennik" data-seq="60"><caption class="mono">orientacyjny współczynnik filtracji</caption><thead><tr><th>grunt</th><th>k</th></tr></thead><tbody>{tab}</tbody></table>
<p class="zrodlo mono">Uniwersytet Przyrodniczy w Poznaniu, hydraulika, wykład 8 (wartości w cm/s przeliczone na m/s)</p>
</div>
</section>

<section id="pytania" class="arkusz">
<div class="wrap"><h2>Pytania o pompowanie</h2>{faq(PYTANIA_PROBA)}</div>
</section>
'''
    return powloka('/proba-pompowania/', 'Próbne pompowanie studni — wzór Dupuita i lej depresji | AKWIFER (wzorzec)',
                   'Jak z próbnego pompowania wychodzi wydajność studni: model Dupuita i Sichardta, krzywa depresji, '
                   'współczynnik filtracji gruntów.', tresc)


def strona_przebieg():
    etapy = ''.join('<li><span class="mono">%02d · %s</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(m), e(n), e(t))
                    for i, (m, n, t) in enumerate(ETAPY))
    tresc = glowa('Przebieg wiercenia', ('Sześć etapów,', '<em>sześć dokumentów</em>'),
                  'Studnia jest pod ziemią i nikt jej potem nie zobaczy. Dlatego każdy etap zostawia ślad na papierze — '
                  'kartę otworu, konstrukcję, protokół pompowania.', '06') + f'''
<section id="karta" class="arkusz arkusz--k">
<div class="wrap arkusz__uklad">
<div class="arkusz__karta" data-scrub>{znak(3, 'okno w karcie otworu')}{okno(5, 'Pod kartą — ta sama mapa wody.', 'okno--male')}{karta_otworu()}</div>
<div class="arkusz__t">
<h2>Jak wygląda wiercenie studni głębinowej</h2>
<p class="key">Wiercenie studni to sześć etapów: rozpoznanie, wybór miejsca, wiercenie z próbkami, rura z filtrem, próbne pompowanie i odbiór z protokołem.</p>
<ol class="etapy" data-seq="70">{etapy}</ol>
</div>
</div>
</section>

<section id="na-dzialce" class="arkusz arkusz--r">
<div class="tlo tekstura-kratka" aria-hidden="true"></div>
<div class="wrap rach">
<h2 data-rv="up">Co zostaje na działce</h2>
<p class="key">Na powierzchni zostaje tylko pokrywa studzienki — reszta, czyli rura, filtr, pompa i przewód, jest pod ziemią i opisana w dokumentach.</p>
<ul class="inwentarz"><li><b>Rura z filtrem</b><span>filtr naprzeciw warstwy wodonośnej</span></li><li><b>Obsypka i uszczelnienie</b><span>żeby woda z góry nie spływała do studni</span></li><li><b>Pompa głębinowa</b><span>dobrana do wydajności z pompowania</span></li><li><b>Zbiornik i automatyka</b><span>ciśnienie w kranach</span></li><li><b>Studzienka z pokrywą</b><span>dostęp do głowicy</span></li><li><b>Protokół</b><span>Q, s, zwierciadło, filtr</span></li></ul>
</div>
</section>

<section id="pytania" class="arkusz">
<div class="wrap"><h2>Pytania o przebieg</h2>{faq(PYTANIA_PRZEBIEG)}</div>
</section>
'''
    return powloka('/przebieg/', 'Jak wygląda wiercenie studni głębinowej — 6 etapów | AKWIFER (wzorzec)',
                   'Etapy wiercenia studni: rozpoznanie, miejsce otworu, wiercenie z próbkami, rura i filtr, próbne '
                   'pompowanie, odbiór z protokołem. Jakie dokumenty dostajesz.', tresc)


def strona_formalnosci():
    lista = ['Głębokość do 30 m?', 'Pobór do 5 m³ na dobę (dom jednorodzinny — zwykle tak)?',
             'Woda na potrzeby domu, nie firmy?', 'Działka poza strefą ochronną ujęcia?',
             'Znasz granicę działki i miejsce szamba?']
    spr = ''.join('<label class="kz__znak"><input type="checkbox" name="f%d"><span>%s</span></label>' % (i, e(t)) for i, t in enumerate(lista))
    tresc = glowa('Formalności · studnia głębinowa', ('Do trzydziestu metrów', '<em>— bez urzędu</em>'),
                  'Granica jest jedna i liczbowa: 30 m głębokości i 5 m³ wody na dobę. Poniżej niej urząd niczego nie '
                  'wymaga, powyżej zaczyna się procedura.', '30 m') + f'''
<section id="trzydziesci" class="arkusz arkusz--g">
<div class="wrap arkusz__uklad">
<div class="arkusz__t" data-scrub>
{znak(4, 'okno na granicy')}
<h2>Czy studnię głębinową trzeba zgłaszać?</h2>
<p class="key">Studni do 30 m na potrzeby domu, z poborem do 5 m³ na dobę, nie trzeba zgłaszać ani uzyskiwać na nią pozwolenia.</p>
<p>Prawo wodne (art. 395) zwalnia z pozwolenia i zgłoszenia wodnoprawnego, Prawo budowlane (art. 29) z pozwolenia na budowę i zgłoszenia obudowy ujęcia, a Prawo geologiczne i górnicze (art. 3 pkt 2a) wyłącza taki otwór z robót geologicznych.</p>
{okno(6, 'Mapa wody nie zna granic działek — przepisy znają.', 'okno--male')}
</div>
<figure class="arkusz__rys2" data-rv="mask">{granica_30()}</figure>
</div>
</section>

<section id="lista" class="arkusz arkusz--zg">
<div class="wrap arkusz__uklad">
<div class="arkusz__t"><h2>Pięć pytań na tak</h2><p class="key">Jeśli na wszystkie odpowiadasz „tak”, studnia mieści się w limicie bez formalności.</p>{faq(PYTANIA_FORMAL)}</div>
<form class="kz kz--lista" data-seq="60" aria-label="Lista do sprawdzenia" onsubmit="return false">{spr}<p class="zrodlo">Lista zostaje na tym ekranie — nic nie jest wysyłane.</p></form>
</div>
</section>

<section id="odleglosci" class="arkusz arkusz--k">
<div class="wrap arkusz__uklad">
<div class="arkusz__t"><h2>Jak daleko od szamba i granicy?</h2>
<p class="key">Rozporządzenie o warunkach technicznych (§ 31) podaje dla studni m.in. 5 m od granicy działki i 30 m od miejsca rozsączania ścieków.</p>
<p>Przepisy przewidują wyjątki dla studni wierconych, ujmujących wodę spod nieprzepuszczalnej warstwy — miejsce otworu ustala się na działce, przed wierceniem.</p>
<p class="zrodlo mono">§ 31 WT wg muratordom.pl — sprawdź w aktualnym tekście rozporządzenia</p></div>
<figure class="arkusz__rys2" data-rv="mask">{plan_odleglosci()}</figure>
</div>
</section>
'''
    return powloka('/formalnosci/', 'Studnia głębinowa do 30 m bez zgłoszenia — formalności | AKWIFER (wzorzec)',
                   'Studnia do 30 m i 5 m³ na dobę: bez zgłoszenia i pozwolenia. Co powyżej 30 m, odległości od szamba '
                   'i granicy. Prawo wodne art. 395, Prawo budowlane art. 29.', tresc)


def strona_kontakt():
    tresc = glowa('Zgłoszenie · wycena', ('Pięć odpowiedzi', '<em>zamiast formularza</em>'),
                  'Firma studniarska nie potrzebuje od Ciebie danych osobowych, żeby oszacować studnię — potrzebuje '
                  'wiedzieć, gdzie jest działka i ile wody zużyjecie.', '5') + f'''
<section id="karta-zgloszenia" class="arkusz arkusz--zg">
<div class="wrap arkusz__uklad">
<div class="arkusz__t"><h2>Karta zgłoszenia</h2>
<p class="key">Z liczby osób wychodzi zapotrzebowanie: przyjmujemy ok. 0,1 m³ na osobę na dobę, a podlewany ogród dokłada drugie tyle w sezonie — obie liczby to przykład do podmiany przez firmę.</p>
{zadzwon()}</div>
{karta_zgloszenia('k1')}
</div>
</section>

<section id="okno" class="arkusz arkusz--k">
<div class="wrap arkusz__uklad arkusz__uklad--odwr">
{okno(7, 'Ostatni otwór. Pod całą stroną leżała ta sama mapa wody.', 'okno--duze')}
<div class="arkusz__t">{znak(5, 'ostatnie okno')}<h2>Pod każdą działką jest mapa</h2>
<p class="key">Każda działka leży na polu wody podziemnej, którego kształt opisują hydroizohipsy — studnia jest w nim jednym otworem, który zmienia je wokół siebie.</p>
<p>Ta strona jest wzorcem dla firm studniarskich: pokazuje fizykę zawodu zamiast zdjęć maszyn. U prawdziwego klienta do mapy dochodzą jego realizacje, opinie i numer telefonu.</p>
<a class="link" href="/">Wróć na mapę {STRZALKA}</a></div>
</div>
</section>
'''
    return powloka('/kontakt/', 'Zgłoszenie studni — co podać do wyceny | AKWIFER (strona wzorcowa)',
                   'Karta zgłoszenia studni głębinowej: miejscowość, liczba osób, ogród, dojazd, prąd. Szacunek '
                   'zużycia wody i gotowa treść zgłoszenia.', tresc)


# ---------------------------------------------------------------- zapis
def sieroty(doc):
    czesci = re.split(r'(<script.*?</script>|<svg.*?</svg>|<pre.*?</pre>)', doc, flags=re.S)
    return ''.join(c if c.startswith(('<script', '<svg', '<pre')) else
                   re.sub(r'(?<=[\s>(„])([aiouwzAIOUWZ]) (?=\S)', r'\1&nbsp;', c) for c in czesci)


def _ver():
    h = hashlib.md5()
    for p in ('assets/css/site.css', 'assets/js/site.js'):
        h.update((SITE / p).read_bytes())
    return h.hexdigest()[:8]


def main():
    global VER, FV
    (SITE / 'assets/css').mkdir(parents=True, exist_ok=True)
    (SITE / 'assets/js').mkdir(parents=True, exist_ok=True)
    css = (brand.css_root() + (WZORCE / 'ruch' / 'ruch.css').read_text(encoding='utf-8')
           + (ROOT / 'src' / 'site.css').read_text(encoding='utf-8'))
    js = ((WZORCE / 'ruch' / 'ruch.js').read_text(encoding='utf-8')
          + (ROOT / 'src' / 'site.js').read_text(encoding='utf-8'))
    (SITE / 'assets/css/site.css').write_text(css, encoding='utf-8')
    (SITE / 'assets/js/site.js').write_text(js, encoding='utf-8')
    (SITE / 'favicon.svg').write_text(brand.FAVICON, encoding='utf-8')
    VER = _ver()
    FV = hashlib.md5((SITE / 'assets/css/fonts.css').read_bytes()).hexdigest()[:8]

    strony = {'/': strona_glowna(), '/proba-pompowania/': strona_proba(), '/przebieg/': strona_przebieg(),
              '/formalnosci/': strona_formalnosci(), '/kontakt/': strona_kontakt()}
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
        glowa('404', ('Tu nie ma wody.',), 'Ten adres nie istnieje. <a class="link" href="/">Wróć na mapę</a>.', '404'))),
        encoding='utf-8')
    naglowki = '/assets/*\n  Cache-Control: public, max-age=86400\n'
    if DEMO:
        naglowki = '/*\n  X-Robots-Tag: noindex, nofollow, noarchive, noimageindex\n' + naglowki
    (SITE / '_headers').write_text(naglowki, encoding='utf-8')
    (SITE / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')

    slow = {s: len(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|svg|style).*?</\1>', ' ', t, flags=re.S))).split())
            for s, t in strony.items()}
    print('%d podstron, v=%s, DEMO=%s · słowa: %s' % (len(strony), VER, DEMO, ', '.join('%s %d' % kv for kv in slow.items())))
    bramka = WZORCE / 'audyt' / 'audyt.py'
    if bramka.exists() and subprocess.run([sys.executable, str(bramka), str(ROOT)]).returncode:
        raise SystemExit('Bramka zamknięta — patrz lista wyżej.')


VER = FV = ''
if __name__ == '__main__':
    main()
