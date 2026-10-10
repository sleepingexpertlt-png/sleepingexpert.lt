<?php
/** Blokatoriaus testai be WordPress: php tests/blocker-test.php */

define('ABSPATH', __DIR__);
function add_action() {}
function apply_filters($n, $v) { return $v; }
require __DIR__ . '/../includes/settings.php';
require __DIR__ . '/../includes/blocker.php';

$known = se_consent_known_services();
$rules = ['src' => $known['src'], 'inline' => $known['inline']];
$fail  = 0;

function check($name, $cond) {
    global $fail;
    echo ($cond ? "ok   " : "FAIL ") . $name . "\n";
    if (!$cond) $fail++;
}

$b = function ($html) use ($rules) { return se_consent_block_html($html, $rules); };

$o = $b('<script src="https://connect.facebook.net/en_US/fbevents.js" async></script>');
check('Meta src blokuojamas', strpos($o, 'type="text/plain" data-se-consent="marketing') !== false && strpos($o, 'async') !== false);

$o = $b("<script>!function(f,b,e,v,n,t,s){}(window);fbq('init','123');</script>");
check('Meta inline blokuojamas', strpos($o, 'data-se-consent="marketing') !== false && strpos($o, "fbq('init','123')") !== false);

$o = $b('<script type="text/javascript">(function(c,l,a,r,i,t,y){t.src="https://www.clarity.ms/tag/"+i})()</script>');
check('Clarity -> statistics, originalus type išsaugotas', strpos($o, 'data-se-consent="statistics') !== false && strpos($o, 'data-se-type="text/javascript"') !== false && substr_count($o, 'type=') === 2);

$o = $b('<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>');
check('gtag.js advanced režimu neblokuojamas', strpos($o, 'text/plain') === false);

$basic = $rules; $basic['src'] += $known['basic_google'];
$o = se_consent_block_html('<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>', $basic);
check('gtag.js basic režimu blokuojamas', strpos($o, 'data-se-consent="statistics') !== false);

$o = $b('<script type="application/ld+json">{"fbq(":1}</script>');
check('JSON-LD nepaliečiamas', strpos($o, 'text/plain') === false);

$o = $b('<script>var a = 1;</script><script src="/wp-includes/js/jquery/jquery.min.js"></script>');
check('Paprasti scenarijai nepaliečiami', strpos($o, 'text/plain') === false);

$o = $b('<script data-se-consent-ignore>fbq("track","PageView")</script>');
check('data-se-consent-ignore gerbiamas', strpos($o, 'text/plain') === false);

$o = $b('<script type="text/plain" data-cookieconsent="statistics">ga()</script>');
check('Cookiebot žymėjimas perimamas', strpos($o, 'data-se-consent="statistics') !== false && substr_count($o, 'type=') === 1);

$o = $b('<script data-cookieconsent="ignore">fbq("x")</script>');
check('Cookiebot ignore gerbiamas', strpos($o, 'text/plain') === false);

$o = $b('<script type="module" src="https://analytics.tiktok.com/x.js"></script>');
check('module tipas atkuriamas', strpos($o, 'data-se-type="module"') !== false);

$o = $b('<iframe width="560" height="315" src="https://www.youtube.com/embed/abc" allowfullscreen></iframe>');
check('YouTube iframe blokuojamas', strpos($o, 'data-se-src="https://www.youtube.com/embed/abc"') !== false && strpos($o, ' src=') === false && strpos($o, 'data-se-consent="marketing') !== false);

$o = $b('<iframe src="https://example.com/form"></iframe>');
check('Nežinomas iframe nepaliečiamas', $o === '<iframe src="https://example.com/form"></iframe>');

$o = $b("<script src='https://snap.licdn.com/li.lms-analytics/insight.min.js'></script>");
check('Kabutės \' palaikomos', strpos($o, 'data-se-consent="marketing') !== false);

$o = $b('<script src="https://connect.facebook.net/en_US/fbevents.js"></script>');
check('Paslaugos ID pažymėtas (marketing:meta)', strpos($o, 'data-se-consent="marketing:meta"') !== false);
$o = $b('<script src="https://www.clarity.ms/tag/x"></script>');
check('Paslaugos ID pažymėtas (statistics:clarity)', strpos($o, 'data-se-consent="statistics:clarity"') !== false);

check('IP maskavimas v4', (function () { require_once __DIR__ . '/../includes/log.php'; return se_consent_mask_ip('192.168.1.77') === '192.168.1.0'; })());
check('IP maskavimas v6', se_consent_mask_ip('2001:db8:abcd:12::1') === '2001:db8:abcd::');

echo $fail ? "\n$fail FAIL\n" : "\nVisi testai praėjo\n";
exit($fail ? 1 : 0);
