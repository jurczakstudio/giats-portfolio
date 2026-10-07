// Kadr hero z pompą pod kursorem i klikniętymi studniami (bez static). node dane/zrzuty/kadr.mjs [ścieżka] [szer]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const s = process.argv[2] || '/', w = +(process.argv[3] || 1440);
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: w, height: w < 500 ? 844 : 900 } });
const bl = []; p.on('pageerror', e => bl.push(e.message)); p.on('console', m => m.type() !== 'log' && bl.push(m.text()));
await p.goto('http://127.0.0.1:8788' + s, { waitUntil: 'load' });
await p.waitForTimeout(400);
console.log('gl:', await p.evaluate(() => document.documentElement.className));
await p.mouse.move(w * .3, 600); await p.mouse.click(w * .3, 600);
await p.mouse.move(w * .62, 380); await p.waitForTimeout(2600);
await p.screenshot({ path: 'dane/zrzuty/kadr-hero.png' });
const y = await p.evaluate(() => { const o = document.querySelector('.okno--sym') || document.querySelector('[data-okno]'); return o.getBoundingClientRect().top + scrollY - 200; });
await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(1200);
await p.screenshot({ path: 'dane/zrzuty/kadr-okno.png' });
console.log('błędy:', bl.join(' | ') || 'brak');
await b.close();
