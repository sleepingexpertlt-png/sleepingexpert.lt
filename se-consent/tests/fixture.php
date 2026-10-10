<?php
/** Sugeneruoja testinį puslapį taip, kaip jį matytų lankytojas: php tests/fixture.php > page.html */

define('ABSPATH', __DIR__);
function add_action() {}
function apply_filters($n, $v) { return $v; }
function get_option($n, $d = false) { return $d; }
require __DIR__ . '/../includes/settings.php';
require __DIR__ . '/../includes/blocker.php';

$known = se_consent_known_services();
$rules = ['src' => $known['src'] + ['tracker.test/order-a.js' => 'statistics'], 'inline' => $known['inline'] + ['__orderB' => 'statistics']];
$cookies = [];
foreach (se_consent_cookie_list() as $c) {
    $cookies[$c['category']][] = [$c['name'], $c['provider'], $c['purpose'], $c['expiry']];
}
$cfg = [
    'version' => 1, 'expiryDays' => 365, 'domain' => '', 'gcm' => true, 'adsRedaction' => true,
    'urlPassthrough' => false, 'gaCookieDays' => 395, 'compat' => true, 'floating' => true, 'position' => 'bottom',
    'logUrl' => 'https://shop.test/wp-json/se-consent/v1/log', 'privacyUrl' => '/privatumo-politika/',
    'colors' => ['#142b6f', '#ffd602'], 'rules' => $rules, 'cookies' => $cookies,
    't' => se_consent_default_texts()['lt'],
];
$head = '<style>' . file_get_contents(__DIR__ . '/../assets/consent.css') . '</style>'
    . '<script id="se-consent-config" data-se-consent-ignore>window.SE_CONSENT_CONFIG=' . json_encode($cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . ';</script>'
    . '<script id="se-consent-js" data-se-consent-ignore>' . file_get_contents(__DIR__ . '/../assets/consent.js') . '</script>';

$body = <<<HTML
<!doctype html><html lang="lt"><head><meta charset="utf-8">{$head}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TEST"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-TEST');</script>
<script>!function(f){f.__fbInline=(f.__fbInline||0)+1;var t=document.createElement('script');t.async=!0;t.src='https://connect.facebook.net/en_US/fbevents.js';document.head.appendChild(t)}(window);/* fbq( */</script>
<script src="https://tracker.test/order-a.js"></script>
<script>window.__orderB = (window.__orderA === 1) ? 'after-a' : 'before-a';</script>
</head><body>
<h1>Testas</h1>
<iframe width="560" height="315" src="https://www.youtube.com/embed/abc"></iframe>
<a href="#se-consent" id="footer-link">Slapukai</a>
<button id="inject" onclick="var s=document.createElement('script');s.src='https://analytics.tiktok.com/i18n/pixel/events.js';document.body.appendChild(s)">inject</button>
</body></html>
HTML;
echo se_consent_block_html($body, $rules);
