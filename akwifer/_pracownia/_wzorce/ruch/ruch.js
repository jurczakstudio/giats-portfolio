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
