/*! SE Consent standalone — sugeneruota 2026-10-10 */
window.SE_CONSENT_CONFIG={"version":1,"expiryDays":365,"domain":"","gcm":true,"adsRedaction":true,"urlPassthrough":false,"gaCookieDays":395,"gpc":true,"uet":true,"clarity":true,"services":[["ga4","Google Analytics","statistics",["_ga","_ga_*","_gid","_gat*"]],["clarity","Microsoft Clarity","statistics",["_clck","_clsk","CLID","MUID"]],["google-ads","Google Ads","marketing",["_gcl_au","_gcl_aw","_gcl_dc","_gcl_gb"]],["meta","Meta (Facebook) Pixel","marketing",["_fbp","_fbc"]],["tiktok","TikTok Pixel","marketing",["_ttp","_tt_enable_cookie","ttcsid*"]],["youtube","YouTube","marketing",[]],["maps","Google Maps","marketing",[]]],"compat":true,"floating":true,"position":"bottom","logUrl":"","privacyUrl":"/privatumo-politika/","colors":["#142b6f","#ffd602"],"rules":{"src":{"google-analytics.com/analytics.js":"statistics:ga4","clarity.ms":"statistics:clarity","static.hotjar.com":"statistics:hotjar","script.hotjar.com":"statistics:hotjar","mc.yandex.ru":"statistics:yandex","player.vimeo.com":"statistics:vimeo","googleadservices.com":"marketing:google-ads","googlesyndication.com":"marketing:google-ads","doubleclick.net":"marketing:google-ads","connect.facebook.net":"marketing:meta","facebook.com/tr":"marketing:meta","analytics.tiktok.com":"marketing:tiktok","bat.bing.com":"marketing:bing","snap.licdn.com":"marketing:linkedin","s.pinimg.com":"marketing:pinterest","static.criteo.net":"marketing:criteo","static.klaviyo.com":"marketing:klaviyo","omnisnippet1.com":"marketing:omnisend","omnisrc.com":"marketing:omnisend","js.hs-scripts.com":"marketing:hubspot","youtube.com/embed":"marketing:youtube","youtube-nocookie.com/embed":"marketing:youtube","google.com/maps":"marketing:maps","maps.googleapis.com":"marketing:maps"},"inline":{"clarity.ms":"statistics:clarity","hotjar.com":"statistics:hotjar","mc.yandex.ru":"statistics:yandex","fbq(":"marketing:meta","ttq.load":"marketing:tiktok","ttq.page":"marketing:tiktok","uetq":"marketing:bing","_linkedin_partner_id":"marketing:linkedin","pintrk(":"marketing:pinterest","klaviyo":"marketing:klaviyo","omnisend":"marketing:omnisend"}},"cookies":{"necessary":[["se_consent","sleepingexpert.lt","Išsaugo jūsų slapukų sutikimą","1 metai"],["woocommerce_cart_hash","sleepingexpert.lt","Krepšelio turinio pakeitimų sekimas","Sesija"],["woocommerce_items_in_cart","sleepingexpert.lt","Ar krepšelyje yra prekių","Sesija"],["wp_woocommerce_session_*","sleepingexpert.lt","Krepšelio sesija","2 dienos"],["wordpress_logged_in_*","sleepingexpert.lt","Prisijungimo sesija","Sesija"]],"statistics":[["_ga","Google","Unikalus lankytojo identifikatorius statistikai","2 metai"],["_ga_*","Google","Sesijos būsena Google Analytics 4","2 metai"],["_clck","Microsoft Clarity","Clarity lankytojo ID","1 metai"],["_clsk","Microsoft Clarity","Clarity sesijos sujungimas","1 diena"]],"marketing":[["_gcl_au","Google","Google Ads konversijų sekimas","3 mėnesiai"],["_fbp","Meta","Meta reklamos ir konversijų sekimas","3 mėnesiai"],["_fbc","Meta","Paspaudimo ant Meta reklamos identifikatorius","3 mėnesiai"],["IDE","Google (doubleclick.net)","Reklamos rodymas ir matavimas","13 mėnesių"]]},"t":{"title":"Mes naudojame slapukus","body":"Būtinieji slapukai užtikrina svetainės ir krepšelio veikimą. Su jūsų sutikimu naudosime ir statistikos bei rinkodaros slapukus, kad tobulintume svetainę ir rodytume aktualius pasiūlymus. Sutikimą galite bet kada pakeisti.","accept_all":"Sutinku su visais","reject_all":"Tik būtinieji","customize":"Nustatymai","save":"Išsaugoti pasirinkimą","privacy":"Privatumo politika","settings_title":"Slapukų nustatymai","always_on":"Visada įjungta","blocked_content":"Šis turinys rodomas tik sutikus su rinkodaros slapukais.","blocked_button":"Leisti ir rodyti","reopen":"Slapukų nustatymai","cookies":"Slapukai","services":"Paslaugos","cat":{"necessary":["Būtinieji","Reikalingi svetainės veikimui: krepšelis, prisijungimas, saugumas, jūsų sutikimo išsaugojimas. Jų išjungti negalima."],"preferences":["Nuostatų","Įsimena jūsų pasirinkimus, pvz. kalbą ar regioną."],"statistics":["Statistikos","Padeda suprasti, kaip lankytojai naudojasi svetaine (anonimizuota statistika)."],"marketing":["Rinkodaros","Naudojami reklamai ir jos efektyvumui matuoti (Google Ads, Meta ir kt.)."]}}};
(function(d){var s=d.createElement("style");s.id="se-consent-css";s.textContent=".se-c{--se-c1:#142b6f;--se-c2:#ffd602;position:fixed;z-index:2147483646;left:0;right:0;bottom:0;display:flex;justify-content:center;padding:12px;font:14px/1.5 system-ui,-apple-system,\"Segoe UI\",Roboto,sans-serif;color:#1d1d1f;pointer-events:none}\n.se-c--center{top:0;align-items:center;background:rgba(0,0,0,.45);pointer-events:auto}\n.se-c__box{pointer-events:auto;box-sizing:border-box;width:100%;max-width:960px;max-height:calc(100vh - 24px);overflow:auto;background:#fff;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.25);padding:20px 22px}\n.se-c__box:focus{outline:none}\n.se-c--open .se-c__box{max-width:720px}\n.se-c__title{margin:0 0 6px;font-size:18px;font-weight:700;line-height:1.3;color:var(--se-c1)}\n.se-c__body{margin:0 0 14px}\n.se-c__body a{color:var(--se-c1);text-decoration:underline}\n.se-c__actions{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}\n.se-c__btn{flex:1 1 180px;min-height:44px;padding:10px 16px;border-radius:8px;border:2px solid var(--se-c1);font-family:inherit;font-size:15px;font-weight:600;line-height:1.2;cursor:pointer}\n.se-c__btn--1{background:var(--se-c1);color:#fff}\n.se-c__btn--2{background:var(--se-c1);color:#fff}\n.se-c__btn--3{background:#fff;color:var(--se-c1)}\n.se-c__btn:hover{filter:brightness(1.12)}\n.se-c__btn:focus-visible,.se-c__sw:focus-visible,.se-c-fab:focus-visible,.se-c-ph button:focus-visible{outline:3px solid var(--se-c2);outline-offset:2px}\n.se-c__details{margin:0 0 14px}\n.se-c__cat{border-top:1px solid #e5e5ea;padding:10px 0}\n.se-c__cat p{margin:4px 0;color:#48484a}\n.se-c__cat-h{display:flex;justify-content:space-between;align-items:center;gap:12px}\n.se-c__on{font-size:12px;color:#2e7d32;font-weight:600}\n.se-c__sw{appearance:none;-webkit-appearance:none;position:relative;flex:none;width:44px;height:24px;margin:0;border-radius:12px;background:#c7c7cc;cursor:pointer;transition:background .15s}\n.se-c__sw::after{content:\"\";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;transition:transform .15s}\n.se-c__sw:checked{background:var(--se-c1)}\n.se-c__sw:checked::after{transform:translateX(20px)}\n.se-c__svcs{list-style:none;margin:6px 0 4px;padding:0 0 0 12px;border-left:2px solid #e5e5ea}\n.se-c__svcs li{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:4px 0;font-size:13px}\n.se-c__sw--svc{width:36px;height:20px}\n.se-c__sw--svc::after{width:14px;height:14px}\n.se-c__sw--svc:checked::after{transform:translateX(16px)}\n.se-c details summary{cursor:pointer;color:var(--se-c1);font-size:13px}\n.se-c table{width:100%;border-collapse:collapse;font-size:12px;margin-top:6px}\n.se-c td{padding:4px 6px;border-bottom:1px solid #f0f0f3;vertical-align:top;word-break:break-word}\n.se-c-fab{--se-c1:#142b6f;position:fixed;z-index:2147483645;left:16px;bottom:16px;width:44px;height:44px;border-radius:50%;border:0;background:var(--se-c1);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.25);opacity:.85}\n.se-c-fab:hover{opacity:1}\n.se-c-fab[hidden]{display:none}\n.se-c-ph{box-sizing:border-box;max-width:100%;min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:16px;background:#f2f2f7;border-radius:8px;text-align:center;font:14px/1.5 system-ui,sans-serif}\n.se-c-ph p{margin:0}\n.se-c-ph button{min-height:40px;padding:8px 16px;border:0;border-radius:8px;background:#142b6f;color:#fff;font-weight:600;cursor:pointer}\n@media (max-width:600px){.se-c{padding:0}.se-c__box{border-radius:12px 12px 0 0;padding:16px}.se-c__btn{flex-basis:100%}.se-c--center .se-c__box{border-radius:12px;margin:12px}}\n@media (prefers-reduced-motion:reduce){.se-c__sw,.se-c__sw::after{transition:none}}";(d.head||d.documentElement).appendChild(s)})(document);
/*! SE Consent — savas slapukų sutikimų valdiklis. Jokių išorinių priklausomybių. */
(function (w, d) {
  'use strict';
  var C = w.SE_CONSENT_CONFIG;
  if (!C || w.SEConsent) return;

  var CATS = ['necessary', 'preferences', 'statistics', 'marketing'];
  var COOKIE = 'se_consent';
  // Tekstai: vienos kalbos (C.t) arba kelių (C.i18n), parenkama pagal <html lang>.
  var T = C.t || (C.i18n && (C.i18n[(d.documentElement.lang || '').slice(0, 2).toLowerCase()] || C.i18n[C.defaultLang] || C.i18n[Object.keys(C.i18n)[0]]));
  var state = read();          // {id, v, t, m, c:{preferences:bool,...}, s:{paslauga:false}} arba null
  var SVC = C.services || [];  // [[id, pavadinimas, kategorija, [slapukai]], ...]
  var lastFocus = null;
  var listeners = [];
  var queue = [];              // aktyvuojami scenarijai, vykdomi griežta DOM tvarka
  var running = false;

  // ---------------------------------------------------------------- Consent Mode v2
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }

  // Paslauga leidžiama, kai įjungta jos kategorija ir lankytojas jos atskirai neišjungė.
  function svcOn(st, id, cat) {
    return !!(st && st.c[cat] && !(st.s && st.s[id] === false));
  }

  function gcmState(c, s) {
    var g = function (on) { return on ? 'granted' : 'denied'; };
    var st = { c: c, s: s };
    var ads = svcOn(st, 'google-ads', 'marketing');
    return {
      ad_storage: g(ads),
      ad_user_data: g(ads),
      ad_personalization: g(ads),
      analytics_storage: g(svcOn(st, 'ga4', 'statistics')),
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
    if (state) gtag('consent', 'update', gcmState(state.c, state.s));
  }

  // Microsoft UET (Bing Ads) consent mode — tas pats principas kaip Google.
  if (C.uet) {
    w.uetq = w.uetq || [];
    w.uetq.push('consent', 'default', { ad_storage: 'denied' });
    if (state) w.uetq.push('consent', 'update', { ad_storage: svcOn(state, 'bing', 'marketing') ? 'granted' : 'denied' });
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

  // spec: "marketing", "marketing:meta" arba kelios per kablelį.
  function allowed(spec) {
    var list = String(spec).split(',');
    for (var i = 0; i < list.length; i++) {
      var p = list[i].trim().split(':');
      if (p[0] === 'necessary') continue;
      if (!state || !state.c[p[0]]) return false;
      if (p[1] && state.s && state.s[p[1]] === false) return false;
    }
    return true;
  }

  function catOf(spec) { return String(spec).split(':')[0]; }

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
    if (cat && catOf(cat) !== 'necessary' && !allowed(cat)) neutralize(el, cat);
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
          if (cat && catOf(cat) !== 'necessary' && !allowed(cat) && !el.hasAttribute('data-se-consent-ignore')) neutralize(el, cat);
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
          guardFrame(n);
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

  // Be serverio filtro (versija ne WordPress): iframe sustabdomas vos parseriui jį įterpus.
  function guardFrame(f) {
    if (f.hasAttribute('data-se-src') || f.hasAttribute('data-se-consent-ignore')) return;
    var src = f.getAttribute('src');
    var cat = f.getAttribute('data-cookieconsent') || matchRule(src, C.rules.src);
    if (!src || !cat || cat === 'ignore' || catOf(cat) === 'necessary' || allowed(cat)) return;
    f.setAttribute('data-se-src', src);
    f.setAttribute('data-se-consent', cat);
    f.removeAttribute('src');
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
    ph.lastChild.onclick = function () { allowOnly(cats, 'placeholder'); };
    f.style.display = 'none';
    f.parentNode.insertBefore(ph, f);
  }

  // Leidžiama tik nurodyta paslauga (pvz. YouTube ar žemėlapis), ne visa jos kategorija.
  function allowOnly(specs, method) {
    var c = current();
    var sv = currentSvc();
    String(specs).split(',').forEach(function (spec) {
      var p = spec.trim().split(':');
      if (!c[p[0]]) {
        SVC.forEach(function (x) { if (x[2] === p[0]) sv[x[0]] = false; });
        c[p[0]] = true;
      }
      if (p[1]) delete sv[p[1]];
    });
    save(c, method, sv);
  }

  // ---------------------------------------------------------------- sutikimo išsaugojimas
  function current() {
    var c = {};
    for (var i = 1; i < CATS.length; i++) c[CATS[i]] = !!(state && state.c[CATS[i]]);
    return c;
  }

  function currentSvc() {
    var sv = {};
    if (state && state.s) for (var k in state.s) sv[k] = state.s[k];
    return sv;
  }

  function save(c, method, sv) {
    var prev = state;
    var clean = {};
    for (var i = 1; i < CATS.length; i++) clean[CATS[i]] = !!c[CATS[i]];
    var off = {};
    SVC.forEach(function (x) { if (sv && sv[x[0]] === false && clean[x[2]]) off[x[0]] = false; });
    state = { id: prev ? prev.id : uuid(), v: C.version, t: Date.now(), m: method, c: clean, s: off };
    write(state);

    if (C.gcm) gtag('consent', 'update', gcmState(clean, off));
    if (C.uet) w.uetq.push('consent', 'update', { ad_storage: svcOn(state, 'bing', 'marketing') ? 'granted' : 'denied' });
    var withdrawn = [];
    if (prev) {
      for (var k in prev.c) {
        if (prev.c[k] && !clean[k]) { withdrawn.push(k); deleteCookies((C.cookies && C.cookies[k] || []).map(function (r) { return r[0]; })); }
      }
      SVC.forEach(function (x) {
        if (svcOn(prev, x[0], x[2]) && !svcOn(state, x[0], x[2])) { withdrawn.push(x[0]); deleteCookies(x[3] || []); }
      });
    }

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

  // Trinama visuose domeno variantuose (be domeno, host, .host, .šakninis) — kitaip _fbp, _ga
  // ant ".domenas.lt" išgyvena atšaukimą (pastebėta Klaro ir tarteaucitron analizėje).
  function deleteCookies(patterns) {
    var names = d.cookie.split(';').map(function (p) { return p.split('=')[0].trim(); });
    var host = location.hostname;
    var parts = host.split('.');
    var domains = ['', host, '.' + host];
    if (parts.length > 2) domains.push('.' + parts.slice(-2).join('.'));
    if (parts.length === 2) domains.push('.' + host);
    patterns.forEach(function (pat) {
      var re = new RegExp('^' + pat.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$');
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
    var body = JSON.stringify({ id: s.id, v: s.v, m: s.m, c: s.c, s: s.s, u: location.pathname });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(C.logUrl, new Blob([body], { type: 'application/json' }))) return;
    } catch (e) { /* nukrenta į fetch */ }
    if (w.fetch) fetch(C.logUrl, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' } });
  }

  // ---------------------------------------------------------------- pranešimai kitiems
  function announce(changed) {
    var c = state ? state.c : {};
    var detail = { necessary: true, preferences: !!c.preferences, statistics: !!c.statistics, marketing: !!c.marketing, method: state && state.m, changed: !!changed, services: {} };
    SVC.forEach(function (x) { detail.services[x[0]] = svcOn(state, x[0], x[2]); });

    // Microsoft Clarity consent API (nuo 2025 m. privaloma EEE); veikia ir prieš Clarity įkėlimą per eilę.
    if (C.clarity) {
      w.clarity = w.clarity || function () { (w.clarity.q = w.clarity.q || []).push(arguments); };
      w.clarity('consentv2', {
        analytics_Storage: detail.services.clarity ? 'granted' : 'denied',
        ad_Storage: detail.marketing ? 'granted' : 'denied'
      });
    }

    // WP Consent API (tik WordPress; kitose platformose šie slapukai nereikalingi)
    if (C.wpConsentApi !== false) {
    var wp = { functional: true, preferences: detail.preferences, statistics: detail.statistics, 'statistics-anonymous': detail.statistics, marketing: detail.marketing };
    var ev = {};
    for (var k in wp) {
      var val = wp[k] ? 'allow' : 'deny';
      d.cookie = 'wp_consent_' + k + '=' + val + ';path=/;max-age=' + (C.expiryDays * 86400) + ';SameSite=Lax' + (C.domain ? ';domain=' + C.domain : '');
      ev[k] = val;
    }
    d.dispatchEvent(new CustomEvent('wp_listen_for_consent_change', { detail: ev }));
    }

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
    // Rodomos tik svetainėje naudojamos kategorijos (C.categories); būtinosios — visada.
    CATS.filter(function (k) { return k === 'necessary' || !C.categories || C.categories.indexOf(k) !== -1; }).forEach(function (k) {
      var info = T.cat[k];
      var list = ((T.cookieList || C.cookies || {})[k]) || [];
      var rows = list.map(function (r) {
        return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td><td>' + esc(r[3]) + '</td></tr>';
      }).join('');
      var svcs = SVC.filter(function (x) { return x[2] === k; }).map(function (x) {
        return '<li><span>' + esc(x[1]) + '</span><input type="checkbox" role="switch" class="se-c__sw se-c__sw--svc" data-svc="' + esc(x[0]) + '" data-svc-cat="' + k + '" aria-label="' + esc(x[1]) + '"' + (svcOn(state, x[0], k) ? ' checked' : '') + '></li>';
      }).join('');
      var toggle = k === 'necessary'
        ? '<span class="se-c__on">' + esc(T.always_on) + '</span>'
        : '<input type="checkbox" role="switch" class="se-c__sw" data-cat="' + k + '" aria-label="' + esc(info[0]) + '"' + (c[k] ? ' checked' : '') + '>';
      cats += '<div class="se-c__cat"><div class="se-c__cat-h"><strong>' + esc(info[0]) + '</strong>' + toggle + '</div>' +
        '<p>' + esc(info[1]) + '</p>' +
        (svcs ? '<ul class="se-c__svcs" aria-label="' + esc(T.services || 'Paslaugos') + '">' + svcs + '</ul>' : '') +
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
          ((T.privacyUrl || C.privacyUrl) ? ' <a href="' + esc(T.privacyUrl || C.privacyUrl) + '">' + esc(T.privacy) + '</a>' : '') + '</p>' +
        '<div class="se-c__details" hidden>' + cats + '</div>' +
        '<div class="se-c__actions">' +
          '<button type="button" class="se-c__btn se-c__btn--2" data-a="reject">' + esc(T.reject_all) + '</button>' +
          '<button type="button" class="se-c__btn se-c__btn--3" data-a="customize">' + esc(T.customize) + '</button>' +
          '<button type="button" class="se-c__btn se-c__btn--1" data-a="accept">' + esc(T.accept_all) + '</button>' +
        '</div>' +
      '</div>';
    root.addEventListener('click', onClick);
    root.addEventListener('change', function (e) {
      var t = e.target;
      if (t.hasAttribute('data-cat')) {
        var all = root.querySelectorAll('[data-svc-cat="' + t.getAttribute('data-cat') + '"]');
        for (var i = 0; i < all.length; i++) all[i].checked = t.checked;
      } else if (t.hasAttribute('data-svc')) {
        var cat = t.getAttribute('data-svc-cat');
        var any = root.querySelectorAll('[data-svc-cat="' + cat + '"]:checked').length > 0;
        var sw = root.querySelector('[data-cat="' + cat + '"]');
        if (sw) sw.checked = any;
      }
    });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && state) { hideBanner(); return; }
      // Fokuso spąstai, kai dialogas modalinis (nustatymai arba langas centre) — EAA / WCAG 2.1.
      if (e.key === 'Tab' && root.getAttribute('aria-modal') === 'true') {
        var f = root.querySelectorAll('button,input,a[href],summary');
        var vis = [];
        for (var i = 0; i < f.length; i++) if (f[i].offsetParent !== null) vis.push(f[i]);
        if (!vis.length) return;
        var first = vis[0], last = vis[vis.length - 1];
        if (e.shiftKey && (d.activeElement === first || !root.contains(d.activeElement))) { last.focus(); e.preventDefault(); }
        else if (!e.shiftKey && d.activeElement === last) { first.focus(); e.preventDefault(); }
      }
    });
    if (C.position === 'center') root.setAttribute('aria-modal', 'true');
    d.body.appendChild(root);
  }

  function onClick(e) {
    var a = e.target.getAttribute && e.target.getAttribute('data-a');
    if (!a) return;
    if (a === 'accept') save({ preferences: true, statistics: true, marketing: true }, 'accept_all');
    else if (a === 'reject') save({}, 'reject_all');
    else if (a === 'customize') openDetails();
    else if (a === 'save') {
      var c = {}, sv = {};
      var sw = root.querySelectorAll('[data-cat]');
      for (var i = 0; i < sw.length; i++) c[sw[i].getAttribute('data-cat')] = sw[i].checked;
      var ss = root.querySelectorAll('[data-svc]');
      for (var j = 0; j < ss.length; j++) if (!ss[j].checked) sv[ss[j].getAttribute('data-svc')] = false;
      save(c, 'custom', sv);
    }
  }

  function openDetails() {
    var det = root.querySelector('.se-c__details');
    det.hidden = false;
    root.classList.add('se-c--open');
    root.setAttribute('aria-modal', 'true');
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
    else lastFocus = d.activeElement;
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
    // Fokusas grąžinamas ten, kur buvo prieš atidarant (pvz. poraštės nuoroda).
    if (lastFocus && lastFocus !== d.body && d.contains(lastFocus) && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    lastFocus = null;
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
    has: function (spec) { return !!state && allowed(spec); },
    show: showBanner,
    hide: hideBanner,
    accept: function (c, method, sv) { save(c || { preferences: true, statistics: true, marketing: true }, method || 'api', sv); },
    withdraw: function () { save({}, 'withdraw'); },
    // Pvz. SEConsent.allowService('maps') paspaudus „Rodyti žemėlapį".
    allowService: function (id) {
      var svc = SVC.filter(function (x) { return x[0] === id; })[0];
      if (!svc) return false;
      if (!allowed(svc[2] + ':' + id)) allowOnly(svc[2] + ':' + id, 'service');
      return true;
    },
    onChange: function (fn) { listeners.push(fn); }
  };

  function boot() {
    activateAll();
    if (state) {
      announce(false);
      floating();
    } else if (C.gpc && navigator.globalPrivacyControl) {
      // Global Privacy Control: naršyklė jau pasakė "ne" — banerio nerodome, fiksuojame atsisakymą.
      save({}, 'gpc');
    } else {
      showBanner(false);
    }
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', boot);
  else boot();
})(window, document);
