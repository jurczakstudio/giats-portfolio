// Test: konsola, odsłonięcia, symulator ↔ lej, okna wycięte, karta zgłoszenia, poziomy scroll 390. BASE=… node dane/zrzuty/test.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const B = process.env.BASE || 'http://127.0.0.1:8788';
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, isMobile: w === 390, hasTouch: w === 390 });
  const p = await ctx.newPage(); const bl = [];
  p.on('pageerror', e => bl.push(e.message)); p.on('console', m => m.type() === 'error' && bl.push(m.text()));
  for (const s of ['/', '/proba-pompowania/', '/przebieg/', '/formalnosci/', '/kontakt/']) {
    await p.goto(B + s);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += 300) { await p.mouse.wheel(0, 300); await p.waitForTimeout(20); }
    await p.waitForTimeout(1300);
    const r = await p.evaluate(() => ({ nie: document.querySelectorAll('[data-rv]:not(.in)').length,
      okna: document.querySelectorAll('.arkusz.ma-okno').length, gl: document.documentElement.classList.contains('mapa-on'),
      poziomy: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      odczyt: [...document.querySelectorAll('[data-odczyt]')].map(o => o.textContent).join(' | ') }));
    console.log(w, s, JSON.stringify(r));
  }
  await p.goto(B + '/proba-pompowania/');
  await p.fill('[data-q]', '6'); await p.dispatchEvent('[data-q]', 'input');
  console.log(w, 'Q=6 średni:', await p.textContent('[data-s]'), await p.textContent('[data-rl]'), '| krzywa:', (await p.getAttribute('.kd__woda', 'd')).slice(0, 40));
  await p.selectOption('[data-k]', '1e-05');
  console.log(w, 'Q=6 drobny — uwaga widoczna:', await p.isVisible('[data-sym-uwaga]'));
  await p.goto(B + '/kontakt/');
  await p.fill('[name=osoby]', '4'); await p.check('[name=ogrod]');
  console.log(w, 'karta:', await p.textContent('[data-kz-szac]'));
  console.log(w, 'błędy:', bl.join(' | ') || 'brak');
  await ctx.close();
}
await b.close();
