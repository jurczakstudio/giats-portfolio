# -*- coding: utf-8 -*-
"""AKWIFER (strona wzorcowa) — pobranie krojów z Google Fonts do własnego hostingu.

Spectral (nagłówki, szeryf z kursywą — tekst mapy) + Onest (tekst) + IBM Plex Mono (rzędne, metry).
Zostawiamy tylko podzbiory `latin` i `latin-ext` (polskie znaki — sprawdzone 28.09.2026).
Uruchamiane raz na projekt.
"""
import os, re, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site/assets/fonts')
CSS = os.path.join(ROOT, 'site/assets/css/fonts.css')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36')
API = ('https://fonts.googleapis.com/css2'
       '?family=Spectral:ital,wght@0,300;0,400;0,500;1,300;1,400'
       '&family=Onest:wght@400;500;600'
       '&family=IBM+Plex+Mono:wght@400;500'
       '&display=swap')
KEEP = ('latin', 'latin-ext')


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=60).read()


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    os.makedirs(os.path.dirname(CSS), exist_ok=True)
    css = get(API).decode('utf-8')
    blocks = re.findall(r'(/\* (\S+) \*/\s*)?@font-face \{(.*?)\}', css, re.S)
    out, seen = [], {}
    for _, subset, body in blocks:
        if subset not in KEEP:
            continue
        fam = re.search(r"font-family: '([^']+)'", body).group(1)
        style = re.search(r'font-style: (\w+)', body).group(1)
        weight = re.search(r'font-weight: ([\d ]+)', body).group(1).strip()
        url = re.search(r'src: url\((\S+)\)', body).group(1)
        if url in seen:
            name = seen[url]
        else:
            name = '%s-%s%s-%s.woff2' % (fam.lower().replace(' ', '-'), weight.replace(' ', '-'), '-i' if style == 'italic' else '', subset)
            open(os.path.join(OUT, name), 'wb').write(get(url))
            seen[url] = name
            print('  %-32s %6.1f kB' % (name, os.path.getsize(os.path.join(OUT, name)) / 1024))
        rng = re.search(r'unicode-range: ([^;]+);', body).group(1)
        out.append(
            "@font-face {\n  font-family: '%s';\n  font-style: %s;\n  font-weight: %s;\n"
            "  font-display: swap;\n  src: url(../fonts/%s) format('woff2');\n"
            "  unicode-range: %s;\n}" % (fam, style, weight, name, rng))
    header = ('/* Kroje hostowane lokalnie — pobrane skryptem fonts.py z Google Fonts\n'
              '   (licencja OFL). Bez połączeń do fonts.googleapis.com. */\n')
    open(CSS, 'w', encoding='utf-8').write(header + '\n'.join(out) + '\n')
    print('%d plików -> %s' % (len(seen), CSS))


if __name__ == '__main__':
    main()
