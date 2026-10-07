// Kadry z interakcją (bez static): telefon — hero i robota; desktop — tryb właściciela + karta + SMS + kalkulator.
// node dane/zrzuty/kadr.mjs   (serwer: python3 -m http.server 8788 --directory site)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const B = 'http://127.0.0.1:8788';
const b = await chromium.launch();
const bl = [];
const strona = async (w) => {
  const p = await b.newPage({ viewport: { width: w, height: w < 500 ? 844 : 900 }, isMobile: w < 500, hasTouch: w < 500 });
  p.on('pageerror', e => bl.push(e.message)); p.on('console', m => m.type() === 'error' && bl.push(m.text()));
  return p;
};
const do_ = async (p, sel) => { await p.evaluate(s => document.querySelector(s).scrollIntoView({ block: 'start' }), sel); await p.waitForTimeout(1300); };

let p = await strona(390);
await p.goto(B + '/', { waitUntil: 'load' }); await p.waitForTimeout(1500);
await p.screenshot({ path: 'dane/zrzuty/kadr-390-hero.png' });
await p.selectOption('#h-gmina', 'kornik'); await p.click('.hero__szybko button'); await p.waitForTimeout(1500);
await p.screenshot({ path: 'dane/zrzuty/kadr-390-karta.png' });
await do_(p, '#powiat'); await p.screenshot({ path: 'dane/zrzuty/kadr-390-powiat.png' });
await do_(p, '#robota'); await p.screenshot({ path: 'dane/zrzuty/kadr-390-robota.png' });
await p.close();

p = await strona(1440);
await p.goto(B + '/?wlasciciel=1', { waitUntil: 'load' }); await p.waitForTimeout(1500);
await p.screenshot({ path: 'dane/zrzuty/kadr-1440-wl.png' });
await do_(p, '#karta');
await p.selectOption('#karta [data-gmina]', 'komorniki');
await p.click('#karta .karta__cel:nth-of-type(3)');
await p.fill('#karta [data-osoby]', '6'); await p.dispatchEvent('#karta [data-osoby]', 'input');
await p.waitForTimeout(900);
await p.screenshot({ path: 'dane/zrzuty/kadr-1440-karta.png' });
const sms = await p.getAttribute('#karta [data-sms]', 'href');
const z = await p.textContent('#karta [data-r-z]');
await p.goto(B + '/dla-firm/', { waitUntil: 'load' }); await p.waitForTimeout(800);
const pod = await p.textContent('[data-sms-podglad]');
const kalk = [await p.textContent('[data-k-rok]'), await p.textContent('[data-k-jedno]')];
const wl = await p.evaluate(() => document.documentElement.classList.contains('wl'));
await do_(p, '#droga'); await p.screenshot({ path: 'dane/zrzuty/kadr-1440-dlafirm.png' });
await p.goto(B + '/gmina/lubon/', { waitUntil: 'load' }); await p.waitForTimeout(800);
const stala = await p.inputValue('[data-karta] [data-gmina]');
console.log('SMS zawiera Komorniki:', decodeURIComponent(sms).includes('Komorniki'), '| zużycie:', z.trim());
console.log('podgląd na /dla-firm/ pamięta kartę:', pod.includes('Komorniki'), '| tryb właściciela pamiętany:', wl);
console.log('kalkulator:', kalk.join(' / '), '| podstrona Luboń ma gminę:', stala);
console.log('błędy:', bl.join(' | ') || 'brak');
await b.close();
