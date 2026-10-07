# Lokalny generator kadrów AKWIFER

Generuje dwa kadry z `dane/zamowienie-obrazow.md` (`hero-wiertnica`, `woda-szklanka`) na Twoim PC:
po 4 warianty seedów, stykówka do porównania, wybrany wariant jest kopiowany do `zrodla/gen/`.

## 1. Instalacja (raz)
Dwuklik `generator\INSTALUJ.cmd`, albo ręcznie: `py -3 generator\instaluj.py`.

- najpierw pokaże sprzęt: GPU i VRAM z `nvidia-smi`, sterownik, RAM, wolne miejsce, Pythona;
- założy venv `C:\gen\venv` (inna ścieżka: `--venv D:\gen\venv`);
- zainstaluje torch z indeksu pytorch.org dobranego do sterownika: **≥ 570 → cu128** (RTX 50xx też),
  **≥ 525 → cu126**, brak NVIDII → CPU;
- doinstaluje diffusers, transformers, accelerate, sentencepiece, protobuf, pillow, psutil
  i na koniec sprawdzi, czy `torch.cuda.is_available()`.

Sam raport bez instalacji: `py -3 generator\instaluj.py --tylko-raport`.

## 2. Generowanie
Dwuklik `generator\GENERUJ.cmd`. Po skończeniu otworzy folder `zrodla\gen\warianty\`.

| VRAM | model (auto) | rozdzielczość bazowa → po upscale 1,5× | jakość |
|---|---|---|---|
| ≥ 12 GB | FLUX.1-schnell, bf16, `enable_model_cpu_offload()`, 4 kroki | hero 1536×864 → 2304×1296, woda 1024×1280 → 1536×1920 | najlepsza: fotorealizm, czyste tło |
| 8–11 GB | SDXL base + refiner, 40 kroków | 1344×768 → 2016×1152, 896×1120 → 1344×1680 | dobra; dłonie i drobna mechanika bywają krzywe |
| < 8 GB / CPU | SDXL-Turbo, 4 kroki | 768×432 → 1152×648, 512×640 → 768×960 | szkic: miękko, plastikowo, detale rozjechane |

Wymuszenie modelu: `GENERUJ.cmd --model sdxl` (`flux` / `sdxl` / `turbo`). Inne seedy: `--seedy 5 6 7 8`.
Jeden kadr: `--tylko hero`. Bez upscale: `--upscale 1`.

Do wiedzenia:
- **FLUX z offloadem potrzebuje ~32 GB RAM** (sam model to ~24 GB w bf16). Przy 16 GB Windows będzie
  swapował i jeden kadr może trwać kilka minut zamiast ~30–60 s. Instalator ostrzeże.
- Pierwsze uruchomienie pobiera model do `%USERPROFILE%\.cache\huggingface`: FLUX ~34 GB,
  SDXL z refinerem ~14 GB, Turbo ~7 GB.
- **Upscale to Lanczos z lekkim wyostrzeniem, nie AI.** Powiększa czysto, ale nie dorysuje detalu.
  `images.py` i tak bierze maks. 2200 px szerokości.
- **Prompty:** FLUX bierze pełny prompt z `zamowienie-obrazow.md`, więc zmiana promptu to edycja .md.
  SDXL i Turbo czytają tylko 77 tokenów, dlatego dostają skrót z `SKROT` w `gen.py` plus negatywny prompt
  (bez tekstu, logo i twarzy). Jeśli zmieniasz prompt w .md, popraw też `SKROT`.
- Każdy PNG ma w metadanych model, seed, prompt i rozmiar. Wariant da się odtworzyć.

## 3. Wybór i build
Obejrzyj `zrodla\gen\warianty\przeglad-*.jpg` (stykówki) albo pojedyncze PNG, potem:

    GENERUJ.cmd --wybierz hero=s23 woda=s11
    python images.py && python build.py

Bramka audytu w `build.py` musi przejść. Podpis „ilustracja poglądowa” build dodaje sam.
Do repo idą tylko wybrane `zrodla/gen/*.png`. Folder `warianty/` jest w `.gitignore`.

## Licencje i Hugging Face
- FLUX.1-schnell: Apache 2.0. SDXL base i refiner: CreativeML Open RAIL++-M. Oba są OK do użytku komercyjnego.
- **SDXL-Turbo: licencja niekomercyjna Stability AI.** Na stronę firmy klienta potrzebna byłaby
  ich licencja komercyjna. Traktuj go tylko jako szkic.
- **FLUX.1-schnell jest za bramką „auto”.** Trzeba być zalogowanym i raz kliknąć *Agree* na
  https://huggingface.co/black-forest-labs/FLUX.1-schnell. Akceptacja jest natychmiastowa. Potem w terminalu:
  `C:\gen\venv\Scripts\hf.exe auth login` i token (Read) wklejasz tylko tam.
  SDXL i Turbo działają bez logowania. Bez tego kroku `gen.py` zatrzyma się na 401/403 i wypisze tę instrukcję.
