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

# Rachunek ogrodu (W6, F18). Cena wody: Aquanet, gospodarstwa domowe, 19.12.2025–18.12.2026.
WODOCIAG = {'woda': 6.27, 'scieki': 9.91,
            'zrodlo': 'taryfa Aquanet dla gospodarstw domowych, 19.12.2025–18.12.2026 (aquanet.pl)'}
PRAD_M3 = 0.40    # ZAŁOŻENIE: pompa 1,1 kW przy 3 m³/h ≈ 0,37 kWh/m³ × ok. 1,1 zł/kWh — pokazane na stronie
OGROD = {'m2': 300, 'dawka': 20, 'tygodnie': 20}   # ZAŁOŻENIA domyślne, edytowalne: l/m² na tydzień, tygodni sezonu

# Mapa (W7, F19): granice OSM (ODbL) z dane/00-gminy-granice.json; gminy bez danych PIG w zestawie
BEZ_DANYCH = {'kostrzyn': 'Kostrzyn', 'murowana-goslina': 'Murowana Goślina', 'pobiedziska': 'Pobiedziska',
              'puszczykowo': 'Puszczykowo'}

# v3 — Gwarancja przejrzystości (W10, F21). PRZYKŁADOWE zasady firmy fikcyjnej; wartości rynkowe tam, gdzie są.
GWARANCJA = [
    ('200 zł', 'za każdy metr ponad pakiet', 'Cenę metra znasz przed wierceniem. Nie rośnie, gdy wiertło idzie głębiej.'),
    ('+10 m', 'i telefon do Ciebie', 'Jeśli po 10 m ponad prognozę nie ma wody, zatrzymujemy się i dzwonimy. Dalej wiercimy tylko za Twoją zgodą.'),
    ('100 zł/m', 'za suchy otwór', 'Nie trafimy na wodę — płacisz tylko za metry, bez pompy, osprzętu i dojazdu.'),
    ('15 min', 'na oddzwonienie', 'Pn–sob 7–19. Kartę z SMS-a mamy przed oczami, kiedy dzwonimy.'),
]

# Pakiety (W10) — cena „od” = metry pakietu × 200 zł/m + osprzęt od 2 500 zł (rynek, F8). PRZYKŁAD.
PAKIETY = [
    {'slug': 'ogrod', 'nazwa': 'Ogród', 'do': 15, 'cel': 'nawadnianie',
     'co': ['wiercenie do 15 m', 'pompa do podlewania', 'zawór i przyłącze ogrodowe', 'karta otworu']},
    {'slug': 'dom', 'nazwa': 'Dom', 'do': 30, 'cel': 'dom',
     'co': ['wiercenie do 30 m — bez zgłoszeń', 'pompa głębinowa i hydrofor', 'próbne pompowanie', 'badanie wody', 'paszport studni']},
    {'slug': 'gleboko', 'nazwa': 'Głęboko', 'do': 60, 'cel': 'dom',
     'co': ['wiercenie do 60 m', 'projekt robót geologicznych', 'dokumentacja i pozwolenie wodnoprawne', 'pompa, hydrofor, badanie wody', 'paszport studni']},
]

# Przepisy 2026 (W11)
ABOLICJA = {'do': '2027-12-31', 'oplata': '6\u00a0601,67\u00a0zł', 'akt': 'Dz.U. 2026 poz. 1033, art. 524a — w mocy od 18.08.2026',
            'zrodlo': 'https://nieruchomosci.infor.pl/7635786,masz-niezgloszona-studnie-mozna-uniknac-oplaty-legalizacyjnej-i-kary.html'}
NIZOWKA = {'nr': '8/2026', 'miesiace': 'lipiec, sierpień i wrzesień 2026 (ostrzeżenia nr 6, 7 i 8/2026)',
           'zrodlo': 'https://www.pgi.gov.pl/psh/psh-2/aktualna-sytuacja-hydrogeologiczna/11982-ostrzezenie-hydrogeologiczne-psg-nr-8-2026/file.html'}
