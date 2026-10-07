
/* site.js — AKWIFER, koncept LEJ. Doklejany za ruch.js.
   Sygnatura: żywa mapa hydroizohips (WebGL) — kursor = pompa, klik = studnia, okna w arkuszach.
   Model pola jest JEDEN: ta sama funkcja liczy obraz (GLSL) i odczyty pod oknami (JS).
   Technika okien i linii w shaderze za giats.me (E. Giatsidis, MIT); kod własny. ES5. */
(function () {
  'use strict';
  var STAT = window.matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]static=1/.test(location.search);
  var qa = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var pl = function (x, d) { return x.toFixed(d === undefined ? 1 : d).replace('.', ','); };
  var html = document.documentElement;

  /* ---- menu ------------------------------------------------------------ */
  var przycisk = document.querySelector('.nag__przycisk'), menu = document.getElementById('menu');
  if (przycisk && menu) {
    var ustaw = function (o) { menu.classList.toggle('otwarte', o); przycisk.setAttribute('aria-expanded', o ? 'true' : 'false'); };
    przycisk.addEventListener('click', function () { ustaw(!menu.classList.contains('otwarte')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') ustaw(false); });
    document.addEventListener('click', function (e) { if (!menu.contains(e.target) && e.target !== przycisk) ustaw(false); });
  }

  /* ---- model próby pompowania (Dupuit + Sichardt) ----------------------- */
  var MODEL = { H: 12, r: 0.0625 };
  function proba(Qm3h, k) {
    var Q = Qm3h / 3600, H = MODEL.H, r = MODEL.r;
    var f = function (s) { var R = Math.max(3000 * s * Math.sqrt(k), r * 1.01); return Math.PI * k * (2 * H * s - s * s) / Math.log(R / r) - Q; };
    var lo = 1e-4, hi = H * 0.95, i, mid;
    if (f(hi) < 0) return null;
    for (i = 0; i < 60; i++) { mid = (lo + hi) / 2; if (f(mid) < 0) lo = mid; else hi = mid; }
    var s = (lo + hi) / 2;
    return { s: s, R: 3000 * s * Math.sqrt(k) };
  }
  var POMPA = { s: 1.16, R: 24.5 };   // bieżące wartości z symulatora (domyślnie 2,5 m³/h, piasek średni)

  /* ---- pole zwierciadła: TO SAMO co w shaderze -------------------------- */
  var MPP = 0.1, RW = 0.0625, PAR = 0.5, EX = 3;   // m na px · promień studni · mapa jedzie z połową prędkości scrolla · przewyższenie leja
  var czas = 0;
  function glebokosc(wx, wy, studnie) {
    var x = wx * MPP, y = wy * MPP;
    var d = 6.0 + 1.8 * Math.sin(x * 0.021 + 1.3 * Math.sin(y * 0.017 + czas * 0.05))
      + 1.2 * Math.sin(y * 0.029 - 0.8 * Math.sin(x * 0.011))
      + 0.5 * Math.sin((x + y) * 0.043 + czas * 0.03) + y * 0.004;
    for (var i = 0; i < studnie.length; i++) {
      var q = studnie[i], r = Math.max(Math.hypot(wx - q[0], wy - q[1]) * MPP, 1.0);
      if (r < q[3]) d += EX * q[2] * Math.log(q[3] / r) / Math.log(q[3] / RW);
    }
    return d;
  }

  var FRAG = [
    '#extension GL_OES_standard_derivatives : enable',
    'precision highp float;',
    'uniform vec2 uRes; uniform float uDpr; uniform float uOff; uniform float uTime;',
    'uniform vec4 uW[8]; uniform int uN;',
    'const float MPP = 0.1; const float RW = 0.0625; const float STEP = 0.25; const float EX = 3.0;',
    'float glebokosc(vec2 w, out float lej) {',
    '  vec2 m = w * MPP;',
    '  float d = 6.0 + 1.8 * sin(m.x * 0.021 + 1.3 * sin(m.y * 0.017 + uTime * 0.05))',
    '    + 1.2 * sin(m.y * 0.029 - 0.8 * sin(m.x * 0.011))',
    '    + 0.5 * sin((m.x + m.y) * 0.043 + uTime * 0.03) + m.y * 0.004;',
    '  lej = 0.0;',
    '  for (int i = 0; i < 8; i++) {',
    '    if (i >= uN) break;',
    '    vec4 q = uW[i];',
    '    float r = max(distance(w, q.xy) * MPP, 1.0);',
    '    if (r < q.w) { float s = EX * q.z * log(q.w / r) / log(q.w / RW); d += s; lej += s; }',
    '  }',
    '  return d;',
    '}',
    'void main() {',
    '  vec2 px = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y) / uDpr;',
    '  float lej; float d = glebokosc(px + vec2(0.0, uOff), lej);',
    '  float f = d / STEP; float fw = fwidth(f);',
    '  float g = abs(fract(f - 0.5) - 0.5) / max(fw, 1e-4);',
    '  float cienka = 1.0 - clamp(g - 0.35, 0.0, 1.0);',
    '  float fm = d; float gm = abs(fract(fm - 0.5) - 0.5) / max(fwidth(fm), 1e-4);',
    '  float gruba = 1.0 - clamp(gm * 0.55 - 0.45, 0.0, 1.0);',
    '  vec3 papier = vec3(0.945, 0.929, 0.890);',
    '  vec3 woda = vec3(0.122, 0.373, 0.620);',
    '  vec3 kol = mix(papier, vec3(0.850, 0.890, 0.925), clamp(lej * 0.3, 0.0, 0.7));',
    '  float a = max(cienka * 0.42, gruba * 0.85) * clamp(1.5 - fw * 1.3, 0.0, 1.0);',
    '  gl_FragColor = vec4(mix(kol, woda, a), 1.0);',
    '}'].join('\n');
  var VERT = 'attribute vec2 p; void main(){ gl_Position = vec4(p, 0.0, 1.0); }';

  var canvas = document.querySelector('canvas.mapa');
  var gl = null, U = {}, dpr = 1, W = 0, Hh = 0;
  var kursor = null;                 // [x, y] w px kadru albo null
  var pompaSila = STAT ? 1 : 0;      // 0..1 — lej narasta w czasie pompowania
  var wiercone = [];                 // [wx, wy, s, R] — studnie wywiercone kliknięciem (świat)
  var okna = qa('[data-okno]');
  var oknoSym = document.querySelector('.okno--sym');

  function swiatY(yKadru) { return yKadru + window.scrollY * PAR; }

  function studnie() {
    var out = [];
    if (kursor) out.push([kursor[0], swiatY(kursor[1]), POMPA.s * pompaSila, POMPA.R]);
    if (oknoSym) {
      var r = oknoSym.getBoundingClientRect();
      if (r.bottom > -200 && r.top < Hh + 200) out.push([r.left + r.width / 2, swiatY(r.top + r.height / 2), POMPA.s, POMPA.R]);
    }
    return out.concat(wiercone).slice(0, 8);
  }

  function initGL() {
    if (!canvas) return false;
    try {
      gl = canvas.getContext('webgl', { antialias: false, alpha: false, preserveDrawingBuffer: false });
    } catch (e) { gl = null; }
    if (!gl || !gl.getExtension('OES_standard_derivatives')) return false;
    var sh = function (typ, src) {
      var s = gl.createShader(typ); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    };
    try {
      var p = gl.createProgram();
      gl.attachShader(p, sh(gl.VERTEX_SHADER, VERT)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, FRAG));
      gl.linkProgram(p);
      if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
      gl.useProgram(p);
      var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      var loc = gl.getAttribLocation(p, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
      ['uRes', 'uDpr', 'uOff', 'uTime', 'uW', 'uN'].forEach(function (n) { U[n] = gl.getUniformLocation(p, n); });
    } catch (e) { gl = null; return false; }
    return true;
  }

  function rozmiar() {
    var mobil = window.innerWidth <= 760;
    dpr = Math.min(window.devicePixelRatio || 1, mobil ? 1 : 1.5);
    W = window.innerWidth; Hh = window.innerHeight;
    if (canvas) { canvas.width = Math.round(W * dpr); canvas.height = Math.round(Hh * dpr); }
    if (gl) gl.viewport(0, 0, canvas.width, canvas.height);
    wytnijOkna();
    if (gl && STAT) rysuj();
  }

  function rysuj() {
    var st = studnie(), dane = new Float32Array(32);
    st.forEach(function (q, i) { dane[i * 4] = q[0]; dane[i * 4 + 1] = q[1]; dane[i * 4 + 2] = q[2]; dane[i * 4 + 3] = q[3]; });
    if (gl) {
      gl.uniform2f(U.uRes, canvas.width, canvas.height); gl.uniform1f(U.uDpr, dpr);
      gl.uniform1f(U.uOff, window.scrollY * PAR); gl.uniform1f(U.uTime, czas);
      gl.uniform4fv(U.uW, dane); gl.uniform1i(U.uN, st.length);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    // odczyty pod oknami — z tego samego pola
    okna.forEach(function (o) {
      var r = o.getBoundingClientRect();
      if (r.bottom < 0 || r.top > Hh) return;
      var d = glebokosc(r.left + r.width / 2, swiatY(r.top + r.height / 2), st);
      var el = o.querySelector('[data-odczyt]');
      if (el) el.textContent = 'zwierciadło ' + pl(d, 2) + ' m';
    });
  }

  /* ---- okna: wycięcie w papierze arkusza ------------------------------- */
  function wytnijOkna() {
    okna.forEach(function (o) {
      var ark = o.closest('.arkusz');
      if (!ark) return;
      var ra = ark.getBoundingClientRect(), ro = o.getBoundingClientRect();
      ark.classList.add('ma-okno');
      ark.style.setProperty('--ox', (ro.left - ra.left + ro.width / 2).toFixed(1) + 'px');
      ark.style.setProperty('--oy', (ro.top - ra.top + ro.height / 2).toFixed(1) + 'px');
      ark.style.setProperty('--or', (ro.width / 2 - 1).toFixed(1) + 'px');
    });
  }

  if (initGL()) {
    html.classList.add('mapa-on', 'okna');
    rozmiar();
    window.addEventListener('resize', rozmiar);
    if (window.ResizeObserver) { var ro = new ResizeObserver(function () { wytnijOkna(); }); qa('.arkusz').forEach(function (a) { ro.observe(a); }); }
    if (document.fonts) document.fonts.ready.then(wytnijOkna);
    window.addEventListener('load', wytnijOkna);

    if (STAT) {
      kursor = [W * 0.68, Hh * 0.42];
      rysuj();
      window.addEventListener('scroll', function () { requestAnimationFrame(rysuj); }, { passive: true });
    } else {
      var ost = 0;
      (function petla(t) {
        requestAnimationFrame(petla);
        if (document.hidden || t - ost < 30) return;   // ok. 30 kl./s
        var dt = Math.min(0.1, (t - ost) / 1000); ost = t;
        czas += dt;
        pompaSila += ((kursor ? 1 : 0) - pompaSila) * Math.min(1, dt * 1.6);   // lej narasta i zanika
        rysuj();
      })(0);

      // mysz: kursor = pompa
      window.addEventListener('pointermove', function (e) {
        if (e.pointerType !== 'mouse') return;
        kursor = [e.clientX, e.clientY];
      }, { passive: true });
      document.addEventListener('mouseleave', function () { kursor = null; });

      // klik na otwartej mapie = wiercenie studni (maks. 5)
      var sek = document.querySelector('.mapa-sek');
      if (sek) {
        sek.addEventListener('click', function (e) {
          if (e.target.closest('a, button, input, select, label')) return;
          wiercone.push([e.clientX, swiatY(e.clientY), POMPA.s, POMPA.R]);
          if (wiercone.length > 5) wiercone.shift();
        });
        // dotyk: przytrzymanie = pompa w tym miejscu
        var trzyma = null;
        sek.addEventListener('pointerdown', function (e) {
          if (e.pointerType === 'mouse') return;
          trzyma = setTimeout(function () { kursor = [e.clientX, e.clientY]; }, 220);
        });
        ['pointerup', 'pointercancel'].forEach(function (z) {
          sek.addEventListener(z, function (e) {
            if (e.pointerType === 'mouse') return;
            clearTimeout(trzyma); setTimeout(function () { kursor = null; }, 1600);
          });
        });
      }
      // przycisk „Włącz pompę” (telefon)
      qa('[data-pompuj]').forEach(function (b) {
        b.addEventListener('click', function () {
          kursor = [W * 0.5, Hh * 0.45];
          window.scrollTo({ top: 0, behavior: 'smooth' });
          b.textContent = 'Pompa pracuje — patrz na mapę';
          setTimeout(function () { kursor = null; b.textContent = 'Włącz pompę jeszcze raz'; }, 7000);
        });
      });
    }
  }

  /* ---- symulator ------------------------------------------------------- */
  qa('[data-sym]').forEach(function (f) {
    var q = f.querySelector('[data-q]'), k = f.querySelector('[data-k]');
    var licz = function () {
      var Q = +q.value, kk = +k.value, w = proba(Q, kk);
      f.querySelector('[data-q-out]').textContent = pl(Q);
      f.querySelector('[data-sym-uwaga]').hidden = !!w;
      if (!w) { ['[data-s]', '[data-rl]', '[data-qj]'].forEach(function (s) { f.querySelector(s).textContent = '—'; }); return; }
      f.querySelector('[data-s]').textContent = pl(w.s, 2) + ' m';
      f.querySelector('[data-rl]').textContent = pl(w.R, 0) + ' m';
      f.querySelector('[data-qj]').textContent = pl(Q / w.s, 1) + ' m³/h·m';
      POMPA.s = w.s; POMPA.R = Math.max(w.R, 1);
      krzywa(w);
    };
    q.addEventListener('input', licz); k.addEventListener('change', licz);
    licz();
  });

  /* ---- krzywa depresji (Dupuit): h(x)² = h_w² + (H² − h_w²)·ln(x/r)/ln(R/r) -- */
  function krzywa(w) {
    qa('[data-krzywa]').forEach(function (svg) {
      var H = MODEL.H, r = MODEL.r, hw = H - w.s, sx = 2.2, sy = 220 / H, cx = 320, top = 40;
      var pts = [], i, x, h, y;
      for (i = -60; i <= 60; i++) {
        x = Math.max(Math.abs(i) / 60 * Math.max(w.R, 1), r);
        h = x >= w.R ? H : Math.sqrt(hw * hw + (H * H - hw * hw) * Math.log(x / r) / Math.log(w.R / r));
        y = top + (H - h) * sy;
        pts.push((cx + (i < 0 ? -1 : 1) * Math.min(x * sx, 320)).toFixed(1) + ' ' + y.toFixed(1));
      }
      svg.querySelector('.kd__woda').setAttribute('d', 'M0 ' + top + ' L' + pts.join(' L') + ' L640 ' + top + ' L640 260 L0 260 Z');
      svg.querySelector('[data-kd-s]').textContent = 's = ' + pl(w.s, 2) + ' m';
      svg.querySelector('[data-kd-R]').textContent = 'R = ' + pl(w.R, 0) + ' m';
    });
  }

  /* ---- karta zgłoszenia ------------------------------------------------ */
  qa('[data-kz]').forEach(function (f) {
    var pod = f.querySelector('[data-kz-podglad]'), szac = f.querySelector('[data-kz-szac]');
    var TXT = { ogrod: 'podlewany ogród', dojazd: 'wiertnica dojedzie', prad: 'jest prąd', szambo: 'znam miejsce szamba' };
    var skladaj = function () {
      var miejsce = f.querySelector('[name=miejsce]').value.trim(), osoby = parseInt(f.querySelector('[name=osoby]').value, 10) || 0;
      var ogrod = f.querySelector('[name=ogrod]').checked, co = [];
      qa('input[type=checkbox]', f).forEach(function (c) { if (c.checked) co.push(TXT[c.name]); });
      var m3 = osoby * 0.1 * (ogrod ? 2 : 1);
      szac.textContent = osoby ? 'Zużycie szacunkowe: ok. ' + pl(m3, 1) + ' m³/d — ' + (m3 <= 5 ? 'w limicie 5 m³/d' : 'ponad 5 m³/d: pozwolenie wodnoprawne') : 'Zużycie szacunkowe: — m³/d';
      var t = 'Dzień dobry, pytam o studnię głębinową.';
      if (miejsce) t += '\nDziałka: ' + miejsce + '.';
      if (osoby) t += '\nW domu: ' + osoby + ' os. (ok. ' + pl(m3, 1) + ' m³/d).';
      if (co.length) t += '\nWiem: ' + co.join(', ') + '.';
      pod.textContent = t;
      return t;
    };
    f.addEventListener('input', skladaj); f.addEventListener('change', skladaj);
    var kop = f.querySelector('[data-kz-kopiuj]');
    if (kop) kop.addEventListener('click', function () {
      var t = skladaj();
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { kop.textContent = 'Skopiowane'; });
    });
    skladaj();
  });
})();
