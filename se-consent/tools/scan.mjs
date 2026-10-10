// SE Consent atitikties skeneris (Cookiebot mėnesinio skenavimo pakaitalas + daugiau).
//
//   NODE_PATH=$(npm root -g) node tools/scan.mjs https://sleepingexpert.lt [--max 40] [--json report.json] [--no-ocd]
//
// Ką tikrina kiekviename puslapyje (iš sitemap.xml):
//   A. BE sutikimo: slapukai, localStorage, užklausos trečiosioms šalims, "fingerprinting" API.
//   B. Banerio kokybė: "Atmesti" pirmame sluoksnyje, vienodi mygtukai, nurodytos paskirtys.
//   C. SU sutikimu: visi slapukai (ir HttpOnly) → palyginimas su deklaruotu sąrašu; nedeklaruoti
//      automatiškai klasifikuojami pagal Open Cookie Database (Apache-2.0).
//   D. Atšaukimas: SEConsent.withdraw() → perkrovus sekikliai nebeveikia, slapukai ištrinti.
//   E. Slapukų galiojimas ≤ 13 mėn., sutikimo galiojimas.
//   F. Nežinomi trečiųjų šalių domenai įvertinami pagal elgseną (slapukai, jų trukmė,
//      fingerprinting API, sekimo pikseliai) — idėja iš olafuraron/tracker-classifier
//      požymių svarbos analizės, be nekomercinės licencijos duomenų.
//
// Išeities kodas 1, jei rasta pažeidimų — tinka cron/CI.

import { createRequire } from 'node:module';
import { writeFileSync, readFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const OCD_URL = 'https://raw.githubusercontent.com/jkwakman/Open-Cookie-Database/master/open-cookie-database.csv';
const OCD_CACHE = path.join(HERE, '.cache', 'open-cookie-database.csv');
const MAX_COOKIE_DAYS = 395; // 13 mėn. (CNIL / EDPB praktika)

// Užklausos, kurios be sutikimo leidžiamos (Consent Mode advanced siunčia pings be slapukų; CDN, šriftai).
const ALLOWED_PRECONSENT = [/googletagmanager\.com/, /google-analytics\.com\/g\/collect/, /fonts\.(googleapis|gstatic)\.com/, /gstatic\.com/, /cdn\.jsdelivr\.net/, /cdnjs\.cloudflare\.com/, /unpkg\.com/];

// ---------------------------------------------------------------- Open Cookie Database
function parseCsv(text) {
  const rows = [];
  let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (q) {
      if (ch === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (ch === '"') q = false; else cell += ch;
    } else if (ch === '"') q = true;
    else if (ch === ',') { row.push(cell); cell = ''; }
    else if (ch === '\n' || ch === '\r') {
      if (ch === '\r' && text[i + 1] === '\n') i++;
      row.push(cell); rows.push(row); row = []; cell = '';
    } else cell += ch;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  return rows;
}

const OCD_CAT = { functional: 'necessary', security: 'necessary', personalization: 'preferences', analytics: 'statistics', marketing: 'marketing' };
// OCD "Functional" dažnai reiškia trečiosios šalies įrankį (pvz. Hotjar ID). Būtinaisiais laikome tik
// pačios svetainės infrastruktūrą; kitiems — tiekėjo kategorija arba bent "preferences" (reikia sutikimo).
const INFRA = /^(wordpress|woocommerce|php|cloudflare|wp engine|litespeed|nginx|apache|stripe|paypal|paysera|montonio|recaptcha|google recaptcha|cookiebot|se consent)/i;
const VENDOR_CAT = [
  [/hotjar|clarity|google analytics|matomo|piwik|yandex|mixpanel|amplitude|heap|segment|plausible/i, 'statistics'],
  [/facebook|meta|tiktok|linkedin|pinterest|bing|microsoft advertising|google ads|doubleclick|criteo|taboola|outbrain|snapchat|twitter|klaviyo|omnisend|hubspot/i, 'marketing'],
];
function ocdCategory(rawCat, platform) {
  for (const [re, cat] of VENDOR_CAT) if (re.test(platform)) return cat;
  const cat = OCD_CAT[(rawCat || '').trim().toLowerCase()] || 'marketing';
  return cat === 'necessary' && !INFRA.test(platform) ? 'preferences' : cat;
}

export async function loadOcd({ offline = false } = {}) {
  let text = null;
  const fresh = existsSync(OCD_CACHE) && Date.now() - statSync(OCD_CACHE).mtimeMs < 7 * 86400e3;
  if (!fresh && !offline) {
    try {
      const r = await fetch(OCD_URL);
      if (r.ok) {
        text = await r.text();
        mkdirSync(path.dirname(OCD_CACHE), { recursive: true });
        writeFileSync(OCD_CACHE, text);
      }
    } catch { /* naudojamas podėlis */ }
  }
  if (!text && existsSync(OCD_CACHE)) text = readFileSync(OCD_CACHE, 'utf8');
  if (!text) return null;
  const [head, ...rows] = parseCsv(text);
  const ix = (n) => head.findIndex((h) => h.trim().toLowerCase().startsWith(n));
  const c = { platform: ix('platform'), cat: ix('category'), name: ix('cookie'), domain: ix('domain'), desc: ix('description'), ret: ix('retention'), ctrl: ix('data controller'), wild: ix('wildcard') };
  const exact = new Map(), prefix = [], domains = new Map();
  for (const r of rows) {
    const name = (r[c.name] || '').trim();
    if (!name) continue;
    const e = {
      name, platform: r[c.platform] || '', controller: r[c.ctrl] || '', description: (r[c.desc] || '').replace(/\s+/g, ' ').trim(),
      retention: r[c.ret] || '', category: ocdCategory(r[c.cat], r[c.platform] || ''),
    };
    if (r[c.wild] === '1') prefix.push(e); else if (!exact.has(name)) exact.set(name, e);
    for (const d of (r[c.domain] || '').split(/[\s,;]+/)) {
      const h = d.replace(/^\*?\./, '').toLowerCase();
      if (h.includes('.') && !domains.has(h)) domains.set(h, e);
    }
  }
  prefix.sort((a, b) => b.name.length - a.name.length);
  return {
    size: exact.size + prefix.length,
    cookie: (n) => exact.get(n) || prefix.find((e) => n.startsWith(e.name)) || null,
    domain: (h) => { for (const [d, e] of domains) if (h === d || h.endsWith('.' + d)) return e; return null; },
  };
}

// ---------------------------------------------------------------- fingerprinting instrumentavimas
// Įterpiama prieš bet kurį puslapio scenarijų; fiksuoja, kuris scenarijus (URL iš steko) kvietė API.
const FP_INIT = `(() => {
  const out = window.__seFp = [];
  const who = () => {
    const m = (new Error().stack || '').match(/https?:\\/\\/[^\\s)]+?(?=:\\d+:\\d+)/g) || [];
    return m[0] || location.href;
  };
  const rec = (api) => { if (out.length < 500) out.push([api, who()]); };
  const wrap = (proto, fn, api) => {
    if (!proto || !proto[fn]) return;
    const orig = proto[fn];
    proto[fn] = function () { rec(api); return orig.apply(this, arguments); };
  };
  const getter = (proto, prop, api) => {
    const d = proto && Object.getOwnPropertyDescriptor(proto, prop);
    if (!d || !d.get) return;
    Object.defineProperty(proto, prop, { configurable: true, enumerable: d.enumerable, get() { rec(api); return d.get.call(this); } });
  };
  wrap(window.HTMLCanvasElement && HTMLCanvasElement.prototype, 'toDataURL', 'canvas');
  wrap(window.CanvasRenderingContext2D && CanvasRenderingContext2D.prototype, 'getImageData', 'canvas');
  wrap(window.CanvasRenderingContext2D && CanvasRenderingContext2D.prototype, 'measureText', 'fonts');
  wrap(window.WebGLRenderingContext && WebGLRenderingContext.prototype, 'getParameter', 'webgl');
  wrap(window.OfflineAudioContext && OfflineAudioContext.prototype, 'startRendering', 'audio');
  wrap(window.AudioContext && AudioContext.prototype, 'createOscillator', 'audio');
  wrap(window.RTCPeerConnection && RTCPeerConnection.prototype, 'createDataChannel', 'webrtc');
  wrap(window.NavigatorUAData && NavigatorUAData.prototype, 'getHighEntropyValues', 'ua-high-entropy');
  wrap(window.FontFaceSet && FontFaceSet.prototype, 'check', 'fonts');
  ['hardwareConcurrency', 'deviceMemory', 'plugins', 'mimeTypes', 'maxTouchPoints'].forEach((p) => getter(Navigator.prototype, p, 'navigator'));
  ['colorDepth', 'pixelDepth', 'availWidth'].forEach((p) => getter(Screen.prototype, p, 'screen'));
})();`;

// ---------------------------------------------------------------- pagalbinės
const hostOf = (u) => { try { return new URL(u).hostname.toLowerCase(); } catch { return ''; } };
const daysLeft = (c) => (c.expires > 0 ? Math.round((c.expires - Date.now() / 1000) / 86400) : 0);

function matcher(declared) {
  const res = [];
  for (const [cat, list] of Object.entries(declared || {})) {
    for (const row of list) {
      const re = new RegExp('^' + row[0].replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$');
      res.push([re, cat]);
    }
  }
  return (name) => (res.find(([re]) => re.test(name)) || [])[1] || null;
}

async function urlsFromSitemap(base, max) {
  const seen = new Set([base + '/']);
  const queue = [base + '/sitemap.xml', base + '/sitemap_index.xml', base + '/wp-sitemap.xml'];
  const done = new Set();
  while (queue.length && seen.size < max) {
    const sm = queue.shift();
    if (done.has(sm)) continue;
    done.add(sm);
    let xml = '';
    try { const r = await fetch(sm); if (!r.ok) continue; xml = await r.text(); } catch { continue; }
    for (const [, loc] of xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)) {
      if (/\.xml(\?|$)/.test(loc)) queue.push(loc);
      else if (seen.size < max) seen.add(loc);
    }
  }
  return [...seen];
}

// Banerio patikra pirmame sluoksnyje (veikia ir su kitais CMP pagal tekstą).
const BANNER_PROBE = () => {
  const vis = (el) => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const root = document.getElementById('se-consent') || document.querySelector('[id*="cookie" i][role="dialog"],[class*="cookie" i][role="dialog"],#CybotCookiebotDialog,[id*="consent" i]');
  if (!root || !vis(root)) return { present: false };
  const btns = [...root.querySelectorAll('button,a[role="button"],[role="button"]')].filter(vis);
  const find = (re, attr) => btns.find((b) => (attr && b.getAttribute('data-a') === attr) || re.test(b.textContent.trim()));
  const accept = find(/^(sutinku|priimti|leisti visus|accept|allow all|agree)/i, 'accept');
  const reject = find(/(atmesti|tik būtin|nesutinku|reject|decline|deny|necessary only|only necessary)/i, 'reject');
  const area = (b) => { const r = b.getBoundingClientRect(); return r.width * r.height; };
  const cfg = window.SE_CONSENT_CONFIG;
  const purposes = cfg
    ? ['preferences', 'statistics', 'marketing'].every((k) => cfg.t && cfg.t.cat && cfg.t.cat[k] && cfg.t.cat[k][1])
    : /(statistik|rinkodar|analyt|marketing|reklam)/i.test(root.textContent);
  return {
    present: true,
    rejectFirstLayer: !!reject,
    equalWeight: !!(accept && reject) && Math.min(area(accept), area(reject)) / Math.max(area(accept), area(reject)) > 0.8,
    purposes,
    expiryDays: cfg ? cfg.expiryDays : null,
  };
};

// ---------------------------------------------------------------- skenavimas
export async function scanSite(base, { max = 40, ocd = null, log = () => {} } = {}) {
  const { chromium } = require('playwright');
  base = base.replace(/\/$/, '');
  const siteHost = hostOf(base).replace(/^www\./, '');
  const firstParty = (h) => h === siteHost || h.endsWith('.' + siteHost);
  const browser = await chromium.launch();
  const urls = await urlsFromSitemap(base, max);

  const report = {
    base, scannedAt: new Date().toISOString(), urls,
    checks: {}, violations: [], undeclared: [], longCookies: [], suspects: [], thirdParties: [],
  };
  const vmap = new Map(), umap = new Map(), lmap = new Map();
  const domains = new Map(); // host -> {cookies:Set, maxDays, fp:Set, pixels, beforeConsent}
  const dom = (h) => { if (!domains.has(h)) domains.set(h, { cookies: new Set(), maxDays: 0, fp: new Set(), pixels: 0, beforeConsent: false }); return domains.get(h); };
  const note = (map, key, val, url) => {
    if (!map.has(key)) map.set(key, { ...val, urls: [] });
    const e = map.get(key);
    if (e.urls.length < 5 && !e.urls.includes(url)) e.urls.push(url);
  };
  let declared = null, banner = null, withdrawal = null;

  const observe = (page, bucket) => {
    page.on('request', (r) => bucket.push({ url: r.url(), type: r.resourceType() }));
  };
  const absorb = (reqs, phaseBefore) => {
    for (const r of reqs) {
      const h = hostOf(r.url);
      if (!h || firstParty(h)) continue;
      const d = dom(h);
      if (phaseBefore && !ALLOWED_PRECONSENT.some((re) => re.test(r.url))) d.beforeConsent = true;
      // Sekimo pikselis: vaizdas/ping su ilgu užklausos parametrų rinkiniu.
      if ((r.type === 'image' || r.type === 'ping' || r.type === 'other') && (new URL(r.url).search.length > 40)) d.pixels++;
    }
  };
  const absorbFp = async (page) => {
    const fp = await page.evaluate(() => window.__seFp || []).catch(() => []);
    for (const [api, src] of fp) {
      const h = hostOf(src);
      if (h && !firstParty(h)) dom(h).fp.add(api);
    }
  };

  for (const url of urls) {
    const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (SE-Consent-Scanner) Chrome/130' });
    await ctx.addInitScript(FP_INIT);
    const page = await ctx.newPage();
    const before = [];
    observe(page, before);
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    } catch (e) {
      log(`! ${url}: ${e.message.split('\n')[0]}`);
      await ctx.close();
      continue;
    }
    await page.waitForTimeout(1500);
    if (!declared) declared = await page.evaluate(() => (window.SE_CONSENT_CONFIG || {}).cookies || null);
    if (!banner) banner = await page.evaluate(BANNER_PROBE);
    const cat = matcher(declared);

    // A. Be sutikimo
    for (const c of await ctx.cookies()) {
      const h = c.domain.replace(/^\./, '');
      if (!firstParty(h)) { dom(h).cookies.add(c.name); dom(h).beforeConsent = true; }
      const k = cat(c.name);
      if (k !== 'necessary') note(vmap, 'cookie:' + c.name, { check: 'before_consent', type: 'slapukas', name: c.name, domain: c.domain, category: k || 'nedeklaruotas' }, url);
    }
    for (const key of await page.evaluate(() => Object.keys(localStorage))) {
      const k = cat(key);
      if (k !== 'necessary') note(vmap, 'ls:' + key, { check: 'before_consent', type: 'localStorage', name: key, category: k || 'nedeklaruotas' }, url);
    }
    absorb(before, true);
    for (const r of before) {
      const h = hostOf(r.url);
      if (h && !firstParty(h) && !ALLOWED_PRECONSENT.some((re) => re.test(r.url))) note(vmap, 'req:' + h, { check: 'before_consent', type: 'užklausa', name: h }, url);
    }
    await absorbFp(page);
    const fpBefore = await page.evaluate(() => (window.__seFp || []).length).catch(() => 0);

    // C. Su sutikimu
    const after = [];
    observe(page, after);
    const hasCmp = await page.evaluate(() => { if (!window.SEConsent) return false; window.SEConsent.accept(); return true; });
    if (!hasCmp) {
      note(vmap, 'no-cmp', { check: 'cmp', type: 'SE Consent nerastas puslapyje', name: '-' }, url);
      await ctx.close();
      continue;
    }
    await page.waitForTimeout(4000);
    absorb(after, false);
    if ((await page.evaluate(() => (window.__seFp || []).length).catch(() => 0)) > fpBefore) await absorbFp(page);
    for (const c of await ctx.cookies()) {
      const h = c.domain.replace(/^\./, '');
      const days = daysLeft(c);
      if (!firstParty(h)) { const d = dom(h); d.cookies.add(c.name); d.maxDays = Math.max(d.maxDays, days); }
      if (days > MAX_COOKIE_DAYS) note(lmap, c.name, { name: c.name, domain: c.domain, days }, url);
      if (!cat(c.name)) {
        const o = ocd && ocd.cookie(c.name);
        note(umap, c.name, {
          name: c.name, domain: c.domain, expires: days ? days + ' d.' : 'sesija',
          suggestion: o ? `${c.name} | ${o.controller || o.platform} | ${o.category} | ${o.description} | ${o.retention}` : `${c.name} | ${h} | ? | ? | ${days ? days + ' d.' : 'sesija'}`,
          source: o ? 'Open Cookie Database' : null,
        }, url);
      }
    }

    // D. Atšaukimas (tikrinamas viename puslapyje — to pakanka logikai patikrinti)
    if (!withdrawal) {
      const declaredNonNecessary = (await ctx.cookies()).filter((c) => firstParty(c.domain.replace(/^\./, '')) && ['statistics', 'marketing', 'preferences'].includes(cat(c.name)));
      const reqs = [];
      observe(page, reqs);
      await Promise.all([page.waitForEvent('load', { timeout: 15000 }).catch(() => null), page.evaluate(() => window.SEConsent.withdraw())]);
      await page.waitForTimeout(3000);
      const left = (await ctx.cookies()).filter((c) => declaredNonNecessary.some((d) => d.name === c.name && d.domain === c.domain));
      const leaking = [...new Set(reqs.map((r) => hostOf(r.url)).filter((h) => h && !firstParty(h) && ![...ALLOWED_PRECONSENT].some((re) => re.test('https://' + h + '/'))))];
      withdrawal = { tested: url, cookiesLeft: left.map((c) => c.name), requestsAfter: leaking, ok: !left.length && !leaking.length };
    }
    log('.');
    await ctx.close();
  }
  await browser.close();

  // F. Nežinomų domenų elgsenos įvertinimas
  for (const [h, d] of domains) {
    report.thirdParties.push(h);
    const known = ocd && ocd.domain(h);
    let score = 0;
    const why = [];
    if (d.cookies.size) { score += 2; why.push(`slapukai: ${[...d.cookies].slice(0, 4).join(', ')}`); }
    if (d.maxDays > 30) { score += 1; why.push(`galioja ${d.maxDays} d.`); }
    if (d.fp.size) { score += d.fp.size; why.push(`fingerprinting API: ${[...d.fp].join(', ')}`); }
    if (d.pixels) { score += 1; why.push(`sekimo pikseliai/ping: ${d.pixels}`); }
    if (known) { score += 2; why.push(`Open Cookie Database: ${known.platform} (${known.category})`); }
    if (score >= 3) {
      report.suspects.push({ host: h, score, category: known ? known.category : (d.fp.size ? 'marketing' : 'statistics'), beforeConsent: d.beforeConsent, why, rule: `${h} | ${known ? known.category : 'marketing'}` });
    }
  }
  report.suspects.sort((a, b) => b.score - a.score);
  report.thirdParties.sort();
  report.violations = [...vmap.values()];
  report.undeclared = [...umap.values()];
  report.longCookies = [...lmap.values()].sort((a, b) => b.days - a.days);

  // CNIL dažniausiai baudžiami 4 pažeidimai + 2 papildomi.
  report.checks = {
    noTrackersBeforeConsent: { ok: report.violations.filter((v) => v.check === 'before_consent').length === 0, label: 'Nieko neveikia iki sutikimo' },
    rejectOnFirstLayer: { ok: !!(banner && banner.present && banner.rejectFirstLayer && banner.equalWeight), label: '„Atmesti" pirmame sluoksnyje, vienodo svorio kaip „Sutinku"', detail: banner },
    purposesListed: { ok: !!(banner && banner.purposes) && !!declared, label: 'Nurodytos kiekvienos kategorijos paskirtys ir slapukai' },
    withdrawalWorks: { ok: !!(withdrawal && withdrawal.ok), label: 'Atšaukus sutikimą sekikliai sustoja, slapukai ištrinami', detail: withdrawal },
    cookieLifetime: { ok: report.longCookies.length === 0, label: `Slapukai galioja ≤ ${MAX_COOKIE_DAYS} d. (13 mėn.)` },
    consentExpiry: { ok: !!(banner && banner.expiryDays && banner.expiryDays <= MAX_COOKIE_DAYS), label: 'Sutikimas klausiamas iš naujo ≤ 13 mėn.', detail: banner && banner.expiryDays },
  };
  report.score = Object.values(report.checks).filter((c) => c.ok).length + '/' + Object.keys(report.checks).length;
  report.ocd = ocd ? ocd.size : 0;
  return report;
}

export function printReport(r) {
  const out = [];
  out.push(`\nAtitiktis: ${r.score}`);
  for (const c of Object.values(r.checks)) out.push(`  ${c.ok ? '✓' : '✗'} ${c.label}`);
  out.push('\n== Veikia BE sutikimo ==');
  if (!r.violations.length) out.push('nėra ✓');
  for (const v of r.violations) out.push(`✗ ${v.type}: ${v.name}${v.domain ? ' (' + v.domain + ')' : ''}${v.category ? ' [' + v.category + ']' : ''} — pvz. ${v.urls[0]}`);
  if (r.checks.withdrawalWorks.detail && !r.checks.withdrawalWorks.ok) {
    const w = r.checks.withdrawalWorks.detail;
    out.push(`\n== Atšaukimas neveikia (${w.tested}) ==`);
    if (w.cookiesLeft.length) out.push('liko slapukai: ' + w.cookiesLeft.join(', '));
    if (w.requestsAfter.length) out.push('užklausos po atšaukimo: ' + w.requestsAfter.join(', '));
  }
  out.push('\n== Slapukai ilgesni nei 13 mėn. ==');
  if (!r.longCookies.length) out.push('nėra ✓');
  for (const c of r.longCookies) {
    out.push(`! ${c.name} (${c.domain}) — ${c.days} d.${/^_ga/.test(c.name) ? "  → gtag('config', 'G-…', { cookie_expires: 34128000 })" : ''}`);
  }
  out.push('\n== Nedeklaruoti slapukai — įklijuokite į Nustatymai → SE Consent → Slapukų sąrašas ==');
  if (!r.undeclared.length) out.push('nėra ✓');
  for (const u of r.undeclared) out.push(`${u.suggestion}${u.source ? '' : '   ← rankiniu būdu'}`);
  out.push('\n== Tikėtini sekikliai tarp trečiųjų šalių (elgsenos įvertinimas) ==');
  if (!r.suspects.length) out.push('nėra ✓');
  for (const s of r.suspects) out.push(`${s.beforeConsent ? '✗' : '•'} ${s.host} (balas ${s.score}) — ${s.why.join('; ')}\n    taisyklė: ${s.rule}`);
  out.push('\n== Visi trečiųjų šalių domenai ==\n' + (r.thirdParties.join('\n') || '—'));
  return out.join('\n');
}

// ---------------------------------------------------------------- CLI
if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const args = process.argv.slice(2);
  const base = args.find((a) => /^https?:\/\//.test(a));
  const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
  if (!base) {
    console.error('Naudojimas: node tools/scan.mjs https://svetaine.lt [--max 40] [--json report.json] [--no-ocd]');
    process.exit(2);
  }
  const ocd = args.includes('--no-ocd') ? null : await loadOcd();
  console.log(`Open Cookie Database: ${ocd ? ocd.size + ' įrašų' : 'nepasiekiama — klasifikavimas be jos'}`);
  const r = await scanSite(base, { max: Number(opt('--max', 40)), ocd, log: (m) => process.stdout.write(m) });
  console.log(`\nNuskenuota ${r.urls.length} puslapių`);
  console.log(printReport(r));
  const json = opt('--json', null);
  if (json) writeFileSync(json, JSON.stringify(r, null, 2));
  const bad = Object.values(r.checks).some((c) => !c.ok) || r.undeclared.length;
  process.exit(bad ? 1 : 0);
}
