# -*- coding: utf-8 -*-
"""AKWIFER — instalator lokalnego generatora obrazów (venv + torch z CUDA + diffusers).

    py -3 generator\\instaluj.py                 # Windows (albo dwuklik INSTALUJ.cmd)
    python3 generator/instaluj.py --venv ~/gen/venv

1. Pokazuje sprzęt: nvidia-smi (GPU, VRAM, sterownik), RAM, wolne miejsce, Python.
2. Zakłada venv (domyślnie C:\\gen\\venv) i instaluje torch z właściwym indeksem CUDA:
   sterownik >= 570 → cu128 (działa też z RTX 50xx), >= 525 → cu126, brak NVIDII → CPU.
3. Doinstalowuje diffusers, transformers, accelerate, sentencepiece, protobuf, pillow.
Nie dotyka tokenów Hugging Face — jeśli model wymaga logowania, gen.py to powie.
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

DOMYSLNY_VENV = r'C:\gen\venv' if os.name == 'nt' else str(Path.home() / 'gen' / 'venv')
PAKIETY = ['diffusers>=0.32', 'transformers', 'accelerate', 'sentencepiece', 'protobuf', 'pillow', 'psutil']


def ram_gb():
    try:
        if os.name == 'nt':
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong),
                            ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                            ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                            ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                            ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
            m = MS()
            m.dwLength = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.ullTotalPhys / 2 ** 30
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 2 ** 30
    except Exception:
        return None


def nvidia():
    """[(nazwa, vram_gb, sterownik)] albo [] gdy brak nvidia-smi."""
    if not shutil.which('nvidia-smi'):
        return []
    try:
        out = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,driver_version',
                              '--format=csv,noheader,nounits'], capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, OSError):
        return []
    gpu = []
    for linia in out.strip().splitlines():
        nazwa, mib, sterownik = [x.strip() for x in linia.split(',')]
        gpu.append((nazwa, int(float(mib)) / 1024, sterownik))
    return gpu


def indeks_torch(gpu):
    if not gpu:
        return 'cpu'
    glowna = int(gpu[0][2].split('.')[0])
    if glowna >= 570:
        return 'cu128'
    if glowna >= 525:
        return 'cu126'
    raise SystemExit('Sterownik NVIDII %s jest za stary dla torch z CUDA 12 — zaktualizuj go (nvidia.com/drivers).' % gpu[0][2])


def raport(cel):
    gpu = nvidia()
    print('=== SPRZĘT ===')
    if gpu:
        for nazwa, vram, sterownik in gpu:
            print('GPU:     %s — %.1f GB VRAM, sterownik %s' % (nazwa, vram, sterownik))
    else:
        print('GPU:     brak NVIDII (nvidia-smi nie odpowiada) — generacja na CPU, patrz README')
    r = ram_gb()
    print('RAM:     %s' % ('%.1f GB' % r if r else '?'))
    kat = Path(cel).anchor or str(Path(cel).resolve().anchor)
    wolne = shutil.disk_usage(kat if os.path.exists(kat) else '.').free / 2 ** 30
    print('Dysk:    %.0f GB wolnego na %s (modele: FLUX ~34 GB, SDXL+refiner ~14 GB, SDXL-Turbo ~7 GB)' % (wolne, kat))
    print('Python:  %s (%s)' % (platform.python_version(), sys.executable))
    if gpu:
        vram = gpu[0][1]
        if vram >= 12:
            print('Wybór:   FLUX.1-schnell, bf16, enable_model_cpu_offload()')
            if r and r < 30:
                print('UWAGA:   FLUX z offloadem chce ~32 GB RAM; przy %.0f GB będzie swap (wolno). Alternatywa: --model sdxl' % r)
        elif vram >= 8:
            print('Wybór:   SDXL base + refiner (FLUX możliwy: --model flux, ale wolny przy offloadzie)')
        else:
            print('Wybór:   SDXL-Turbo — jakość szkicowa, patrz README')
    print()
    return gpu, wolne


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--venv', default=DOMYSLNY_VENV)
    ap.add_argument('--tylko-raport', action='store_true', help='pokaż sprzęt i nic nie instaluj')
    a = ap.parse_args()

    if sys.version_info < (3, 10):
        raise SystemExit('Potrzebny Python >= 3.10 (jest %s).' % platform.python_version())
    gpu, wolne = raport(a.venv)
    if a.tylko_raport:
        return
    if wolne < 25:
        print('UWAGA: mało miejsca — sam torch z CUDA to ~5 GB, modele kolejne 7–34 GB.\n')

    venv = Path(a.venv)
    py = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not py.exists():
        print('Zakładam venv: %s' % venv)
        subprocess.run([sys.executable, '-m', 'venv', str(venv)], check=True)
    pip = [str(py), '-m', 'pip', 'install', '--upgrade']
    subprocess.run(pip + ['pip'], check=True)

    idx = indeks_torch(gpu)
    print('Instaluję torch (%s)…' % idx)
    subprocess.run(pip + ['torch', '--index-url', 'https://download.pytorch.org/whl/' + idx], check=True)
    subprocess.run(pip + PAKIETY, check=True)

    test = ('import torch, diffusers; print("torch", torch.__version__, "| CUDA:", torch.cuda.is_available(), '
            '"|", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU", "| diffusers", diffusers.__version__)')
    subprocess.run([str(py), '-c', test], check=True)
    print('\nFLUX.1-schnell wymaga jednorazowo: zaakceptuj warunki na huggingface.co/black-forest-labs/FLUX.1-schnell'
          ' i zaloguj się: %s auth login' % py.with_name('hf'))
    print('\nGotowe. Generowanie:  %s generator%sgen.py   (albo GENERUJ.cmd)' % (py, os.sep))


if __name__ == '__main__':
    main()
