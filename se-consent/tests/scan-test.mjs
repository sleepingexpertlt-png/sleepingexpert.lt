// Skenerio testas su vietine svetaine ir "trečiąja šalimi": NODE_PATH=$(npm root -g) node tests/scan-test.mjs
import http from 'node:http';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scanSite, loadOcd, printReport } from '../tools/scan.mjs';

const dir = path.dirname(fileURLToPath(import.meta.url));
const listen = (handler) => new Promise((res) => { const s = http.createServer(handler).listen(0, '127.0.0.1', () => res(s)); });

// Trečioji šalis (127.0.0.1 — kitas host nei "localhost").
const tp = await listen((req, res) => {
  const js = (b) => { res.writeHead(200, { 'Content-Type': 'application/javascript' }); res.end(b); };
  if (req.url.startsWith('/blocked-stats.js')) {
    // Statistika: nustato _ga (2 metai) ir nedeklaruotą Hotjar slapuką.
    return js('document.cookie="_ga=GA1.1.1;path=/;max-age=63072000";document.cookie="_hjSessionUser_123=x;path=/;max-age=31536000";');
  }
  if (req.url.startsWith('/leaky.js')) {
    // Neblokuojamas sekiklis: fingerprinting + pikselis iškart, be sutikimo.
    return js(`var c=document.createElement('canvas');c.getContext('2d').fillText('x',1,1);c.toDataURL();
      navigator.hardwareConcurrency;new Image().src=document.currentScript.src.replace('leaky.js','px.gif')+'?uid=1234567890abcdef&sid=abcdefabcdef&ev=pageview&ts='+Date.now();`);
  }
  if (req.url.startsWith('/px.gif')) { res.writeHead(200, { 'Content-Type': 'image/gif' }); return res.end(Buffer.from('R0lGODlhAQABAAAAACw=', 'base64')); }
  res.writeHead(404); res.end();
});
const tpUrl = `http://127.0.0.1:${tp.address().port}`;
const html = execFileSync('php', [path.join(dir, 'scan-fixture.php'), tpUrl]).toString();

const site = await listen((req, res) => {
  if (req.url === '/sitemap.xml') {
    res.writeHead(200, { 'Content-Type': 'application/xml' });
    return res.end(`<urlset><url><loc>http://localhost:${site.address().port}/</loc></url></urlset>`);
  }
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(html);
});
// localhost klausosi 127.0.0.1 — tas pats serveris, bet kitas host vardas.
const base = `http://localhost:${site.address().port}`;

let fails = 0;
const check = (name, cond, extra = '') => { console.log(`${cond ? 'ok  ' : 'FAIL'} ${name}${!cond && extra ? ' — ' + extra : ''}`); if (!cond) fails++; };

const ocd = await loadOcd();
check('Open Cookie Database įkelta', ocd && ocd.size > 1000, String(ocd && ocd.size));
const r = await scanSite(base, { max: 5, ocd });
console.log(printReport(r));
console.log('');

const leak = r.violations.find((v) => v.type === 'užklausa' && v.name === '127.0.0.1');
check('Nutekantis sekiklis aptiktas kaip pažeidimas', !!leak);
check('Užblokuotas statistikos scenarijus nenustatė slapukų iki sutikimo', !r.violations.some((v) => v.type === 'slapukas'));
const s = r.suspects.find((x) => x.host === '127.0.0.1');
check('Elgsenos įvertinimas: canvas + navigator + pikselis', s && s.why.join(' ').includes('canvas') && s.why.join(' ').includes('navigator') && s.why.join(' ').includes('pikseliai'), JSON.stringify(s));
check('Pasiūlyta blokavimo taisyklė', s && s.rule === '127.0.0.1 | marketing');
check('_ga ilgesnis nei 13 mėn.', r.longCookies.some((c) => c.name === '_ga' && c.days > 395));
const hj = r.undeclared.find((u) => u.name === '_hjSessionUser_123');
check('Nedeklaruotas Hotjar slapukas klasifikuotas per Open Cookie Database', hj && hj.source === 'Open Cookie Database' && /\| statistics \|/.test(hj.suggestion), JSON.stringify(hj));
check('„Atmesti" pirmame sluoksnyje ir vienodo svorio', r.checks.rejectOnFirstLayer.ok, JSON.stringify(r.checks.rejectOnFirstLayer.detail));
check('Paskirtys nurodytos', r.checks.purposesListed.ok);
check('Atšaukimas: _ga ištrintas', r.checks.withdrawalWorks.detail && !r.checks.withdrawalWorks.detail.cookiesLeft.includes('_ga'), JSON.stringify(r.checks.withdrawalWorks.detail));
check('Bendras įvertinimas rodo trūkumus', r.score !== '6/6' && !r.checks.noTrackersBeforeConsent.ok);

tp.close(); site.close();
console.log(fails ? `\n${fails} FAIL` : '\nVisi skenerio testai praėjo');
process.exit(fails ? 1 : 0);
