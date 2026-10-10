<?php
/**
 * Pašalinus įskiepį ištrinami nustatymai ir sutikimų žurnalas.
 * Prieš šalinant eksportuokite žurnalą (CSV), jei jo reikia kaip sutikimų įrodymo.
 */

if (!defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

global $wpdb;
$wpdb->query("DROP TABLE IF EXISTS {$wpdb->prefix}se_consent_log"); // phpcs:ignore
delete_option('se_consent_settings');
delete_option('se_consent_db_version');
wp_clear_scheduled_hook('se_consent_purge');
