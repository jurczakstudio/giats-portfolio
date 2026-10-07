/* ruch.js — warstwa ruchu Jurczak Studio. Zero bibliotek, ES5.
   Kontrakt nazw: NASTART.md, część D1. Kopiuj ten plik do projektu bez zmian;
   sygnaturę projektu dopisuj OSOBNO, poniżej, albo we własnym pliku.

   Trzy bezpieczniki (NASTART.md D2):
     1. prefers-reduced-motion: reduce  -> wszystko od razu w pozycji końcowej
     2. ?static=1 w adresie             -> to samo (zrzuty, audyt)
     3. .js-gate                        -> HTML jest kompletny bez JS; klasę ukrywającą
                                           (`ruch`) dokłada dopiero ten plik

   Obsługiwane atrybuty:
     data-rv="up|mask|split|scale"  odsłonięcie w kadrze; data-rvd = opóźnienie ms
     data-seq="60"                  dzieci wchodzą po kolei, co 60 ms
     data-par="0.2"                 paralaksa warstwy, -1..1
     data-pin="200"                 sekcja przyklejona na 200vh przewijania
     data-scrub                     postęp 0..1 sekcji podawany do CSS jako --p
     data-count="12,5"              licznik liczby (przecinek = separator dziesiętny)
     data-hover                     pozycja kursora jako --mx/--my w procentach
     data-drag  data-drift="0.35"   poziome przeciąganie + powolny dryf
*/
(function () {
  'use strict';

  var root = document.documentElement;
  var STATYCZNIE =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
    /[?&]static=1/.test(location.search);

  /* ---- 1. bramka JS ------------------------------------------------------
     Dopiero tutaj wolno cokolwiek ukryć. Bez tego pliku (albo z błędem w nim)
     strona zostaje kompletna, tylko bez ruchu. */
  if (!STATYCZNIE) root.classList.add('ruch');
  else root.classList.add('ruch-off');

  var qa = function (sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  };

  /* ---- 2. odsłanianie: data-rv, data-seq --------------------------------- */
  (function () {
    // data-seq rozdaje dzieciom opóźnienia, zanim ruszy obserwator
    qa('[data-seq]').forEach(function (kon) {
      var krok = parseInt(kon.getAttribute('data-seq'), 10) || 60;
      var dzieci = qa('[data-rv]', kon);
      if (!dzieci.length) dzieci = Array.prototype.slice.call(kon.children);
      dzieci.forEach(function (el, i) {
        if (!el.hasAttribute('data-rv')) el.setAttribute('data-rv', 'up');
        if (!el.hasAttribute('data-rvd')) el.setAttribute('data-rvd', i * krok);
      });
    });

    var cele = qa('[data-rv]');
    if (!cele.length) return;

    var odsloń = function (el, natychmiast) {
      if (el.classList.contains('in')) return;
      var d = natychmiast ? 0 : parseInt(el.getAttribute('data-rvd'), 10) || 0;
      el.style.setProperty('--rvd', d + 'ms');
      el.classList.add('in');
    };

    if (STATYCZNIE) { cele.forEach(function (el) { odsloń(el, true); }); return; }

    // Szybkie przewijanie zostawiało puste ekrany (bug złapany u Lewartowskich
    // 16.09.2026). Dlatego: zapas 20% w dół ORAZ pomiar prędkości — przy szybkim
    // scrollu odsłaniamy bez opóźnień, bo i tak nikt nie zobaczy choreografii.
    var ostY = window.scrollY, predkosc = 0, ostT = performance.now();
    var mierz = function () {
      var t = performance.now(), dt = t - ostT;
      if (dt > 0) {
        predkosc = Math.abs(window.scrollY - ostY) / dt * 1000; // px/s
        ostY = window.scrollY; ostT = t;
      }
      requestAnimationFrame(mierz);
    };
    requestAnimationFrame(mierz);

    // Brak IntersectionObserver (bardzo stara przeglądarka): nie ma czego pilnować,
    // pokazujemy wszystko od razu. Inaczej klasa `ruch` zostałaby na <html>
    // i strona byłaby pusta.
    if (typeof IntersectionObserver !== 'function') {
      cele.forEach(function (el) { odsloń(el, true); });
      return;
    }

    // Sygnałem życia obserwatora jest WYWOŁANIE callbacku, nie odsłonięcie.
    // IntersectionObserver zawsze zgłasza pierwszą partię wpisów — także dla
    // elementów poza ekranem, z isIntersecting === false, które odrzucamy niżej.
    // Gdyby czuwak pytał „czy coś się odsłoniło", na stronie bez [data-rv]
    // w pierwszym ekranie odpaliłby się mimo sprawnego obserwatora.
    var zyje = false;

    var io = new IntersectionObserver(function (wpisy) {
      zyje = true;
      wpisy.forEach(function (w) {
        if (!w.isIntersecting) return;
        odsloń(w.target, predkosc > 2200);
        io.unobserve(w.target);
      });
    }, { rootMargin: '0px 0px 20% 0px', threshold: 0.05 });

    cele.forEach(function (el) { io.observe(el); });

    // Czuwak: TYLKO gdy obserwator nie dał znaku życia (błąd, nietypowa
    // przeglądarka). Wcześniej odsłaniał bezwarunkowo, przez co każde
    // odsłonięcie poniżej pierwszego ekranu działo się po 1,2 s od wejścia,
    // a nie przy dojściu do sekcji — choreografia scrollowa była martwa
    // na każdej stronie pracowni.
    //
    // W karcie w tle przeglądarka wstrzymuje rAF i dostarczanie wpisów
    // obserwatora, więc „brak znaku życia" znaczy tam „nikt nie patrzy",
    // a nie „obserwator padł". Gdybyśmy odsłonili, użytkownik po powrocie
    // do karty zastałby całą stronę już rozpakowaną. Dlatego w tle czuwak
    // się nie wykonuje, tylko przekłada na moment, gdy karta wróci.
    var czuwak = function () {
      if (zyje) return;
      if (document.hidden) {
        document.addEventListener('visibilitychange', function wroc() {
          if (document.hidden) return;
          document.removeEventListener('visibilitychange', wroc);
          setTimeout(czuwak, 1200);
        });
        return;
      }
      cele.forEach(function (el) { odsloń(el, true); });
    };
    setTimeout(czuwak, 1200);

    // Wydruk i wyszukiwanie w treści (Ctrl+F) muszą widzieć wszystko.
    window.addEventListener('beforeprint', function () {
      cele.forEach(function (el) { odsloń(el, true); });
    });
  })();

  /* ---- 3. scroll: data-par, data-pin, data-scrub -------------------------
     Jedna pętla rAF na całą stronę, jeden odczyt układu na klatkę.          */
  (function () {
    var par = qa('[data-par]');
    var scrub = qa('[data-scrub]');
    qa('[data-pin]').forEach(function (s) {
      s.style.setProperty('--pin', (parseInt(s.getAttribute('data-pin'), 10) || 200) + 'vh');
    });

    if (STATYCZNIE || (!par.length && !scrub.length)) {
      scrub.forEach(function (el) { el.style.setProperty('--p', '1'); });
      return;
    }

    var h = window.innerHeight;
    window.addEventListener('resize', function () { h = window.innerHeight; }, { passive: true });

    var widoczny = function (r) { return r.bottom > -200 && r.top < h + 200; };

    (function petla() {
      if (!document.hidden) {
        par.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (!widoczny(r)) return;
          var sila = parseFloat(el.getAttribute('data-par')) || 0;
          // -1 na górze ekranu, +1 na dole
          var t = (r.top + r.height / 2 - h / 2) / (h / 2);
          el.style.setProperty('--par', (t * sila * 100).toFixed(2) + 'px');
        });

        scrub.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (!widoczny(r)) return;
          var zakres = r.height + h;
          var p = zakres > 0 ? (h - r.top) / zakres : 0;
          el.style.setProperty('--p', Math.min(1, Math.max(0, p)).toFixed(4));
        });
      }
      requestAnimationFrame(petla);
    })();
  })();

  /* ---- 4. liczniki: data-count ------------------------------------------ */
  (function () {
    var liczniki = qa('[data-count]');
    if (!liczniki.length) return;

    var ustaw = function (el, v, dec) {
      el.textContent = v.toFixed(dec).replace('.', ',');
    };
    var docelowa = function (el) {
      return parseFloat((el.getAttribute('data-count') || '0').replace(',', '.'));
    };
    var miejsca = function (el) {
      return ((el.getAttribute('data-count') || '').split(',')[1] || '').length;
    };

    if (STATYCZNIE) {
      liczniki.forEach(function (el) { ustaw(el, docelowa(el), miejsca(el)); });
      return;
    }

    var io = new IntersectionObserver(function (wpisy) {
      wpisy.forEach(function (w) {
        if (!w.isIntersecting) return;
        var el = w.target, koniec = docelowa(el), dec = miejsca(el), start = null;
        io.unobserve(el);
        (function tik(ts) {
          if (!start) start = ts;
          var p = Math.min(1, (ts - start) / 1400);
          ustaw(el, koniec * (1 - Math.pow(1 - p, 3)), dec);
          if (p < 1) requestAnimationFrame(tik);
        })(performance.now());
      });
    }, { threshold: 0.4 });

    liczniki.forEach(function (el) { io.observe(el); });
  })();

  /* ---- 5. światło pod kursorem: data-hover ------------------------------
     Zapis do CSS raz na klatkę, nie raz na zdarzenie.                       */
  (function () {
    var cele = qa('[data-hover]');
    if (!cele.length || STATYCZNIE) return;

    var czeka = null;
    var brudny = { el: null, x: 50, y: 50 };
    var zapisz = function () {
      czeka = null;
      if (!brudny.el) return;
      brudny.el.style.setProperty('--mx', brudny.x.toFixed(1) + '%');
      brudny.el.style.setProperty('--my', brudny.y.toFixed(1) + '%');
    };

    cele.forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        brudny.el = el;
        brudny.x = (e.clientX - r.left) / r.width * 100;
        brudny.y = (e.clientY - r.top) / r.height * 100;
        if (!czeka) czeka = requestAnimationFrame(zapisz);
      }, { passive: true });

      el.addEventListener('pointerleave', function () {
        el.style.removeProperty('--mx');
        el.style.removeProperty('--my');
      });
    });
  })();

  /* ---- 6. przeciąganie i dryf: data-drag -------------------------------- */
  (function () {
    qa('[data-drag]').forEach(function (sc) {
      var dotkniety = STATYCZNIE, wcisniety = false, sx = 0, sl = 0, ruch = 0;
      var dryf = parseFloat(sc.getAttribute('data-drift'));
      if (isNaN(dryf)) dryf = 0.35;

      var stop = function () { dotkniety = true; };
      ['wheel', 'touchstart', 'focusin', 'keydown'].forEach(function (z) {
        sc.addEventListener(z, stop, { passive: true });
      });

      if (dryf > 0 && !STATYCZNIE) {
        (function petla() {
          if (dotkniety) return;
          if (!document.hidden) {
            sc.scrollLeft += dryf;
            // zawinięcie, żeby dryf nie kończył się ścianą
            if (sc.scrollLeft + sc.clientWidth >= sc.scrollWidth - 1) sc.scrollLeft = 0;
          }
          requestAnimationFrame(petla);
        })();
      }

      sc.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        wcisniety = true; ruch = 0; sx = e.clientX; sl = sc.scrollLeft;
        sc.classList.add('ciagnie'); stop();
      });
      window.addEventListener('pointermove', function (e) {
        if (!wcisniety) return;
        var dx = e.clientX - sx;
        ruch = Math.max(ruch, Math.abs(dx));
        sc.scrollLeft = sl - dx;
      });
      window.addEventListener('pointerup', function () {
        wcisniety = false; sc.classList.remove('ciagnie');
      });
      // Przeciągnięcie nie może zadziałać jak kliknięcie w kafelek.
      sc.addEventListener('click', function (e) {
        if (ruch > 6) { e.preventDefault(); e.stopPropagation(); }
      }, true);
    });
  })();
})();

/* AKWIFER v2 „ZLECENIE” — karta zlecenia (W4), tryb właściciela (W5), kalkulator dla firm.
   Wycena liczona tak samo jak w build.py: wycena(). Bez JS karta pokazuje wartości z buildu. */
(function () {
  'use strict';
  var D = {"gminy": [{"slug": "lubon", "nazwa": "Luboń", "mediana": 14.0, "otworow": 12, "min": 11.9, "gzwp": ""}, {"slug": "poznan", "nazwa": "Poznań", "mediana": 17.0, "otworow": 410, "min": 10.0, "gzwp": ""}, {"slug": "tarnowo-podgorne", "nazwa": "Tarnowo Podgórne", "mediana": 36.0, "otworow": 16, "min": 15.0, "gzwp": ""}, {"slug": "mosina", "nazwa": "Mosina", "mediana": 40.0, "otworow": 66, "min": 17.0, "gzwp": "Pradolina Warszawa – Berlin (GZWP 150)"}, {"slug": "suchy-las", "nazwa": "Suchy Las", "mediana": 43.0, "otworow": 17, "min": 15.0, "gzwp": ""}, {"slug": "buk", "nazwa": "Buk", "mediana": 46.5, "otworow": 6, "min": 10.2, "gzwp": "Dolina Kopalna Wielkopolska (GZWP 144)"}, {"slug": "steszew", "nazwa": "Stęszew", "mediana": 49.6, "otworow": 12, "min": 21.0, "gzwp": "Dolina Kopalna Wielkopolska (GZWP 144)"}, {"slug": "dopiewo", "nazwa": "Dopiewo", "mediana": 51.7, "otworow": 9, "min": 30.0, "gzwp": ""}, {"slug": "rokietnica", "nazwa": "Rokietnica", "mediana": 56.5, "otworow": 20, "min": 19.5, "gzwp": ""}, {"slug": "kleszczewo", "nazwa": "Kleszczewo", "mediana": 64.0, "otworow": 8, "min": 43.0, "gzwp": "Subzbiornik Inowrocław - Gniezno (GZWP 143)"}, {"slug": "swarzedz", "nazwa": "Swarzędz", "mediana": 65.0, "otworow": 35, "min": 10.0, "gzwp": "Subzbiornik Inowrocław - Gniezno (GZWP 143)"}, {"slug": "czerwonak", "nazwa": "Czerwonak", "mediana": 71.5, "otworow": 16, "min": 10.5, "gzwp": ""}, {"slug": "kornik", "nazwa": "Kórnik", "mediana": 100.0, "otworow": 27, "min": 12.5, "gzwp": "Dolina Kopalna Wielkopolska (GZWP 144)"}, {"slug": "komorniki", "nazwa": "Komorniki", "mediana": 110.0, "otworow": 5, "min": 22.0, "gzwp": ""}], "rynek": {"mb": [200, 350], "osprzet": [2500, 8000]}, "zuzycie": 0.1, "cele": {"dom": ["Dom", 1.0], "ogrod": ["Dom i ogród", 2.0], "nawadnianie": ["Ogród / nawadnianie", 3.0]}, "termin": "listopad 2026 — 3 wolne dni", "tel": "+48000000000"};
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
