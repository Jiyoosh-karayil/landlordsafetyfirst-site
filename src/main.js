(function () {
  var C = window.LSF || {};
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* ---------- storage (can throw in some contexts) ---------- */
  function getPref(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function setPref(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* ---------- mobile menu ---------- */
  var menuBtn = $('.menu-btn'), nav = $('#nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---------- services menu ---------- */
  var megaBtn = $('.mega-btn'), mega = $('#mega');
  function closeMega() { if (mega) { mega.classList.remove('open'); megaBtn.setAttribute('aria-expanded', 'false'); } }
  if (megaBtn && mega) {
    megaBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = mega.classList.toggle('open');
      megaBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) { if (!mega.contains(e.target)) closeMega(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mega.classList.contains('open')) { closeMega(); megaBtn.focus(); }
    });
  }

  /* ---------- tracking: calls, WhatsApp, forms ---------- */
  function track(name, label) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, { event_category: 'lead', event_label: location.pathname });
    if (C.adsId && label) window.gtag('event', 'conversion', { send_to: C.adsId + '/' + label });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) track('call_click', C.labelCall);
    else if (href.indexOf('wa.me') > -1) track('whatsapp_click', C.labelWhatsapp);
  });

  /* ---------- consent (Consent Mode v2, default denied in <head>) ---------- */
  var bar = $('#consent');
  if (bar && C.analytics) {
    var choice = getPref('lsf-consent');
    if (choice === 'granted') grant();
    else if (!choice) bar.classList.add('show');
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      var v = b.getAttribute('data-consent');
      setPref('lsf-consent', v);
      if (v === 'granted') grant();
      bar.classList.remove('show');
    });
  }
  $$('[data-reset-consent]').forEach(function (b) {
    b.addEventListener('click', function () {
      try { localStorage.removeItem('lsf-consent'); } catch (e) {}
      if (bar) bar.classList.add('show'); else b.textContent = 'No tracking cookies are in use on this site right now.';
    });
  });
  function grant() {
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', { ad_storage: 'granted', analytics_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted' });
    }
  }

  /* ---------- dates: no booking in the past ---------- */
  var tmr = new Date(); tmr.setDate(tmr.getDate() + 1);
  var tmrIso = tmr.toISOString().slice(0, 10);
  $$('input[data-min-tomorrow]').forEach(function (i) { i.min = tmrIso; });

  /* ---------- EICR code checker ---------- */
  var checker = $('#checker');
  if (checker && C.codes) {
    var out = $('#verdict');
    var buttons = $$('.code-btn', checker);
    function show(code) {
      var d = C.codes[code];
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-code') === code ? 'true' : 'false'); });
      out.innerHTML = '<dl>' + row('Result', '<span class="status" style="background:' + d.colour + '">' + d.result + '</span>') +
        row('Means', d.means) + row('Deadline', d.deadline) + row('What we do', d.action) + row('Typical cost', d.cost) +
        '</dl><div class="cta btn-row">' + d.cta + '</div>';
    }
    function row(k, v) { return '<div class="verdict-row"><dt>' + k + '</dt><dd>' + v + '</dd></div>'; }
    buttons.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-code')); }); });
  }

  /* ---------- instant price picker (same maths as build.py) ---------- */
  var P = C.pricing;
  function money(n) { return '£' + Math.round(n).toLocaleString('en-GB'); }
  function vat(ex) { return Math.round(ex * (1 + P.vat)); }
  function roundTo(x) { return Math.floor(x / P.round + 0.5) * P.round; }
  function itemEx(it, type, beds) { return it.base[type] + Math.max(0, beds - it.incl[type]) * it.per[type]; }
  function calc(type, beds, ids) {
    var lines = [], certs = 0, addons = 0, n = 0;
    P.items.forEach(function (it) {
      if (ids.indexOf(it.id) < 0) return;
      var ex = itemEx(it, type, beds);
      lines.push([it.label, ex]);
      if (it.cert) { certs += ex; n++; } else addons += ex;
    });
    var rate = 0;
    P.tiers.forEach(function (t) { if (n >= t[0]) rate = t[1]; });
    var sub = certs + addons;
    var total = rate ? roundTo(certs * (1 - rate) + addons) : sub;
    var floored = total < P.min;
    if (floored) total = P.min;
    return { lines: lines, sub: sub, saving: floored ? 0 : Math.max(0, sub - total), rate: rate, ex: total, inc: vat(total), floored: floored };
  }
  var TYPE_TXT = { flat: 'Flat', house: 'House', hmo: 'HMO', commercial: 'Commercial premises' };

  function initPicker(root) {
    var beds = $('[name="beds"]', root), bedsLabel = $('[data-beds-label]', root);
    var params = new URLSearchParams(location.search);
    if (root.hasAttribute('data-read-url') && params.get('type')) {
      var r = $('input[name="ptype"][value="' + params.get('type') + '"]', root);
      if (r) r.checked = true;
      if (params.get('beds') && beds) beds.value = params.get('beds');
      var want = (params.get('items') || '').split(',');
      $$('input[name="item"]', root).forEach(function (c) { c.checked = want.indexOf(c.value) > -1; });
    }
    function state() {
      var t = ($('input[name="ptype"]:checked', root) || {}).value || 'flat';
      var b = beds ? parseInt(beds.value, 10) || 0 : 2;
      var ids = $$('input[name="item"]:checked', root).map(function (c) { return c.value; });
      return { type: t, beds: b, ids: ids };
    }
    function bedTxt(s) {
      if (s.type === 'hmo') return s.beds + ' lettable room' + (s.beds === 1 ? '' : 's');
      if (s.type === 'commercial') return '';
      return s.beds === 0 ? 'studio' : s.beds + ' bedroom' + (s.beds === 1 ? '' : 's');
    }
    function render() {
      var s = state();
      if (bedsLabel) bedsLabel.textContent = s.type === 'hmo' ? 'Lettable rooms' : 'Bedrooms';
      var commercial = s.type === 'commercial';
      root.classList.toggle('is-commercial', commercial);
      P.items.forEach(function (it) {
        var el = $('[data-price-for="' + it.id + '"]', root);
        if (el) el.textContent = commercial ? 'quote' : money(vat(itemEx(it, s.type, s.beds)));
      });
      var prop = $('[data-sum="prop"]', root), lines = $('[data-sum="lines"]', root), saving = $('[data-sum="saving"]', root),
          amt = $('[data-sum="amt"]', root), ex = $('[data-sum="ex"]', root), min = $('[data-sum="min"]', root),
          book = $('[data-sum="book"]', root), com = $('[data-sum="commercial"]', root), totalRow = $('[data-sum="total"]', root),
          hidden = $('input[name="quote_total"]', root);
      if (prop) prop.textContent = TYPE_TXT[s.type] + (bedTxt(s) ? ', ' + bedTxt(s) : '');
      if (commercial) {
        if (lines) lines.innerHTML = s.ids.length ? s.ids.map(function (id) {
          var it = P.items.filter(function (x) { return x.id === id; })[0]; return '<li><span>' + it.label + '</span><span>quote</span></li>'; }).join('') : '<li class="empty">Tick what you need.</li>';
        if (saving) saving.hidden = true;
        if (totalRow) totalRow.hidden = true;
        if (ex) ex.hidden = true;
        if (min) min.hidden = true;
        if (com) com.hidden = false;
        if (book) book.setAttribute('href', '/commercial/#quote');
        if (hidden) hidden.value = 'commercial: quote';
        return;
      }
      if (com) com.hidden = true;
      if (totalRow) totalRow.hidden = false;
      if (ex) ex.hidden = false;
      if (!s.ids.length) {
        if (lines) lines.innerHTML = '<li class="empty">Tick at least one certificate to see a price.</li>';
        if (saving) saving.hidden = true;
        if (amt) amt.textContent = '—';
        if (ex) ex.textContent = '';
        if (min) min.hidden = true;
        if (book) book.setAttribute('aria-disabled', 'true');
        if (hidden) hidden.value = '';
        return;
      }
      var q = calc(s.type, s.beds, s.ids);
      if (lines) lines.innerHTML = q.lines.map(function (l) { return '<li><span>' + l[0] + '</span><span class="tnum">' + money(vat(l[1])) + '</span></li>'; }).join('');
      if (saving) {
        saving.hidden = !q.saving;
        saving.innerHTML = '<span>Bundle saving (' + Math.round(q.rate * 100) + '%)</span><span class="tnum">−' + money(vat(q.sub) - q.inc) + '</span>';
      }
      if (amt) {
        if (amt.textContent !== money(q.inc)) { amt.classList.remove('tick'); void amt.offsetWidth; amt.classList.add('tick'); }
        amt.textContent = money(q.inc);
      }
      if (ex) ex.textContent = money(q.ex) + ' + VAT';
      if (min) min.hidden = !q.floored;
      if (book) {
        book.removeAttribute('aria-disabled');
        book.setAttribute('href', '/book/?type=' + s.type + '&beds=' + s.beds + '&items=' + s.ids.join(','));
      }
      if (hidden) hidden.value = money(q.inc) + ' inc VAT (' + money(q.ex) + ' + VAT)';
    }
    root.addEventListener('change', render);
    var bk = $('[data-sum="book"]', root);
    if (bk) bk.addEventListener('click', function (e) {
      if (bk.getAttribute('aria-disabled') === 'true') { e.preventDefault(); var f = $('input[name="item"]', root); if (f) f.focus(); }
    });
    render();
  }
  if (P) $$('[data-picker]').forEach(initPicker);

  /* ---------- forms: quote, booking, reminder ---------- */
  var SUBMIT_LABEL = {};
  $$('form[data-form]').forEach(function (form) {
    var type = form.getAttribute('data-form');
    var msg = $('.form-msg', form);
    var submit = $('button[type="submit"]', form);
    SUBMIT_LABEL[type] = submit ? submit.innerHTML : '';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      msg.className = 'form-msg';
      msg.textContent = '';
      var hp = $('.hp input', form);
      if (hp && hp.value) return; // bot
      var bad = [];
      $$('[required]', form).forEach(function (el) {
        var empty = el.type === 'checkbox' ? !el.checked : !String(el.value).trim();
        el.setAttribute('aria-invalid', empty ? 'true' : 'false');
        if (empty) bad.push(el);
      });
      if (type === 'booking' && !$$('input[name="item"]:checked', form).length && !(($('input[name="ptype"]:checked', form) || {}).value === 'commercial')) {
        msg.textContent = 'Tick at least one certificate or service at the top of the form.';
        msg.className = 'form-msg err';
        return;
      }
      if (bad.length) {
        var names = bad.map(function (el) {
          if (el.getAttribute('data-label')) return el.getAttribute('data-label');
          var l = el.id && $('label[for="' + el.id + '"]', form);
          return l ? l.textContent.replace(/\(optional\)/, '').trim() : el.name;
        });
        msg.textContent = 'Please fill in: ' + names.join(', ') + '.';
        msg.className = 'form-msg err';
        bad[0].focus();
        return;
      }
      var data = { form_type: type };
      new FormData(form).forEach(function (v, k) {
        if (k === 'company_url') return;
        v = String(v).trim();
        if (data[k] !== undefined) data[k] = [].concat(data[k], v); else data[k] = v;
      });
      data.page = location.pathname;
      data.submitted_at = new Date().toISOString();
      if (!C.formEndpoint) {
        msg.innerHTML = 'Online requests are not switched on yet. Call ' + C.phoneLink + ' and we will sort it out.';
        msg.className = 'form-msg err';
        return;
      }
      submit.disabled = true;
      submit.textContent = 'Sending…';
      fetch(C.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); })
        .then(function () {
          form.reset();
          if (type === 'reminder') msg.textContent = 'Done. We will remind you 30 days before it expires.';
          else if (type === 'booking') msg.textContent = 'Booking request sent. ' + C.responsePromise + ' We will confirm your slot and send a payment link.';
          else msg.textContent = 'Request sent. ' + C.responsePromise;
          msg.className = 'form-msg ok';
          track(type === 'booking' ? 'booking_request' : type === 'reminder' ? 'reminder_signup' : 'form_submit', type === 'booking' ? (C.labelBooking || C.labelForm) : C.labelForm);
        })
        .catch(function () {
          msg.innerHTML = 'That did not send. Call ' + C.phoneLink + ' or try again.';
          msg.className = 'form-msg err';
        })
        .then(function () { submit.disabled = false; submit.innerHTML = SUBMIT_LABEL[type]; });
    });
  });

  /* ---------- motion: header, headline, reveals, counters ---------- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var head = $('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  if (!reduce) {
    $$('[data-split]').forEach(function (el) {
      var i = 0;
      el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = document.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(function (part) {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
              var w = document.createElement('span'); w.className = 'w'; w.setAttribute('aria-hidden', 'true');
              var inner = document.createElement('span'); inner.textContent = part; inner.style.setProperty('--i', i++);
              w.appendChild(inner); frag.appendChild(w);
            });
            n.parentNode.replaceChild(frag, n);
          } else if (n.nodeType === 1) walk(n);
        });
      })(el);
    });
  }
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count')) || 0, t0 = null, dur = 1400 + Math.min(end, 40) * 15;
    if (reduce || end <= 1) { el.textContent = end; return; }
    el.textContent = '0';
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(end * e);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var revealEls = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        $$('[data-count]', en.target).forEach(function (c) { if (!c.getAttribute('data-done')) { c.setAttribute('data-done', '1'); countUp(c); } });
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }
})();
