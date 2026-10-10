/*! SE Consent — savas slapukų sutikimų valdiklis. Jokių išorinių priklausomybių. */
(function (w, d) {
  'use strict';
  var C = w.SE_CONSENT_CONFIG;
  if (!C || w.SEConsent) return;

  var CATS = ['necessary', 'preferences', 'statistics', 'marketing'];
  var COOKIE = 'se_consent';
  var T = C.t;
  var state = read();          // {id, v, t, m, c:{preferences:bool,...}} arba null
  var listeners = [];
  var queue = [];              // aktyvuojami scenarijai, vykdomi griežta DOM tvarka
  var running = false;

  // ---------------------------------------------------------------- Consent Mode v2
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }

  function gcmState(c) {
    var g = function (on) { return on ? 'granted' : 'denied'; };
    return {
      ad_storage: g(c.marketing),
      ad_user_data: g(c.marketing),
      ad_personalization: g(c.marketing),
      analytics_storage: g(c.statistics),
      functionality_storage: g(c.preferences),
      personalization_storage: g(c.preferences),
      security_storage: 'granted'
    };
  }

  if (C.gcm) {
    var def = gcmState({});
    def.wait_for_update = 500;
    gtag('consent', 'default', def);
    if (C.adsRedaction) gtag('set', 'ads_data_redaction', true);
    if (C.urlPassthrough) gtag('set', 'url_passthrough', true);
    // Google slapukai pagal nutylėjimą galioja 2 metus; ribojame iki 13 mėn. (taikoma visiems gtag config).
    if (C.gaCookieDays) gtag('set', { cookie_expires: C.gaCookieDays * 86400 });
    // Grįžtančiam lankytojui sutikimas pritaikomas sinchroniškai — pirmas puslapio peržiūros
    // įvykis jau keliauja su teisinga būsena (kaip Cookiebot).
    if (state) gtag('consent', 'update', gcmState(state.c));
  }

  // WP Consent API (WooCommerce, Site Kit ir kt. skaito šias reikšmes).
  w.wp_consent_type = 'optin';
  w.wp_fallback_consent_type = 'optin';

  // ---------------------------------------------------------------- būsena
  function read() {
    var m = d.cookie.match(/(?:^|;\s*)se_consent=([^;]+)/);
    if (!m) return null;
    try {
      var o = JSON.parse(decodeURIComponent(m[1]));
      if (!o || o.v !== C.version || !o.c) return null;
      return o;
    } catch (e) {
      return null;
    }
  }

  function write(o) {
    var v = encodeURIComponent(JSON.stringify(o));
    var c = COOKIE + '=' + v + ';path=/;max-age=' + (C.expiryDays * 86400) + ';SameSite=Lax';
    if (C.domain) c += ';domain=' + C.domain;
    if (location.protocol === 'https:') c += ';Secure';
    d.cookie = c;
  }

  function uuid() {
    if (w.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (ch) {
      var r = Math.random() * 16 | 0;
      return (ch === 'x' ? r : (r & 3 | 8)).toString(16);
    });
  }

  function allowed(cats) {
    var list = String(cats).split(',');
    for (var i = 0; i < list.length; i++) {
      var k = list[i].trim();
      if (k === 'necessary') continue;
      if (!state || !state.c[k]) return false;
    }
    return true;
  }

  function matchRule(str, rules) {
    if (!str) return null;
    var s = String(str).toLowerCase();
    for (var p in rules) {
      if (Object.prototype.hasOwnProperty.call(rules, p) && s.indexOf(p.toLowerCase()) !== -1) return rules[p];
    }
    return null;
  }

  // ---------------------------------------------------------------- blokavimas naršyklėje
  // Serveris jau užblokavo HTML'e esančius sekiklius. Čia gaudomi tie, kuriuos įterpia kiti
  // scenarijai vėliau (pvz. GTM Custom HTML žyma, įskiepio JS).
  var JS_TYPES = { '': 1, 'text/javascript': 1, 'application/javascript': 1, 'module': 1 };

  function neutralize(el, cat) {
    if (el.type && el.type !== 'text/plain') el.setAttribute('data-se-type', el.type);
    el.type = 'text/plain';
    el.setAttribute('data-se-consent', cat);
  }

  function guardNew(el) {
    if (el.hasAttribute('data-se-consent') || el.hasAttribute('data-se-consent-ignore')) return;
    if (!JS_TYPES[(el.getAttribute('type') || '').toLowerCase()]) return;
    var cat = el.src ? matchRule(el.src, C.rules.src) : matchRule(el.textContent, C.rules.inline);
    if (cat && cat !== 'necessary' && !allowed(cat)) neutralize(el, cat);
  }

  var srcDesc = w.HTMLScriptElement && Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src');
  var origCreate = d.createElement;
  d.createElement = function (tag) {
    var el = origCreate.apply(d, arguments);
    if (srcDesc && String(tag).toLowerCase() === 'script') {
      Object.defineProperty(el, 'src', {
        configurable: true,
        get: function () { return srcDesc.get.call(el); },
        set: function (v) {
          var cat = matchRule(v, C.rules.src);
          if (cat && cat !== 'necessary' && !allowed(cat) && !el.hasAttribute('data-se-consent-ignore')) neutralize(el, cat);
          srcDesc.set.call(el, v);
        }
      });
      var origSet = el.setAttribute;
      el.setAttribute = function (n, v) {
        if (String(n).toLowerCase() === 'src') { el.src = v; return; }
        return origSet.apply(el, arguments);
      };
    }
    return el;
  };

  // Firefox: parserio įterpti scenarijai sustabdomi prieš vykdymą.
  d.addEventListener('beforescriptexecute', function (e) {
    var el = e.target;
    if (el.type === 'text/plain') return;
    guardNew(el);
    if (el.type === 'text/plain') e.preventDefault();
  }, true);

  var observer = new MutationObserver(function (muts) {
    for (var i = 0; i < muts.length; i++) {
      var added = muts[i].addedNodes;
      for (var j = 0; j < added.length; j++) {
        var n = added[j];
        if (n.nodeType !== 1) continue;
        if (n.tagName === 'SCRIPT') {
          if (n.getAttribute('type') !== 'text/plain') guardNew(n);
          enqueue(n);
        } else if (n.tagName === 'IFRAME') {
          prepareFrame(n);
        }
      }
    }
  });
  observer.observe(d.documentElement, { childList: true, subtree: true });

  // ---------------------------------------------------------------- aktyvavimas
  function blockedCats(el) {
    return el.getAttribute('data-se-consent') || el.getAttribute('data-cookieconsent');
  }

  function enqueue(el) {
    if (el.tagName !== 'SCRIPT' || el.getAttribute('type') !== 'text/plain' || el.__seQueued) return;
    var cats = blockedCats(el);
    if (!cats || cats === 'ignore' || !allowed(cats)) return;
    el.__seQueued = true;
    queue.push(el);
    pump();
  }

  function pump() {
    if (running) return;
    var el = queue.shift();
    if (!el) return;
    running = true;
    var s = origCreate.call(d, 'script');
    for (var i = 0; i < el.attributes.length; i++) {
      var a = el.attributes[i];
      if (a.name === 'type' || a.name === 'data-se-type' || a.name === 'data-se-consent') continue;
      s.setAttribute(a.name, a.value);
    }
    s.setAttribute('data-se-consent-ignore', '');
    var t = el.getAttribute('data-se-type');
    if (t) s.type = t;
    var next = function () { running = false; pump(); };
    if (el.src) {
      s.async = el.hasAttribute('async');
      s.onload = s.onerror = next;
      srcDesc.set.call(s, el.src);
    } else {
      s.text = el.text;
    }
    if (el.parentNode) {
      el.parentNode.replaceChild(s, el);
    } else {
      (d.head || d.documentElement).appendChild(s);
    }
    // async scenarijus nelaukiamas (jis ir originaliai nelaukė); inline įvykdomas iškart.
    if (!el.src || s.async) next();
  }

  function activateAll() {
    var list = d.querySelectorAll('script[type="text/plain"][data-se-consent],script[type="text/plain"][data-cookieconsent]');
    for (var i = 0; i < list.length; i++) enqueue(list[i]);
    var frames = d.querySelectorAll('iframe[data-se-src]');
    for (var j = 0; j < frames.length; j++) prepareFrame(frames[j]);
  }

  function prepareFrame(f) {
    var cats = f.getAttribute('data-se-consent');
    if (!f.hasAttribute('data-se-src') || !cats) return;
    var ph = f.previousElementSibling;
    var hasPh = ph && ph.className === 'se-c-ph';
    if (allowed(cats)) {
      f.src = f.getAttribute('data-se-src');
      f.removeAttribute('data-se-src');
      f.style.display = '';
      if (hasPh) ph.parentNode.removeChild(ph);
      return;
    }
    if (hasPh || !d.body) return;
    ph = origCreate.call(d, 'div');
    ph.className = 'se-c-ph';
    ph.style.width = f.width ? f.width + 'px' : '100%';
    ph.style.height = f.height ? f.height + 'px' : '';
    ph.innerHTML = '<p></p><button type="button"></button>';
    ph.firstChild.textContent = T.blocked_content;
    ph.lastChild.textContent = T.blocked_button;
    ph.lastChild.onclick = function () {
      var c = current();
      cats.split(',').forEach(function (k) { c[k.trim()] = true; });
      save(c, 'placeholder');
    };
    f.style.display = 'none';
    f.parentNode.insertBefore(ph, f);
  }

  // ---------------------------------------------------------------- sutikimo išsaugojimas
  function current() {
    var c = {};
    for (var i = 1; i < CATS.length; i++) c[CATS[i]] = !!(state && state.c[CATS[i]]);
    return c;
  }

  function save(c, method) {
    var prev = state;
    var clean = {};
    for (var i = 1; i < CATS.length; i++) clean[CATS[i]] = !!c[CATS[i]];
    state = { id: prev ? prev.id : uuid(), v: C.version, t: Date.now(), m: method, c: clean };
    write(state);

    if (C.gcm) gtag('consent', 'update', gcmState(clean));
    var withdrawn = [];
    if (prev) {
      for (var k in prev.c) if (prev.c[k] && !clean[k]) withdrawn.push(k);
    }
    withdrawn.forEach(deleteCookies);

    log(state);
    hideBanner();
    announce(true);

    // Jau paleisto sekiklio "išjungti" neįmanoma — atšaukus sutikimą puslapis perkraunamas.
    if (withdrawn.length) {
      setTimeout(function () { location.reload(); }, 150);
      return;
    }
    activateAll();
  }

  function deleteCookies(cat) {
    var defs = (C.cookies && C.cookies[cat]) || [];
    var names = d.cookie.split(';').map(function (p) { return p.split('=')[0].trim(); });
    var host = location.hostname;
    var parts = host.split('.');
    var domains = ['', host, '.' + host];
    if (parts.length > 2) domains.push('.' + parts.slice(-2).join('.'));
    if (parts.length === 2) domains.push('.' + host);
    defs.forEach(function (def) {
      var re = new RegExp('^' + def[0].replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$');
      names.forEach(function (n) {
        if (!re.test(n)) return;
        domains.forEach(function (dm) {
          d.cookie = n + '=;path=/;max-age=0' + (dm ? ';domain=' + dm : '');
        });
      });
    });
  }

  function log(s) {
    if (!C.logUrl) return;
    var body = JSON.stringify({ id: s.id, v: s.v, m: s.m, c: s.c, u: location.pathname });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(C.logUrl, new Blob([body], { type: 'application/json' }))) return;
    } catch (e) { /* nukrenta į fetch */ }
    if (w.fetch) fetch(C.logUrl, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' } });
  }

  // ---------------------------------------------------------------- pranešimai kitiems
  function announce(changed) {
    var c = state ? state.c : {};
    var detail = { necessary: true, preferences: !!c.preferences, statistics: !!c.statistics, marketing: !!c.marketing, method: state && state.m, changed: !!changed };

    // WP Consent API
    var wp = { functional: true, preferences: detail.preferences, statistics: detail.statistics, 'statistics-anonymous': detail.statistics, marketing: detail.marketing };
    var ev = {};
    for (var k in wp) {
      var val = wp[k] ? 'allow' : 'deny';
      d.cookie = 'wp_consent_' + k + '=' + val + ';path=/;max-age=' + (C.expiryDays * 86400) + ';SameSite=Lax' + (C.domain ? ';domain=' + C.domain : '');
      ev[k] = val;
    }
    d.dispatchEvent(new CustomEvent('wp_listen_for_consent_change', { detail: ev }));

    w.dataLayer.push({ event: changed ? 'se_consent_update' : 'se_consent_ready', se_consent: detail });
    if (C.compat) {
      // Cookiebot dataLayer įvykiai — esami GTM trigeriai veikia be pakeitimų.
      w.dataLayer.push({ event: 'cookie_consent_update' });
      ['preferences', 'statistics', 'marketing'].forEach(function (k) {
        if (detail[k]) w.dataLayer.push({ event: 'cookie_consent_' + k });
      });
      syncCookiebot();
      fire('CookiebotOnConsentReady');
      if (changed) {
        var any = detail.preferences || detail.statistics || detail.marketing;
        fire(any ? 'CookiebotOnAccept' : 'CookiebotOnDecline');
        var cb = w[any ? 'CookiebotCallback_OnAccept' : 'CookiebotCallback_OnDecline'];
        if (typeof cb === 'function') try { cb(); } catch (e) { /* svetimas kodas */ }
      }
    }
    for (var i = 0; i < listeners.length; i++) {
      try { listeners[i](detail); } catch (e) { /* svetimas kodas */ }
    }
  }

  function fire(name) {
    try { w.dispatchEvent(new Event(name)); } catch (e) { /* senos naršyklės */ }
  }

  // ---------------------------------------------------------------- Cookiebot suderinamumas
  var Cookiebot = null;
  function syncCookiebot() {
    if (!Cookiebot) return;
    var c = state ? state.c : {};
    Cookiebot.consent = { necessary: true, preferences: !!c.preferences, statistics: !!c.statistics, marketing: !!c.marketing, method: state ? state.m : null, stamp: state ? state.id : '0' };
    Cookiebot.consented = !!(c.preferences || c.statistics || c.marketing);
    Cookiebot.declined = !!state && !Cookiebot.consented;
    Cookiebot.hasResponse = !!state;
    Cookiebot.consentID = state ? state.id : '0';
  }
  if (C.compat && !w.Cookiebot) {
    Cookiebot = {
      show: function () { showBanner(false); },
      hide: hideBanner,
      renew: function () { showBanner(true); },
      withdraw: function () { save({}, 'withdraw'); },
      submitCustomConsent: function (p, s, m) { save({ preferences: p, statistics: s, marketing: m }, 'custom'); },
      runScripts: activateAll
    };
    w.Cookiebot = w.CookieConsent = Cookiebot;
    syncCookiebot();
  }

  // ---------------------------------------------------------------- UI
  var root = null;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
    });
  }

  function build() {
    var c = current();
    var cats = '';
    CATS.forEach(function (k) {
      var info = T.cat[k];
      var list = (C.cookies && C.cookies[k]) || [];
      var rows = list.map(function (r) {
        return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td><td>' + esc(r[3]) + '</td></tr>';
      }).join('');
      var toggle = k === 'necessary'
        ? '<span class="se-c__on">' + esc(T.always_on) + '</span>'
        : '<input type="checkbox" role="switch" class="se-c__sw" data-cat="' + k + '" aria-label="' + esc(info[0]) + '"' + (c[k] ? ' checked' : '') + '>';
      cats += '<div class="se-c__cat"><div class="se-c__cat-h"><strong>' + esc(info[0]) + '</strong>' + toggle + '</div>' +
        '<p>' + esc(info[1]) + '</p>' +
        (rows ? '<details><summary>' + esc(T.cookies) + ' (' + list.length + ')</summary><table>' + rows + '</table></details>' : '') +
        '</div>';
    });

    root = origCreate.call(d, 'div');
    root.id = 'se-consent';
    root.className = 'se-c se-c--' + C.position;
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-labelledby', 'se-c-title');
    root.setAttribute('aria-describedby', 'se-c-body');
    root.style.setProperty('--se-c1', C.colors[0]);
    root.style.setProperty('--se-c2', C.colors[1]);
    root.innerHTML =
      '<div class="se-c__box" tabindex="-1">' +
        '<h2 id="se-c-title" class="se-c__title">' + esc(T.title) + '</h2>' +
        '<p id="se-c-body" class="se-c__body">' + esc(T.body) +
          (C.privacyUrl ? ' <a href="' + esc(C.privacyUrl) + '">' + esc(T.privacy) + '</a>' : '') + '</p>' +
        '<div class="se-c__details" hidden>' + cats + '</div>' +
        '<div class="se-c__actions">' +
          '<button type="button" class="se-c__btn se-c__btn--2" data-a="reject">' + esc(T.reject_all) + '</button>' +
          '<button type="button" class="se-c__btn se-c__btn--3" data-a="customize">' + esc(T.customize) + '</button>' +
          '<button type="button" class="se-c__btn se-c__btn--1" data-a="accept">' + esc(T.accept_all) + '</button>' +
        '</div>' +
      '</div>';
    root.addEventListener('click', onClick);
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && state) hideBanner();
    });
    d.body.appendChild(root);
  }

  function onClick(e) {
    var a = e.target.getAttribute && e.target.getAttribute('data-a');
    if (!a) return;
    if (a === 'accept') save({ preferences: true, statistics: true, marketing: true }, 'accept_all');
    else if (a === 'reject') save({}, 'reject_all');
    else if (a === 'customize') openDetails();
    else if (a === 'save') {
      var c = {};
      var sw = root.querySelectorAll('.se-c__sw');
      for (var i = 0; i < sw.length; i++) c[sw[i].getAttribute('data-cat')] = sw[i].checked;
      save(c, 'custom');
    }
  }

  function openDetails() {
    var det = root.querySelector('.se-c__details');
    det.hidden = false;
    root.classList.add('se-c--open');
    var b = root.querySelector('[data-a="customize"]');
    b.setAttribute('data-a', 'save');
    b.textContent = T.save;
    var t = root.querySelector('.se-c__title');
    t.textContent = T.settings_title;
    var first = root.querySelector('.se-c__sw');
    if (first) first.focus();
  }

  function showBanner(details) {
    if (!d.body) {
      d.addEventListener('DOMContentLoaded', function () { showBanner(details); });
      return;
    }
    if (root) root.parentNode.removeChild(root);
    build();
    if (details) openDetails();
    // Fokusas į patį dialogą, ne į "Sutinku" — joks pasirinkimas nėra peršamas.
    else root.querySelector('.se-c__box').focus({ preventScroll: true });
    var fb = d.getElementById('se-consent-reopen');
    if (fb) fb.hidden = true;
  }

  function hideBanner() {
    if (root && root.parentNode) root.parentNode.removeChild(root);
    root = null;
    floating();
  }

  function floating() {
    if (!C.floating || !state || !d.body) return;
    var b = d.getElementById('se-consent-reopen');
    if (!b) {
      b = origCreate.call(d, 'button');
      b.id = 'se-consent-reopen';
      b.type = 'button';
      b.className = 'se-c-fab';
      b.setAttribute('aria-label', T.reopen);
      b.title = T.reopen;
      b.style.setProperty('--se-c1', C.colors[0]);
      b.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5zm-4.5 9a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm4 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm5 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2zM9 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>';
      b.onclick = function () { showBanner(true); };
      d.body.appendChild(b);
    }
    b.hidden = false;
  }

  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href="#se-consent"],.se-consent-open,a[href*="Cookiebot.renew"],a[href*="Cookiebot.show"]');
    if (!a) return;
    e.preventDefault();
    showBanner(true);
  });

  // ---------------------------------------------------------------- viešas API
  w.SEConsent = {
    get: function () { return state ? JSON.parse(JSON.stringify(state)) : null; },
    has: function (cat) { return !!state && allowed(cat); },
    show: showBanner,
    hide: hideBanner,
    accept: function (c, method) { save(c || { preferences: true, statistics: true, marketing: true }, method || 'api'); },
    withdraw: function () { save({}, 'withdraw'); },
    onChange: function (fn) { listeners.push(fn); }
  };

  function boot() {
    activateAll();
    if (state) {
      announce(false);
      floating();
    } else {
      showBanner(false);
    }
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', boot);
  else boot();
})(window, document);
