(function () {
  gsap.registerPlugin(CustomEase);
  CustomEase.create("minaraSnap", "M0,0 C0.95,0.03 0,0.98 1,1");
  gsap.defaults({ ease: "minaraSnap" });
  var K = 1080 * 0.9 / 390, OX = 54, OY = 96;
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  function build() {
    var app = $('#app');
    // measure an element in app (pt) coordinates — called before any offsets are applied
    function R(el) {
      if (typeof el === 'string') el = $(el);
      var a = app.getBoundingClientRect(), b = el.getBoundingClientRect(), k = a.width / 390;
      var x = (b.left - a.left) / k, y = (b.top - a.top) / k, w = b.width / k, h = b.height / k;
      return { x: x, y: y, w: w, h: h, cx: x + w / 2, cy: y + h / 2 };
    }
    var tl = gsap.timeline({ paused: true });

    // ---- camera: focus point (pt) at zoom s; clamped so the frame never shows outside the app
    function camTo(t, px, py, s, d, ease) {
      if (s > 1) px = 195 + (px - 195) * 0.5; // lean toward the cursor, keep the rest of the row in frame
      var X = 540 - (OX + px * K) * s, Y = 960 - (OY + py * K) * s;
      X = Math.min(0, Math.max(1080 - 1080 * s, X));
      Y = Math.min(0, Math.max(1920 - 1920 * s, Y));
      tl.to('#cam', { x: X, y: Y, scale: s, duration: d || 0.7, ease: ease || 'minaraSnap' }, t);
    }
    function camReset(t, d) { tl.to('#cam', { x: 0, y: 0, scale: 1, duration: d || 0.6 }, t); }

    // ---- cursor
    function curShow(t, x, y) { tl.set('#cursor', { x: x, y: y }, t); tl.to('#dot', { opacity: 1, scale: 1, duration: 0.25, ease: 'power2.out' }, t); }
    function curHide(t) { tl.to('#dot', { opacity: 0, scale: 0.6, duration: 0.25, ease: 'power2.in' }, t); }
    function curMove(t, x, y, d) { tl.to('#cursor', { x: x, y: y, duration: d || 0.45 }, t); }
    function tap(t) {
      tl.to('#dot', { scale: 0.78, duration: 0.08, ease: 'power2.out' }, t);
      tl.to('#dot', { scale: 1, duration: 0.18, ease: 'back.out(2)' }, t + 0.08);
      tl.fromTo('#rip', { scale: 0.4, opacity: 0.55 }, { scale: 2.1, opacity: 0, duration: 0.5, ease: 'power2.out', immediateRender: false }, t);
    }
    function moveTap(t, el, d) { var r = (typeof el === 'string') ? MAP[el] : el; if (!r) throw new Error('unmeasured ' + el); curMove(t, r.cx, r.cy, d || 0.45); tap(t + (d || 0.45) + 0.03); return t + (d || 0.45) + 0.03; }

    // ---- push transition helpers
    function pushIn(t, inSel, outSel) {
      tl.fromTo(inSel, { x: 390 }, { x: 0, duration: 0.45, immediateRender: false }, t);
      if (outSel) tl.to(outSel, { x: -110, duration: 0.45 }, t);
    }
    function pushBack(t, outSel, inSel) {
      tl.to(outSel, { x: 390, duration: 0.45 }, t);
      if (inSel) tl.fromTo(inSel, { x: -110 }, { x: 0, duration: 0.45, immediateRender: false }, t);
    }

    // ---- streaming words: wrap words of .stream nodes into spans (setup only)
    function splitWords(el) {
      var words = [];
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var parts = c.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
            parts.forEach(function (p) {
              if (!p) return;
              if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
              var s = document.createElement('span'); s.textContent = p; s.className = 'w'; frag.appendChild(s); words.push(s);
            });
            node.replaceChild(frag, c);
          } else if (c.nodeType === 1 && !c.classList.contains('n')) { walk(c); }
          else if (c.nodeType === 1) { words.push(c); }
        });
      })(el);
      return words;
    }
    function stream(t, el, per) {
      var ws = splitWords(typeof el === 'string' ? $(el) : el);
      gsap.set(ws, { opacity: 0 });
      ws.forEach(function (w, i) { tl.to(w, { opacity: 1, duration: 0.18, ease: 'power1.out' }, t + i * (per || 0.045)); });
      return t + ws.length * (per || 0.045);
    }

    // ================= MEASURE (all at rest) =================
    var m = {
      input: R('#composer .field'), send: R('#send'), status: R('#status'), chips: R('#chips'),
      p2: R('#p2'), ways: R('#ways'), hWays: R('#h-ways'), hRun: R('#h-run'), cc1: R('#cc1'), cc1ret: R('#cc1-ret'), cc1run: R('#cc1-run'),
      tStrat: R('#t-strat'), tabMkt: R('#tab-mkt'), fbtn: R('#fbtn'), pillBtc: R('#pill-btc'), fconfirm: R('#fconfirm'),
      cardTop: R('#card-top'), kgrid: R('#kgrid'), btnRun: R('#btn-run'),
