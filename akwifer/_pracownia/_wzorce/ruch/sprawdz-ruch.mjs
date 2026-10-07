/* sprawdz-ruch.mjs — bramka ruchu w prawdziwej przeglądarce.
   Panel podglądu w aplikacji ma document.hidden === true, więc wstrzymuje rAF
   i dostarczanie wpisów IntersectionObserver. Pomiar w nim pokazuje fałszywą
   porażkę. Ten skrypt odpala chromium bez okna, gdzie karta jest widoczna.

   Uruchomienie (playwright-core NIE jest zależnością żadnego projektu —
   instalujemy doraźnie w katalogu tymczasowym, nigdy w katalogu klienta):
     npm install playwright-core
     node sprawdz-ruch.mjs http://localhost:8781/ http://localhost:8781/uslugi/blaty/

   Co mierzy — trzy rzeczy, bo każda z osobna daje się oszukać:
     1. NA STARCIE, bez przewijania: ile [data-rv] odsłoniło się mimo tego, że
        leży poniżej zasięgu obserwatora. Oczekiwane 0. Powyżej zera znaczy,
        że czuwak znów odsłania na ślepo i choreografia scrollowa jest martwa.
        UWAGA na definicję „poniżej": ruch.js ma rootMargin 0px 0px 20%, więc
        element do 20% wysokości okna pod krawędzią odsłania się ZGODNIE
        z umową. Próg 100% zamiast 120% daje fałszywe alarmy.
     2. PO PRZEWINIĘCIU: ile zostało nieodsłoniętych. Oczekiwane 0, nie licząc
        elementów w kontenerach display:none (np. paski tylko na telefon).
        Sam punkt 1. nie wystarcza — „nic się nie odsłoniło" zdaje go równie
        dobrze przy sprawnej choreografii, co przy całkiem martwym ruchu.
     3. BEZPIECZNIKI: ?static=1 oraz prefers-reduced-motion mają dać
        html.ruch-off i komplet odsłonięty od razu.                            */
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';

const MARGINES = 1.20; // rootMargin 20% z ruch.js

function chromeExe() {
  const root = path.join(process.env.LOCALAPPDATA || '', 'ms-playwright');
  if (!fs.existsSync(root)) return null;
  // chrome.exe z pakietu chromium- bywa nieuruchamialny (spawn UNKNOWN);
  // headless shell startuje i wystarcza, bo i tak nie oglądamy okna.
  const dir = fs.readdirSync(root)
    .filter(d => d.startsWith('chromium_headless_shell-'))
    .sort((a, b) => parseInt(b.split('-')[1], 10) - parseInt(a.split('-')[1], 10))[0];
  if (!dir) return null;
  const p = path.join(root, dir, 'chrome-headless-shell-win64', 'chrome-headless-shell.exe');
  return fs.existsSync(p) ? p : null;
}

const POMIAR = () => {
  const H = innerHeight;
  const cele = [...document.querySelectorAll('[data-rv]')];
  const widoczny = el => {
    for (let n = el; n; n = n.parentElement) {
      if (getComputedStyle(n).display === 'none') return false;
    }
    return true;
  };
  return {
    html: document.documentElement.className,
    hidden: document.hidden,
    wszystkich: cele.length,
    odsloniete: cele.filter(el => el.classList.contains('in')).length,
    // 1.20 = 100% okna + rootMargin 20%
    przedwczesne: cele.filter(el =>
      el.getBoundingClientRect().top >= H * 1.20 && el.classList.contains('in')).length,
    zalegle: cele.filter(el =>
      !el.classList.contains('in') && widoczny(el)).length,
  };
};

async function strona(browser, url, opcje = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, ...opcje });
  const page = await ctx.newPage();
  try {
    await page.goto(url, { waitUntil: 'load', timeout: 20000 });
  } catch (e) {
    await ctx.close();
    return { url, blad: String(e.message).split('\n')[0] };
  }
  await page.waitForTimeout(2200); // czuwak ma 1200 ms — mierzymy po nim
  const start = await page.evaluate(POMIAR);

  await page.evaluate(async () => {
    const krok = innerHeight * 0.5;
    for (let y = 0; y < document.body.scrollHeight + innerHeight; y += krok) {
      scrollTo(0, y);
      await new Promise(r => setTimeout(r, 180));
    }
  });
  await page.waitForTimeout(900);
  const koniec = await page.evaluate(POMIAR);
  await ctx.close();
  return { url, przedwczesne: start.przedwczesne, naStarcie: start.odsloniete,
           poPrzewinieciu: koniec.odsloniete + '/' + koniec.wszystkich,
           zalegle: koniec.zalegle, html: koniec.html, hidden: koniec.hidden };
}

const URLE = process.argv.slice(2);
if (!URLE.length) {
  console.error('podaj co najmniej jeden adres, np. http://localhost:8781/');
  process.exit(2);
}
const exe = chromeExe();
const browser = await chromium.launch({ executablePath: exe || undefined, headless: true });

let bledy = 0;
for (const url of URLE) {
  const r = await strona(browser, url);
  const zle = r.blad || r.przedwczesne > 0 || r.zalegle > 0 || r.hidden;
  if (zle) bledy++;
  console.log((zle ? 'ŹLE  ' : 'OK   ') + JSON.stringify(r));
}
// bezpieczniki sprawdzamy na pierwszym adresie
for (const [opis, url, opcje] of [
  ['?static=1      ', URLE[0] + (URLE[0].includes('?') ? '&' : '?') + 'static=1', {}],
  ['reduced-motion ', URLE[0], { reducedMotion: 'reduce' }],
]) {
  const r = await strona(browser, url, opcje);
  const [a, b] = String(r.poPrzewinieciu).split('/');
  const zle = r.blad || r.html !== 'ruch-off' || a !== b;
  if (zle) bledy++;
  console.log((zle ? 'ŹLE  ' : 'OK   ') + opis + JSON.stringify(r));
}
await browser.close();
console.log(bledy ? 'BRAMKA ZAMKNIĘTA (' + bledy + ')' : 'BRAMKA OTWARTA');
process.exit(bledy ? 1 : 0);
