<?php
/**
 * Nustatymai, numatytosios reikšmės ir žinomų paslaugų / slapukų žinynas.
 */

if (!defined('ABSPATH')) {
    exit;
}

const SE_CONSENT_OPTION = 'se_consent_settings';

/** Kategorijos — tokie pat raktai kaip Cookiebot, kad migracija būtų be pakeitimų. */
const SE_CONSENT_CATEGORIES = ['necessary', 'preferences', 'statistics', 'marketing'];

function se_consent_defaults() {
    return [
        // Didinant versiją visi lankytojai vėl pamato banerį (pvz. pasikeitus slapukų sąrašui).
        'consent_version'   => 1,
        'expiry_days'       => 365,
        'cookie_domain'     => '',        // pvz. ".sleepingexpert.lt" — bendras sutikimas subdomenams
        'gcm_enabled'       => 1,         // Google Consent Mode v2
        'gcm_mode'          => 'advanced', // advanced: Google žymos neblokuojamos (cookieless pings); basic: blokuojamos
        'gcm_ads_redaction' => 1,
        'gcm_url_passthrough' => 0,
        'gpc'               => 1,         // Global Privacy Control: naršyklės "ne" = atsisakymas be banerio
        'uet'               => 1,         // Microsoft UET consent mode
        'clarity_consent'   => 1,         // Microsoft Clarity consentv2 signalas
        // Baneryje rodomos tik svetainėje naudojamos paslaugos (kurias — parodo skeneris).
        // Blokavimo taisyklės galioja VISOMS registro paslaugoms, nepriklausomai nuo šio sąrašo.
        'services_shown'    => ['ga4', 'clarity', 'google-ads', 'meta', 'tiktok', 'youtube', 'maps'],
        'ga_cookie_days'    => 395,       // Google slapukų (_ga, _gcl_au) galiojimas; numatyta Google — 2 metai, leidžiama ≤ 13 mėn.
        'auto_block'        => 1,
        'cookiebot_compat'  => 1,         // window.Cookiebot, CookiebotOnAccept, dataLayer cookie_consent_* įvykiai
        'floating_button'   => 1,
        'log_retention_months' => 24,
        'privacy_url'       => '/privatumo-politika/',
        'color_primary'     => '#142b6f',
        'color_accent'      => '#ffd602',
        'position'          => 'bottom',  // bottom | center
        'extra_rules'       => '',        // eilutės: "šablonas | kategorija"
        'cookies'           => se_consent_default_cookies(),
        'texts'             => se_consent_default_texts(),
    ];
}

function se_consent_settings() {
    $saved = get_option(SE_CONSENT_OPTION, []);
    $s     = array_replace(se_consent_defaults(), is_array($saved) ? $saved : []);
    $s['texts'] = array_replace_recursive(se_consent_default_texts(), (array) $s['texts']);
    return $s;
}

function se_consent_default_texts() {
    return [
        'lt' => [
            'title'       => 'Mes naudojame slapukus',
            'body'        => 'Būtinieji slapukai užtikrina svetainės ir krepšelio veikimą. Su jūsų sutikimu naudosime ir statistikos bei rinkodaros slapukus, kad tobulintume svetainę ir rodytume aktualius pasiūlymus. Sutikimą galite bet kada pakeisti.',
            'accept_all'  => 'Sutinku su visais',
            'reject_all'  => 'Tik būtinieji',
            'customize'   => 'Nustatymai',
            'save'        => 'Išsaugoti pasirinkimą',
            'privacy'     => 'Privatumo politika',
            'settings_title' => 'Slapukų nustatymai',
            'always_on'   => 'Visada įjungta',
            'blocked_content' => 'Šis turinys rodomas tik sutikus su rinkodaros slapukais.',
            'blocked_button'  => 'Leisti ir rodyti',
            'reopen'      => 'Slapukų nustatymai',
            'cookies'     => 'Slapukai',
            'services'    => 'Paslaugos',
            'cat' => [
                'necessary'   => ['Būtinieji', 'Reikalingi svetainės veikimui: krepšelis, prisijungimas, saugumas, jūsų sutikimo išsaugojimas. Jų išjungti negalima.'],
                'preferences' => ['Nuostatų', 'Įsimena jūsų pasirinkimus, pvz. kalbą ar regioną.'],
                'statistics'  => ['Statistikos', 'Padeda suprasti, kaip lankytojai naudojasi svetaine (anonimizuota statistika).'],
                'marketing'   => ['Rinkodaros', 'Naudojami reklamai ir jos efektyvumui matuoti (Google Ads, Meta ir kt.).'],
            ],
        ],
        'en' => [
            'title'       => 'We use cookies',
            'body'        => 'Necessary cookies keep the site and your cart working. With your consent we also use statistics and marketing cookies to improve the site and show relevant offers. You can change your choice at any time.',
            'accept_all'  => 'Accept all',
            'reject_all'  => 'Necessary only',
            'customize'   => 'Settings',
            'save'        => 'Save selection',
            'privacy'     => 'Privacy policy',
            'settings_title' => 'Cookie settings',
            'always_on'   => 'Always on',
            'blocked_content' => 'This content is shown only after accepting marketing cookies.',
            'blocked_button'  => 'Allow and show',
            'reopen'      => 'Cookie settings',
            'cookies'     => 'Cookies',
            'services'    => 'Services',
            'cat' => [
                'necessary'   => ['Necessary', 'Required for the site to work: cart, login, security and storing your consent. They cannot be disabled.'],
                'preferences' => ['Preferences', 'Remember your choices such as language or region.'],
                'statistics'  => ['Statistics', 'Help us understand how visitors use the site (anonymised).'],
                'marketing'   => ['Marketing', 'Used for advertising and measuring its effectiveness (Google Ads, Meta, etc.).'],
            ],
        ],
    ];
}

/**
 * Paslaugų registras: kiekviena paslauga turi savo jungiklį banerio nustatymuose (kaip Klaro,
 * tarteaucitron, CookieConsent v3) ir savo slapukų sąrašą, kuris tiksliai ištrinamas atšaukus.
 * 'src' — URL fragmentai (<script src>, <iframe src>), 'inline' — įterpto kodo fragmentai.
 * Google gtag.js / GTM čia nėra: juos valdo Consent Mode (basic režimu — 'basic_google').
 * Slapukų sąrašai — viešai dokumentuoti faktai (tiekėjų dokumentacija, Open Cookie Database).
 */
function se_consent_services() {
    return apply_filters('se_consent_services', [
        'ga4'        => ['Google Analytics', 'statistics', ['google-analytics.com/analytics.js'], [], ['_ga', '_ga_*', '_gid', '_gat*']],
        'clarity'    => ['Microsoft Clarity', 'statistics', ['clarity.ms'], ['clarity.ms'], ['_clck', '_clsk', 'CLID', 'MUID']],
        'hotjar'     => ['Hotjar', 'statistics', ['static.hotjar.com', 'script.hotjar.com'], ['hotjar.com'], ['_hj*']],
        'yandex'     => ['Yandex Metrica', 'statistics', ['mc.yandex.ru'], ['mc.yandex.ru'], ['_ym_*', 'yandexuid']],
        'vimeo'      => ['Vimeo', 'statistics', ['player.vimeo.com'], [], ['vuid']],
        'google-ads' => ['Google Ads', 'marketing', ['googleadservices.com', 'googlesyndication.com', 'doubleclick.net'], [], ['_gcl_au', '_gcl_aw', '_gcl_dc', '_gcl_gb']],
        'meta'       => ['Meta (Facebook) Pixel', 'marketing', ['connect.facebook.net', 'facebook.com/tr'], ['fbq('], ['_fbp', '_fbc']],
        'tiktok'     => ['TikTok Pixel', 'marketing', ['analytics.tiktok.com'], ['ttq.load', 'ttq.page'], ['_ttp', '_tt_enable_cookie', 'ttcsid*']],
        'bing'       => ['Microsoft Advertising (Bing)', 'marketing', ['bat.bing.com'], ['uetq'], ['_uetsid', '_uetvid', '_uetmsclkid']],
        'linkedin'   => ['LinkedIn Insight', 'marketing', ['snap.licdn.com'], ['_linkedin_partner_id'], ['li_fat_id', 'li_sugr', 'lidc']],
        'pinterest'  => ['Pinterest Tag', 'marketing', ['s.pinimg.com'], ['pintrk('], ['_pin_unauth', '_pinterest_ct_ua', '_epik']],
        'criteo'     => ['Criteo', 'marketing', ['static.criteo.net'], [], ['cto_bundle', 'cto_bidid']],
        'klaviyo'    => ['Klaviyo', 'marketing', ['static.klaviyo.com'], ['klaviyo'], ['__kla_id']],
        'omnisend'   => ['Omnisend', 'marketing', ['omnisnippet1.com', 'omnisrc.com'], ['omnisend'], ['omnisendContactID', 'omnisendSessionID', 'soundestID', 'omnisendAnonymousID']],
        'hubspot'    => ['HubSpot', 'marketing', ['js.hs-scripts.com'], [], ['__hstc', 'hubspotutk', '__hssc', '__hssrc']],
        'youtube'    => ['YouTube', 'marketing', ['youtube.com/embed', 'youtube-nocookie.com/embed'], [], []],
        'maps'       => ['Google Maps', 'marketing', ['google.com/maps', 'maps.googleapis.com'], [], []],
    ]);
}

/** Suderinamumas su ankstesne struktūra: šablonas => "kategorija:paslauga". */
function se_consent_known_services() {
    $src = $inline = [];
    foreach (se_consent_services() as $id => $svc) {
        foreach ($svc[2] as $p) {
            $src[$p] = $svc[1] . ':' . $id;
        }
        foreach ($svc[3] as $p) {
            $inline[$p] = $svc[1] . ':' . $id;
        }
    }
    return [
        'src'    => $src,
        'inline' => $inline,
        'basic_google' => [
            'googletagmanager.com/gtag/js' => 'statistics:ga4',
            'googletagmanager.com/gtm.js'  => 'statistics',
        ],
    ];
}

/** Naršyklei: [[id, pavadinimas, kategorija, [slapukai]], ...] — tik rodomos paslaugos (null = visos). */
function se_consent_client_services($shown = null) {
    $out = [];
    foreach (se_consent_services() as $id => $svc) {
        if (is_array($shown) && !in_array($id, $shown, true)) {
            continue;
        }
        $out[] = [$id, $svc[0], $svc[1], $svc[4]];
    }
    return $out;
}

/**
 * Taisyklės blokatoriui: žinomos + administratoriaus papildomos.
 * @return array{src: array<string,string>, inline: array<string,string>}
 */
function se_consent_rules() {
    $s     = se_consent_settings();
    $known = se_consent_known_services();
    $rules = ['src' => $known['src'], 'inline' => $known['inline']];
    if (!$s['gcm_enabled'] || $s['gcm_mode'] === 'basic') {
        $rules['src'] += $known['basic_google'];
    }
    foreach (preg_split('/\r\n|\r|\n/', (string) $s['extra_rules']) as $line) {
        $parts = array_map('trim', explode('|', $line));
        if (count($parts) === 2 && $parts[0] !== '' && in_array($parts[1], SE_CONSENT_CATEGORIES, true)) {
            $rules['src'][$parts[0]]    = $parts[1];
            $rules['inline'][$parts[0]] = $parts[1];
        }
    }
    return apply_filters('se_consent_rules', $rules);
}

/**
 * Slapukų deklaracijos įrašai. Formatas eilutėje: pavadinimas | tiekėjas | kategorija | paskirtis | galiojimas
 */
function se_consent_default_cookies() {
    return implode("\n", [
        'se_consent | sleepingexpert.lt | necessary | Išsaugo jūsų slapukų sutikimą | 1 metai',
        'wp_consent_* | sleepingexpert.lt | necessary | Perduoda sutikimą kitiems įskiepiams (WP Consent API) | 1 metai',
        'woocommerce_cart_hash | sleepingexpert.lt | necessary | Krepšelio turinio pakeitimų sekimas | Sesija',
        'woocommerce_items_in_cart | sleepingexpert.lt | necessary | Ar krepšelyje yra prekių | Sesija',
        'wp_woocommerce_session_* | sleepingexpert.lt | necessary | Krepšelio sesija | 2 dienos',
        'wordpress_logged_in_* | sleepingexpert.lt | necessary | Prisijungimo sesija | Sesija',
        '_ga | Google | statistics | Unikalus lankytojo identifikatorius statistikai | 2 metai',
        '_ga_* | Google | statistics | Sesijos būsena Google Analytics 4 | 2 metai',
        '_clck | Microsoft Clarity | statistics | Clarity lankytojo ID | 1 metai',
        '_clsk | Microsoft Clarity | statistics | Clarity sesijos sujungimas | 1 diena',
        '_gcl_au | Google | marketing | Google Ads konversijų sekimas | 3 mėnesiai',
        '_fbp | Meta | marketing | Meta reklamos ir konversijų sekimas | 3 mėnesiai',
        '_fbc | Meta | marketing | Paspaudimo ant Meta reklamos identifikatorius | 3 mėnesiai',
        'IDE | Google (doubleclick.net) | marketing | Reklamos rodymas ir matavimas | 13 mėnesių',
    ]);
}

/** @return array<int, array{name:string,provider:string,category:string,purpose:string,expiry:string}> */
function se_consent_cookie_list() {
    $out = [];
    foreach (preg_split('/\r\n|\r|\n/', (string) se_consent_settings()['cookies']) as $line) {
        $p = array_map('trim', explode('|', $line));
        if (count($p) < 3 || $p[0] === '' || !in_array($p[2], SE_CONSENT_CATEGORIES, true)) {
            continue;
        }
        $out[] = [
            'name'     => $p[0],
            'provider' => $p[1],
            'category' => $p[2],
            'purpose'  => $p[3] ?? '',
            'expiry'   => $p[4] ?? '',
        ];
    }
    return $out;
}

function se_consent_lang() {
    $locale = function_exists('determine_locale') ? determine_locale() : get_locale();
    $lang   = strtolower(substr((string) $locale, 0, 2));
    $texts  = se_consent_settings()['texts'];
    return isset($texts[$lang]) ? $lang : 'lt';
}
