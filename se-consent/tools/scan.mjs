// Slapukų skeneris (Cookiebot mėnesinio skenavimo pakaitalas).
//
//   NODE_PATH=$(npm root -g) node tools/scan.mjs https://sleepingexpert.lt [--max 40] [--json report.json]
//
// Kiekvienam puslapiui iš sitemap.xml:
//   1) be sutikimo — surenka slapukus, localStorage ir užklausas trečiosioms šalims.
//      Bet kas, kas nėra "necessary", čia yra PAŽEIDIMAS (sekiklis veikia be sutikimo).
//   2) paspaudus "Sutinku su visais" — surenka visus slapukus (ir HttpOnly) ir palygina
//      su deklaruotu sąrašu (SE_CONSENT_CONFIG.cookies). Nedeklaruotus reikia įrašyti į nustatymus.
// Išeities kodas 1, jei rasta pažeidimų arba nedeklaruotų slapukų — tinka cron/CI.

import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const base = (args.find((a) => /^https?:\/\//.test(a)) || '').replace(/\/$/, '');
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const max = Number(opt('--max', 40));
const jsonOut = opt('--json', null);
if (!base) {
  console.error('Naudojimas: node tools/scan.mjs https://svetaine.lt [--max 40] [--json report.json]');
  process.exit(2);
}
const host = new URL(base).hostname.replace(/^www\./, '');
const isThirdParty = (u) => { try { return !new URL(u).hostname.endsWith(host); } catch { return false; } };
// Užklausos, kurios be sutikimo leidžiamos (Consent Mode advanced siunčia be slapukų pings).
const ALLOWED_PRECONSENT = [/googletagmanager\.com/, /google-analytics\.com\/g\/collect/, /fonts\.(googleapis|gstatic)\.com/, /gstatic\.com/, /cdn\.jsdelivr\.net/, /cdnjs\.cloudflare\.com/];

async function urlsFromSitemap() {
  const seen = new Set([base + '/']);
  const queue = [base + '/sitemap.xml', base + '/sitemap_index.xml', base + '/wp-sitemap.xml'];
  while (queue.length && seen.size < max) {
    const sm = queue.shift();
    let xml = '';
    try { const r = await fetch(sm); if (!r.ok) continue; xml = await r.text(); } catch { continue; }
    for (const [, loc] of xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)) {
      if (/\.xml(\?|$)/.test(loc)) queue.push(loc);
      else if (seen.size < max) seen.add(loc);
    }
  }
  return [...seen];
}

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

const browser = await chromium.launch();
const urls = await urlsFromSitemap();
console.log(`Skenuojama ${urls.length} puslapių iš ${base}\n`);

const violations = new Map();  // raktas -> {type, name, category, urls}
const undeclared = new Map();
const thirdParties = new Set();
let declared = null;

const note = (map, key, val, url) => {
  if (!map.has(key)) map.set(key, { ...val, urls: [] });
  const e = map.get(key);
  if (e.urls.length < 5 && !e.urls.includes(url)) e.urls.push(url);
};

for (const url of urls) {
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (SE-Consent-Scanner) Chrome/130' });
  const page = await ctx.newPage();
  const requests = [];
  page.on('request', (r) => requests.push(r.url()));
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  } catch (e) {
    console.log(`! ${url}: ${e.message.split('\n')[0]}`);
    await ctx.close();
    continue;
  }
  await page.waitForTimeout(1500);
  if (!declared) declared = await page.evaluate(() => (window.SE_CONSENT_CONFIG || {}).cookies || null);
  const cat = matcher(declared);

  // 1) Be sutikimo
  for (const c of await ctx.cookies()) {
    const k = cat(c.name);
    if (k !== 'necessary') note(violations, 'cookie:' + c.name, { type: 'slapukas', name: c.name, domain: c.domain, category: k || 'nedeklaruotas' }, url);
  }
  const ls = await page.evaluate(() => Object.keys(localStorage));
  for (const key of ls) {
    const k = cat(key);
    if (k !== 'necessary') note(violations, 'ls:' + key, { type: 'localStorage', name: key, category: k || 'nedeklaruotas' }, url);
  }
  for (const r of requests) {
    if (!isThirdParty(r)) continue;
    const h = new URL(r).hostname;
    thirdParties.add(h);
    if (!ALLOWED_PRECONSENT.some((re) => re.test(r))) note(violations, 'req:' + h, { type: 'užklausa', name: h }, url);
  }

  // 2) Su sutikimu
  const accepted = await page.evaluate(() => {
    if (!window.SEConsent) return false;
    window.SEConsent.accept();
    return true;
  });
  if (accepted) {
    await page.waitForTimeout(4000);
    for (const c of await ctx.cookies()) {
      if (!cat(c.name)) note(undeclared, c.name, { name: c.name, domain: c.domain, expires: c.expires > 0 ? Math.round((c.expires - Date.now() / 1000) / 86400) + ' d.' : 'sesija' }, url);
    }
    for (const r of requests) if (isThirdParty(r)) thirdParties.add(new URL(r).hostname);
  } else {
    note(violations, 'no-cmp', { type: 'SE Consent nerastas puslapyje', name: '-' }, url);
  }
  process.stdout.write('.');
  await ctx.close();
}
await browser.close();

console.log('\n\n== Pažeidimai (veikia BE sutikimo) ==');
if (!violations.size) console.log('nėra ✓');
for (const v of violations.values()) console.log(`✗ ${v.type}: ${v.name}${v.domain ? ' (' + v.domain + ')' : ''}${v.category ? ' [' + v.category + ']' : ''} — pvz. ${v.urls[0]}`);

console.log('\n== Nedeklaruoti slapukai (įrašykite į Nustatymai → SE Consent → Slapukų sąrašas) ==');
if (!undeclared.size) console.log('nėra ✓');
for (const u of undeclared.values()) console.log(`? ${u.name} | ${u.domain} | ? | ? | ${u.expires}`);

console.log('\n== Trečiųjų šalių domenai ==\n' + [...thirdParties].sort().join('\n'));

if (jsonOut) {
  writeFileSync(jsonOut, JSON.stringify({ base, scannedAt: new Date().toISOString(), urls, violations: [...violations.values()], undeclared: [...undeclared.values()], thirdParties: [...thirdParties].sort() }, null, 2));
}
process.exit(violations.size || undeclared.size ? 1 : 0);
