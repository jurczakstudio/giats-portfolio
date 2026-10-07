# 07 — MOBILE · AKWIFER

Zrzuty: `dane/zrzuty/*-390.jpg` (całe strony, `?static=1`). Test: `node dane/zrzuty/test.mjs` —
5 adresów × 390/1440: 0 nieodsłoniętych, okna wycięte, WebGL działa, 0 poziomego scrolla, 0 błędów.

## Sygnatura na 390 px
| | |
|---|---|
| **Jak działa** | nie ma kursora: przytrzymanie palca na mapie = pompa w tym miejscu; sekcja „Pompa w kieszeni” (tylko telefon) ma przycisk, który włącza pompę na środku mapy na 7 s i przewija na górę |
| **Dlaczego inaczej** | `hover: none` — na dotyku nie ma ruchu kursora, a przytrzymanie koliduje z przewijaniem; przycisk jest jedynym pewnym sterowaniem (W4) |
| **Wydajność** | płótno w DPR 1 na telefonie (desktop maks. 1,5), ok. 30 kl./s, zatrzymane w karcie w tle; jeden shader, zero tekstur. **Pomiar z dławieniem CPU 6× — do zrobienia lokalnie** |

## Sekcje tylko na jednym urządzeniu
| Sekcja | Gdzie | Po co |
|---|---|---|
| Pompa w kieszeni (`#pompa`) | telefon (`hover: none`) | przycisk pompy zamiast kursora |
| podpowiedź „Rusz kursorem / kliknij” | desktop | na telefonie: „Przytrzymaj palec” |

## Zapis decyzji
| Akt | Desktop | Telefon |
|---|---|---|
| Mapa | tytuł na otwartej mapie, legenda w rogu | legenda pod tekstem, mapa w kadrze 92 svh |
| Arkusze | dwie kolumny: tekst + okno | okno pod tekstem, 74 vw; przy próbie okno pod symulatorem |
| Próba | wyniki w trzech kolumnach | dwie kolumny |
| Rachunek | tabela | wiersze tabeli jako karty (pozycja nad jednostką i ceną) |
| Baner wzorca | pełny | skrócony („strona wzorcowa · firma fikcyjna”) |

Znany artefakt narzędzia: zrzut `fullPage` w Playwright na 390 px rozciąga płótno do ~10 000 px
i przekracza limit tekstury — w zrzutach okna są puste, na żywym kadrze (`kadr.mjs`) mapa działa.
