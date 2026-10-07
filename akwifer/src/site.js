
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

  // Inne części strony (mapa, rachunek ogrodu) słuchają zmian karty
  var poZmianie = [];
  function ustawGmine(slug) {
    stan.gmina = slug;
    pisz(KLUCZ, JSON.stringify(stan));
    qa('[data-karta]').forEach(function (k) { k.querySelector('[data-gmina]').value = slug; rysuj(k); });
    odswiezSms();
    poZmianie.forEach(function (f) { f(); });
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
      poZmianie.forEach(function (f) { f(); });
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
      ustawGmine(s.value);
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


  // ---- mapa powiatu (W7): najazd / dotknięcie wybiera gminę, drugie kliknięcie otwiera jej stronę
  qa('[data-mapa]').forEach(function (f) {
    var info = document.querySelector('[data-mapa-info]');
    var wybrana = null;
    var pokaz = function (slug) {
      var g = gmina[slug];
      if (!g || !info) return;
      wybrana = slug;
      qa('.m__g', f).forEach(function (a) { a.classList.toggle('m__g--akt', a.getAttribute('data-g') === slug); });
      var w = wycena({ gmina: slug, cel: 'dom', osoby: 4 });
      info.querySelector('[data-mi-n]').textContent = g.nazwa;
      info.querySelector('[data-mi-med]').textContent = metry(g.mediana) + ' m';
      info.querySelector('[data-mi-min]').textContent = metry(g.min) + ' m';
      info.querySelector('[data-mi-otw]').textContent = g.otworow;
      info.querySelector('[data-mi-f]').textContent = w.f[0];
      info.querySelector('[data-mi-link]').setAttribute('href', '/gmina/' + slug + '/');
      var b = info.querySelector('[data-mi-karta]');
      b.classList.toggle('btn--gotowe', stan.gmina === slug);
    };
    qa('.m__g[data-g]', f).forEach(function (a) {
      var slug = a.getAttribute('data-g');
      a.addEventListener('pointerenter', function (ev) { if (ev.pointerType === 'mouse') pokaz(slug); });
      a.addEventListener('focus', function () { pokaz(slug); });
      // dotyk: pierwsze dotknięcie wybiera, drugie otwiera stronę gminy; mysz i klawiatura: od razu
      a.addEventListener('pointerdown', function (ev) { a._dotyk = ev.pointerType !== 'mouse'; a._byla = wybrana === slug && a._potw; });
      a.addEventListener('click', function (ev) {
        if (a._dotyk && !a._byla) { ev.preventDefault(); qa('.m__g', f).forEach(function (x) { x._potw = false; }); a._potw = true; pokaz(slug); }
        a._dotyk = false;
      });
    });
    var b = info && info.querySelector('[data-mi-karta]');
    if (b) b.addEventListener('click', function () {
      ustawGmine(wybrana);
      var cel = document.getElementById('karta');
      if (cel) cel.scrollIntoView({ behavior: root.classList.contains('ruch') ? 'smooth' : 'auto' });
    });
    pokaz(stan.gmina);
    poZmianie.push(function () { pokaz(stan.gmina); });
  });

  // ---- rachunek ogrodu (W6): to samo, co rachunek_dane() i rachunek_svg() w build.py
  qa('[data-ogrod]').forEach(function (f) {
    var fig = document.querySelector('.ogrod__w'), svg = fig && fig.querySelector('[data-rachunek-svg]');
    var v = function (a) { var x = parseFloat(String(f.querySelector('[' + a + ']').value).replace(',', '.')); return x > 0 ? x : 0; };
    var NS = 'http://www.w3.org/2000/svg';
    var el = function (tag, at, txt) {
      var n = document.createElementNS(NS, tag);
      for (var k in at) n.setAttribute(k, at[k]);
      if (txt != null) n.textContent = txt;
      return n;
    };
    function lata(lo, hi) {
      var r = function (x) { return x >= 1.5 ? String(Math.round(x)) : pl(x, 1); };
      if (!isFinite(lo) || lo > 30) return 'ponad 30 lat';
      return hi <= 30 ? r(lo) + '–' + r(hi) + ' lat' : 'od ' + r(lo) + ' lat';
    }
    function licz() {
      var w = wycena(stan);
      var cena = v('data-o-woda') + (f.querySelector('[data-o-scieki]').checked ? D.wodociag.scieki : 0);
      var m3 = v('data-o-m2') * v('data-o-dawka') * v('data-o-tyg') / 1000;
      var roczna = m3 * cena, oszcz = m3 * Math.max(0.01, cena - D.prad);
      var lo = w.koszt[0], hi = w.koszt[1], z = [lo / oszcz, hi / oszcz];
      fig.querySelector('[data-o-m3]').textContent = pl(m3, 0) + ' m³';
      fig.querySelector('[data-o-rok]').textContent = zl(roczna) + ' zł';
      fig.querySelector('[data-o-zwrot]').textContent = m3 > 0 ? lata(z[0], z[1]) : '—';
      fig.querySelector('[data-o-gmina]').textContent = w.g.nazwa;
      fig.querySelector('[data-o-koszt]').textContent = zl(lo) + '–' + zl(hi) + ' zł';
      // wykres
      // viewBox = prawdziwa szerokość wykresu, żeby opisy miały pełne 14 px także na telefonie
      var W = Math.round(svg.getBoundingClientRect().width) || 640, H = W < 500 ? 240 : 300, L = 64, R = 16, T = 16, B = 40, LAT = 15;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      var ymax = Math.max(roczna * LAT, hi + m3 * D.prad * LAT) * 1.08;
      var X = function (t) { return L + t / LAT * (W - L - R); };
      var Y = function (y) { return T + (1 - y / ymax) * (H - T - B); };
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var krok = Math.pow(10, String(Math.floor(ymax / 4)).length) / 10 || 1;
      krok = [1, 2, 2.5, 5, 10].map(function (k) { return k * krok; }).filter(function (k) { return ymax / k <= 5; })[0];
      for (var y = 0; y <= ymax; y += krok) {
        svg.appendChild(el('line', { 'class': 'r__siatka', x1: L, x2: W - R, y1: Y(y), y2: Y(y) }));
        svg.appendChild(el('text', { 'class': 'r__os', x: L - 8, y: Y(y) + 5 }, y < 1000 ? zl(y) : pl(y / 1000, y % 1000 ? 1 : 0) + ' tys.'));
      }
      for (var t = 0; t <= LAT; t += 5) svg.appendChild(el('text', { 'class': 'r__os r__os--x', x: X(t), y: H - 12 }, t + (t >= 5 ? ' lat' : ' ')));
      var pr = m3 * D.prad * LAT;
      svg.appendChild(el('path', { 'class': 'r__pas', d: 'M' + X(0) + ' ' + Y(lo) + 'L' + X(LAT) + ' ' + Y(lo + pr) + 'L' + X(LAT) + ' ' + Y(hi + pr) + 'L' + X(0) + ' ' + Y(hi) + 'Z' }));
      svg.appendChild(el('path', { 'class': 'r__kran', d: 'M' + X(0) + ' ' + Y(0) + 'L' + X(LAT) + ' ' + Y(roczna * LAT) }));
      z.forEach(function (x) { if (x <= LAT) svg.appendChild(el('circle', { 'class': 'r__zw', cx: X(x), cy: Y(roczna * x), r: 6 })); });
    }
    f.addEventListener('input', licz);
    f.addEventListener('change', licz);
    poZmianie.push(licz);
    var szer = 0;
    addEventListener('resize', function () { var x = Math.round(svg.getBoundingClientRect().width); if (x !== szer) { szer = x; licz(); } });
    if (fig && svg) licz();
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
