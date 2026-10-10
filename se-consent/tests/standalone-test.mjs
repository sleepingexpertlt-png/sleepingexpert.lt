// Versijos be WordPress testas: NODE_PATH=$(npm root -g) node tests/standalone-test.mjs
// Puslapis NEFILTRUOTAS serveryje — sekikliai įdėti įprastai, kaip bet kurioje platformoje.
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));
const lib = execFileSync('php', [path.join(dir, '../tools/build-standalone.php')]).toString();
const html = `<!doctype html><html lang="lt"><head><meta charset="utf-8">
<script src="/se-consent.js"></script>
<script async src="https://connect.facebook.net/en_US/fbevents.js"></script>
<script>window.__fbInline=1;/* fbq('init','1') */</script>
<script src="https://static.hotjar.com/c/hotjar-1.js"></script>
<script type="text/plain" data-se-consent="marketing" src="https://analytics.tiktok.com/x.js"></script>
</head><body><h1>Bet kuri platforma</h1>
<iframe width="560" height="315" src="https://www.youtube.com/embed/abc"></iframe>
</body></html>`;

let fails = 0;
const check = (n, c, x = '') => { console.log(`${c ? 'ok  ' : 'FAIL'} ${n}${!c && x ? ' — ' + x : ''}`); if (!c) fails++; };
const browser = await chromium.launch();
const ctx = await browser.newContext();
const page = await ctx.newPage();
const hits = [];
await page.route('**/*', (route) => {
  const u = route.request().url();
  const js = (b) => route.fulfill({ status: 200, contentType: 'application/javascript', body: b });
  if (u === 'https://shop.test/se-consent.js') return js(lib);
  if (u.startsWith('https://shop.test/')) return route.fulfill({ status: 200, contentType: 'text/html', body: html });
  hits.push(u);
  if (u.includes('fbevents.js')) return js('window.__fb=1;');
  if (u.includes('hotjar')) return js('window.__hj=1;');
  if (u.includes('tiktok')) return js('window.__tt=1;');
  if (u.includes('youtube.com/embed')) return route.fulfill({ status: 200, contentType: 'text/html', body: 'video' });
  return route.fulfill({ status: 404, body: '' });
});
await page.goto('https://shop.test/');
await page.waitForTimeout(500);
check('Baneris rodomas', await page.isVisible('#se-consent'));
check('Nepažymėti sekikliai NEPALEISTI iki sutikimo', await page.evaluate(() => !window.__fb && !window.__hj));
check('YouTube neužkrautas iki sutikimo', !hits.some((u) => u.includes('youtube')), hits.join(', '));
check('Pažymėtas (data-se-consent) sekiklis net nesiunčiamas', !hits.some((u) => u.includes('tiktok')));
console.log('info  naršyklės išankstinis atsisiuntimas be paleidimo: ' + hits.map((u) => new URL(u).hostname).join(', '));
check('Inline Meta kodas nepaleistas', await page.evaluate(() => !window.__fbInline));
check('Consent Mode default denied', await page.evaluate(() => window.dataLayer[0][0] === 'consent' && window.dataLayer[0][2].ad_storage === 'denied'));
await page.click('[data-a="accept"]');
await page.waitForTimeout(600);
check('Po sutikimo viskas paleista', await page.evaluate(() => window.__fb === 1 && window.__hj === 1 && window.__fbInline === 1 && window.__tt === 1));
check('YouTube įkeltas po sutikimo', hits.some((u) => u.includes('youtube.com/embed')));
await page.reload();
await page.waitForTimeout(600);
check('Grįžus paleidžiama be paspaudimo', await page.evaluate(() => window.__fb === 1 && window.__hj === 1));
await browser.close();
console.log(fails ? `\n${fails} FAIL` : '\nVisi versijos be WordPress testai praėjo');
process.exit(fails ? 1 : 0);
