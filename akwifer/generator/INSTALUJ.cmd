@echo off
rem AKWIFER - instalacja lokalnego generatora obrazow (venv C:\gen\venv + torch z CUDA + diffusers).
rem Dwuklik. Wymaga Pythona 3.10-3.13 z python.org (launcher "py"). Inna sciezka venv: INSTALUJ.cmd --venv D:\gen\venv
cd /d "%~dp0.."
set PY=python
where py >nul 2>nul && set PY=py -3
%PY% generator\instaluj.py %*
pause
