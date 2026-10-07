// Zrzuty całej strony (390 i 1440) z ?static=1 + konsola + poziomy scroll.
// Użycie: node dane/zrzuty/zrzut.mjs [ścieżki...]   (serwer: python -m http.server 8787 --directory site)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const BASE = process.env.BASE || 'http://127.0.0.1:8788';
const sciezki = process.argv.slice(2).length ? process.argv.slice(2) : ['/'];
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
for (const w of [390, 1440]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, deviceScaleFactor: 1, isMobile: w === 390, hasTouch: w === 390 });
  const p = await ctx.newPage();
  const bledy = [];
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') bledy.push(m.text()); });
  p.on('pageerror', e => bledy.push('JS: ' + e.message));
  for (const s of sciezki) {
    await p.goto(BASE + s + '?static=1', { waitUntil: 'load' });
    // leniwe obrazy: przejedź stronę, potem wróć na górę
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += 600) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(30); }
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(700);
    const sz = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight }));
    const nazwa = (s === '/' ? 'glowna' : s.replace(/\//g, '')) + '-' + w;
    await p.screenshot({ path: `dane/zrzuty/${nazwa}.png`, fullPage: true });
    console.log(nazwa, 'wys', sz.h, sz.sw > sz.cw ? `POZIOMY SCROLL ${sz.sw}>${sz.cw}` : 'ok', bledy.splice(0).join(' | '));
  }
  await ctx.close();
}
await b.close();
