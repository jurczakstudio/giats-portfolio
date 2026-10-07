# -*- coding: utf-8 -*-
"""AKWIFER — wyłącznie dane. Firma FIKCYJNA (strona wzorcowa zawodu). Źródła: dane/01-fakty.json."""

FIRMA = {
    'nazwa': 'AKWIFER — studnie głębinowe',
    'krotka': 'AKWIFER',
    'tel': '600 000 000',          # PRZYKŁAD — oznaczony na stronie
    'tel_e164': '+48600000000',
    'godziny': 'pn–sob 7–19',      # PRZYKŁAD
    'zasieg': 'do 60 km od bazy',  # PRZYKŁAD
}

# Model próby pompowania (F3–F6). Jednostki SI.
MODEL = {
    'r_studni': 0.0625,        # m — otwór 125 mm
    'H': 12.0,                 # m — miąższość warstwy nad spągiem (przykład)
    'grunty': [                # (etykieta, k m/s) — F6, UP Poznań wykład 8
        ('piasek drobny', 1e-5),
        ('piasek średni', 5e-5),
        ('piasek gruboziarnisty', 1e-4),
        ('piasek ze żwirem', 5e-4),
    ],
    'Q_min': 0.5, 'Q_max': 8.0, 'Q_dom': 2.5,   # m³/h
}

RYNEK = {'mb': (200, 350), 'pompa': (1500, 5000), 'hydrofor': (1000, 3000),
         'zrodlo': 'kb.pl, „Wiercenie studni głębinowej w 2026 roku”, 1 sierpnia 2026'}

# Cennik PRZYKŁADOWY (do podmiany na cennik klienta) — wartości mieszczą się w widełkach rynku F8.
CENNIK = [
    ('Wiercenie Ø 125 mm, piaski', 'za metr', '240 zł'),
    ('Rura PVC z filtrem szczelinowym', 'za metr', 'w cenie wiercenia'),
    ('Pompa głębinowa 1,1 kW z montażem', 'komplet', '2 900 zł'),
    ('Zbiornik hydroforowy 100 l + automatyka', 'komplet', '1 900 zł'),
    ('Studzienka z pokrywą i wyprowadzenie do 10 m', 'komplet', '1 600 zł'),
    ('Próbne pompowanie z protokołem', 'za otwór', 'w cenie'),
]

ETAPY = [
    ('0 m', 'Rozpoznanie', 'Mapa hydrogeologiczna arkusza, otwory w okolicy z bazy PIG, rozmowa o zużyciu wody. Z tego bierze się przewidywana głębokość — zanim ktokolwiek wjedzie na działkę.'),
    ('0 m', 'Miejsce otworu', 'Odległość od granicy, szamba i budynków; dojazd dla wiertnicy. Miejsca nie wybiera się „gdzie wygodnie”, tylko tam, gdzie przepisy i grunt pozwalają.'),
    ('0 → strop', 'Wiercenie i próbki', 'Co metr albo przy każdej zmianie gruntu próbka urobku do karty otworu. Karta to dowód, przez co wiercono — dostajesz ją po robocie.'),
    ('strop → spąg', 'Rura i filtr', 'Filtr staje naprzeciw najlepiej przepuszczalnej warstwy, obsypka żwirowa wokół, uszczelnienie nad warstwą wodonośną — żeby woda z góry nie spływała do studni.'),
    ('cała głębokość', 'Próbne pompowanie', 'Pompowanie ze stałą wydajnością i pomiar depresji: z Q i s wynika wydajność jednostkowa i dobór pompy. Tę liczbę dostajesz na piśmie.'),
    ('0 m', 'Pompa, zbiornik, odbiór', 'Pompa dobrana do wydajności studni, nie odwrotnie. Próbka wody do laboratorium i protokół: głębokość, filtr, zwierciadło, Q, s.'),
]

PYTANIA_PROBA = [
    ('Po co próbne pompowanie, skoro woda leci?',
     'Bo „leci” nie mówi, ile studnia odda bez osuszenia — dopiero stała wydajność Q i zmierzona depresja s pozwalają dobrać pompę.',
     'Z tych dwóch liczb wychodzi wydajność jednostkowa q = Q/s. Pompa większa niż możliwości studni będzie ją osuszać i pracować na sucho.'),
    ('Czy ten symulator mówi, ile da moja studnia?',
     'Nie — to model poglądowy: wzór Dupuita dla zwierciadła swobodnego i promień leja ze wzoru Sichardta, przy założonej miąższości warstwy 12 m.',
     'Prawdziwy wynik daje dopiero pompowanie na działce. Model pokazuje zależności: ten sam pobór w drobnym piasku robi dużo głębszy lej niż w żwirze.'),
    ('Czym jest lej depresji?',
     'To obniżenie zwierciadła wody wokół pompowanej studni — najgłębsze przy rurze, coraz płytsze aż do promienia R, gdzie znika.',
     'Na mapie hydroizohips widać go jako koncentryczne linie wokół otworu. Dwie studnie zbyt blisko siebie mają nakładające się leje i odbierają sobie wodę.'),
]

PYTANIA_PRZEBIEG = [
    ('Co dostanę na piśmie po wierceniu?',
     'Kartę otworu (przez jakie warstwy wiercono), opis konstrukcji studni (rura, filtr, głębokości) i protokół próbnego pompowania (Q, s, zwierciadło).',
     'To dokumenty, które przydadzą się przy każdej wymianie pompy i każdym serwisie — także u innej firmy.'),
    ('Ile metrów będzie miała studnia?',
     'Tyle, ile wynika z budowy warstw w tym miejscu — średnie głębokości ujęć różnią się między zbiornikami wód podziemnych od 30 do 60 m.',
     'Przykładowo: GZWP 138 (pradolina Toruń–Eberswalde) — średnio 30 m, GZWP 141 (dolna Wisła) — 40 m, GZWP 144 (Wielkopolska Dolina Kopalna) — 60 m.'),
    ('Czy wodę trzeba badać?',
     'Tak — po wykonaniu studni próbka idzie do laboratorium, bo żelaza i manganu nie widać, dopóki nie zabrudzą armatury.',
     'Od wyniku zależy, czy potrzebny jest odżelaziacz, zmiękczacz albo lampa UV.'),
]

PYTANIA_FORMAL = [
    ('Czy studnię do 30 m trzeba zgłaszać?',
     'Nie — studnia do 30 m na potrzeby domu, z poborem do 5 m³ na dobę, nie wymaga ani zgłoszenia, ani pozwolenia.',
     'Podstawa: Prawo wodne art. 395, Prawo budowlane art. 29, Prawo geologiczne i górnicze art. 3 pkt 2a.'),
    ('A głębiej niż 30 m?',
     'Głębiej potrzebny jest projekt robót geologicznych zatwierdzony przez starostę przed wierceniem, dokumentacja hydrogeologiczna po nim i pozwolenie wodnoprawne.',
     'To samo dotyczy płytszej studni dla działalności gospodarczej albo poboru ponad 5 m³ na dobę.'),
]
