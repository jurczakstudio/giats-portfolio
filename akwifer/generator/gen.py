# -*- coding: utf-8 -*-
"""AKWIFER — lokalny generator kadrów (FLUX.1-schnell / SDXL / SDXL-Turbo przez diffusers).

    C:\\gen\\venv\\Scripts\\python generator\\gen.py                     # oba kadry, 4 seedy, model wg VRAM
    ...\\python generator\\gen.py --tylko hero --seedy 7 8 9 10
    ...\\python generator\\gen.py --model sdxl                          # wymuś model (flux | sdxl | turbo)
    ...\\python generator\\gen.py --wybierz hero=s3 woda=s1             # kopiuj wybrane warianty

Prompty czyta z dane/zamowienie-obrazow.md (blok „PROMPT DO SKOPIOWANIA”), więc zmiana promptu = edycja .md.
Warianty → zrodla/gen/warianty/<plik>-s<seed>.png + przeglad-<plik>.jpg (stykówka do porównania).
Wybrany wariant → zrodla/gen/<plik>.png; dalej: python images.py && python build.py.
"""
import argparse
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # akwifer/
ZAMOWIENIE = ROOT / 'dane' / 'zamowienie-obrazow.md'
GEN = ROOT / 'zrodla' / 'gen'
WARIANTY = GEN / 'warianty'

MODELE = {
    'flux': 'black-forest-labs/FLUX.1-schnell',            # Apache 2.0
    'sdxl': 'stabilityai/stable-diffusion-xl-base-1.0',    # + refiner, CreativeML Open RAIL++-M
    'turbo': 'stabilityai/sdxl-turbo',                     # licencja niekomercyjna SAI — patrz README
}
REFINER = 'stabilityai/stable-diffusion-xl-refiner-1.0'

# kadr: (plik, {model: (szer, wys)}) — wymiary podzielne przez 16, natywne „kubełki” modeli
KADRY = {
    'hero': ('hero-wiertnica', {'flux': (1536, 864), 'sdxl': (1344, 768), 'turbo': (768, 432)}),
    'woda': ('woda-szklanka', {'flux': (1024, 1280), 'sdxl': (896, 1120), 'turbo': (512, 640)}),
}
# FLUX nie ma negatywnego promptu — zakazy są w treści promptu; dla SDXL dokładamy je tutaj
NEGATYW = ('text, letters, caption, watermark, logo, signature, brand name, face, portrait, person looking at camera, '
           'deformed hands, extra fingers, cartoon, illustration, 3d render, oversaturated, blurry, lowres')
# SDXL/Turbo czytają przez CLIP tylko 77 tokenów — pełny prompt z .md urwałby się w połowie (tło, światło).
# Te skróty niosą to samo, w kolejności ważności. FLUX (T5, 256 tokenów) bierze pełny prompt z zamówienia.
SKROT = {
    'hero-wiertnica': 'cinematic photo, blue hour, flat rural building plot in western Poland, compact orange '
                      'trailer-mounted water well drilling rig on the right third, mast raised, warm work lights, '
                      'unfinished grey block house behind, low mist over ploughed fields, poplars on horizon, '
                      'deep blue sky fading to amber, empty dark field on the left, 35mm film grain, realistic',
    'woda-szklanka': 'product photo, early morning backlight, weathered hand holding clear glass under small brass '
                     'tap on black PVC well head pipe, crystal-clear water pouring, droplets, bubbles, dark '
                     'out-of-focus garden at dawn, cold blue background, warm golden light on glass, 85mm macro, realistic',
}
SEEDY = [11, 23, 37, 41]
UPSCALE = 1.5


def prompty():
    """{plik: prompt} z zamówienia — tekst między „PROMPT DO SKOPIOWANIA:” a „Jeśli wyjdzie źle”."""
    md = ZAMOWIENIE.read_text(encoding='utf-8')
    wynik = {}
    for blok in md.split('ZAMÓWIENIE OBRAZU')[1:]:
        plik = re.search(r'`([\w-]+)\.png`', blok)
        tresc = re.search(r'PROMPT DO SKOPIOWANIA:\s*\n(.*?)\n\s*Jeśli wyjdzie', blok, re.S)
        if plik and tresc:
            wynik[plik.group(1)] = ' '.join(tresc.group(1).split())
    for plik, _ in KADRY.values():
        if plik not in wynik:
            raise SystemExit('Nie znalazłem promptu dla %s w %s' % (plik, ZAMOWIENIE))
    return wynik


def dobierz_model(torch):
    if not torch.cuda.is_available():
        return 'turbo', 0.0
    vram = torch.cuda.get_device_properties(0).total_memory / 2 ** 30
    if vram >= 11.5:                     # karty „12 GB” raportują ~11.9
        return 'flux', vram
    if vram >= 7.5:
        return 'sdxl', vram
    return 'turbo', vram


def blad_hf(e, repo):
    nazwa = type(e).__name__
    if 'Gated' in nazwa or 'gated' in str(e).lower() or '401' in str(e) or '403' in str(e):
        raise SystemExit('\nModel %s wymaga akceptacji licencji / logowania na Hugging Face.\n'
                         '1) wejdź na https://huggingface.co/%s i zaakceptuj warunki,\n'
                         '2) w tym oknie: %s auth login   (starsze wersje: huggingface-cli login)\n'
                         '   i wklej token TYLKO tam — nigdzie indziej.\n'
                         % (repo, repo, Path(sys.executable).with_name('hf')))
    raise e


def zaladuj(model, torch):
    import diffusers
    cuda = torch.cuda.is_available()
    try:
        if model == 'flux':
            pipe = diffusers.FluxPipeline.from_pretrained(MODELE['flux'], torch_dtype=torch.bfloat16)
            if cuda:
                pipe.enable_model_cpu_offload()
                pipe.vae.enable_tiling()
            return pipe, None
        dtype = torch.float16 if cuda else torch.float32
        kw = {'torch_dtype': dtype, 'use_safetensors': True}
        if cuda:
            kw['variant'] = 'fp16'
        pipe = diffusers.AutoPipelineForText2Image.from_pretrained(MODELE[model], **kw)
        ref = None
        if model == 'sdxl':
            ref = diffusers.StableDiffusionXLImg2ImgPipeline.from_pretrained(
                REFINER, text_encoder_2=pipe.text_encoder_2, vae=pipe.vae, **kw)
        for p in (pipe, ref):
            if p is None:
                continue
            if cuda:
                p.enable_model_cpu_offload()
                p.vae.enable_tiling()
        return pipe, ref
    except Exception as e:  # noqa: BLE001 — rozpoznajemy błędy dostępu HF, resztę przepuszczamy
        blad_hf(e, MODELE[model] if 'refiner' not in str(e) else REFINER)


def generuj(model, pipe, ref, prompt, w, h, seed, torch, kroki=None):
    g = torch.Generator('cpu').manual_seed(seed)
    if model == 'flux':
        return pipe(prompt, width=w, height=h, num_inference_steps=kroki or 4, guidance_scale=0.0,
                    max_sequence_length=256, generator=g).images[0]
    if model == 'turbo':
        return pipe(prompt, width=w, height=h, num_inference_steps=kroki or 4, guidance_scale=0.0, generator=g).images[0]
    lat = pipe(prompt, negative_prompt=NEGATYW, width=w, height=h, num_inference_steps=kroki or 40, guidance_scale=6.0,
               denoising_end=0.8, output_type='latent', generator=g).images
    return ref(prompt, negative_prompt=NEGATYW, image=lat, num_inference_steps=kroki or 40, denoising_start=0.8,
               generator=g).images[0]


def podbij(im, skala):
    """Upscale Lanczos + lekki unsharp. To nie jest AI-upscaler — nie dorysuje detalu, tylko powiększy czysto."""
    from PIL import ImageFilter
    if skala <= 1:
        return im
    x = im.resize((round(im.width * skala), round(im.height * skala)), resample=3)   # 3 = LANCZOS
    return x.filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=3))


def stykowka(plik, sciezki):
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert('RGB') for p in sciezki]
    w = 640
    mini = [i.resize((w, round(i.height * w / i.width)), resample=3) for i in ims]
    h = max(m.height for m in mini)
    sheet = Image.new('RGB', (w * 2 + 30, (h + 40) * ((len(mini) + 1) // 2) + 10), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for n, (m, p) in enumerate(zip(mini, sciezki)):
        x, y = 10 + (n % 2) * (w + 10), 10 + (n // 2) * (h + 40)
        sheet.paste(m, (x, y))
        d.text((x, y + m.height + 8), p.stem, fill=(230, 230, 230))
    out = WARIANTY / ('przeglad-%s.jpg' % plik)
    sheet.save(out, quality=88)
    return out


def wybierz(pary):
    for para in pary:
        if '=' not in para:
            raise SystemExit('Format: --wybierz hero=s23 woda=s11 (s<seed> z nazwy wariantu)')
        kadr, war = para.split('=', 1)
        if kadr not in KADRY:
            raise SystemExit('Nieznany kadr %s (są: %s)' % (kadr, ', '.join(KADRY)))
        plik = KADRY[kadr][0]
        war = war if war.startswith('s') else 's' + war
        src = WARIANTY / ('%s-%s.png' % (plik, war))
        if not src.exists():
            raise SystemExit('Brak %s — dostępne: %s' % (src.name, ', '.join(p.name for p in WARIANTY.glob(plik + '-s*.png'))))
        dst = GEN / (plik + '.png')
        shutil.copyfile(src, dst)
        print('%s → %s' % (src.name, dst.relative_to(ROOT)))
    print('\nDalej:  python images.py && python build.py')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--model', choices=list(MODELE), help='domyślnie wg VRAM: >=12 GB flux, 8–11 sdxl, mniej/CPU turbo')
    ap.add_argument('--tylko', choices=list(KADRY), nargs='+', help='które kadry (domyślnie wszystkie)')
    ap.add_argument('--seedy', type=int, nargs='+', default=SEEDY)
    ap.add_argument('--upscale', type=float, default=UPSCALE, help='powiększenie po generacji (1 = bez), domyślnie 1.5')
    ap.add_argument('--kroki', type=int, help='nadpisz liczbę kroków (szybkie próby; jakość spada)')
    ap.add_argument('--wybierz', nargs='+', metavar='KADR=sSEED', help='skopiuj wybrane warianty do zrodla/gen/')
    a = ap.parse_args()

    if a.wybierz:
        return wybierz(a.wybierz)

    import torch
    model, vram = dobierz_model(torch)
    model = a.model or model
    print('GPU: %s' % ('%s, %.1f GB VRAM' % (torch.cuda.get_device_name(0), vram) if vram else 'brak CUDA → CPU'))
    print('Model: %s (%s)' % (model, MODELE[model]))
    if model == 'turbo':
        print('UWAGA: SDXL-Turbo daje szkic ~512–768 px; na hero strony to jakość poglądowa, nie zdjęcie.')
    if not torch.cuda.is_available() and model != 'turbo':
        print('UWAGA: %s na CPU to dziesiątki minut na obraz i >32 GB RAM. Przerwij Ctrl+C, jeśli to pomyłka.' % model)

    P = prompty() if model == 'flux' else SKROT
    WARIANTY.mkdir(parents=True, exist_ok=True)
    pipe, ref = zaladuj(model, torch)
    from PIL import PngImagePlugin
    for kadr in a.tylko or list(KADRY):
        plik, wymiary = KADRY[kadr]
        w, h = wymiary[model]
        zapisane = []
        for seed in a.seedy:
            t = time.time()
            im = generuj(model, pipe, ref, P[plik], w, h, seed, torch, a.kroki)
            im = podbij(im, a.upscale)
            meta = PngImagePlugin.PngInfo()
            for k, v in (('model', MODELE[model]), ('seed', str(seed)), ('prompt', P[plik]),
                         ('rozmiar_bazowy', '%dx%d' % (w, h)), ('upscale', str(a.upscale))):
                meta.add_text(k, v)
            out = WARIANTY / ('%s-s%d.png' % (plik, seed))
            im.save(out, pnginfo=meta)
            zapisane.append(out)
            print('  %s  %dx%d  %.0f s' % (out.name, im.width, im.height, time.time() - t))
        print('Stykówka: %s' % stykowka(plik, zapisane).relative_to(ROOT))

    print('\nObejrzyj zrodla/gen/warianty/, potem np.:\n  %s generator/gen.py --wybierz hero=s%d woda=s%d'
          % (Path(sys.executable).name, a.seedy[0], a.seedy[0]))


if __name__ == '__main__':
    main()
