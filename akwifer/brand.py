# -*- coding: utf-8 -*-
"""AKWIFER — paleta, skala (tokeny --fs-*), sygnet. Decyzje: dane/04-kierunek.md."""

PALETA = {
    'papier': '#f1ede3',      # arkusz mapy (W5)
    'papier-2': '#e7e1d2',
    'papier-3': '#d8d0bc',
    'atrament': '#1a232b',    # tekst
    'olowek': '#4e5861',      # tekst drugi
    'izolinia': '#1f5f9e',    # JEDYNY akcent — hydroizohipsy (W1)
    'izolinia-jasna': '#9ab9d8',
    'glina': '#9b7a52',       # tylko w przekrojach
    'piasek': '#d9c7a0',
    'wodonosny': '#b9c6cf',
}

SKALA = {
    'fs-mini': '0.875rem',
    'fs-maly': '0.9375rem',
    'fs-tekst': '1.0625rem',
    'fs-lead': 'clamp(1.125rem, 1rem + .5vw, 1.375rem)',
    'fs-h3': 'clamp(1.25rem, 1.1rem + .7vw, 1.625rem)',
    'fs-h2': 'clamp(2rem, 1.3rem + 2.6vw, 3.5rem)',
    'fs-h1': 'clamp(2.75rem, 1.4rem + 5.4vw, 6.5rem)',
    'fs-liczba': 'clamp(2.5rem, 1.6rem + 3.6vw, 5rem)',
}


def css_root():
    linie = [':root {']
    linie += ['  --%s: %s;' % (k, v) for k, v in PALETA.items()]
    linie += ['  --%s: %s;' % (k, v) for k, v in SKALA.items()]
    linie += [
        "  --serif: 'Spectral', Georgia, serif;",
        "  --sans: 'Onest', system-ui, sans-serif;",
        "  --mono: 'IBM Plex Mono', ui-monospace, monospace;",
        '}', '']
    return '\n'.join(linie)


# Sygnet: trzy hydroizohipsy uginające się w lej wokół otworu.
SYGNET = ('<svg class="sygnet" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="#1f5f9e" stroke-width="1.6">'
          '<path d="M2 8c8 0 10 6 14 6s6-6 14-6"/><path d="M2 15c9 0 11 5 14 5s5-5 14-5"/>'
          '<path d="M2 22c9 0 12 3 14 3s5-3 14-3"/><circle cx="16" cy="27" r="2.2" fill="#1a232b" stroke="none"/></svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#f1ede3"/>'
           '<g fill="none" stroke="#1f5f9e" stroke-width="1.8"><path d="M2 8c8 0 10 6 14 6s6-6 14-6"/>'
           '<path d="M2 15c9 0 11 5 14 5s5-5 14-5"/><path d="M2 22c9 0 12 3 14 3s5-3 14-3"/></g>'
           '<circle cx="16" cy="27" r="2.2" fill="#1a232b"/></svg>')


def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def kontrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


if __name__ == '__main__':
    for t in ('atrament', 'olowek', 'izolinia'):
        for tlo in ('papier', 'papier-2'):
            print('%-9s na %-8s %.2f' % (t, tlo, kontrast(PALETA[t], PALETA[tlo])))
    print('papier na izolinia %.2f' % kontrast(PALETA['papier'], PALETA['izolinia']))
