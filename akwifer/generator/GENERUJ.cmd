@echo off
rem AKWIFER - generowanie wariantow kadrow (hero-wiertnica, woda-szklanka) lokalnym modelem.
rem   GENERUJ.cmd                              4 warianty obu kadrow, model wg VRAM
rem   GENERUJ.cmd --tylko hero --seedy 5 6     wybrane kadry/seedy
rem   GENERUJ.cmd --wybierz hero=s23 woda=s11   kopiuj wybrane do zrodla\gen\
rem Inny venv: set GEN_VENV=D:\gen\venv przed uruchomieniem.
cd /d "%~dp0.."
if "%GEN_VENV%"=="" set GEN_VENV=C:\gen\venv
if not exist "%GEN_VENV%\Scripts\python.exe" (echo Brak venv w %GEN_VENV% - najpierw generator\INSTALUJ.cmd & pause & exit /b 1)
"%GEN_VENV%\Scripts\python.exe" generator\gen.py %* || (pause & exit /b 1)
if exist zrodla\gen\warianty start "" zrodla\gen\warianty
pause
