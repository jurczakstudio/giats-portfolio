@echo off
rem AKWIFER — wdrożenie strony wzorcowej na akwifer.jurczakstudio.pl (Cloudflare Workers, tryb DEMO/noindex).
rem Dwuklik z katalogu projektu. Wymaga: git, python (Pillow), node; wrangler zalogowany (npx wrangler login).
cd /d "%~dp0"
git pull --ff-only origin studnie-wzorzec || goto blad
python build.py || goto blad
call npx wrangler deploy || goto blad
echo.
echo Gotowe: https://akwifer.jurczakstudio.pl
pause
exit /b 0
:blad
echo.
echo Wdrozenie przerwane - patrz komunikat wyzej.
pause
exit /b 1
