<?php
/** Testinė svetainė skeneriui: php tests/scan-fixture.php http://127.0.0.1:PORT */

define('ABSPATH', __DIR__);
function add_action() {}
function apply_filters($n, $v) { return $v; }
function get_option($n, $d = false) { return $d; }
require __DIR__ . '/../includes/settings.php';
require __DIR__ . '/../includes/blocker.php';

$tp    = $argv[1];
$known = se_consent_known_services();
$rules = ['src' => $known['src'] + ['/blocked-stats.js' => 'statistics'], 'inline' => $known['inline']];
$cookies = [];
foreach (se_consent_cookie_list() as $c) {
    $cookies[$c['category']][] = [$c['name'], $c['provider'], $c['purpose'], $c['expiry']];
}
$cfg = [
    'version' => 1, 'expiryDays' => 365, 'domain' => '', 'gcm' => true, 'adsRedaction' => true,
    'urlPassthrough' => false, 'gaCookieDays' => 395, 'compat' => true, 'floating' => true, 'position' => 'bottom',
    'logUrl' => '', 'privacyUrl' => '/privatumo-politika/', 'colors' => ['#142b6f', '#ffd602'],
    'rules' => $rules, 'cookies' => $cookies, 't' => se_consent_default_texts()['lt'],
];
$head = '<style>' . file_get_contents(__DIR__ . '/../assets/consent.css') . '</style>'
    . '<script id="se-consent-config" data-se-consent-ignore>window.SE_CONSENT_CONFIG=' . json_encode($cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . ';</script>'
    . '<script id="se-consent-js" data-se-consent-ignore>' . file_get_contents(__DIR__ . '/../assets/consent.js') . '</script>';

echo se_consent_block_html(<<<HTML
<!doctype html><html lang="lt"><head><meta charset="utf-8">{$head}
<script src="{$tp}/blocked-stats.js"></script>
<script src="{$tp}/leaky.js"></script>
</head><body><h1>Skenerio testas</h1></body></html>
HTML, $rules);
