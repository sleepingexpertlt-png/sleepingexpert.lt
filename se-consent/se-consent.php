<?php
/**
 * Plugin Name: SE Consent
 * Description: Savas slapukų sutikimų valdymas (Cookiebot pakaitalas): baneris, scenarijų blokavimas iki sutikimo, Google Consent Mode v2, sutikimų žurnalas, slapukų deklaracija, WP Consent API.
 * Version: 1.0.0
 * Requires PHP: 7.4
 * Author: Sleeping Expert
 * Text Domain: se-consent
 *
 * Kodėl savas: Cookiebot kaina auga pagal puslapių skaičių, o jo uc.js kraunamas iš
 * trečiosios šalies serverio (lėtina LCP, siunčia lankytojų duomenis Usercentrics).
 * Čia viskas veikia iš mūsų serverio, be jokių išorinių užklausų.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('SE_CONSENT_VERSION', '1.0.0');
define('SE_CONSENT_FILE', __FILE__);
define('SE_CONSENT_DIR', plugin_dir_path(__FILE__));
define('SE_CONSENT_URL', plugin_dir_url(__FILE__));

require_once SE_CONSENT_DIR . 'includes/settings.php';
require_once SE_CONSENT_DIR . 'includes/blocker.php';
require_once SE_CONSENT_DIR . 'includes/frontend.php';
require_once SE_CONSENT_DIR . 'includes/log.php';
require_once SE_CONSENT_DIR . 'includes/declaration.php';
require_once SE_CONSENT_DIR . 'includes/wp-consent-api.php';

if (is_admin()) {
    require_once SE_CONSENT_DIR . 'includes/admin.php';
}

register_activation_hook(__FILE__, 'se_consent_activate');
register_deactivation_hook(__FILE__, 'se_consent_deactivate');

function se_consent_activate() {
    se_consent_log_install();
    if (!get_option(SE_CONSENT_OPTION)) {
        add_option(SE_CONSENT_OPTION, se_consent_defaults());
    }
    if (!wp_next_scheduled('se_consent_purge')) {
        wp_schedule_event(time() + HOUR_IN_SECONDS, 'daily', 'se_consent_purge');
    }
}

function se_consent_deactivate() {
    wp_clear_scheduled_hook('se_consent_purge');
}
