<?php
/**
 * Išvestis <head> pradžioje: Consent Mode numatytosios reikšmės + konfigūracija + consent.js.
 * Viskas įterpiama tiesiai į HTML (~12 KB), todėl nėra jokios papildomos užklausos.
 */

if (!defined('ABSPATH')) {
    exit;
}

// Prioritetas -1000: Consent Mode "default" privalo būti prieš bet kurią Google žymą (GTM, gtag).
add_action('wp_head', 'se_consent_print_head', -1000);

function se_consent_client_config() {
    $s    = se_consent_settings();
    $lang = se_consent_lang();
    $cookies = [];
    foreach (se_consent_cookie_list() as $c) {
        $cookies[$c['category']][] = [$c['name'], $c['provider'], $c['purpose'], $c['expiry']];
    }
    $rules = se_consent_rules();
    return [
        'version'     => (int) $s['consent_version'],
        'expiryDays'  => max(1, min(395, (int) $s['expiry_days'])), // ne daugiau 13 mėn. (EDPB/CNIL gairės)
        'domain'      => (string) $s['cookie_domain'],
        'gcm'         => (bool) $s['gcm_enabled'],
        'adsRedaction'=> (bool) $s['gcm_ads_redaction'],
        'urlPassthrough' => (bool) $s['gcm_url_passthrough'],
        'gaCookieDays' => max(0, min(395, (int) $s['ga_cookie_days'])),
        'compat'      => (bool) $s['cookiebot_compat'],
        'floating'    => (bool) $s['floating_button'],
        'position'    => $s['position'] === 'center' ? 'center' : 'bottom',
        'logUrl'      => esc_url_raw(rest_url('se-consent/v1/log')),
        'privacyUrl'  => esc_url_raw($s['privacy_url']),
        'colors'      => [sanitize_hex_color($s['color_primary']) ?: '#142b6f', sanitize_hex_color($s['color_accent']) ?: '#ffd602'],
        'rules'       => ['src' => $rules['src'], 'inline' => $rules['inline']],
        'cookies'     => $cookies,
        't'           => $s['texts'][$lang],
    ];
}

function se_consent_print_head() {
    $cfg = se_consent_client_config();
    $js  = (string) file_get_contents(SE_CONSENT_DIR . 'assets/consent.js');
    $css = (string) file_get_contents(SE_CONSENT_DIR . 'assets/consent.css');
    $json = wp_json_encode($cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG);

    echo "<!-- SE Consent " . esc_html(SE_CONSENT_VERSION) . " -->\n";
    echo '<style id="se-consent-css">' . $css . "</style>\n"; // phpcs:ignore WordPress.Security.EscapeOutput
    echo '<script id="se-consent-config" data-se-consent-ignore>window.SE_CONSENT_CONFIG=' . $json . ";</script>\n"; // phpcs:ignore
    echo '<script id="se-consent-js" data-se-consent-ignore>' . $js . "</script>\n"; // phpcs:ignore
}

/** [se_consent_link]Slapukų nustatymai[/se_consent_link] — nuoroda banerio atidarymui (pvz. poraštėje). */
add_shortcode('se_consent_link', function ($atts, $content = '') {
    $label = $content !== '' ? $content : se_consent_settings()['texts'][se_consent_lang()]['reopen'];
    return '<a href="#se-consent" class="se-consent-open">' . esc_html($label) . '</a>';
});
