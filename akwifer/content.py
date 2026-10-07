# -*- coding: utf-8 -*-
"""AKWIFER v2 „ZLECENIE” — wyłącznie dane. Firma FIKCYJNA, dane gmin PRAWDZIWE (dane/00-gminy-pig.json, F13)."""
import json
from pathlib import Path

FIRMA = {
    'nazwa': 'AKWIFER — studnie głębinowe',
    'tel': '000 000 000',          # numer niemożliwy do wybrania — firma fikcyjna
    'tel_e164': '+48000000000',
    'godziny': 'pn–sob 7–19',      # PRZYKŁAD
    'baza': 'powiat poznański',
    'termin': 'listopad 2026 — 3 wolne dni',   # PRZYKŁAD — właściciel wpisuje sam
}

_SUROWE = json.loads((Path(__file__).parent / 'dane' / '00-gminy-pig.json').read_text(encoding='utf-8'))
# GZWP wycięte z opisu agregatora (tylko tam, gdzie go podał)
GMINY = []
for slug, g in sorted(_SUROWE.items(), key=lambda kv: kv[1]['mediana']):
    gz = ''
    if '(GZWP' in g['gzwp']:
        gz = ' '.join(g['gzwp'].split('zbiornika: ')[1].split()).replace(' )', ')')
    GMINY.append({'slug': slug, 'nazwa': g['nazwa'], 'mediana': g['mediana'], 'otworow': g['otworow'],
                  'min': g['najplytsze'], 'gzwp': gz})
SREDNIA_POWIATU = 52.5    # mapastudni.pl, „Średnia dla powiatu Poznań”
ZRODLO_PIG = 'rejestr PIG-PIB (Centralna Baza Danych Geologicznych) przez mapastudni.pl, dane z 08.06.2026'

# Rynek (F8, kb.pl 01.08.2026)
RYNEK = {'mb': (200, 350), 'osprzet': (2500, 8000)}   # osprzęt = pompa 1,5–5 tys. + hydrofor 1–3 tys.
ZUZYCIE_OS = 0.1   # m³ na osobę na dobę — przyjęte ok. 100 l (oznaczone na stronie jako założenie)

CELE = [('dom', 'Dom', 1.0), ('ogrod', 'Dom i ogród', 2.0), ('nawadnianie', 'Ogród / nawadnianie', 3.0)]

ETAPY = [
    ('Telefon albo karta', 'Dzwonisz albo wysyłasz kartę z tej strony. Oddzwaniamy z pytaniami o działkę — gmina i cel już są.'),
    ('Oględziny i papiery', 'Miejsce otworu, dojazd, odległości. Jeśli w Twojej gminie studnia wyjdzie ponad 30 m — przygotowujemy projekt robót geologicznych.'),
    ('Wiercenie', 'Zwykle jeden dzień na działce. Karta otworu: co metr opis gruntu.'),
    ('Próbne pompowanie', 'Stała wydajność, pomiar depresji — z tego dobór pompy, nie z katalogu.'),
    ('Odbiór i paszport', 'Pompa, zbiornik, studzienka, próbka wody do laboratorium. Dostajesz paszport studni.'),
]

PASZPORT = {   # PRZYKŁADOWY paszport (dane wymyślone, oznaczone)
    'numer': 'AKW-2026-041', 'gmina': 'Kórnik', 'data': '14.05.2026',
    'glebokosc': 62.0, 'filtr': '54–60 m', 'zw_stat': 18.4, 'zw_dyn': 21.9, 'Q': 3.0,
    'pompa': 'pompa głębinowa 4″, 1,1 kW', 'zbiornik': 'hydrofor 100 l',
    'woda': [('żelazo', 0.38, 0.2, 'mg/l'), ('mangan', 0.04, 0.05, 'mg/l'), ('azotany', 6.0, 50, 'mg/l')],
    'przeglady': [('2027-05', 'kontrola ciśnienia w zbiorniku'), ('2028-05', 'przegląd pompy, pomiar zwierciadła'),
                  ('2029-05', 'badanie wody')],
}
