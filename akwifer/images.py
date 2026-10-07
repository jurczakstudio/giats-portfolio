# -*- coding: utf-8 -*-
"""AKWIFER v2 — kadrowanie obrazów generowanych (Higgsfield) do WebP + manifest.json.

    python images.py     # po wrzuceniu plików do zrodla/gen/ (nazwy: dane/zamowienie-obrazow.md)

Brakujący plik = build użyje planszy zastępczej (SVG), więc strona działa bez zdjęć.
"""
import json
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'site' / 'assets' / 'img' / 'w'
GEN = ROOT / 'zrodla' / 'gen'

# slug: (plik, proporcja docelowa w/h, szerokości)
KADRY = {
    'hero': ('hero-wiertnica', 16 / 9, (800, 1400, 2200)),
    'hero-pion': ('hero-wiertnica', 4 / 5, (480, 900)),
    'woda': ('woda-szklanka', 4 / 5, (480, 900, 1300)),
}


def kadr(im, prop):
    w, h = im.size
    if w / h > prop:
        nw = round(h * prop)
        x = round((w - nw) * .62)          # wiertnica jest po prawej — kadr trzyma prawą stronę
        return im.crop((x, 0, x + nw, h))
    nh = round(w / prop)
    return im.crop((0, round((h - nh) * .4), w, round((h - nh) * .4) + nh))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    man = {}
    for slug, (plik, prop, szer) in KADRY.items():
        src = next((p for p in GEN.glob(plik + '.*') if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')), None)
        if not src:
            print('%-10s brak %s — zostaje plansza zastępcza' % (slug, plik))
            continue
        im = kadr(Image.open(src).convert('RGB'), prop)
        ws = []
        for w in szer:
            w = min(w, im.width)
            if w in ws:
                continue
            x = im.resize((w, round(w / prop)), Image.LANCZOS)
            if w < im.width * .7:
                x = x.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2))
            x.save(OUT / ('%s-%d.webp' % (slug, w)), 'WEBP', quality=80, method=6)
            ws.append(w)
        man[slug] = {'w': ws, 'ratio': round(1 / prop, 4)}
        print('%-10s %s → %s' % (slug, src.name, ws))
    (OUT / 'manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
