# -*- coding: utf-8 -*-
"""AKWIFER — jednorazowe pobranie granic gmin (OpenStreetMap przez Nominatim, licencja ODbL).

    python mapa_pobierz.py     # zapisuje dane/00-gminy-granice.json; build.py czyta tylko ten plik

Gminy powiatu poznańskiego + Poznań. Cztery gminy bez danych PIG w zestawie (Kostrzyn, Murowana Goślina,
Pobiedziska, Puszczykowo) też pobieramy — mapa pokazuje je na szaro jako „brak danych”, żeby powiat był cały.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = 'JurczakStudio-akwifer/1.0 (strona wzorcowa; jednorazowe pobranie granic)'
GMINY = {
    'buk': 'gmina Buk', 'czerwonak': 'gmina Czerwonak', 'dopiewo': 'gmina Dopiewo', 'kleszczewo': 'gmina Kleszczewo',
    'komorniki': 'gmina Komorniki', 'kornik': 'gmina Kórnik', 'lubon': 'Luboń', 'mosina': 'gmina Mosina',
    'poznan': 'Poznań', 'rokietnica': 'gmina Rokietnica', 'steszew': 'gmina Stęszew', 'suchy-las': 'gmina Suchy Las',
    'swarzedz': 'gmina Swarzędz', 'tarnowo-podgorne': 'gmina Tarnowo Podgórne',
    'kostrzyn': 'gmina Kostrzyn', 'murowana-goslina': 'gmina Murowana Goślina', 'pobiedziska': 'gmina Pobiedziska',
    'puszczykowo': 'Puszczykowo',
}


def szukaj(q):
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({
        'q': q + ', województwo wielkopolskie', 'format': 'jsonv2', 'polygon_geojson': 1,
        'polygon_threshold': 0.0003, 'limit': 5})
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
        wyniki = json.load(r)
    for w in wyniki:
        if w.get('category') == 'boundary' and w['geojson']['type'] in ('Polygon', 'MultiPolygon'):
            return w
    raise SystemExit('brak granicy dla: ' + q)


def main():
    out = {}
    for slug, q in GMINY.items():
        w = szukaj(q)
        out[slug] = {'osm': '%s/%s' % (w['osm_type'], w['osm_id']), 'nazwa_osm': w['name'], 'geojson': w['geojson']}
        print('%-18s %-12s %s' % (slug, out[slug]['osm'], w['display_name'][:70]))
        time.sleep(1.2)   # zasady użycia Nominatim: max 1 zapytanie/s
    (ROOT / 'dane' / '00-gminy-granice.json').write_text(json.dumps(out, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
