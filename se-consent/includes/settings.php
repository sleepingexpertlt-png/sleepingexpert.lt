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
 * Žinomos paslaugos: šablonas (dalis URL arba įterpto scenarijaus teksto) => kategorija.
 * 'src' tikrinamas prieš <script src>/<iframe src>, 'inline' — prieš įterptų scenarijų turinį.
 * Google žymos (gtag.js, GTM) čia nėra: jas valdo Consent Mode. Basic režimu jos pridedamos atskirai.
 */
function se_consent_known_services() {
    return [
        'src' => [
            'connect.facebook.net'      => 'marketing',
            'facebook.com/tr'           => 'marketing',
            'googleadservices.com'      => 'marketing',
            'googlesyndication.com'     => 'marketing',
            'doubleclick.net'           => 'marketing',
            'analytics.tiktok.com'      => 'marketing',
            'snap.licdn.com'            => 'marketing',
            'bat.bing.com'              => 'marketing',
            's.pinimg.com'              => 'marketing',
            'static.criteo.net'         => 'marketing',
            'static.klaviyo.com'        => 'marketing',
            'omnisnippet1.com'          => 'marketing',
            'omnisrc.com'               => 'marketing',
            'js.hs-scripts.com'         => 'marketing',
            'youtube.com/embed'         => 'marketing',
            'youtube-nocookie.com/embed'=> 'marketing',
            'google.com/maps/embed'     => 'marketing',
            'maps.googleapis.com'       => 'marketing',
            'player.vimeo.com'          => 'statistics',
            'clarity.ms'                => 'statistics',
            'static.hotjar.com'         => 'statistics',
            'script.hotjar.com'         => 'statistics',
            'mc.yandex.ru'              => 'statistics',
            'google-analytics.com/analytics.js' => 'statistics',
        ],
        'inline' => [
            'fbq('                      => 'marketing',
            'ttq.load'                  => 'marketing',
            '_linkedin_partner_id'      => 'marketing',
            'uetq'                      => 'marketing',
            'pintrk('                   => 'marketing',
            'omnisend'                  => 'marketing',
            'klaviyo'                   => 'marketing',
            'clarity.ms'                => 'statistics',
            'hotjar.com'                => 'statistics',
            'mc.yandex.ru'              => 'statistics',
        ],
        'basic_google' => [
            'googletagmanager.com/gtag/js' => 'statistics',
            'googletagmanager.com/gtm.js'  => 'statistics',
        ],
    ];
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
