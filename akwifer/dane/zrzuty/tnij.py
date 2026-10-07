# -*- coding: utf-8 -*-
"""Tnie zrzut całej strony na kawałki do obejrzenia: python dane/zrzuty/tnij.py plik.png N szer cel_prefix"""
import sys
from PIL import Image
plik, n, szer, cel = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
im = Image.open(plik); W, H = im.size; h = -(-H // n)
for i in range(n):
    c = im.crop((0, i * h, W, min(H, (i + 1) * h))); c.thumbnail((szer, 2400)); c.save('%s%d.png' % (cel, i))
