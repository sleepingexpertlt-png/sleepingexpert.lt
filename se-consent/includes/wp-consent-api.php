<?php
/**
 * WP Consent API integracija (https://wordpress.org/plugins/wp-consent-api/).
 * Naršyklės pusę (wp_consent_* slapukai, wp_listen_for_consent_change įvykis) atlieka consent.js;
 * čia tik deklaruojamas suderinamumas ir sutikimo tipas, kad WooCommerce / Site Kit pasitikėtų mumis.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_filter('wp_get_consent_type', function () {
    return 'optin';
});

add_action('plugins_loaded', function () {
    $plugin = plugin_basename(SE_CONSENT_FILE);
    add_filter("wp_consent_api_registered_{$plugin}", '__return_true');
});
