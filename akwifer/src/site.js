
/* AKWIFER v2 „ZLECENIE” — karta zlecenia (W4), tryb właściciela (W5), kalkulator dla firm.
   Wycena liczona tak samo jak w build.py: wycena(). Bez JS karta pokazuje wartości z buildu. */
(function () {
  'use strict';
  var D = __DANE__;
  var root = document.documentElement;
  var qa = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var KLUCZ = 'akwifer-karta', KLUCZ_WL = 'akwifer-wl';
  var czytaj = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
  var pisz = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };

  var gmina = {};
  D.gminy.forEach(function (g) { gmina[g.slug] = g; });

  var pl = function (x, d) { return x.toFixed(d).replace('.', ','); };
  var metry = function (x) { return pl(x, x % 1 ? 1 : 0); };
  var zl = function (x) { return String(Math.round(x / 100) * 100).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };

  function wycena(s) {
    var g = gmina[s.gmina] || gmina.mosina;
    var lo = g.min, hi = Math.max(g.mediana, g.min);
    var r = { g: g, lo: lo, hi: hi,
      koszt: [lo * D.rynek.mb[0] + D.rynek.osprzet[0], hi * D.rynek.mb[1] + D.rynek.osprzet[1]],
      zuz: s.osoby * D.zuzycie * D.cele[s.cel][1] };
    if (hi <= 30) r.f = ['zwykle bez zgłoszeń', 'połowa otworów w gminie jest płytsza niż ' + metry(g.mediana) + ' m — studnia domowa zwykle mieści się w 30 m'];
    else if (lo > 30) r.f = ['prawie na pewno ponad 30 m', 'nawet najpłytsze ujęcie w rejestrze ma ' + metry(lo) + ' m — potrzebny projekt robót geologicznych; przygotowujemy go'];
    else r.f = ['zależy od działki', 'najpłytsze ujęcia mieszczą się w 30 m, ale połowa otworów jest głębsza — jeśli przekroczymy 30 m, papiery są po naszej stronie'];
    return r;
  }

  function sms(s) {
    var w = wycena(s);
    return 'Dzień dobry, pytam o studnię głębinową.\n' +
      'Gmina: ' + w.g.nazwa + '\n' +
      'Na co: ' + D.cele[s.cel][0] + ', ' + s.osoby + ' os.\n' +
      'Z karty: ' + metry(w.lo) + '–' + metry(w.hi) + ' m, ' + zl(w.koszt[0]) + '–' + zl(w.koszt[1]) + ' zł\n' +
      'Proszę o kontakt.';
  }

  // ---- stan karty: adres (?gmina=) > zapis w przeglądarce > domyślny
  var stan = { gmina: 'mosina', cel: 'dom', osoby: 4 };
  try { var z = JSON.parse(czytaj(KLUCZ) || 'null'); if (z && gmina[z.gmina] && D.cele[z.cel]) stan = z; } catch (e) {}
  var zAdresu = (location.search.match(/[?&]gmina=([\w-]+)/) || [])[1];
  if (zAdresu && gmina[zAdresu]) stan.gmina = zAdresu;
  var stala = document.querySelector('[data-gmina-stala]');
  if (stala) stan.gmina = stala.getAttribute('data-gmina-stala');

  function odswiezSms() {
    var t = sms(stan), href = 'sms:' + D.tel + '?&body=' + encodeURIComponent(t);
    qa('[data-sms]').forEach(function (a) { a.setAttribute('href', href); });
    qa('[data-sms-podglad]').forEach(function (p) { p.textContent = t; });
  }

  function ustaw(el, sel, txt) {
    var x = el.querySelector(sel);
    if (!x || x.textContent === txt) return;
    x.textContent = txt;
    if (x.tagName === 'DD') { x.classList.remove('miga'); void x.offsetWidth; x.classList.add('miga'); }
  }

  function rysuj(k) {
    var w = wycena(stan);
    ustaw(k, '[data-r-m]', metry(w.lo) + '–' + metry(w.hi));
    ustaw(k, '[data-r-zl]', zl(w.koszt[0]) + '–' + zl(w.koszt[1]));
    ustaw(k, '[data-r-f]', w.f[0]);
    ustaw(k, '[data-r-f2]', w.f[1]);
    ustaw(k, '[data-r-z]', 'zużycie ok. ' + pl(w.zuz, 1) + ' m³/dobę · limit bez pozwolenia: 5 m³/dobę' + (w.zuz > 5 ? ' — przekroczony, potrzebne pozwolenie wodnoprawne' : ''));
  }

  qa('[data-karta]').forEach(function (k) {
    var sel = k.querySelector('[data-gmina]'), os = k.querySelector('[data-osoby]');
    sel.value = stan.gmina;
    os.value = stan.osoby;
    qa('input[type="radio"]', k).forEach(function (r) { r.checked = r.value === stan.cel; });
    k.addEventListener('input', function () {
      stan.gmina = sel.value;
      var c = k.querySelector('input[type="radio"]:checked');
      if (c) stan.cel = c.value;
      var n = parseInt(os.value, 10);
      if (n > 0 && n < 50) stan.osoby = n;
      pisz(KLUCZ, JSON.stringify(stan));
      rysuj(k);
      odswiezSms();
    });
    rysuj(k);
  });
  odswiezSms();
  qa('[data-kopiuj]').forEach(function (kop) {
    var napis = kop.textContent;
    kop.addEventListener('click', function () {
      var gotowe = function () { kop.textContent = 'Skopiowano'; setTimeout(function () { kop.textContent = napis; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(sms(stan)).then(gotowe, function () {});
    });
  });

  // ---- hero: wybór gminy → karta poniżej (bez JS: /?gmina=…#karta)
  qa('[data-szybko]').forEach(function (f) {
    var s = f.querySelector('select');
    if (zAdresu || czytaj(KLUCZ)) s.value = stan.gmina;
    f.addEventListener('submit', function (ev) {
      var cel = document.getElementById('karta');
      if (!cel) return;
      ev.preventDefault();
      stan.gmina = s.value;
      pisz(KLUCZ, JSON.stringify(stan));
      qa('[data-karta]').forEach(function (k) { k.querySelector('[data-gmina]').value = stan.gmina; rysuj(k); });
      odswiezSms();
      cel.scrollIntoView({ behavior: root.classList.contains('ruch') ? 'smooth' : 'auto' });
    });
  });

  // ---- tryb „Oczami właściciela” (W5)
  var wl = /[?&]wlasciciel=1/.test(location.search) || czytaj(KLUCZ_WL) === '1';
  var przelacz = function (on) {
    wl = on;
    root.classList.toggle('wl', on);
    qa('[data-tryb-wl]').forEach(function (b) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    pisz(KLUCZ_WL, on ? '1' : '0');
  };
  przelacz(wl);
  qa('[data-tryb-wl]').forEach(function (b) {
    b.addEventListener('click', function () {
      przelacz(!wl);
      if (wl) { var n = qa('[data-notka]').filter(function (x) { return x.getBoundingClientRect().top > 0; })[0]; if (n && n.getBoundingClientRect().top > innerHeight) n.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
    });
  });

  // ---- kalkulator dla firm
  qa('[data-kalk]').forEach(function (f) {
    var v = function (a) { var x = parseFloat(f.querySelector('[' + a + ']').value); return x > 0 ? x : 0; };
    var licz = function () {
      f.querySelector('[data-k-rok]').textContent = zl(v('data-k-zap') * v('data-k-koszt') * 12) + ' zł';
      f.querySelector('[data-k-jedno]').textContent = zl(v('data-k-war') * 12) + ' zł';
    };
    f.addEventListener('input', licz);
    licz();
  });

  // ---- nagłówek i menu
  var nag = document.querySelector('.nag');
  var tlo = function () { nag.classList.toggle('nag--tlo', scrollY > 40); };
  addEventListener('scroll', tlo, { passive: true });
  tlo();
  var guz = document.querySelector('.nag__przycisk'), menu = document.getElementById('menu');
  if (guz) guz.addEventListener('click', function () {
    var o = guz.getAttribute('aria-expanded') !== 'true';
    guz.setAttribute('aria-expanded', o ? 'true' : 'false');
    menu.classList.toggle('otwarte', o);
  });
  qa('#menu a').forEach(function (a) { a.addEventListener('click', function () { if (guz) { guz.setAttribute('aria-expanded', 'false'); menu.classList.remove('otwarte'); } }); });
})();
