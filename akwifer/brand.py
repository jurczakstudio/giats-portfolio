# -*- coding: utf-8 -*-
"""AKWIFER v2 „ZLECENIE” — paleta, skala (tokeny --fs-*), sygnet. Decyzje: dane/04-kierunek.md."""

PALETA = {
    'noc': '#0e1316',        # tło — zmierzch (W5)
    'noc-2': '#161d21',
    'noc-3': '#222b30',
    'kosc': '#ece6da',       # tekst
    'popiol': '#a7a69f',     # tekst drugi
    'sygnal': '#ff6b2c',     # JEDYNY akcent — lampy robocze wiertnicy (W1, W4)
    'woda': '#7cc4d6',       # barwa informacyjna danych (W2), nigdy przycisk
    'notka': '#f3d9a4',      # notki właściciela (W5)
}

SKALA = {
    'fs-mini': '0.875rem',
    'fs-maly': '0.9375rem',
    'fs-tekst': '1.0625rem',
    'fs-lead': 'clamp(1.125rem, 1rem + .45vw, 1.35rem)',
    'fs-h3': 'clamp(1.3rem, 1.1rem + .8vw, 1.75rem)',
    'fs-h2': 'clamp(2.25rem, 1.4rem + 3.2vw, 4.25rem)',
    'fs-h1': 'clamp(3rem, 1.6rem + 6vw, 7.5rem)',
    'fs-liczba': 'clamp(2rem, 1.4rem + 2.6vw, 3.5rem)',
    'fs-gigant': 'clamp(5rem, 2rem + 14vw, 15rem)',
}


def css_root():
    linie = [':root {']
    linie += ['  --%s: %s;' % (k, v) for k, v in PALETA.items()]
    linie += ['  --%s: %s;' % (k, v) for k, v in SKALA.items()]
    linie += ["  --sans: 'Archivo', system-ui, sans-serif;",
              "  --serif: 'Source Serif 4', Georgia, serif;",
              "  --mono: 'DM Mono', ui-monospace, monospace;", '}', '']
    return '\n'.join(linie)


# Sygnet: rura studni z kroplą — prosty, czytelny w 16 px.
SYGNET = ('<svg class="sygnet" viewBox="0 0 32 32" aria-hidden="true"><rect x="13" y="2" width="6" height="20" rx="1" fill="#ece6da"/>'
          '<path d="M16 19c3 4 5 6.4 5 8.4a5 5 0 0 1-10 0c0-2 2-4.4 5-8.4z" fill="#ff6b2c"/></svg>')
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0e1316"/>'
           '<rect x="13" y="3" width="6" height="18" rx="1" fill="#ece6da"/>'
           '<path d="M16 18c3 4 5 6.4 5 8.4a5 5 0 0 1-10 0c0-2 2-4.4 5-8.4z" fill="#ff6b2c"/></svg>')


def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def kontrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


if __name__ == '__main__':
    for t in ('kosc', 'popiol', 'sygnal', 'woda', 'notka'):
        for tlo in ('noc', 'noc-2', 'noc-3'):
            print('%-7s na %-6s %.2f' % (t, tlo, kontrast(PALETA[t], PALETA[tlo])))
    print('noc na sygnal %.2f' % kontrast(PALETA['noc'], PALETA['sygnal']))
