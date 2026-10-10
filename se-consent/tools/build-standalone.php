<?php
/**
 * Versija be WordPress (bet kuriai platformai): php tools/build-standalone.php [config.json] > dist/se-consent.js
 *
 * Įdėjimas: <script src="/se-consent.js"></script> — PIRMAS elementas <head>, prieš GTM ir kitus scenarijus.
 * Be serverio filtro sekikliai blokuojami naršyklėje (parserio ir dinaminiai scenarijai), todėl
 * eilė svarbi: viskas, kas įkelta ANKSČIAU už šį failą, nebus sustabdyta.
 * config.json (neprivaloma) perrašo numatytąsias reikšmes: privacyUrl, logUrl, colors, cookies ir kt.
 */

define('ABSPATH', __DIR__);
function add_action() {}
function apply_filters($n, $v) { return $v; }
function get_option($n, $d = false) { return $d; }
require __DIR__ . '/../includes/settings.php';

$over  = isset($argv[1]) ? json_decode((string) file_get_contents($argv[1]), true) : [];
$lang  = $over['lang'] ?? 'lt';
$known = se_consent_known_services();
$cookies = [];
foreach (se_consent_cookie_list() as $c) {
    if ($c['name'] === 'wp_consent_*') continue;
    $cookies[$c['category']][] = [$c['name'], $c['provider'], $c['purpose'], $c['expiry']];
}
$cfg = array_replace([
    'version' => 1, 'expiryDays' => 365, 'domain' => '', 'gcm' => true, 'adsRedaction' => true,
    'urlPassthrough' => false, 'gaCookieDays' => 395, 'gpc' => true, 'uet' => true, 'clarity' => true, 'services' => se_consent_client_services($over['services'] ?? se_consent_defaults()['services_shown']), 'compat' => true, 'floating' => true, 'position' => 'bottom',
    'logUrl' => '', 'privacyUrl' => '/privatumo-politika/', 'colors' => ['#142b6f', '#ffd602'],
    'rules' => ['src' => $known['src'], 'inline' => $known['inline']],
    'cookies' => $cookies, 't' => se_consent_default_texts()[$lang],
], array_diff_key($over, ['lang' => 1, 'services' => 1]));

$css = trim((string) file_get_contents(__DIR__ . '/../assets/consent.css'));
echo "/*! SE Consent standalone — sugeneruota " . gmdate('Y-m-d') . " */\n";
echo 'window.SE_CONSENT_CONFIG=' . json_encode($cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . ";\n";
echo '(function(d){var s=d.createElement("style");s.id="se-consent-css";s.textContent=' . json_encode($css, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . ';(d.head||d.documentElement).appendChild(s)})(document);' . "\n";
echo file_get_contents(__DIR__ . '/../assets/consent.js');
