// Kadry v3 z ruchem: hero, gwarancja, zejście (3 fazy), pakiety, przepisy, zgłoszenie. node dane/zrzuty/v3.mjs [1440|390]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const w = +(process.argv[2] || 1440), B = 'http://127.0.0.1:8788', bl = [];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: w, height: w < 500 ? 844 : 900 }, isMobile: w < 500, hasTouch: w < 500 });
p.on('pageerror', e => bl.push(e.message)); p.on('console', m => m.type() === 'error' && bl.push(m.text()));
await p.goto(B + '/', { waitUntil: 'load' }); await p.waitForTimeout(1800);
const kadr = async (n) => p.screenshot({ path: `dane/zrzuty/v3-${w}-${n}.png` });
await kadr('1-hero');
await p.selectOption('[data-gmina-hero]', 'kornik'); await p.waitForTimeout(900); await kadr('2-hero-kornik');
const top = async (sel) => p.evaluate(s => document.querySelector(s).getBoundingClientRect().top + scrollY, sel);
const jedz = async (y) => { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(1300); };
await jedz(await top('#gwarancja')); await kadr('3-gwarancja');
const z = await top('#zejscie'), zh = await p.evaluate(() => document.querySelector('#zejscie').offsetHeight - innerHeight);
for (const [i, f] of [[4, .15], [5, .5], [6, .97]]) { await jedz(z + zh * f); await kadr(`${i}-zejscie`); }
await jedz(await top('#pakiety')); await kadr('7-pakiety');
await jedz(await top('#przepisy')); await kadr('8-przepisy');
await jedz(await top('#zgloszenie')); await kadr('9-zgloszenie');
console.log(w, 'błędy:', bl.join(' | ') || 'brak');
await b.close();
