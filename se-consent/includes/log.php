<?php
/**
 * Sutikimų žurnalas — BDAR 7 str. 1 d. įrodymas, kad sutikimas buvo gautas.
 * Saugoma: sutikimo ID, laikas, pasirinkimai, banerio versija, būdas, puslapis,
 * IP su nunulinta paskutine dalimi ir naršyklės (UA) santrauka. Pilnas IP nesaugomas.
 */

if (!defined('ABSPATH')) {
    exit;
}

const SE_CONSENT_DB_VERSION = 1;

function se_consent_log_table() {
    global $wpdb;
    return $wpdb->prefix . 'se_consent_log';
}

function se_consent_log_install() {
    global $wpdb;
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    $table   = se_consent_log_table();
    $charset = $wpdb->get_charset_collate();
    dbDelta("CREATE TABLE {$table} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        consent_id char(36) NOT NULL,
        created_at datetime NOT NULL,
        version smallint(5) unsigned NOT NULL DEFAULT 1,
        method varchar(20) NOT NULL DEFAULT '',
        preferences tinyint(1) NOT NULL DEFAULT 0,
        statistics tinyint(1) NOT NULL DEFAULT 0,
        marketing tinyint(1) NOT NULL DEFAULT 0,
        ip_masked varchar(45) NOT NULL DEFAULT '',
        user_agent varchar(255) NOT NULL DEFAULT '',
        url varchar(255) NOT NULL DEFAULT '',
        PRIMARY KEY  (id),
        KEY consent_id (consent_id),
        KEY created_at (created_at)
    ) {$charset};");
    update_option('se_consent_db_version', SE_CONSENT_DB_VERSION);
}

add_action('plugins_loaded', function () {
    if ((int) get_option('se_consent_db_version') !== SE_CONSENT_DB_VERSION) {
        se_consent_log_install();
    }
});

/** 192.168.1.77 => 192.168.1.0; 2001:db8:abcd:12::1 => 2001:db8:abcd:: */
function se_consent_mask_ip($ip) {
    if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
        return preg_replace('/\.\d+$/', '.0', $ip);
    }
    if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
        $bin = inet_pton($ip);
        return inet_ntop(substr($bin, 0, 6) . str_repeat("\0", 10));
    }
    return '';
}

add_action('rest_api_init', function () {
    register_rest_route('se-consent/v1', '/log', [
        'methods'             => 'POST',
        'callback'            => 'se_consent_log_endpoint',
        'permission_callback' => '__return_true', // anoniminiai lankytojai; apsauga — validacija ir dažnio riba
    ]);
});

function se_consent_log_endpoint(WP_REST_Request $req) {
    $data = json_decode($req->get_body(), true);
    if (!is_array($data)) {
        return new WP_REST_Response(['ok' => false], 400);
    }
    $id = isset($data['id']) ? (string) $data['id'] : '';
    if (!preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i', $id)) {
        return new WP_REST_Response(['ok' => false], 400);
    }
    $methods = ['accept_all', 'reject_all', 'custom', 'placeholder', 'withdraw', 'api'];
    $method  = in_array($data['m'] ?? '', $methods, true) ? $data['m'] : 'api';
    $c       = is_array($data['c'] ?? null) ? $data['c'] : [];

    $ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '');
    // Dažnio riba: ne daugiau 20 įrašų per minutę iš vieno (maskuoto) IP.
    $rk    = 'se_consent_rl_' . md5(se_consent_mask_ip($ip));
    $count = (int) get_transient($rk);
    if ($count >= 20) {
        return new WP_REST_Response(['ok' => false], 429);
    }
    set_transient($rk, $count + 1, MINUTE_IN_SECONDS);

    global $wpdb;
    $wpdb->insert(se_consent_log_table(), [
        'consent_id'  => strtolower($id),
        'created_at'  => current_time('mysql', true),
        'version'     => max(0, min(65535, (int) ($data['v'] ?? 0))),
        'method'      => $method,
        'preferences' => !empty($c['preferences']) ? 1 : 0,
        'statistics'  => !empty($c['statistics']) ? 1 : 0,
        'marketing'   => !empty($c['marketing']) ? 1 : 0,
        'ip_masked'   => se_consent_mask_ip($ip),
        'user_agent'  => substr(sanitize_text_field((string) ($_SERVER['HTTP_USER_AGENT'] ?? '')), 0, 255),
        'url'         => substr(sanitize_text_field((string) wp_parse_url((string) ($data['u'] ?? '/'), PHP_URL_PATH)), 0, 255),
    ]);
    return new WP_REST_Response(['ok' => true], 201);
}

add_action('se_consent_purge', function () {
    global $wpdb;
    $months = max(1, (int) se_consent_settings()['log_retention_months']);
    $table  = se_consent_log_table();
    $wpdb->query($wpdb->prepare("DELETE FROM {$table} WHERE created_at < (UTC_TIMESTAMP() - INTERVAL %d MONTH)", $months)); // phpcs:ignore
});

/** Statistika administratoriaus skydeliui. */
function se_consent_log_stats($days = 30) {
    global $wpdb;
    $table = se_consent_log_table();
    $row = $wpdb->get_row($wpdb->prepare(
        "SELECT COUNT(*) total,
            SUM(method='accept_all') accept_all,
            SUM(method='reject_all') reject_all,
            SUM(method IN ('custom','placeholder')) custom,
            SUM(statistics) statistics,
            SUM(marketing) marketing
         FROM {$table} WHERE created_at >= (UTC_TIMESTAMP() - INTERVAL %d DAY)", // phpcs:ignore
        $days
    ), ARRAY_A);
    return array_map('intval', (array) $row);
}
