// Naršyklės testai: NODE_PATH=$(npm root -g) node tests/browser-test.mjs
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));
const html = execFileSync('php', [path.join(dir, 'fixture.php')]).toString();

const ORIGIN = 'https://shop.test';
let fails = 0;
const check = (name, cond, extra = '') => {
  console.log(`${cond ? 'ok  ' : 'FAIL'} ${name}${!cond && extra ? ' — ' + extra : ''}`);
  if (!cond) fails++;
};

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });

async function newPage(ctx) {
  const logs = [];
  const page = await ctx.newPage();
  await page.route('**/*', async (route) => {
    const u = route.request().url();
    const js = (body) => route.fulfill({ status: 200, contentType: 'application/javascript', body });
    if (u.startsWith(ORIGIN + '/wp-json/se-consent/v1/log')) {
      logs.push(JSON.parse(route.request().postData() || '{}'));
      return route.fulfill({ status: 201, body: '{"ok":true}' });
    }
    if (u.startsWith(ORIGIN)) return route.fulfill({ status: 200, contentType: 'text/html', body: html });
    if (u.includes('googletagmanager.com/gtag/js')) return js('window.__gtag=1;');
    if (u.includes('connect.facebook.net')) return js('window.__fb=(window.__fb||0)+1; document.cookie="_fbp=fb.1.123;path=/";');
    if (u.includes('tracker.test/order-a.js')) return new Promise((r) => setTimeout(r, 150)).then(() => js('window.__orderA=1;'));
    if (u.includes('analytics.tiktok.com')) return js('window.__tiktok=1;');
    if (u.includes('youtube.com/embed')) return route.fulfill({ status: 200, contentType: 'text/html', body: '<p>video</p>' });
    return route.fulfill({ status: 404, body: '' });
  });
  return { page, logs };
}

const consentCalls = (page) => page.evaluate(() =>
  window.dataLayer.filter((a) => a[0] === 'consent').map((a) => [a[1], a[2].ad_storage, a[2].analytics_storage]));

// 1. Pirmas apsilankymas — niekas nepaleista.
{
  const ctx = await browser.newContext();
  const { page, logs } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.waitForTimeout(300);
  check('Baneris rodomas', await page.isVisible('#se-consent'));
  check('Meta nepaleista iki sutikimo', await page.evaluate(() => !window.__fb && !window.__fbInline));
  check('Statistikos scenarijai nepaleisti', await page.evaluate(() => !window.__orderA && !window.__orderB));
  check('gtag.js veikia (Consent Mode advanced)', await page.evaluate(() => window.__gtag === 1));
  const calls = await consentCalls(page);
  check('Consent default = denied, pirmas dataLayer įrašas', JSON.stringify(calls) === '[["default","denied","denied"]]', JSON.stringify(calls));
  check('Google slapukų galiojimas apribotas 395 d.', await page.evaluate(() => window.dataLayer.some((a) => a[0] === 'set' && a[1] && a[1].cookie_expires === 395 * 86400)));
  check('YouTube iframe be src + placeholderis', await page.evaluate(() => !document.querySelector('iframe').getAttribute('src') && !!document.querySelector('.se-c-ph')));
  check('Atmesti ir sutikti mygtukai vienodo dydžio', await page.evaluate(() => {
    const a = document.querySelector('[data-a="accept"]').getBoundingClientRect();
    const r = document.querySelector('[data-a="reject"]').getBoundingClientRect();
    return Math.abs(a.width - r.width) < 2 && Math.abs(a.height - r.height) < 2;
  }));

  await page.click('#inject');
  await page.waitForTimeout(200);
  check('Dinamiškai įterptas TikTok užblokuotas', await page.evaluate(() => !window.__tiktok));

  // Atmesti
  await page.click('[data-a="reject"]');
  await page.waitForTimeout(300);
  check('Atmetus baneris dingsta', !(await page.isVisible('#se-consent')));
  check('Atmetus Meta nepaleista', await page.evaluate(() => !window.__fb));
  check('Žurnale reject_all', logs.length === 1 && logs[0].m === 'reject_all' && logs[0].c.marketing === false, JSON.stringify(logs));
  check('Plaukiojantis mygtukas rodomas', await page.isVisible('#se-consent-reopen'));
  check('wp_consent_marketing=deny', (await ctx.cookies()).some((c) => c.name === 'wp_consent_marketing' && c.value === 'deny'));

  // Grįžtantis lankytojas
  await page.reload();
  await page.waitForTimeout(300);
  check('Grįžus baneris nerodomas', !(await page.isVisible('#se-consent')));
  check('Grįžus Meta vis dar nepaleista', await page.evaluate(() => !window.__fb));
  await ctx.close();
}

// 2. Sutikti su visais.
{
  const ctx = await browser.newContext();
  const { page, logs } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.click('#inject');
  await page.click('[data-a="accept"]');
  await page.waitForTimeout(600);
  check('Sutikus Meta inline + fbevents.js paleisti po 1 kartą', await page.evaluate(() => window.__fbInline === 1 && window.__fb === 1));
  check('Eiliškumas išlaikytas (B po A)', await page.evaluate(() => window.__orderB === 'after-a'), await page.evaluate(() => window.__orderB));
  check('Užblokuotas TikTok paleistas po sutikimo', await page.evaluate(() => window.__tiktok === 1));
  check('Iframe įkeltas, placeholderis pašalintas', await page.evaluate(() => document.querySelector('iframe').src.includes('youtube.com/embed') && !document.querySelector('.se-c-ph')));
  const calls = await consentCalls(page);
  check('Consent update = granted', JSON.stringify(calls.at(-1)) === '["update","granted","granted"]', JSON.stringify(calls));
  check('Cookiebot suderinamumas', await page.evaluate(() => window.Cookiebot.consent.marketing === true && window.Cookiebot.consented === true));
  check('GTM įvykis cookie_consent_marketing', await page.evaluate(() => window.dataLayer.some((e) => e.event === 'cookie_consent_marketing')));
  check('Žurnale accept_all', logs.at(-1)?.m === 'accept_all');

  // Grįžus — sutikimas taikomas iškart po default
  await page.reload();
  await page.waitForTimeout(600);
  const c2 = await consentCalls(page);
  check('Grįžus: default, tada iškart update granted', JSON.stringify(c2) === '[["default","denied","denied"],["update","granted","granted"]]', JSON.stringify(c2));
  check('Grįžus Meta paleista be paspaudimo', await page.evaluate(() => window.__fb === 1 && window.__fbInline === 1));

  // Atšaukti rinkodarą per nustatymus
  check('_fbp slapukas yra', (await ctx.cookies()).some((c) => c.name === '_fbp'));
  await page.click('#se-consent-reopen');
  await page.uncheck('.se-c__sw[data-cat="marketing"]');
  await Promise.all([page.waitForEvent('load'), page.click('[data-a="save"]')]);
  await page.waitForTimeout(400);
  check('Atšaukus _fbp ištrintas', !(await ctx.cookies()).some((c) => c.name === '_fbp'));
  check('Atšaukus po perkrovimo Meta nepaleista', await page.evaluate(() => !window.__fb));
  check('Atšaukus statistika liko', await page.evaluate(() => window.SEConsent.has('statistics') && !window.SEConsent.has('marketing')));
  await ctx.close();
}

// 3. Placeholderio mygtukas ir nuoroda poraštėje.
{
  const ctx = await browser.newContext();
  const { page } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.click('.se-c-ph button');
  await page.waitForTimeout(300);
  check('Placeholderis leidžia tik rinkodarą', await page.evaluate(() => window.SEConsent.has('marketing') && !window.SEConsent.has('statistics')));
  await page.click('#footer-link');
  check('Poraštės nuoroda atidaro nustatymus', await page.isVisible('.se-c__details'));
  await ctx.close();
}

// 5. Atskira paslauga: rinkodara leidžiama, bet Meta išjungta.
{
  const ctx = await browser.newContext();
  const { page, logs } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.click('[data-a="customize"]');
  await page.check('[data-cat="marketing"]');
  check('Kategorijos jungiklis įjungia visas jos paslaugas', await page.evaluate(() => [...document.querySelectorAll('[data-svc-cat="marketing"]')].every((x) => x.checked)));
  await page.uncheck('[data-svc="meta"]');
  check('Viena išjungta paslauga kategorijos neišjungia', await page.isChecked('[data-cat="marketing"]'));
  await page.click('#inject');
  await page.click('[data-a="save"]');
  await page.waitForTimeout(600);
  check('Meta NEpaleista (išjungta atskirai)', await page.evaluate(() => !window.__fb && !window.__fbInline));
  check('TikTok ir YouTube paleisti (rinkodara leista)', await page.evaluate(() => window.__tiktok === 1 && document.querySelector('iframe').src.includes('youtube')));
  check('Google Ads Consent Mode granted (paslauga neišjungta)', JSON.stringify((await consentCalls(page)).at(-1)) === '["update","granted","denied"]', JSON.stringify((await consentCalls(page)).at(-1)));
  check('API: has("marketing:meta") = false, has("marketing:tiktok") = true', await page.evaluate(() => !window.SEConsent.has('marketing:meta') && window.SEConsent.has('marketing:tiktok')));
  check('Žurnale išjungta paslauga meta', logs.at(-1)?.s?.meta === false, JSON.stringify(logs.at(-1)));
  check('dataLayer se_consent.services.meta = false', await page.evaluate(() => window.dataLayer.filter((e) => e.event === 'se_consent_update').at(-1).se_consent.services.meta === false));
  await page.reload();
  await page.waitForTimeout(500);
  check('Grįžus Meta lieka išjungta', await page.evaluate(() => !window.__fb && !window.__fbInline));
  await ctx.close();
}

// 6. Atšaukiama tik viena paslauga — trinami tik jos slapukai.
{
  const ctx = await browser.newContext();
  const { page } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.click('[data-a="accept"]');
  await page.waitForTimeout(500);
  await page.evaluate(() => { document.cookie = '_ga=GA1.1.1;path=/'; document.cookie = '_ttp=x;path=/'; });
  await page.click('#se-consent-reopen');
  await page.uncheck('[data-svc="meta"]');
  await Promise.all([page.waitForEvent('load'), page.click('[data-a="save"]')]);
  await page.waitForTimeout(400);
  const names = (await ctx.cookies()).map((c) => c.name);
  check('Atšaukus Meta: _fbp ištrintas, _ga ir _ttp liko', !names.includes('_fbp') && names.includes('_ga') && names.includes('_ttp'), names.join(','));
  await ctx.close();
}

// 7. Placeholderis leidžia TIK tą paslaugą.
{
  const ctx = await browser.newContext();
  const { page } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.click('.se-c-ph button');
  await page.waitForTimeout(400);
  check('YouTube įkeltas', await page.evaluate(() => document.querySelector('iframe').src.includes('youtube')));
  check('Meta per YouTube placeholderį NEleista', await page.evaluate(() => !window.__fb && !window.__fbInline && !window.SEConsent.has('marketing:meta')));
  await ctx.close();
}

// 8. Global Privacy Control.
{
  const ctx = await browser.newContext();
  await ctx.addInitScript(() => Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { get: () => true }));
  const { page, logs } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.waitForTimeout(300);
  check('GPC: baneris nerodomas', !(await page.isVisible('#se-consent')));
  check('GPC: užfiksuotas atsisakymas (m=gpc)', await page.evaluate(() => window.SEConsent.get().m === 'gpc' && !window.SEConsent.has('statistics')) && logs.at(-1)?.m === 'gpc');
  check('GPC: Meta nepaleista', await page.evaluate(() => !window.__fb));
  await ctx.close();
}

// 9. Prieinamumas: fokuso spąstai, Esc, fokuso grąžinimas; UET ir Clarity signalai.
{
  const ctx = await browser.newContext();
  const { page } = await newPage(ctx);
  await page.goto(ORIGIN + '/');
  await page.click('[data-a="reject"]');
  await page.focus('#footer-link');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(200);
  check('Nustatymų dialogas aria-modal', await page.getAttribute('#se-consent', 'aria-modal') === 'true');
  let inside = true;
  for (let i = 0; i < 40; i++) {
    await page.keyboard.press('Tab');
    if (!(await page.evaluate(() => document.getElementById('se-consent').contains(document.activeElement)))) { inside = false; break; }
  }
  check('Tab neišeina iš dialogo (40 paspaudimų)', inside);
  await page.keyboard.press('Escape');
  check('Esc uždaro, fokusas grįžta į nuorodą', !(await page.isVisible('#se-consent')) && await page.evaluate(() => document.activeElement.id === 'footer-link'));
  check('UET consent default denied', await page.evaluate(() => JSON.stringify(window.uetq.slice(0, 3)) === '["consent","default",{"ad_storage":"denied"}]'));
  check('Clarity consentv2 signalas siunčiamas', await page.evaluate(() => (window.clarity.q || []).some((a) => a[0] === 'consentv2' && a[1].analytics_Storage === 'denied')));
  await ctx.close();
}

// 4. Našumas — banerio JS + CSS dydis.
{
  const kb = (Buffer.byteLength(html.match(/<script id="se-consent-js"[^>]*>([\s\S]*?)<\/script>/)[1]) / 1024).toFixed(1);
  console.log(`info consent.js ${kb} KB (be minifikavimo, be išorinių užklausų)`);
}

await browser.close();
console.log(fails ? `\n${fails} FAIL` : '\nVisi naršyklės testai praėjo');
process.exit(fails ? 1 : 0);
